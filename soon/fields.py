# -*- coding: utf-8 -*-

"""
.. module:: soon.fields
    :synopsis: Custom WTForms fields
"""

import calendar
import datetime
import os

from flask import current_app
from flask_wtf.file import FileField
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage


class UploadFileField(FileField):

    def __init__(self, upload_to=None, *args, **kwargs):
        """
        Overrides constructor method of `FileField` allowing `UploadFileField`
        to take extra arguments.

        Kwargs:
            upload_to (str): Relative path to upload files to
        """

        if upload_to:
            self.upload_to = upload_to

        return super(UploadFileField, self).__init__(*args, **kwargs)

    def make_paths(self, obj):
        """
        Returns built paths for saving to the file system, storing a relative
        path in a DB and the secure filename. In the case where the exact same
        filename exists in the same directory a UNIX timestamp is appended
        to the end of the filename to ensure no overwrites of existing files
        occure.

        Args:
            obj (obj): The object being populated by the form

        Returns.
            tuple. Realtive path, Absolute path, filename
        """

        config = current_app.config
        relative_base = getattr(self, 'realtive_base', config['MEDIA_REL_DIR'])
        absolute_base = getattr(self, 'absolute_base', config['MEDIA_ABS_DIR'])

        # upload_to is a relative path from the realtive_base
        upload_to = getattr(self, 'upload_to', None)

        # If upload_to is given update base paths to include the upload_to
        # path
        if upload_to:
            absolute_base = os.path.join(
                absolute_base,
                upload_to)
            relative_base = os.path.join(
                relative_base,
                upload_to)

        # Get filename
        filename = secure_filename(self.data.filename)

        absolute_path = os.path.join(
            absolute_base,
            filename)

        if os.path.exists(absolute_path):
            # A File with the same name already exists in this dir
            # we will alter the filename to contain a timestamp of the upload
            # date of this file
            now = datetime.datetime.utcnow()
            timestamp = calendar.timegm(now.utctimetuple())
            name, ext = os.path.splitext(filename)

            # build filename
            filename = '{name}_{timestamp}.{ext}'.format(
                name=name,
                timestamp=timestamp,
                ext=ext)

            # Reset absolute_path to use the new filename
            absolute_path = os.path.join(
                absolute_base,
                filename)

        relative_path = os.path.join(
            relative_base,
            filename)

        return absolute_path, relative_path, filename

    def populate_obj(self, obj, name):
        """
        Called when populating an object such as a SQLAlchemy model with
        field data.

        In the case of `UploadFileField` this method will trigger the
        proceess of safely saving the file and setting the field data
        to be a relative path to the file.

        Args:
            obj (obj): Instance of the object
            name (str): Name of the field
        """

        if self.data and isinstance(self.data, FileStorage):
            absolute_path, relative_path, filename = self.make_paths(obj)
            self.save(absolute_path)

            # Set field attribute to be value of the relative save path
            setattr(obj, name, relative_path)

    def save(self, absolute_path):
        """
        Save the file to the file system. In the event the destination
        directory does not exist it will attempt to create it.

        Args:
            absolute_path (str): The path to save the file too
        """

        base = os.path.dirname(os.path.realpath(absolute_path))

        # If the absolute_base does not exist create it
        if not os.path.exists(base):
            os.makedirs(base)

        self.data.save(absolute_path)

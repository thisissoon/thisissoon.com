# -*- coding: utf-8 -*-

"""
.. module:: soon.jobs.forms
   :synopsis: WTForms for jobs module
"""

import os

from flask import current_app
from flask.ext.wtf import Form
from soon.ext import db
from flask_wtf.file import FileAllowed, FileRequired
from soon.jobs.models import Job
from werkzeug import secure_filename
from wtforms_alchemy import model_form_factory

ModelForm = model_form_factory(Form)

file_required = FileRequired('Job Spec PDF required.')
file_allowed = FileAllowed(['pdf', ], 'PDF Only')


class JobForm(ModelForm):

    class Meta:
        model = Job
        only = ['title', 'blurb', 'spec']
        # WTForms-Alchemy adds default validators which are not required for
        # File Fields so we HAVE to explicitly set the Validators for File
        # Fields
        field_args = {
            'spec': {
                'validators': [
                    file_required,
                    file_allowed]}}

    def validate_spec(form, field):
        """
        Here we will save the file and update the field data to be a
        relative path to the saved file.
        """

        # If no data don't try to save the file
        if field.data:

            # Get filename and set relative path
            f = form.spec.data
            filename = secure_filename(f.filename)
            rel = os.path.join('jobs', filename)

            # Save the file to the file system
            f.save(os.path.join(
                current_app.config['MEDIA_ABS_DIR'],
                rel))

            # Set the data to be a relative path
            field.data = rel

        field.data = form._obj.spec

    @classmethod
    def get_session():
        return db.session


class JobUpdateForm(JobForm):

    def __init__(self, *args, **kwargs):
        super(JobUpdateForm, self).__init__(*args, **kwargs)

        # For updates a file is not required
        self['spec'].validators = [file_allowed, ]

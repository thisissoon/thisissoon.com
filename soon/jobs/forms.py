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
                    FileRequired('Job Spec PDF required.'),
                    FileAllowed(['pdf', ], 'PDF Only')]}}

    def validate_spec(form, field):
        """
        Here we will save the file and update the field data to be a
        relative path to the saved file.
        """

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

    @classmethod
    def get_session():
        return db.session

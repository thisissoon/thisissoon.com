# -*- coding: utf-8 -*-

"""
.. module:: soon.jobs.forms
   :synopsis: WTForms for jobs module
"""

from flask.ext.wtf import Form
from soon.ext import db
from flask_wtf.file import FileAllowed, FileRequired
from soon.jobs.models import Job
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

    @classmethod
    def get_session():
        return db.session


class JobUpdateForm(JobForm):

    def __init__(self, *args, **kwargs):
        super(JobUpdateForm, self).__init__(*args, **kwargs)

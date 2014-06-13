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

    file_required = FileRequired('Job Spec PDF required.')
    file_allowed = FileAllowed(['pdf', ], 'PDF Only')

    class Meta(object):
        model = Job
        only = ['title', 'blurb', 'spec']

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self['spec'].validators = [self.file_required, self.file_allowed]

    @classmethod
    def get_session():
        return db.session


class JobUpdateForm(JobForm):

    def __init__(self, *args, **kwargs):
        super(JobUpdateForm, self).__init__(*args, **kwargs)
        self['spec'].validators = [self.file_allowed, ]

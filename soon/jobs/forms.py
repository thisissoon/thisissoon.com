# -*- coding: utf-8 -*-

"""
.. module:: soon.jobs.forms
   :synopsis: WTForms for jobs module
"""


from flask.ext.wtf import Form
from soon.ext import db
from soon.jobs.models import Job
from wtforms_alchemy import model_form_factory

ModelForm = model_form_factory(Form)


class JobForm(ModelForm):

    class Meta:
        model = Job
        only = ['title', 'blurb', 'spec']

    @classmethod
    def get_session():
        return db.session

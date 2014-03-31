# -*- coding: utf-8 -*-

"""
.. module:: soon.auth.forms
   :synopsis: WTForms for authentication module
"""

from flask.ext.login import login_user
from flask.ext.security.utils import verify_and_update_password
from flask.ext.wtf import Form
from soon.auth.models import User
from soon.ext import db
from wtforms_alchemy import model_form_factory
from wtforms.validators import ValidationError

ModelForm = model_form_factory(Form)


class AuthenticationForm(ModelForm):

    class Meta:
        model = User
        only = ['email', 'password']
        # We don't care if the email exists as this is an authentication form
        unique_validator = lambda **kwargs: lambda *args, **kwargs: True

    def validate_password(form, field):
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if not user:
            raise ValidationError('Inccorect Email or Password combination')
        if not verify_and_update_password(field.data, user):
            raise ValidationError('Inccorect Email or Password combination')

        login_user(user)

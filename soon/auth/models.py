# -*- coding: utf-8 -*-

"""
.. module:: soon.auth.models
   :synopsis: User authentication models
"""

from flask.ext.security import RoleMixin, UserMixin
from soon.ext import db
from soon.generic.db.mixins import CreateUpdateMixin
from sqlalchemy.dialects import postgresql
from wtforms.fields import PasswordField, TextField


class User(db.Model, UserMixin, CreateUpdateMixin):

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Credentials
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        info={'label': 'E-Mail'})

    password = db.Column(
        db.String(255),
        nullable=False,
        info={'form_field_class': PasswordField,
              'label': 'Password'})

    # Site Administrator
    super_user = db.Column(db.Boolean(), default=False)

    # User status
    active = db.Column(db.Boolean(), default=False)

    # Tracking
    confirmed_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(
        postgresql.INET,
        info={'form_field_class': TextField})
    current_login_ip = db.Column(
        postgresql.INET,
        info={'form_field_class': TextField})
    login_count = db.Column(db.Integer)

    # Relations
    roles = db.relationship(
        'Role',
        secondary='users_roles',
        backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin, CreateUpdateMixin):

    # Primary key
    id = db.Column(db.Integer(), primary_key=True)

    # Details
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class UsersRoles(db.Model):

    __tablename__ = 'users_roles'

    # Foreign Keys

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='cascade'),
        primary_key=True)
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('role.id', ondelete='cascade'),
        primary_key=True)

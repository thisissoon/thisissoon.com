# -*- coding: utf-8 -*-

"""
.. module:: soon.jobs.models
   :synopsis: Job models
"""

from soon.ext import db
from soon.db.mixins import CreateUpdateMixin
from wtforms.fields import FileField


class Job(db.Model, CreateUpdateMixin):

    __tablename__ = 'jobs'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='cascade'),
        nullable=False)

    # Attributes
    title = db.Column(
        db.Unicode(64),
        nullable=False,
        info={
            'label': 'Job Title'})
    blurb = db.Column(
        db.Unicode(144),
        nullable=False,
        info={
            'label': 'Blurb'})
    spec = db.Column(
        db.Unicode(512),
        nullable=False,
        info={
            'label': 'Spec (PDF)',
            'form_field_class': FileField})

    # Relations
    user = db.relationship(
        'User',
        backref=db.backref('jobs', lazy='dynamic'))

    def __repr__(self):
        return '<Job: id={0.id!r} title={0.title!r}>'.format(self)

    def __str__(self):
        return self.title

# -*- coding: utf-8 -*-

"""
.. module:: soon.jobs.models
   :synopsis: Job models
"""

from flask.ext.login import current_user
from soon.db.mixins import CreateUpdateMixin
from soon.ext import db
from soon.jobs.fields import UploadJobSpecField
from soon.jobs.events import job_after_delete
from sqlalchemy import event


class Job(db.Model, CreateUpdateMixin):

    __tablename__ = 'jobs'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='cascade'),
        default=lambda: current_user.id,
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
            'form_field_class': UploadJobSpecField})

    def __repr__(self):
        return '<Job: id={0.id!r} title={0.title!r}>'.format(self)

    def __str__(self):
        return self.title


event.listen(Job, 'after_delete', job_after_delete)

# -*- coding: utf-8 -*-

"""
.. module:: soon.jobs.events
   :synopsis: Functions fired on SQLAlchemy ORM Events
"""

import os

from flask import current_app


def job_after_delete(mapper, connection, target):
    """
    Called after delete of a `Job` object. Deletes attached file
    with the object from the file system.

    Args:
        mapper (sqlalchemy.orm.mapper.Mapper): Mapper target of this event
        connection (sqlalchemy.engine.Connection): The db connection session
        target (soon.jobs.models.Job): The deleted instance
    """

    path = os.path.join(
        current_app.config['MEDIA_ROOT'],
        target.spec)

    if os.path.exists(path):
        os.remove(path)

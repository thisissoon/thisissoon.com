# -*- coding: utf-8 -*-

"""
.. module:: soon.generic.db.mixins
   :synopsis: Helper mixins to extend default model functionality
"""

import datetime

from soon.ext import db


class CreateUpdateMixin(object):
    """
    Mixin provides automatic create and update time stamps on create
    and update of object
    """

    # Timestamps
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)


class GetOrCreateMixin(object):
    """
    Mixin provides functions for django style get_or_create functionality
    """

    @classmethod
    def get_or_create(kls, commit=True, **kwargs):
        """
        Get instance of object or create a new one and return it,
        keyword arguments should be key=value pairs. Returns a tuple, first
        value being a boolean equalling True if instance already existed
        or False if instance is new followed by the object instance.

        :param commit: Automatically commit of new instance
        :type commit: bool -- default True

        :returns: tuple -- Bool, instance
        """

        instance = db.session.query(kls).filter_by(**kwargs).first()
        if instance:
            return True, instance

        instance = kls(**kwargs)

        if commit:
            db.session.add(instance)
            db.session.commit()

        return False, instance

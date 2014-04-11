# -*- coding: utf-8 -*-

"""
.. module:: soon.views.mixins.create
   :synopsis: Mixins for Flask pluggable views for creting objects
"""

from flask import flash
from soon.views.mixins.forms import SingleFormMixin
from soon.views.mixins.models import SingleModelMixin


class CreateMixin(object):

    def __init__(self, *args, **kwargs):
        """
        Constructor for `CreateMixin`. Sets the `form_success_callback`
        attribute.
        """

        self.valid_callback = self.create

    def create(self, data):
        """
        This method is used as the method called on from validitation success,
        this maybe different for different kinds of create views so requires
        implimentation.

        Raises:
            NotImplementedError
        """

        raise NotImplementedError('`create` method is not implimented')


class CreateFormMixin(CreateMixin, SingleFormMixin):

    def get_form(self):
        """
        When using forms, get the form from the form_class attribute and
        instantiate it.
        """

        try:
            form = self._form
        except AttributeError:
            kls = self.get_form_class()

            form = kls()
            form.validate_on_submit()

            self._form = form

        return form


class CreateModelMixin(CreateMixin, SingleModelMixin):

    def create(self, data):
        """
        Create new objects for the supplied model and form data.

        Args:
            data (dict): Data to be used for model creation, key: value

        Raises:
            NotImplementedError
        """

        session = self.get_session()
        model = self.get_model()

        record = model(**data)

        session.add(record)
        session.commit()

        flash('New record created.', 'success')


class CreateModelFormMixin(CreateModelMixin, CreateFormMixin):

    def get_context(self):
        super(CreateModelFormMixin, self).get_context()

        self.context['model'] = self.get_model()

        return self.context

    def create(self, data):
        """
        Creates new object from from data bu populating a blank object
        of the defined model.

        Args:
            data (dict): Data to be used for model creation, key: value

        Raises:
            NotImplementedError
        """

        session = self.get_session()
        model = self.get_model()
        form = self.get_form()

        obj = model()
        form.populate_obj(obj)

        session.add(obj)
        session.commit()

        flash('New record created.', 'success')

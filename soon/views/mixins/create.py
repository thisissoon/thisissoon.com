# -*- coding: utf-8 -*-

"""
.. module:: soon.views.mixins.create
   :synopsis: Mixins for Flask pluggable views for creting objects
"""

from flask import request, flash
from soon.views.mixins.forms import FormMixin
from soon.views.mixins.models import ModelMixin


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


class CreateFormMixin(CreateMixin, FormMixin):

    def get_form(self):
        """
        When using forms, get the form from the form_class attribute and
        instantiate it.
        """

        try:
            form = self._form
        except AttributeError:
            form_class = self.get_form_class()

            # Instantiate the form with only request values
            form = form_class(request.values)
            form.validate_on_submit()

            self._form = form

        return form


class CreateModelMixin(CreateMixin, ModelMixin):

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

# -*- coding: utf-8 -*-

"""
.. module:: soon.views.mixins.update
   :synopsis: Mixins for Flask pluggable views for updating objects
"""

from flask import flash, request
from soon.views.mixins.models import ModelMixin
from soon.views.mixins.forms import FormMixin, ModelFormMixin
from sqlalchemy import update


class UpdateMixin(object):

    def __init__(self, *args, **kwargs):
        """
        Constructor for `UpdateMixin`. Sets the `form_success_callback`
        attribute.
        """

        self.valid_callback = self.update

    def update(self, data):
        """
        This method is used as the method called on from validitation success,
        this maybe different for different kinds of update views so requires
        implimentation.

        Raises:
            NotImplementedError
        """

        raise NotImplementedError('`update` method is not implimented')


class UpdateFormMixin(UpdateMixin, FormMixin):

    def get_context(self):
        """
        Overrides parents context returner adding extra context specific for
        this mixin.

        Returns:
            dict. The context
        """

        super(UpdateFormMixin, self).get_context()

        self.context['form'] = self.get_form()

        return self.context

    def get_form(self):
        """
        Retrun the form instance of the class stored in `form_class`

        Returns:
            obj. Instance of `form_class`
        """

        try:
            return self._form
        except AttributeError:
            form_class = self.get_form_class()
            form = form_class(request.values)
            form.validate_on_submit()
            self._form = form

        return form


class UpdateModelMixin(UpdateMixin, ModelMixin):

    def update(self, data):
        """
        Updates the instance of supplied model with supplied data.

        Args:
            data (dict): Data to update the model instance with
        """

        session = self.get_session()
        obj = self.get_object()
        model = self.get_model()

        stmt = update(model).where(model.id == self.pk).\
            values(**data)

        session.execute(stmt)
        session.commit()

        flash('{0} was update.'.format(obj), 'success')


class UpdateModelFromMixin(UpdateModelMixin, UpdateFormMixin, ModelFormMixin):

    def get_form(self):
        """
        Retrun the form instance of the class stored in `form_class` with
        instance of supplied model.

        Returns:
            obj. Instance of `form_class`
        """

        try:
            return self._form
        except AttributeError:
            form_class = self.get_form_class()
            obj = self.get_object()

            # When updating models we will need to pass the instance of the
            # object to the form
            form = form_class(request.values, obj=obj)
            form.validate_on_submit()

            self._form = form

        return form

    def get(self, pk):
        """
        Handle GET requests where the primary key of the instance to be updated
        is passed in via a uri, for example /edit/1 where the url rule
        would be /edit/<int:pk>. Save the pk as an instance attribute to be
        used in other methods.

        Args:
            pk (int): Primary key of instance to be updated

        Returns:
            str. The rendered template
        """

        self.pk = pk

        return super(UpdateModelMixin, self).get()

    def post(self, pk):
        """
        Handle POST requests where the primary key of the instance to be
        updated is passed in via a uri, for example /edit/1 where the url rule
        would be /edit/<int:pk>. Save the pk as an instance attribute to be
        used in other methods.

        Args:
            pk (int): Primary key of instance to be updated

        Returns:
            str. The rendered template
        """

        self.pk = pk

        return super(UpdateModelMixin, self).post()

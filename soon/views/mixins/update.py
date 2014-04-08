# -*- coding: utf-8 -*-

"""
.. module:: soon.views.mixins.update
   :synopsis: Mixins for Flask pluggable views for updating objects
"""

from flask import flash, request
from soon.views.mixins.models import SingleModelMixin
from soon.views.mixins.forms import (
    SingleFormMixin,
    SingleFormModelMixin,
    MultiFormSingleModelMixin)
from sqlalchemy import update


class UpdateMixin(object):
    """
    #TODO: Doc this
    """

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


class UpdateFormMixin(UpdateMixin, SingleFormMixin):
    """
    #TODO: Doc this
    """

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


class UpdateModelMixin(UpdateMixin, SingleModelMixin):
    """
    #TODO: Doc this
    """

    def update(self, data):
        """
        Updates the instance of supplied model with supplied data.

        Args:
            data (dict): Data to update the model instance with
        """

        session = self.get_session()
        model = self.get_model()
        obj = self.get_object()

        stmt = update(model).where(model.id == self.pk).\
            values(**data)

        session.execute(stmt)
        session.commit()

        flash('{0} was updated.'.format(obj), 'success')


class UpdateModelWithFromMixin(object):
    """
    This mixin provides update functionality for mixins which have a form
    from which to populate the object. This Mixin should be used together
    with `SingleFormMixin` or `MultiFormMixin` to update a single model
    instance.
    """

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

    def update(self):
        """
        Updates the instance of supplied model by populating the object with
        the form data.
        """

        form = self.get_form()
        session = self.get_session()
        obj = self.get_object()

        # Populate object and commit the changes
        form.populate_obj(obj)
        session.commit()

        flash('{0} was updated.'.format(obj), 'success')

    def post(self, pk):
        """
        #TODO: Doc This
        """

        self.pk = pk

        form = self.get_form()

        if not form.errors:
            # Call the callback after if form validated, no data needs to be
            # passed as we are using form.populate_object
            self.valid_callback()

            # Call and return on_complete
            return self.on_complete()

        return self.render()


class UpdateModelFromMixin(
        UpdateModelWithFromMixin,
        UpdateFormMixin,
        SingleFormModelMixin):
    """
    #TODO: Doc this
    """

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

        return super(UpdateModelFromMixin, self).get()


class UpdateMultiFormSingleModelMixin(
        UpdateModelWithFromMixin,
        MultiFormSingleModelMixin):
    """
    #TODO: Doc This
    """

    def __init__(self, *args, **kwargs):
        """
        #TODO: Doc this
        """

        self.valid_callback = self.update

    def get_form(self):
        """
        #TODO: Doc this
        """

        self.get_forms()

        return super(UpdateMultiFormSingleModelMixin, self).get_form()

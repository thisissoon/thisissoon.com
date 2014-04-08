# -*- coding: utf-8 -*-

"""
.. module:: soon.views.mixins.models
   :synopsis: Mixins for Flask pluggable views relating to Database / Model
              integratipon
"""


class SingleModelMixin(object):
    """
    Methods for integrating database models into views.
    """

    def get_context(self):
        """
        Overrides parents context returner adding extra context specific for
        this mixin.

        Returns:
            dict. The context
        """

        super(SingleModelMixin, self).get_context()

        if hasattr(self, 'pk'):
            self.context['obj'] = self.get_object()

        return self.context

    def get_session(self):
        """
        Returns the db session required to perform queries against
        the db, if not implimented raises NotImplementedError

        Returns:
            obj. db session object

        Raises:
            NotImplementedError
        """

        if not hasattr(self, 'session'):
            raise NotImplementedError('`session` attribute required')

        return self.session

    def get_model(self):
        """
        Return the model or raise NotImplementedError

        Returns:
            class. The model class

        Raises:
            NotImplementedError
        """

        if not hasattr(self, 'model'):
            raise NotImplementedError('`model` attribute required')

        # Add it to the context
        self.context['model'] = self.model

        return self.model

    def get_object(self):
        """
        Get an existing object from the database or a 404 if the object
        does not exist.

        Returns:
            obj. An instance of the model

        Raises
            werkzeug.exceptions.NotFound, NotImplementedError
        """

        model = self.get_model()

        try:
            pk = self.pk
        except AttributeError:
            raise NotImplementedError('`pk` has not been set for `get_object`')

        try:
            obj = self._obj
        except AttributeError:
            obj = model.query.filter_by(id=pk).first_or_404()
            self._obj = obj

        return obj

# -*- coding: utf-8 -*-

"""
.. module:: soon.views.mixins.models
   :synopsis: Mixins for Flask pluggable views relating to Database / Model
              integratipon
"""


class ModelMixin(object):
    """
    Methods for integrating database models into views.
    """

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
            werkzeug.exceptions.NotFound
        """

        model = self.get_model()

        try:
            obj = self._obj
        except AttributeError:
            obj = model.query.filter_by(id=self.pk).first_or_404()
            self._obj = obj

        return obj

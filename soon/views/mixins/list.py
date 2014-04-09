# -*- coding: utf-8 -*-

"""
.. module:: soon.views.mixins.list
   :synopsis: Mixins for Flask pluggable views for rendering lists
"""

from flask import url_for
from soon.views.mixins.models import SingleModelMixin
from soon.views.mixins.template import TemplateMixin


class ListModelMixin(SingleModelMixin, TemplateMixin):
    """
    Mixin view class to help with generic list rendering of objects from
    supplied model.

    Usage:

    .. code-block:: pythpn
        :linenos:

        from soon.views.mixins.list import ListModelMixin

        class MyView(ListModelMixin)
            template = 'path/to/template.html'
            model = MyModel
    """

    def get_context(self):
        """
        Override the default `get_context` provided by `TemplateMixin`
        and add the `get_value` method so formatters can be applied to
        specific columns.

        Returns:
            dict. Request context data
        """

        super(ListModelMixin, self).get_context()

        self.context['columns'] = self.columns
        self.context['get_value'] = self.get_value
        self.context['get_column_name'] = self.get_column_name
        self.context['create_url'] = self.get_create_url()

        return self.context

    def get_value(self, instance, name):
        """
        Get the value of the field, if formatters are set for that field
        on the instance use the formatting function and return the value.

        Args:
            instance (obj): An object, for example an SQLAlchemy object
            name (str): Attribute on the instance to get the value for

        Returns:
            str. The formatted (or not) attributes value
        """

        try:
            value = getattr(instance, name)
        except AttributeError:
            value = 'Invalid Attribute: {0}'.format(name)

        if hasattr(self, 'formatters'):
            formatter = self.formatters.get(name)
            if formatter:
                value = formatter(self, value)

        return value

    def get_column_name(self, name):
        """
        Try and get a human friendly name for the column name.

        Args:
            name (str): The column name, ie the field

        Returns:
            str. Human friendly name
        """

        model = self.get_model()
        attr = getattr(model, name)

        try:
            return attr.info['label']
        except:
            name = name.title().replace('_', ' ')

        return name

    def get_create_url(self):
        """
        Get the url for create button links, if not set return None so the
        the buttons are not rendered.

        Returns:
            str. Resolved url or None
        """

        url = getattr(self, 'create_url', None)
        if url:
            return url_for(url)

        return None

    def get(self, current_page=1):
        """
        Handle GET requests to views using this mixin rendering a list
        of records for the supplied model.

        Args:
            current_page (int): Page number of objects to render
        """

        model = self.get_model()
        records_per_page = getattr(self, 'records_per_page', 30)

        pages = model.query.paginate(
            current_page,
            records_per_page,
            False)

        self.context['current_page'] = current_page
        self.context['pages'] = pages

        return self.render()

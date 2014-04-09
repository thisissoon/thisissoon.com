# -*- coding: utf-8 -*-

"""
.. module:: soon.views.mixins.template
   :synopsis: Mixins for Flask pluggable views regardinfg basic template
              rendering
"""

from flask import render_template


class TemplateMixin(object):

    context = {}
    methods = ['GET', ]

    def get_template_name(self):
        """
        Return the template name, if not set raise Not

        Returns:
            str. The templat ename

        Raises:
            NotImplementedError
        """

        if not hasattr(self, 'template'):
            raise NotImplementedError('template attribute required')

        return self.template

    def get_context(self):
        """
        Returns the instance context `dict`.

        Returns:
            dict. Request context data
        """

        return self.context

    def render(self):
        """
        Render the view template with the passed context.

        Args:
            context (dict): Context to be used in the template

        Returns:
            str. The rendered template
        """

        return render_template(
            self.get_template_name(),
            **self.get_context())

    def get(self):
        """
        Default GET request handler

        Returns:
            str. The rendered template
        """

        return self.render()

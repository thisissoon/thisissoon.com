# -*- coding: utf-8 -*-

"""
.. module:: soon.generic.views.mixins
   :synopsis: Mixins for Flask pluggable views
"""

from flask import render_template


class TemplateMixin(object):

    def get_template_name(self):
        """
        Return the template name, if not set raise Not

        :returns: str -- The template name
        """

        if not hasattr(self, 'template'):
            raise NotImplementedError('template attribute required')

        return self.template

    def render(self, context):
        """
        Render the view template with the passed context.

        :param context: Context to be used in the template
        :type context: dict

        :return: str -- The rendered template
        """

        return render_template(self.get_template_name(), **context)

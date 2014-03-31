# -*- coding: utf-8 -*-

"""
.. module:: soon.generic.views.home
   :synopsis: Homepage Views
"""

from flask.views import MethodView
from soon.generic.views.mixins import TemplateMixin


class HomeView(MethodView, TemplateMixin):

    template = 'index.html'

    def get(self):
        """
        Render the homepage on GET requests.
        """

        return self.render()

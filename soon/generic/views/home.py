# -*- coding: utf-8 -*-

"""
.. module:: soon.generic.views.home
   :synopsis: Homepage Views
"""

from flask.views import MethodView


class HomeView(MethodView):

    def get(self):
        """
        Render the homepage on GET requests.
        """

        return 'home'

# -*- coding: utf-8 -*-

"""
.. module:: soon.views.home
   :synopsis: Homepage Views
"""

from flask.views import MethodView
from soon.views.mixins.template import TemplateMixin


class HomeView(TemplateMixin, MethodView):

    template = 'home.html'

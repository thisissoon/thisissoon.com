# -*- coding: utf-8 -*-

"""
.. module:: soon.views.home
   :synopsis: Homepage Views
"""

from flask.views import MethodView
from soon.jobs.models import Job
from soon.views.mixins.list import ListModelMixin


class HomeView(ListModelMixin, MethodView):

    model = Job
    template = 'home.html'

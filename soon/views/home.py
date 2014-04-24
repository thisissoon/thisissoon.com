# -*- coding: utf-8 -*-

"""
.. module:: soon.views.home
   :synopsis: Homepage Views
"""

from flask.ext.velox.views.sqla.read import ModelListView
from soon.jobs.models import Job


class HomeView(ModelListView):
    model = Job
    template = 'home.html'
    paginate = False

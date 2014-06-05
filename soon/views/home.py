# -*- coding: utf-8 -*-

"""
.. module:: soon.views.home
   :synopsis: Homepage Views
"""

from flask.ext.velox.views.sqla.read import ModelListView
from flask.ext.velox.views.template import TemplateView
from soon.jobs.models import Job


class HomeView(ModelListView):
    model = Job
    template = 'home.html'
    paginate = False

# Peabody Portfolio View
class peabody(TemplateView):
    template = 'peabody.html'

# Peabody Portfolio View
class residentadvisor(TemplateView):
    template = 'residentadvisor.html'

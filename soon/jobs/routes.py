# -*- coding: utf-8 -*-

"""
.. module:: soon.jobs.routes
   :synopsis: Flask blueprint instantiation and route definitions
"""

from flask.blueprints import Blueprint
#from soon.jobs.admin import JobAdminView


blueprint = Blueprint(
    'jobs',
    __name__,
    url_prefix='/jobs',
    template_folder='templates')

routes = []

#admin = [
#    JobAdminView(
#        name='Jobs',
#        url='jobs',
#        endpoint='admin.jobs')
#]

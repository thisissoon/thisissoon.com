# -*- coding: utf-8 -*-

"""
.. module:: soon.auth.routes
   :synopsis: Flask blueprint instantiation and route definitions
"""

from flask.blueprints import Blueprint
from soon.auth.admin import UserAdminView


blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth',
    template_folder='templates')

routes = []

admin = [
    UserAdminView(
        name='Users',
        url='users',
        endpoint='admin.users')
]

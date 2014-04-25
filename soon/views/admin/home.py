# -*- coding: utf-8 -*-

"""
.. module:: soon.views.admin
   :synopsis: Base admin views
"""

from flask.ext import admin
from flask.ext.admin import expose_plugview
from flask.ext.login import logout_user
from flask.ext.velox.admin.views.forms import AdminFormView
from flask.ext.velox.views.http import RedirectView
from soon.auth.forms import AuthenticationForm


class AdminHomeView(admin.AdminIndexView):

    @expose_plugview('/')
    class index(AdminFormView):
        form = AuthenticationForm
        template = 'admin/home.html'
        redirect_url_rule = '.index'

    @expose_plugview('/logout')
    class logout(RedirectView):
        rule = '.index'

        def pre_dispatch(self):
            logout_user()

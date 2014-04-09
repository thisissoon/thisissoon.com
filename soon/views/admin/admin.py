# -*- coding: utf-8 -*-

"""
.. module:: soon.views.admin
   :synopsis: Base admin views
"""

from flask import redirect, request, url_for
from flask.ext import admin
from flask.ext.admin import AdminIndexView, expose_plugview
from flask.ext.login import current_user
from flask.views import MethodView


class AdminHomeView(AdminIndexView):

    @expose_plugview('/')
    class index(MethodView):

        def get_form(self, values=None):
            # Due to circular import issues this import had to be
            # isolated here
            from soon.auth.forms import AuthenticationForm
            return AuthenticationForm(values)

        def get(self, admin):
            form = self.get_form()
            return admin.render('admin/home.html', **{
                'form': form
            })

        def post(self, admin):
            form = self.get_form(request.values)
            if form.validate():
                return redirect(url_for('admin.index'))
            return admin.render('admin/home.html', **{
                'form': form
            })
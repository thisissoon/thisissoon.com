# -*- coding: utf-8 -*-

"""
.. module:: soon.views.admin.home
   :synopsis: Views for the admin homepage
"""

from flask import redirect, request, url_for
from flask.ext.admin import AdminIndexView, expose_plugview
from flask.ext.login import logout_user
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

    @expose_plugview('/logout')
    class logout(MethodView):

        def get(self, admin):
            logout_user()
            return redirect(url_for('admin.index'))

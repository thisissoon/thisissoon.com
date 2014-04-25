# -*- coding: utf-8 -*-

"""
.. module:: pravis.package.admin
   :synopsis: Flask super admin integration for package blueprint
"""

from flask.ext.login import current_user
from flask.ext.admin import BaseView, expose_plugview
from flask.ext.velox.formatters import bool_admin_formatter
from flask.ext.velox.admin.views.sqla import forms
from flask.ext.velox.admin.views.sqla import read
from flask.ext.velox.admin.views.sqla.delete import (
    AdminDeleteObjectView,
    AdminMultiDeleteObjectView)
from soon.ext import db
from soon.auth.forms import (
    NewUserAdminForm,
    UpdateUserAdminForm,
    UserPasswordForm)
from soon.auth.models import User


class UserAdminView(BaseView):

    def is_accessible(self):
        if current_user.is_authenticated() and current_user.is_admin:
            return True
        return False

    @expose_plugview('/')
    class index(read.AdminModelTableView):
        model = User
        paginate = True
        columns = ['email', 'active', 'super_user', 'last_login_at']
        formatters = {
            'active': bool_admin_formatter,
            'super_user': bool_admin_formatter
        }
        with_selected = {
            'Delete': '.multi_delete',
        }

    @expose_plugview('/create')
    class create(forms.AdminCreateModelView):
        model = User
        form = NewUserAdminForm
        session = db.session

    @expose_plugview('/update/<int:id>')
    class update(forms.AdminUpdateMultiFormView):
        model = User
        session = db.session
        forms = [
            ('Change Password', UserPasswordForm),
            ('Update User', UpdateUserAdminForm),
        ]

    @expose_plugview('/delete/<int:id>')
    class delete(AdminDeleteObjectView):
        model = User
        session = db.session

    @expose_plugview('/delete')
    class multi_delete(AdminMultiDeleteObjectView):
        model = User
        session = db.session

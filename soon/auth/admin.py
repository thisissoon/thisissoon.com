# -*- coding: utf-8 -*-

"""
.. module:: pravis.package.admin
   :synopsis: Flask super admin integration for package blueprint
"""

from flask.views import MethodView
from flask.ext.admin import expose_plugview
from soon.auth.forms import (
    NewUserAdminForm,
    UpdateUserAdminForm,
    UserPasswordForm)
from soon.auth.models import User
from soon.ext import db
from soon.views.admin import AdminBaseView
from soon.views.admin.mixins import (
    AdminListMixin,
    AdminCreateFormMixin,
    AdmminUpdateMultiFormMixin,
    AdminMultiDeleteMixin)
from soon.views.fmt import bool_admin_fmt


class UserAdminView(AdminBaseView):

    @expose_plugview('/')
    @expose_plugview('/<int:current_page>')
    class index(AdminListMixin, MethodView):

        model = User
        records_per_page = 30
        columns = ['email', 'active', 'super_user', 'last_login_at']
        create_url = 'admin.users.create'
        formatters = {
            'active': bool_admin_fmt,
            'super_user': bool_admin_fmt
        }
        with_selected = [
            ('Delete', 'admin.users.delete'),
        ]

    @expose_plugview('/create')
    class create(AdminCreateFormMixin, MethodView):

        model = User
        form_class = NewUserAdminForm
        session = db.session
        success_url = 'admin.users.index'
        cancel_url = 'admin.users.index'

    @expose_plugview('/edit/<int:pk>')
    class edit(AdmminUpdateMultiFormMixin, MethodView):

        model = User
        session = db.session
        success_url = 'admin.users.index'
        cancel_url = 'admin.users.index'
        delete_url = 'admin.users.delete'
        forms = [
            ('Change Password', UserPasswordForm),
            ('Update User', UpdateUserAdminForm),
        ]

    @expose_plugview('/delete')
    @expose_plugview('/delete/<int:pk>')
    class delete(AdminMultiDeleteMixin, MethodView):

        model = User
        session = db.session
        success_url = 'admin.users.index'
        cancel_url = 'admin.users.index'

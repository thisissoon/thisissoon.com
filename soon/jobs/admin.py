# -*- coding: utf-8 -*-

"""
.. module:: soon.jobs.admin
   :synopsis: Flask super admin integration for jobs blueprint
"""

from flask.views import MethodView
from flask.ext.admin import expose_plugview
from soon.ext import db
from soon.jobs.forms import JobForm
from soon.jobs.models import Job
from soon.views.fmt import datetime_fmt
from soon.views.admin import AdminBaseView
from soon.views.admin.mixins import (
    AdminListMixin,
    AdminCreateFormMixin,
    AdminMultiDeleteMixin)


class JobAdminView(AdminBaseView):

    @expose_plugview('/')
    @expose_plugview('/<int:current_page>')
    class index(AdminListMixin, MethodView):

        model = Job
        records_per_page = 30
        columns = ['title', 'created', 'updated']
        create_url = 'admin.jobs.create'
        delete_url = 'admin.jobs.delete'
        formatters = {
            'created': datetime_fmt,
            'updated': datetime_fmt
        }
        with_selected = [
            ('Delete', 'admin.jobs.delete'),
        ]

    @expose_plugview('/create')
    class create(AdminCreateFormMixin, MethodView):

        model = Job
        form_class = JobForm
        session = db.session
        success_url = 'admin.jobs.index'
        cancel_url = 'admin.jobs.index'

    @expose_plugview('/delete')
    @expose_plugview('/delete/<int:pk>')
    class delete(AdminMultiDeleteMixin, MethodView):

        model = Job
        session = db.session
        success_url = 'admin.jobs.index'
        cancel_url = 'admin.jobs.index'

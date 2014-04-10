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
    AdminCreateFormMixin)


class JobAdminView(AdminBaseView):

    @expose_plugview('/')
    @expose_plugview('/<int:current_page>')
    class index(AdminListMixin, MethodView):

        model = Job
        records_per_page = 30
        columns = ['title', 'created', 'updated']
        create_url = 'admin.jobs.create'
        formatters = {
            'created': datetime_fmt,
            'updated': datetime_fmt
        }

    @expose_plugview('/create')
    class create(AdminCreateFormMixin, MethodView):

        model = Job
        form_class = JobForm
        session = db.session
        success_url = 'admin.jobs.index'
        cancel_url = 'admin.jobs.index'

# -*- coding: utf-8 -*-

"""
.. module:: soon.jobs.admin
   :synopsis: Flask super admin integration for jobs blueprint
"""

from flask.ext.login import current_user
from flask.ext.admin import BaseView, expose_plugview
from flask.ext.velox.admin.views.sqla.read import AdminModelTableView
from flask.ext.velox.admin.views.sqla.forms import (
    AdminCreateModelView,
    AdminUpdateModelView)
from flask.ext.velox.admin.views.sqla.delete import (
    AdminDeleteObjectView,
    AdminMultiDeleteObjectView)
from flask.ext.velox.formatters import datetime_formatter
from soon.ext import db
from soon.jobs.forms import JobForm, JobUpdateForm
from soon.jobs.models import Job


class JobAdminView(BaseView):

    def is_accessible(self):
        if current_user.is_authenticated() and current_user.is_admin:
            return True
        return False

    @expose_plugview('/')
    class index(AdminModelTableView):
        model = Job
        columns = ['title', 'created', 'updated']
        formatters = {
            'created': datetime_formatter,
            'updated': datetime_formatter
        }
        with_selected = {
            'Delete': '.delete_multi',
        }

    @expose_plugview('/create')
    class create(AdminCreateModelView):
        model = Job
        form = JobForm
        session = db.session

    @expose_plugview('/update/<int:id>')
    class update(AdminUpdateModelView):
        model = Job
        session = db.session
        form = JobUpdateForm

    @expose_plugview('/delete/<int:id>')
    class delete(AdminDeleteObjectView):
        model = Job
        session = db.session

    @expose_plugview('/delete')
    class delete_multi(AdminMultiDeleteObjectView):
        model = Job
        session = db.session

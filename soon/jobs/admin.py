# -*- coding: utf-8 -*-

"""
.. module:: soon.jobs.admin
   :synopsis: Flask super admin integration for jobs blueprint
"""

from flask.views import MethodView
from flask.ext.admin import expose_plugview
from soon.jobs.models import Job
from soon.views.admin import AdminBaseView
from soon.views.admin.mixins import AdminListMixin


class JobAdminView(AdminBaseView):

    @expose_plugview('/')
    @expose_plugview('/<int:current_page>')
    class index(AdminListMixin, MethodView):

        model = Job
        records_per_page = 30
        columns = ['title', 'created', 'updated']

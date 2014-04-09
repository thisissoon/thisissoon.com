# -*- coding: utf-8 -*-

"""
.. module:: soon.views.admin.mixins
   :synopsis: Mixin classes specific for the Admin interface
"""

from flask import url_for
from flask.ext import admin
from flask.ext.login import current_user
from soon.views.mixins.create import CreateModelFormMixin
from soon.views.mixins.delete import MultiDeleteModelMixin
from soon.views.mixins.list import ListModelMixin
from soon.views.mixins.template import TemplateMixin
from soon.views.mixins.update import (
    UpdateModelFromMixin,
    UpdateMultiFormSingleModelMixin)


class AdminBaseView(admin.BaseView):

    def is_accessible(self):
        """
        Determines if the use has access to the specified admin class, this
        can be overridden and altered as required.

        Returns:
            bool. If the user has access or not
        """

        if current_user.is_authenticated() and current_user.is_admin:
            return True
        return False


class AdminTemplateMixin(TemplateMixin):

    def render(self):
        """
        Render the admin view template with the passed context.

        Returns:
            str. The rendered template
        """

        return self.admin.render(
            self.get_template_name(),
            **self.get_context())


class AdminListMixin(ListModelMixin, AdminTemplateMixin):

    template = 'admin/forms/list.html'

    def get_context(self):
        """
        Overrides parent `get_context` method, calling the parent
        and adding extra admin specific context
        """

        super(AdminListMixin, self).get_context()

        if hasattr(self, 'with_selected'):
            self.context['with_selected'] = []
            for name, action in self.with_selected:
                self.context['with_selected'].append((name, url_for(action)))

        return self.context

    def get(self, admin, current_page=1):
        """
        Perform the regular get method as defined in `ListMixin` except
        add the the admin argument as an instance attribute so the
        `AdminTemplateMixin` can render using the current admin instance.

        Args:
            admin (object): The view currently executing
            page (int): The page number

        Returns:
            str. The rendered HTML page
        """

        self.admin = admin
        return super(AdminListMixin, self).get(current_page=current_page)


class AdminCreateFormMixin(CreateModelFormMixin, AdminTemplateMixin):

    template = 'admin/forms/create.html'

    def get(self, admin):
        """
        Overrides `get` method defined in `CreateModelFormMixin`
        allowing us to render within an Admin interface

        Args:
            admin (object): The view currently executing

        Returns:
            str. The rendered HTML page
        """

        self.admin = admin

        return super(CreateModelFormMixin, self).get()

    def post(self, admin):
        """
        Overrides `post` method defined in `CreateModelFormMixin`
        allowing us to render within an Admin interface

        Args:
            admin (object): The view currently executing

        Returns:
            str. The rendered HTML page
        """

        self.admin = admin

        return super(CreateModelFormMixin, self).post()


class AdminUpdateFormMixin(UpdateModelFromMixin, AdminTemplateMixin):

    template = 'admin/forms/edit.html'

    def get(self, admin, pk):
        """
        Perform the regular get method as defined in `UpdateModelFromMixin`
        except add the the admin argument as an instance attribute so the
        `AdminTemplateMixin` can render using the current admin instance.

        Args:
            admin (object): The view currently executing
            pk (int): Primary key of object to be updated

        Returns:
            str. The rendered HTML page
        """

        self.admin = admin

        return super(AdminUpdateFormMixin, self).get(pk)

    def post(self, admin, pk):
        """
        Perform the regular `post` method as defined in `UpdateModelFromMixin`
        except add the the admin argument as an instance attribute so the
        `AdminTemplateMixin` can render using the current admin instance.

        Args:
            admin (object): The view currently executing
            pk (int): Primary key of object to be updated

        Returns:
            str. The rendered HTML page
        """

        self.admin = admin

        return super(AdminUpdateFormMixin, self).post(pk)


class AdminMultiDeleteMixin(MultiDeleteModelMixin, AdminTemplateMixin):

    template = 'admin/forms/delete.html'

    def get(self, admin, pk):
        """
        Perform the regular get method as defined in `MultiDeleteModelMixin`
        except add the the admin argument as an instance attribute so the
        `AdminTemplateMixin` can render using the current admin instance.

        Args:
            admin (object): The view currently executing
            pk (int): Primary key of object to delete

        Returns:
            str. The rendered HTML page
        """

        self.admin = admin

        return super(AdminMultiDeleteMixin, self).get(pk)

    def post(self, admin):
        """
        Perform the regular `post` method as defined in `MultiDeleteModelMixin`
        except add the the admin argument as an instance attribute so the
        `AdminTemplateMixin` can render using the current admin instance.

        Args:
            admin (object): The view currently executing

        Returns:
            str. The rendered HTML page
        """

        self.admin = admin

        return super(AdminMultiDeleteMixin, self).post()


class AdmminUpdateMultiFormMixin(
        UpdateMultiFormSingleModelMixin,
        AdminTemplateMixin):

    def get(self, admin, pk):
        self.admin = admin
        self.pk = pk

        return super(AdmminUpdateMultiFormMixin, self).get()

    def post(self, admin, pk):
        self.admin = admin
        self.pk = pk

        return super(AdmminUpdateMultiFormMixin, self).post(pk)

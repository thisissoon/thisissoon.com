# -*- coding: utf-8 -*-

"""
.. module:: soon.views.mixins
   :synopsis: Mixins for Flask pluggable views
"""

from flask import flash, request, redirect, url_for
from soon.views.mixins.template import TemplateMixin
from soon.views.mixins.models import SingleModelMixin


class DeleteMixin(TemplateMixin):

    def get_context(self):
        """
        Overrides existing `get_context` method from `TemplateMixin` adding
        extra context variables data.

        Returns:
            dict. Context data
        """

        super(DeleteMixin, self).get_context()

        self.context['cancel_url'] = self.get_cancel_url()
        self.context['success_url'] = self.get_success_url()

        return self.context

    def is_confirmed(self):
        """
        Checks the request params for a `confirm` argument with the value
        of `True`. This is only relevant if the `DeleteMixin.cofnrim` has been
        set to `True` else this check is ignored. By default all
        `DeleteMixin` attributes are set to `True` so they must be explicitly
        set to `False` for this check to be ignored.

        Returns:
            bool. If the deletion has been confirmed or not
        """

        confirm = getattr(self, 'confirm', True)
        if confirm:
            return bool(request.args.get('confirm', False))

        # If confirm is False return True so confirm check is ignored
        return True

    def get_cancel_url(self):
        """
        Returns the url the cancel button should link to, this requires
        a `cancel_url` attribute to be defined or a `NotImplementedError`
        will be raised.

        Returns:
            str. Resolved url

        Raises:
            NotImplementedError
        """

        try:
            return url_for(self.cancel_url)
        except AttributeError:
            raise NotImplementedError('`cancel_url` attribute required for '
                                      '`DeleteMixin`')

    def get_success_url(self):
        """
        Success url used on successful deletes. This requires a
        `success_url` to be defined or a NotImplementedError exception
        will be raised.

        Returns:
            str. Resolved url

        Raises:
            NotImplementedError
        """

        try:
            return url_for(self.success_url)
        except AttributeError:
            raise NotImplementedError('`success_url` attribute required for '
                                      '`DeleteMixin`')


class DeleteModelMixin(DeleteMixin, SingleModelMixin):

    methods = ['GET', ]

    def get_context(self):
        """
        Overrides existing `get_context` method from `TemplateMixin` adding
        extra context variables data.

        Returns:
            dict. Context data
        """

        super(DeleteModelMixin, self).get_context()

        self.context['obj'] = self.get_object()
        self.context['pk'] = getattr(self, 'pk', None)

        return self.context

    def get(self, pk):
        """
        GET Requests will be on specific single objects, where the uri
        contains the id of the obj to delete.

        Args:
            pk (int): Primary key of object to delete

        Returns:
            str. The rendered HTML page
        """

        self.pk = pk

        if self.is_confirmed():
            session = self.get_session()
            model = self.get_model()
            obj = self.get_object()
            success_url = self.get_success_url()

            model.query.filter_by(id=pk).delete()

            session.commit()  # Delete happens here

            flash('{0} was successfuly deleted'.format(obj), 'success')

            return redirect(success_url)

        return self.render()


class MultiDeleteModelMixin(DeleteModelMixin):
    """
    Also supports single object deletion but adds support for posting
    multiple object ids to delete.
    """

    methods = ['GET', 'POST', ]

    def get_object(self):
        """
        Overrides default `get_object` from `ModelMixin` so no errors are
        thrown if `self.pk` attribute does not exist on the instance, this
        will happen with multi deletes as we will be POSTing mutliple ids
        rather than a single one
        """

        if hasattr(self, 'pk'):
            return super(MultiDeleteModelMixin, self).get_object()
        else:
            return None

    def get_context(self):
        """
        Overrides existing `get_context` method from `TemplateMixin` adding
        extra context variables data.

        Returns:
            dict. Context data
        """

        super(MultiDeleteModelMixin, self).get_context()

        self.context['objects'] = self.get_objects()

        return self.context

    def get_objects(self):
        """
        Get objects to delete,this is used for rendering the confirm page
        so the user can confirm the objects they wish to delete.

        Returns:
            set. Objects marked to be deleted
        """

        objects = set()
        model = self.get_model()

        ids = [int(id) for id in request.values.getlist('objects')]
        if ids:
            for obj in model.query.filter(model.id.in_(ids)).all():
                objects.add(obj)

        return objects

    def delete_multiple(self):
        """
        Delete mutliple objects, this is only called if `is_confirmed` is
        True.
        """

        model = self.get_model()
        session = self.get_session()

        ids = [int(id) for id in request.values.getlist('objects')]
        model.query.filter(model.id.in_(ids)).delete(
            synchronize_session=False)

        session.commit()  # Delete happens here

        flash('{0} record(s) deleted.'.format(len(ids)), 'success')

    def post(self):
        """
        POST requests POST a number of object ids to be delted.

        Returns:
            str. The rendered HTML page
        """

        if self.is_confirmed():
            self.delete_multiple()
            success_url = self.get_success_url()
            return redirect(success_url)

        return self.render()

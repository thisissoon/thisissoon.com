# -*- coding: utf-8 -*-

"""
.. module:: soon.views.mixins.forms
   :synopsis: Mixins for Flask pluggable views relating to rendering and
              processing forms.
"""

from flask import redirect, request, url_for
from soon.views.mixins.models import SingleModelMixin
from soon.views.mixins.template import TemplateMixin


class BaseFormMixin(TemplateMixin):

    methods = ['GET', 'POST']

    def get_context(self):
        """
        Override the default `get_context` provided by `TemplateMixin`
        and add the `is_hidden_field` method so we can tell if fields are
        hidden or not.

        Returns:
            dict. Request context data
        """

        super(BaseFormMixin, self).get_context()

        try:
            from flask.ext.wtf.form import _is_hidden
            self.context['is_hidden_field'] = _is_hidden
        except ImportError:
            pass

        self.context['submit_url'] = self.get_submit_url()
        self.context['cancel_url'] = self.get_cancel_url()
        self.context['delete_url'] = self.get_delete_url()

        return self.context

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
                                      '`FormMixin`')

    def get_cancel_url(self):
        """
        Return the cancel url for exiting the form. This requires a
        `cancel_url` to be defined or a NotImplementedError exception
        will be raised.

        Returns:
            str. The resolved url

        Raises:
            NotImplementedError
        """

        try:
            return url_for(self.cancel_url)
        except AttributeError:
            raise NotImplementedError('`cancel_url` attribute required for '
                                      '`FormMixin`')

    def get_submit_url(self):
        """
        Returns the form submit url, this uses the current request url
        as the submit url but can be overridden as a class attribute
        by defining `submit_url`. This should be a `url_for` compatible
        string.

        Returns:
            str. The resolved url
        """

        submit_url = getattr(self, 'submit_url', request.url_rule.endpoint)

        return url_for(submit_url)

    def get_delete_url(self):
        """
        Returns a resolved delete url to be used on forms where a delete
        button is appropriate. Views should already exist for handling deletes.
        For this method to return a valid url the `delete_url` must be
        defined on the class which uses this mixin. This should be a string
        safe for usage with `url_for`.
        """

        delete_url = getattr(self, 'delete_url', None)

        if delete_url:
            return url_for(delete_url)

        return None

    def on_complete(self):
        """
        Called at the end of the `post` method if form was valid and
        `success_url` was called. This method will attempt to
        first use the `redirect_url` attribute if set to redirect
        to the given string using `url_for`. If the attribute does not exist
        it will do nothing.

        Returns:
            werkzeug.wrappers.Response or None.
        """

        success_url = self.get_success_url()
        return redirect(success_url)


class SingleFormMixin(BaseFormMixin):

    def get_context(self):
        """
        TODO: Doc this
        """

        super(SingleFormMixin, self).get_context()

        self.context['form'] = self.get_form()

        return self.context

    def get_form_class(self):
        """
        Return the form class but do not instantiate, if not set raise
        NotImplementedError.

        Returns:
            class. The form class

        Raises:
            NotImplementedError
        """

        if not hasattr(self, 'form_class'):
            raise NotImplementedError('`form_class` attribute required')

        return self.form_class

    def get_form(self):
        """
        Get form should return an instantiated form, this method requires
        implimentation as it will vary depending on how the form requires
        instantiation.

        Raises:
            NotImplementedError
        """

        raise NotImplementedError('`get_form` method is not implimented')

    def post(self):
        """
        Handle POST requests, this should validate the form with the POST
        data either redirecting or rendering the template.

        Returns:
            str. The rendered template
        """

        form = self.get_form()

        if not form.errors:
            # Call the callback after form validated to do something with
            # the form data
            self.valid_callback(form.data)

            # Call and return on_complete
            return self.on_complete()

        return self.render()


class SingleFormModelMixin(SingleModelMixin, SingleFormMixin):

    def get_submit_url(self):
        """
        Returns the form submit url, this uses the current request url
        as the submit url but can be overridden as a class attribute
        by defining `submit_url`. This should be a `url_for` compatible
        string.

        Returns:
            str. The resolved url
        """

        pk = getattr(self, 'pk', None)
        submit_url = getattr(self, 'submit_url', request.url_rule.endpoint)

        if pk:
            return url_for(submit_url, pk=pk)

        return url_for(submit_url)

    def get_delete_url(self):
        """
        Returns a resolved delete url to be used on forms where a delete
        button is appropriate. Views should already exist for handling deletes.
        For this method to return a valid url the `delete_url` must be
        defined on the class which uses this mixin. This should be a string
        safe for usage with `url_for`.
        """

        pk = getattr(self, 'pk', None)
        delete_url = getattr(self, 'delete_url', None)

        if pk and delete_url:
            return url_for(delete_url, pk=pk)

        return None


class MultiFormMixin(BaseFormMixin):
    """
    This mixin allows for mutliple forms to be rendered on a single view.

    Usage:

    .. code-block:: pythpn
        :linenos:

        from soon.views.mixins.forms import MultiFormMixin

        class MyView(ListModelMixin)
            forms = [
                ('Form 1', MyFormOne),
                ('Form 2', MyFormTwo),
                ('Form 3', MyFormThree)
            ]
    """

    methods = ['GET', 'POST']

    def get_context(self):
        """
        TODO: Doc this
        """

        super(MultiFormMixin, self).get_context()

        self.context['forms'] = self.get_forms()

        return self.context

    def get_form_classes(self):
        """
        Returns the raw form classes defined in `self.forms` attribute

        Returns:
            list. Tuple List of name and uninstantiated class

        Raises:
            NotImplementedError
        """

        try:
            return self.forms
        except AttributeError:
            raise NotImplementedError('`forms` attribute must be defined for'
                                      '`MultiFormMixin` classes')

    def instantiate_form(self, kls, prefix):
        """
        Instantiates the provided form class and returns it
        """

        form = kls(prefix=prefix)
        if request.values.get('form') == prefix:
            form.validate_on_submit()

            # So post has access to the subtmited form
            self._form = form

        return form

    def get_forms(self):
        """
        Takes the raw list of forms with their none instantiated form classes
        and Instantiates them returns them.

        Returns:
            list. Tuple List of name and instantiated class
        """

        try:
            return self._instantiated_forms
        except AttributeError:

            forms = self.get_form_classes()
            instantiated_forms = []

            for i, values in enumerate(forms, start=1):
                name, kls = values
                instantiated_forms.append((
                    name,
                    self.instantiate_form(kls, 'form{0}'.format(i))
                ))

            self._instantiated_forms = instantiated_forms

            return instantiated_forms

    def post(self, pk):
        """
        TODO: Doc this
        """

        self.get_forms()

        if not self.form.errors:
            # Call the callback after form validated to do something with
            # the form data
            self.valid_callback(self.form.data)

            # Call and return on_complete
            return self.on_complete()

        return self.render()


class MultiFormSingleModelMixin(MultiFormMixin, SingleModelMixin):
    """
    Provides ability for mutliple forms on a single view to update a single
    model instance.
    """

    def instantiate_form(self, kls, prefix):
        """
        Instantiates the provided form class and returns it. Overrides
        default `MultiFormMixin` method to pass the model instance object
        tp the form.

        Returns:
            obj. Instantiated form
        """

        form = kls(prefix=prefix, obj=self.get_object())
        if request.values.get('form') == prefix:
            form.validate_on_submit()

            # So post has access to the subtmited form
            self._form = form

        return form

    def get_submit_url(self):
        """
        Returns the form submit url, this uses the current request url
        as the submit url but can be overridden as a class attribute
        by defining `submit_url`. This should be a `url_for` compatible
        string.

        Returns:
            str. The resolved url
        """

        pk = getattr(self, 'pk', None)
        submit_url = getattr(self, 'submit_url', request.url_rule.endpoint)

        if pk:
            return url_for(submit_url, pk=pk)

        return url_for(submit_url)

    def get_delete_url(self):
        """
        Returns a resolved delete url to be used on forms where a delete
        button is appropriate. Views should already exist for handling deletes.
        For this method to return a valid url the `delete_url` must be
        defined on the class which uses this mixin. This should be a string
        safe for usage with `url_for`.
        """

        pk = getattr(self, 'pk', None)
        delete_url = getattr(self, 'delete_url', None)

        if pk and delete_url:
            return url_for(delete_url, pk=pk)

        return None

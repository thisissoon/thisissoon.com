# -*- coding: utf-8 -*-

"""
.. module:: soon.views.fmt
   :synopsis: Methods for formatting output, for example True = Yes
"""

import pytz

from jinja2 import Markup


def bool_fmt(view, value, **kwargs):
    """
    For rendering True / False values in a human friendly way, by default
    True = Yes and False = No however this can be overriden by passing
    true and false keyword args with their respective values.

    Args:
        view (`flask.views.MethodView`): The executing view (self)
        value (bool): The value to evaluate against

    Kwargs:
       true (str): Value to use for True state
       false (str): Value to use for False state

    Returns: str. The value to use
    """

    true_value = kwargs.get('true', 'Yes')
    false_value = kwargs.get('false', 'No')

    if value is True:
        return true_value
    else:
        return false_value


def bool_admin_fmt(view, value):
    """
    Render booleans using HTML rather than plain text for the Admin using
    bootstrap markup.

    Args:
        view (`flask.views.MethodView`): The executing view (self)
        value (bool): The value to evaluate against

    Returns: str. The html value to use
    """

    return Markup(bool_fmt(
        view,
        value,
        true='<i class="icon-ok"></i>',
        false='<i class="icon-remove"></i>'))


def datetime_fmt(view, value):
    """
    Render a sane date time value, for example: dd/mm/yyyy at HH:MM TZ.
    All values should be UTC.

    Args:
        view (`flask.views.MethodView`): The executing view (self)
        value (bool): The value to evaluate against
    """

    value = value.replace(tzinfo=pytz.utc)
    return value.strftime('%d/%m/%Y at %I:%M%p %Z')

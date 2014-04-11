# -*- coding: utf-8 -*-

"""
.. module:: soon.jobs.fields
    :synopsis: Custom WTForm fields specific to Jobs
"""

from soon.fields import UploadFileField


class UploadJobSpecField(UploadFileField):
    """
    Sets the `upload_to` attribute so job files get uploadded to
    `MEDIA_ABS_DIR`/jobs.
    """

    upload_to = 'jobs'

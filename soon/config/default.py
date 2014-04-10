# -*- coding: utf-8 -*-

"""
.. module:: soon.config.default
   :synopsis: Default configuration for Flask, do not use for Production
"""

import os

# Paths

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Debug

DEBUG = True

# Security

SECRET_KEY = 'changeme'
SECURITY_TRACKABLE = True
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = SECRET_KEY

# Database

DEFAULT_DATABASE_URI = 'sqlite://:memory:'
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
    DEFAULT_DATABASE_URI

# Blueprints

BLUEPRINTS = [
    'soon.auth',
    'soon.jobs',
]

# Media (Uploads etc)

# URL to serve media from - used for DEBUG=True only
MEDIA_URL = '/media'
# Relative path used for storing paths in db
MEDIA_REL_DIR = os.path.join('media')
# Absaolute path for actually saving files
MEDIA_ABS_DIR = os.path.join(BASE_DIR, '..', MEDIA_REL_DIR)

# -*- coding: utf-8 -*-

"""
.. module:: soon.app.ext
   :synopsis: Flask extenstions, these are initialized in the application
              factory and external modules
"""

# Databse

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Migrations

from flask.ext.migrate import Migrate
migrate = Migrate()

# Security

from flask.ext.security import Security
security = Security()

# Static Collection

from flask.ext.collect import Collect
collect = Collect()

# Gravatar
from flask.ext.gravatar import Gravatar
gravatar = Gravatar(size=100)

# Velox
from flask.ext.velox import Velox
velox = Velox()

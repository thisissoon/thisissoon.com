# -*- coding: utf-8 -*-

"""
.. module:: soon.app.loader
    :synopsis: Helper utilities for application factory, mostly utilities
               around auto loading blueprints, models and admin registration.
"""

import os

from flask import Flask
from flask.ext.security import SQLAlchemyUserDatastore
from soon.exceptions import ImproperlyConfigured
from soon.generic.views.home import HomeView
from soon.ext import db, migrate, security
from werkzeug import SharedDataMiddleware


admin = None


def load_config(app, override=None):
    """
    Load application configuration from default module then overriding
    by environment variables

    :param app: Flask application instance
    :type app: flask.app.Flask

    :param override: Optional path to a settings file
    :type override: str
    """

    # Default configuration
    app.config.from_object('soon.config.default')

    # Override using os environment variable
    if os.environ.get('SOON_SETTINGS_PATH'):
        app.config.from_envvar('SOON_SETTINGS_PATH')

    # If override path is supplied use those settings
    if override:
        app.config.from_pyfile(override)


def load_models(blueprint):
    """
    Load models from models.py of the blueprint module if it exist.

    :param blueprint: Python module path to module
    :type blueprint: str
    """

    try:
        __import__('{0}.models'.format(blueprint))
    except ImportError:
        # TODO: Log this at debug level
        pass


def load_blueprint(app, blueprint):
    """
    Load the blueprint and register the routes. Routes should be defined as
    a list of tuples of url, view func, for example:

        routes = [
            ('/', IndexView.as_view('index'))
        ]

    Admin views can also be defined but are not required:

        admin = [
            HelloView(name='Hello', endpoint='hello', category='Hello')
        ]

    :param app: Flask application instance
    :type app: flask.app.Flask

    :param blueprint: Python module path to module
    :type blueprint: str
    """

    try:
        module = __import__(
            '{0}.routes'.format(blueprint),
            fromlist=['soon'])
    except ImportError:
        raise ImproperlyConfigured(
            'routes.py not defined for {0} blueprint.'.format(blueprint))

    try:
        for route, view in module.routes:
            module.blueprint.add_url_rule(route, view_func=view)
    except AttributeError:
        raise ImproperlyConfigured('routes list is not defined')

    app.register_blueprint(module.blueprint)

    try:
        for view in module.admin:
            admin.add_view(view)
    except AttributeError:
        # TODO: Log later at debug info
        pass


def register_extenstions(app):
    """
    Register Flask extenstions with application context

    :param app: Flask application instance
    :type app: flask.app.Flask
    """

    # Database (Flask-SQLAlchemy)
    db.init_app(app)

    # Migrations
    migrate.init_app(app, db)

    # Flask Security
    from soon.auth.models import User, Role
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=datastore)

    # Admin
    from flask.ext.admin import Admin
    from soon.generic.views.admin import AdminHomeView

    global admin

    admin = Admin(
        name='soon',
        index_view=AdminHomeView(name='Dashboard'),
        base_template='layout/admin.html')
    admin.init_app(app)


def register_blueprints(app):
    """
    Load application blueprints from config, similar to Django INSTALLED_APPS
    setting which is literally a list of strings of python module paths.

    Each blueprint can contain the following files:

        - __init__.py
        - admin.py - routes for registering admin views
        - models.py - SQL Alchemy models
        - routes.py - Instantiates the blueprint and contains a list named
                      routes contain tuples of (url, view_func), also
                      admin views should be defined in a list.

    :param app: Flask application instance
    :type app: flask.app.Flask
    """

    for blueprint in app.config.get('BLUEPRINTS', []):
        load_models(blueprint)
        load_blueprint(app, blueprint)


def register_uploads(app):
    """
    Register upload endpoints to be served by werkzeug in development,
    do not use for production.

    :param app: Flask application instance
    :type app: flask.app.Flask
    """

    app.add_url_rule('/uploads/<filename>', 'uploads', build_only=True)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/uploads':  app.config['UPLOAD_DIR']
    })


def create_app(config=None):
    """
    Create a flask application, optionally passing in a path to a separate
    config file to override existing configuration

    :param config: Path to config file
    :type config: str

    :returns: flask.app.Flask -- Flask application
    """

    # Initialize Flask Application
    app = Flask(__name__)

    # Load Configuration
    load_config(app)

    # Initialize extensions
    register_extenstions(app)

    # Dynamically load blueprints
    register_blueprints(app)

    # Upload endooints - Only in debug
    if app.config['DEBUG']:
        register_uploads(app)

    # Register homepage
    app.add_url_rule('/', view_func=HomeView.as_view('home'))

    return app

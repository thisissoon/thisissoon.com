# -*- coding: utf-8 -*-

"""
.. module:: soon.app
   :synopsis: Flask application factory
"""

from flask import Flask
from soon.loader import (
    load_config,
    register_extenstions,
    register_blueprints,
    register_uploads)


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

    return app

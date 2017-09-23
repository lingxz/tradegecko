"""
.. module:: __init__
    :synopsis: This is where all our global variables and instantiation
        happens. If there is simple app setup to do, it can be done here, but
        more complex work should be farmed off elsewhere, in order to keep
        this file readable.

.. moduleauthor:: Dan Schlosser <dan@dan@schlosser.io>
"""

import json
import logging
import logging.handlers

from flask import Flask, current_app
from flask_pymongo import PyMongo

app = None
adi = dict()
assets = None
gcal_client = None
mongo = PyMongo()

def create_app(**config_overrides):
    """This is normal setup code for a Flask app, but we give the option
    to provide override configurations so that in testing, a different
    database can be used.
    """

    # we want to modify the global app, not a local copy
    global app
    global adi
    global assets
    global gcal_client
    global mongo
    app = Flask(__name__)

    # Load config then apply overrides
    app.config.from_pyfile('../config/default.py')
    app.config.update(config_overrides)

    # Setup the database.
    mongo.init_app(app)

    # Attach Blueprints (routing) to the app
    register_blueprints(app)

    # Register the logger.
    register_logger(app)

    return app


def register_logger(app):
    """Create an error logger and attach it to ``app``."""

    max_bytes = int(app.config["LOG_FILE_MAX_SIZE"]) * 1024 * 1024   # MB to B
    # Use "# noqa" to silence flake8 warnings for creating a variable that is
    # uppercase.  (Here, we make a class, so uppercase is correct.)
    Handler = logging.handlers.RotatingFileHandler  # noqa
    f_str = ('%(levelname)s @ %(asctime)s @ %(filename)s '
             '%(funcName)s %(lineno)d: %(message)s')

    access_handler = Handler(app.config["WERKZEUG_LOG_NAME"],
                             maxBytes=max_bytes)
    access_handler.setLevel(logging.INFO)
    logging.getLogger("werkzeug").addHandler(access_handler)

    app_handler = Handler(app.config["APP_LOG_NAME"], maxBytes=max_bytes)
    formatter = logging.Formatter(f_str)
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)
    app.logger.addHandler(app_handler)


def register_blueprints(app):
    """Registers all the Blueprints (modules) in a function, to avoid
    circular dependancies.

    Be careful rearranging the order of the app.register_blueprint()
    calls, as it can also result in circular dependancies.
    """
    from app.routes import inventory
    app.register_blueprint(inventory)


def run():
    """Runs the app."""
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'), debug=True)
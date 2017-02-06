"""
The factory pattern implementation for initializing a Flask application.
"""
import os

from flask import Flask

from .config import CONFIG_NAME_MAPPER
from .extensions import db
from .helpers.misc import get_root_path, create_path

# Some convenience constants referencing different project folders
_ROOT_FOLDER = get_root_path(os.path.dirname(os.path.abspath(__file__)))
_INSTANCE_FOLDER = os.path.join(_ROOT_FOLDER, 'instance')
_TEMPLATE_FOLDER = os.path.join(_ROOT_FOLDER, 'templates')
_TMP_FOLDER = os.path.join(_ROOT_FOLDER, 'tmp')


def app_factory(config_env='PRD', app_name=__name__):
    """
    Initialize the application with the specified environment specific configuration.

    Parameters
    ----------
    config_env: string:
        The abbreviation of the environment to load the configuration settings for.
    app_name: string
        The name of the application.

    Returns
    -------
    Flask instance:
        The Flask application instance.
    """

    app = Flask(app_name,
                template_folder=_TEMPLATE_FOLDER,
                instance_path=_INSTANCE_FOLDER,
                instance_relative_config=True)

    config_app(app, config_env)
    config_extensions(app)
    config_blueprints(app)
    configure_error_handlers(app)
    configure_navigation(app)
    configure_debugging(app)

    return app


def init():
    """
    Any initializing that needs to be done is handled here.
    """

    create_path(_INSTANCE_FOLDER)
    create_path(_TMP_FOLDER)


def config_app(app, config_env):
    """
    Load configuration settings from different configuration locations. Variables defined in each consecutive
    configuration file overrides those in the configuration files loaded earlier.

    Configuration variables tha contain sensitive information should be placed in the configuration file(flask.cfg)
    in the instance folder or any location on the OS that is made available by the TEST_FACTORY_APP_CONFIG environment
    variable to the location.

    Configuration locations are:
    1. Environment specific configuration class.
    2. Optionally the flask.cfg conffiguration file in the instance folder.
    3. Optionally a configuration file reference by the TEST_FACTORY_CONFIG_FILE environment variable.

    Parameters
    ----------
    app: flask application instance
        The Flask application instance.
    config_env: string:
        The abbreviation of the environment to load the configuration settings for.
    """

    # Load the environment specific configuration class
    app.config.from_object(CONFIG_NAME_MAPPER[config_env])
    # If the configuration file exists in the instance folder load it
    app.config.from_pyfile('flask.cfg', silent=True)
    # If the TEST_FACTORY_CONFIG_FILE environment variable exists and the file exist load it
    app.config.from_envvar('TEST_FACTORY_APP_CONFIG', silent=True)


def config_extensions(app):
    """
    Initialize extensions.

    Parameters
    ----------
    app: flask application instance
        The Flask application instance.
    """

    db.init_app(app)


def config_blueprints(app):
    """
    Initialize blueprints.

    Parameters
    ----------
    app: flask application instance
        The Flask application instance.
    """
    from test_factory.module.views import tests_blueprint
    app.register_blueprint(tests_blueprint)


def configure_error_handlers(app):
    """
    Setup error handlers.

    Parameters
    ----------
    app: flask application instance
        The Flask application instance.
    """
    pass


def configure_navigation(app):
    """
    Setup site navigation.

    Parameters
    ----------
    app: flask application instance
        The Flask application instance.
    """
    pass


def configure_debugging(app):
    """
    Setup WSGI debugging.

    Parameters
    ----------
    app: flask application instance
        The Flask application instance.
    """
    pass

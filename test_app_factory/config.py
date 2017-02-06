"""
This class defines the different environment specific configuration settings. The BaseConfig defines the default
values for variables. These default values can be overridden bij adding them to the environment specific
configurations.


Sensitive configuration settings should defined in the file flask.cfg in the instance folder. That folder is
normally excluded form source control.
"""
import os

from .helpers.misc import get_root_path

# Simplify the loading of configurations.
CONFIG_NAME_MAPPER = {
    'DEV': 'test_app_factory.config.DevelopmentConfig',
    'TST': 'test_app_factory.config.TestingConfig',
    'PRD': 'test_app_factory.config.ProductionConfig'
}


class BaseConfig(object):
    """
    Base configuration.

    Defines the default values for variables. These default values can be overridden bij adding them to
    the environment specific configurations.
    """
    ENV_ID = "NOT SET"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_DIR = get_root_path(BASE_DIR)

    SERVER_HOST = "localhost"
    SERVER_PORT = 5080

    DEBUG = False
    TESTING = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """
    Development configuration.
    """
    ENV_ID = "DEV"

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BaseConfig.ROOT_DIR, 'instance', 'dev.sqlite')


class TestingConfig(BaseConfig):
    """
    Testing configuration.
    """
    ENV_ID = "TST"

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BaseConfig.ROOT_DIR, 'instance', 'tst.sqlite')


class ProductionConfig(BaseConfig):
    """
    Production configuration.
    """
    ENV_ID = "PRD"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BaseConfig.ROOT_DIR, 'instance', 'prd.sqlite')

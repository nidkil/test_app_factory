"""
    Convenience import methods making it easier to import the app_factory and extensions.

    If new extensions are added that need to be available to other parts of the application, add them to the import
    statement.
"""
from .application import app_factory, db

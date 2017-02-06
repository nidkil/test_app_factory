"""
To avoid the following two errors when using the factory pattern:

    RuntimeError: application not registered on db instance and no application bound to current context

    RuntimeError: working outside of application context

Add app_context before database statements.
"""
import unittest

from flask import current_app as app
from test_app_factory import app_factory, db
from test_app_factory.models import User


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app_factory('TST')

    def setUp(self):
        with self.app.app_context():
            self.client = app.test_client()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_user(self):
        with self.app.app_context():
            db.session.add(User(name='test user', email='test@mail.com'))
            db.session.commit()

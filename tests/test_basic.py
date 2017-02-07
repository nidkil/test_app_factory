"""
Make sure the site is up and running.
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

    def test_index(self):
        with self.app.app_context():
            db.session.add(User(name='test user', email='test@mail.com'))
            db.session.commit()
            response = self.client.get('/')
            self.assertIn(b'This is a quick test to get Flask working with the factory pattern.', response.data)
            self.assertIn(b'[User=test@mail.com]', response.data)

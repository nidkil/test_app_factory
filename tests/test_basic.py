"""
Make sure the site is up and running.
"""
import unittest

from flask import current_app as app
from test_app_factory import app_factory


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app_factory('TST')

    def setUp(self):
        with self.app.app_context():
            self.client = app.test_client()

    def test_index(self):
        result = self.client.get('/')
        assert b'This is a quick test to get Flask working with the factory pattern.' in result.data

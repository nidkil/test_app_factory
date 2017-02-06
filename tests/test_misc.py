"""
Test cases for the misc convenience helper functions.
"""
import os
import tempfile
import unittest

from flask import Flask
from test_factory.helpers.misc import create_path, pretty_print_config, get_root_path, OUTPUT_LIST, OUTPUT_STRING


def get_test_path_1():
    return os.path.join(tempfile.gettempdir(), 'test_this_path')


def get_test_path_2():
    return os.path.join('this', 'is', 'a', 'tst', 'src', 'path', 'with', 'lots', 'of', 'subfolders')


def del_path(path):
    try:
        os.remove(path)
    except OSError:
        pass


def test_path_exists(path):
    return os.path.exists(path) and os.path.isdir(path)


class TestMisc(unittest.TestCase):
    def pretty_print_config(self):
        app = Flask()
        app.config['TEST_VAR_1'] = 'Value 1'
        app.config['TEST_VAR_5'] = 'Value 5'
        app.config['TEST_VAR_3'] = 'Value 3'
        app.config['TEST_VAR_4'] = 'Value 4'
        app.config['TEST_VAR_2'] = 'Value 2'
        test_list = pretty_print_config(app.config, OUTPUT_LIST)
        self.assertTrue('TEST_VAR_1 = Value 1' in test_list)
        test_string = pretty_print_config(app.config, OUTPUT_STRING)
        self.assertTrue(test_string.contains('TEST_VAR_1 = Value 1'))

    def test_get_root_path(self):
        test_path = get_root_path(get_test_path_2())
        self.assertNotEquals(test_path, '/this/is/a/tst/src')

    def test_get_root_path_exception(self):
        test_path = get_root_path(get_test_path_2())
        with self.assertRaises(ValueError):
            get_root_path(test_path, 'it_does_not_exist')

    def test_create_path_does_not_exist(self):
        test_path = get_test_path_1()
        del_path(test_path)
        create_path(test_path)
        self.assertTrue(test_path_exists(test_path))
        del_path(test_path)

    def test_create_path_exist(self):
        test_path = get_test_path_1()

        create_path(test_path)
        self.assertTrue(test_path_exists(test_path))

        create_path(test_path)
        self.assertTrue(test_path_exists(test_path))
        del_path(test_path)

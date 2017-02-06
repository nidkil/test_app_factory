"""
The manager provides convenience settings to control the application. Like starting it (runserver), creating the
database (create_db), running tests (run_tests) or listing the loaded configuration (show_config).

The environment specific config default is 'TST'. To change this set the required environment varible by setting the
environment variable 'TEST_FACTORY_CONFIG' to the required value: 'DEV', 'TST', 'PRD'.
"""
import os
import unittest

from flask_script import Manager, Server, Shell

from test_factory import app_factory, db
from test_factory.models import User
from test_factory.helpers.misc import pretty_print_config

use_config = os.getenv('TEST_FACTORY_CONFIG', 'TST')

app = app_factory(use_config)
manager = Manager(app)

manager.add_command('runserver', Server(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT']))
manager.add_command('shell', Shell())


@manager.command
def create_db():
    """ Creates the db, tables and a test user """
    db.create_all()
    db.session.add(User(name='admin', email='admin@testfactory.com'))
    db.session.commit()


@manager.command
def drop_db():
    """ Drops the db """
    db.drop_all()


@manager.command
def show_config():
    """ Show the active configuration """
    pretty_print_config(app.config)


@manager.command
def run_tests():
    """ Run all test cases """
    test_dir = os.path.join(app.config['ROOT_DIR'], "tests")
    tests = unittest.TestLoader().discover(test_dir, pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        print 'Test result: OK'
        return 0
    else:
        print 'Test result: NOK'
        return 1


if __name__ == "__main__":
    print '>>>>> Using config: {config_name} <<<<<'.format(config_name=use_config)
    print ('>>>>> Starting server at http://{server_host}:{server_port} <<<<<'.
           format(server_host=app.config['SERVER_HOST'],
                  server_port=app.config['SERVER_PORT']))
    manager.run()

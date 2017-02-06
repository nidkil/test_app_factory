# Test Factory Pattern

This is a Flask project that has been setup to use the factory pattern. I set it up because I was running
was stuck while refactoring one of my projects to use the factory pattern. The code would run normally, but
my test cases where failing with the following two errors:

    RuntimeError: application not registered on db instance and no application bound to current context

    RuntimeError: working outside of application context

Most Flask examples don't use the factory pattern so I spent a lot of time searching around to solve the problem.
So I thought I would work it out and share it. Hopefully it saves someone else time.

## The problem

Once your project starts to grow, code organization is everything. Flask provides a number of mechanisms for
code organization. One of these mechanism's is blueprints. Combined with the factory pattern provides a nice way to 
structure and organise code.

Another problem that the factory pattern helps solve is circular dependencies. 

Getting the factory pattern to work isn't hard. Getting it to work correctly, it turned out, was a little harder. 
The problem I had was caused in the testing code. In the following section I will briefly explain how to setup
and use the factory pattern correctly. 

## The lesson learnt

I have added more code than strictly necessary to show the concept of the factory pattern working, just to provide
a more realistic example.

The structure and contents of this example project is:

```
    src
    │   .gitignore
    │   readme.md
    │   manage.py
    │   requirements.txt
    ├── instance
    │   flask.cfg
    ├── test_app_factory
    │   │   __init__.py
    │   │   appliction.py
    │   │   config.py
    │   │   extensions.py
    │   │   models.py
    │   ├── helpers
    │   │   __init__.py
    │   │   misc.py
    │   ├── module
    │   │   __init__.py
    │   │   viws.py
    │   ├── static
    │   │   favicon-16x16.png
    │   │   favicon-32x32.png
    │   └── templates
    │       index.html
    └── tests
        test_basics.py
    
```

Okay, what's important tot point out here?

The core of the factory pattern is setup in `application.py` and `extensions.py`. All extensions are initialized 
in `extensions.py`. If you add additional extensions make sure to add them to the import statement in 
`test_app_factory/__init__.py`. This is a convent way to shorten import statements.

The actual heavy lifting is done in `application.py`. Each part of the application initialization is a separate
function, which are called by the main function `app_factory`. This function takes a string, which specifies the
environment the configuration should be loaded for. The configuration is defined in `config.py`. 

The factory pattern in `application.py` looks like this:

```
    def app_factory(config, name):
        app = Flask(...)

        ...

        return app
```

The function calls a number of functions that load the configuration settings, extensions, blueprints, etc.

Using the factory is really easy, just use the following call:

```
    app = app_factory('TST')
```

To access the app object in modules after the application has been initialized is done using the proxy provided
by Flask:

```
    from flask import current_app as app
```

Now for the part that was driving met crazy, the testing code. I still do not understand fully why it is the 
only place in my code that was causing a problem, probably has to do with the way unittest works. Anyway, to 
get the factory pattern to work you need to add `app_context` to specific statements. Here is an example. 

```
    class TestCase(unittest.TestCase):
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
```

## Conclusion

Finding good examples isn't always easy. The factory pattern can really help to organize the code and make it 
more readable and maintainable.
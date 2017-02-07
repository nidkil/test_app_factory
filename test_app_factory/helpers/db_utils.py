from test_app_factory.application import db

"""

CRUDMixin provides an easier way of handling the four most common model operations (Create, Read, Update,
and Delete).

    def create(cls, commit=True, **kwargs): pass

    def get(cls, id): pass

    def update(self, commit=True, **kwargs): pass

    def delete(self, commit=True): pass

To use CRUDMixin update the model to subclass it.

    from project.data import CRUDMixin

    class User(CRUDMixin, db.Model):

To use the methods.

    user = User.create(**form.data)

    OR

    User.create(name='John', email='john@doe.com', password='12345')

This is better than repeating ourselves.

    user = User()
    form.populate_obj(user)
    db.session.add(user)
    db.session.commit()

https://realpython.com/blog/python/python-web-applications-with-flask-part-ii/#.Uu5-EHddUp8

"""


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    # We will also proxy Flask-SqlAlchemy's get_or_44
    # for symmetry
    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

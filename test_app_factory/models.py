"""
A very basic model for testing purposes.
"""
from test_app_factory.extensions import db


class User(db.Model):
    __tablename__ = 'tbl_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return (
            "<{class_name}("
            "id={self.id}, "
            "name={name}, "
            "email={email} "
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )

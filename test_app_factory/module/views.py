from flask import render_template, Blueprint

from test_app_factory.models import User

tests_blueprint = Blueprint('tests', __name__)


@tests_blueprint.route('/')
@tests_blueprint.route('/' + tests_blueprint.name + '/')
def home():
    user = User.get(1)
    return render_template('index.html', user=user)

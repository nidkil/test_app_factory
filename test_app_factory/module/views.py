from flask import render_template, Blueprint

tests_blueprint = Blueprint('tests', __name__)


@tests_blueprint.route('/')
@tests_blueprint.route('/' + tests_blueprint.name + '/')
def home():
    return render_template('index.html')

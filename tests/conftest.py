from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest
import os

def create_app():

    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'db', 'my__test_database.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SECRET_KEY'] = '7373sfedhrga734826r836872sfed'

    return app


@pytest.fixture(scope='module')
def test_client():
    # Configure the app with the test configuration
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests
    ctx = flask_app.app_context()
    ctx.push()
    
    db = SQLAlchemy()

    db.create_all()  # Create all database tables

    yield testing_client  # this is where the testing happens

    db.session.remove()
    db.drop_all()
    ctx.pop()
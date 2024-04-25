import pytest
from flask import session
import os
from web_app import app, db_test

@pytest.fixture()
def client():
    app.config['TESTING'] = True  # Ensure the app is in testing mode
    return app.test_client()

@pytest.fixture  
def session():  
    yield session  
    session.close()  

@pytest.fixture()
def db():
    DATABASE_PATH = os.path.join(os.getcwd(), 'web_app', 'db', 'my_test_database.db')
    if not DATABASE_PATH:
        db_test.create_test_db()
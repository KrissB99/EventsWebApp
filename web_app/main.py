from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'db', 'my_database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)

from web_app import routes

from web_app.db.models import Users, Events, UsersOnEvents  # Adjust the import according to your project structure

# Include a method to initialize the database
@app.cli.command("create-db")
def create_db():
    """Creates the database with all models."""
    db.create_all()
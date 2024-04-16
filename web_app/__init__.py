from .main import app

from .blueprints.auth import auth
from .blueprints.admin import admin
from .blueprints.main import main

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(main)

from . import exceptions
from flask import render_template

from . import main
from ...helpers import session_exists

@main.route('/')
@main.route('/main')
@main.route('/dashboard')
@session_exists
def dashboard():
    return render_template('dashboard.html', title="Evently | Dashboard")
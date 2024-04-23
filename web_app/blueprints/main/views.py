from flask import render_template
from . import main

@main.route('/main')
def dashboard():
    return render_template('dashboard.html', title="Evently | Dashboard")

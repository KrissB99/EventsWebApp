from flask import render_template

from . import admin
from ...helpers import is_admin, session_exists


@admin.route('/')
@admin.route('/dashboard')
@is_admin
@session_exists
def admin_info():
    return render_template('admin_dashboard.html', title="Evently | Admin dashboard")

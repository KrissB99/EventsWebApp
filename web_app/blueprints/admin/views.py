from flask import render_template, request

from . import admin
from ...helpers import is_admin, session_exists
from ...db.models import Logs

@admin.after_request
def log_status_code(response):
    Logs.new(request.path, response.status_code)
    return response

@admin.route('/')
@admin.route('/dashboard')
@is_admin
@session_exists
def admin_info():
    return render_template('admin_dashboard.html', title="Evently | Admin dashboard")

from . import admin

@admin.route('/admin')
def admin_info():
    return 'Admin page'

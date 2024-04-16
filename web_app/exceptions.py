from .main import app
from flask import redirect, render_template, url_for

@app.route('/404')
def custom_404():
    return render_template('html/404.html', title="404 | Page Not Found"), 404

@app.errorhandler(404)
def page_not_found(_):
    return redirect(url_for('custom_404'))


@app.route('/500')
def custom_500():
    return render_template('html/500.html', title="500 | Internal Server Error"), 500

@app.errorhandler(500)
def internal_server_error(_):
    return redirect(url_for('custom_500'))
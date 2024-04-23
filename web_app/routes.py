from flask import render_template
from web_app.main import app

@app.route('/')
def main_page():
    return render_template('html/home_page.html', title="Evetly | Home Page")
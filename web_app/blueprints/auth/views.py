from flask import session, render_template, redirect, url_for

from . import auth

@auth.route('/sign-in')
def sign_in():
    return render_template('sign_in.html', title="Evently | Sign In")

@auth.route('/sign-up')
def sign_up():
    return render_template('sign_up.html', title="Evently | Sign Up")

from . import auth
from flask import request, session, redirect, url_for

from web_app.db.models import Users
from web_app.helpers import hash_password, check_password
    
@auth.route('/add-user-to-db', methods=['POST'])
def add_user_to_db():
    form = request.json
    
    # If user with this email exists
    if Users.exists(form['email']):
        return {'detail': 'User already registered, please use different email.'}, 400
    
    # Generate salt, hash password and create user
    hashed_password, salt  = hash_password(form['password'])  
    new_user = Users(email=form['email'], is_vege=form['is_vege'], password_hash=hashed_password, salt=salt)
    new_user.add()
    
    # Save user data in session
    session['user_id'] = new_user.id
    session['email'] = new_user.email
    session['admin'] = new_user.is_admin
    
    return {'detail': 'User created succesfully!'}, 201

@auth.route('/sign-in/check-user', methods=['POST'])
def authorize_user():
    form = request.json
    
    # If user not in db
    if user := Users.exists(form['email']):
        # If passwords match
        if check_password(form['password'], user.password_hash, user.salt):
    
            # Save user data in session
            session['user_id'] = user.id
            session['email'] = user.email
            session['admin'] = user.is_admin
            
            return {'detail': 'Welcome to Evently!'}, 200
        return {'detail': 'Wrong password. Please try again.'}, 400
    return {'detail': 'User with such an e-mail does not exist.'}, 400

@auth.route('/logout')
def logout():
    
    # Clean session
    session['user_id'] = None
    session['email'] = None
    session['admin'] = None
    
    return redirect(url_for('auth.sign_in'))
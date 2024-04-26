from . import auth
from flask import request, session, redirect, url_for,jsonify

from web_app.db.models import Users, Logs
from web_app.helpers import hash_password, check_password, clear_session

@auth.after_request
def log_status_code(response):
    Logs.new(request.path, response.status_code)
    return response

# CRUD FOR USER

@auth.route('/users')
def get_users():
    return jsonify([user.to_dict() for user in Users.get_all()])

@auth.route('/user/<int:id>')
def get_user(id: int):
    if user := Users.get_by_id(id): # Get object user
        return jsonify(user.to_dict()) # Send user as json
    return {'detail': 'Such a user does not exist.'}, 404

@auth.route('/user/<int:id>', methods=['PATCH'])
def update_user(id: int):
    data_to_update = request.json # Get data from fetch
    if user := Users.get_by_id(id): # Get object user
        user.update(data_to_update) # Update user
        # Update user data in session
        session['user_id'] = user.id
        session['email'] = user.email
        session['admin'] = user.is_admin
        return {'detail': 'User updated succesfully.'}
    return {'detail': 'Such a user does not exist.'}, 404

@auth.route('/user/<int:id>', methods=['DELETE'])
def remove_user(id: int):
    if user := Users.get_by_id(id): # Get object user
        user.delete() # Remove user
        clear_session() # Clean session
        return {'detail': 'User removed succesfully.'}
    return {'detail': 'Such a user does not exist.'}, 404

# Sign in, sign up and logout
    
@auth.route('/add-user-to-db', methods=['POST'])
def add_user_to_db():
    form = request.json # Get data from fetch

    if Users.exists(form['email']): # If user with this email exists
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
    form = request.json # Get data from fetch
    
    if user := Users.exists(form['email']): # If user not in db
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
    clear_session() # Clean session
    return redirect(url_for('auth.sign_in'))
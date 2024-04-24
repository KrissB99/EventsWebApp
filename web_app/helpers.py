from functools import wraps
from flask import session, redirect, url_for
import os 
import hashlib

def hash_password(password: str) -> tuple[str, str]:
    """Function for hashing passwords using bcrypt library
    
    Args: 
        password [str]: password from form
        
    Returns:
    typle(str, str): hashed password and salt
    
    """
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000
    )
    return hashed_password, salt
    
def check_password(password_to_check:str, true_password:str, salt:str) -> bool:
    """Function checking hashed password from db with given from login form
    
    Args: 
        password_to_check [str]: password from form
        true_password [str]: password from db
        salt [str]: users salt from db
        
    Returns:
    bool: passwords matched or not
    
    """
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password_to_check.encode("utf-8"), salt, 100000
    )
    return hashed_password == true_password

def clear_session():
    del session['user_id']
    del session['email'] 
    del session['admin'] 
    
def session_exists(func):
    """Check if user logged in before giving him permission to enter the page"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        if 'email' not in session:
            return redirect(url_for("auth.sign_in"))
        return func(*args, **kwargs)
    
    return wrapper

def is_admin(func):
    """Check if user is admin before giving him permission to enter the page"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        if session.get('admin') == True:
            return func(*args, **kwargs)
        return redirect(url_for('authorization_error'))
       
    return wrapper
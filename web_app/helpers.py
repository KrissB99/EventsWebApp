from functools import wraps
from flask import session, redirect, url_for
import os 
import hashlib

from exceptions import AuthorizationError

def hash_password(password: str) -> tuple[str]:
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000
    )
    return hashed_password, salt
    
def check_password(password_to_check:str, true_password:str, salt:str) -> bool:
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password_to_check.encode("utf-8"), salt, 100000
    )
    return hashed_password == true_password
    
def check_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        if 'login' not in session:
           return redirect(url_for("login"))
       
        return func(*args, **kwargs)
    
    return wrapper

def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        if session.get('admin') == True:
            return func(*args, **kwargs)
        else:
           raise AuthorizationError(f"User must be an admin to use {func.__name__}.")
       
    
    return wrapper
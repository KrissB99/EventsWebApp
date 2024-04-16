from . import auth

@auth.route('/auth')
def auth_info():
    return 'Auth page'

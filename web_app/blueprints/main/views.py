from . import main

@main.route('/main')
def main_info():
    return 'Main page'

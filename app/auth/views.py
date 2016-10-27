from flask import render_template
from . import auth


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/create_account')
def create_account():
    return render_template('create_account.html')

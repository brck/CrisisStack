from flask import render_template, request
from . import auth
from .forms import UserSignUpForm, DeveloperSignUpForm


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/create_account')
def create_account():
    return render_template('create_account.html')


@auth.route('/create_account/user')
def create_user_account():
    usersignupform = UserSignUpForm()

    return render_template('user_account.html', form=usersignupform)


@auth.route('/create_account/developer')
def create_developer_account():
    developersignupform = DeveloperSignUpForm(request.form)

    return render_template('developer_account.html', form=developersignupform)

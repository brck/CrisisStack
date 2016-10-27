from flask import render_template, request, redirect, url_for
from . import auth
from .forms import UserSignUpForm, DeveloperSignUpForm, LoginForm


@auth.route('/login')
def login():
    loginform = LoginForm()

    return render_template('login.html', form=loginform)


@auth.route('/create_account')
def create_account():
    return render_template('create_account.html')


@auth.route('/create_account/user', methods=['GET', 'POST'])
def create_user_account():
    usersignupform = UserSignUpForm()

    if usersignupform.validate_on_submit():
        return redirect(request.args.get('next') or url_for('home.index'))

    return render_template('user_account.html', form=usersignupform)


@auth.route('/create_account/developer')
def create_developer_account():
    developersignupform = DeveloperSignUpForm(request.form)

    return render_template('developer_account.html', form=developersignupform)

from flask import render_template, request, redirect, url_for, flash
from . import auth
from .. import db
from ..models import User
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
    form = UserSignUpForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created successfully. You can now Login', 'success')
        return redirect(request.args.get('next') or url_for('auth.login'))

    return render_template('user_account.html', form=form)


@auth.route('/create_account/developer')
def create_developer_account():
    developersignupform = DeveloperSignUpForm(request.form)

    return render_template('developer_account.html', form=developersignupform)

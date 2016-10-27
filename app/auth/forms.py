from flask_wtf import Form
from wtforms import SubmitField, validators, PasswordField, StringField, BooleanField, ValidationError
from ..models import User


class LoginForm(Form):
    """Form where users can login"""
    email = StringField("Email", [
        validators.DataRequired("Please enter your login email."),
        validators.Email("Please enter a valid email address.")])
    password = PasswordField('Password', [
        validators.DataRequired("Please enter a password.")])
    remember_me = BooleanField('remember_me', default=False)

    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class UserSignUpForm(Form):
    """Form for user sign up in creating user account"""
    username = StringField('Username', [
        validators.Length(min=6, max=25, message="Username must have more than 6 characters")])
    email = StringField("Email", [
        validators.DataRequired("Please enter your email address."),
        validators.Email("Please enter a valid email address.")])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    accept_tos = BooleanField('I accept the TAC', [validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class DeveloperSignUpForm(Form):
    """Form for developer sign up in creating user account"""
    username = StringField('Username', [
        validators.Length(min=6, max=25, message="Username must have more than 6 characters")],
        render_kw={"placeholder": "Username"})
    email = StringField("Email", [
        validators.DataRequired("Please enter your email address."),
        validators.Email("Please enter a valid email address.")],
        render_kw={"placeholder": "Email"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')],
        render_kw={"placeholder": "Password"})
    confirm = PasswordField('Confirm Password', render_kw={"placeholder": "Confirm Password"})

    full_name = StringField('Full Name', [
        validators.DataRequired("Please provide your names.")],
        render_kw={"placeholder": "Full Name"})
    website = StringField('Website', [
        validators.DataRequired("Please enter your website url."),
        validators.url("lease enter a valid website url.")],
        render_kw={"placeholder": "Website"})
    accept_tos = BooleanField('I accept the TAC', [validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        super(DeveloperSignUpForm, self).__init__(*args, **kwargs)

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

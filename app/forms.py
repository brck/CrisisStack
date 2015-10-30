from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo

class LoginForm(Form):
      username = StringField('Username', [Required()])
      password = PasswordField('Password', [Required()])

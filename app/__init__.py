__author__ = 'Frankie'
import os 


from flask import Flask, render_template, request, flash, g, session, redirect, url_for
from forms import LoginForm
from decorators import requires_login
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'staticfolder')


db = SQLAlchemy(app)

from app import views, models 



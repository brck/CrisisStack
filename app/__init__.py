__author__ = 'Frankie'
import os 
import logging 


from flask import Flask, render_template, request, flash, g, session, redirect, url_for
from forms import LoginForm
from decorators import requires_login
from flask.ext.sqlalchemy import SQLAlchemy
from logging import FileHandler

app = Flask(__name__)
applogger = app.logger 
file_handler = FileHandler("cserror.log")
file_handler.setLevel(logging.DEBUG)
applogger.setLevel(logging.DEBUG)
applogger.addHandler(file_handler)

app.config.from_object('config')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'staticfolder')


db = SQLAlchemy(app)

from app import views, models 



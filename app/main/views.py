from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/app_info')
def app_info():
    return render_template('app_info.html')

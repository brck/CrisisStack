import os, subprocess , shlex , sys , threading 
import json
from datetime import datetime
from app import app , db , models , forms , APP_STATIC 
from flask import Flask, request, render_template, redirect , url_for , flash , jsonify, json 
from flask_json import FlaskJSON , JsonError, json_response, as_json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', applicationset = models.ApplicationTable.query.filter_by(installed=True), notinstalledapps = models.ApplicationTable.query.filter_by(installed=False))

@app.route('/MyApplications')
def MyApplications():
    return render_template("presentapplications.html", presentapplications = models.ApplicationTable.query.filter_by(installed = True))

@app.route('/MyApplications/<int:app_id>', methods =['POST','GET'])
def myapplication(app_id):
  appentry = models.ApplicationTable.query.get(app_id)
  similarapps = models.ApplicationTable.query.filter_by(categoryId = 1 )
  if request.method == 'GET':
     return render_template("applicationprofile.html", appentry = models.ApplicationTable.query.get(app_id),similarapps = models.ApplicationTable.query.filter_by(categoryId = 1 ))
  elif request.method == 'POST':
      commandline = appentry.uninstallscript
      args = shlex.split(commandline)
      if (subprocess.call(args) == 0):
            appentry.installed = False
            db.session.commit()
            return redirect(url_for('index'))
      elif (subprocess.call(args) == 1):
            flash('your application was not successfully installed, Kindly contact your administrator')
            return redirect(url_for('index'))
      else:
           flash ('Program error. Please contact the developer') 
                  
@app.route('/StoreApplications')
def Storeapplications():
    return render_template("storeApplications.html", storeapplications = models.ApplicationTable.query.filter_by(installed= False))	  

@app.route('/StoreApplications/<int:app_id>', methods = ['GET','POST'])
def storeapplication(app_id):
  storeappentry = models.ApplicationTable.query.get(app_id)
  if request.method =='GET':
      return render_template("applicationprofileinstall.html", storeappentry = models.ApplicationTable.query.get(app_id))      
  elif request.method == 'POST':
      commandline = storeappentry.installscript        
      args = shlex.split(commandline)          
      if (subprocess.call(args) == 0):
            storeappentry.installed = True 
            db.session.commit()
            return redirect(url_for('index'))
      elif (subprocess.call(args) == 1):
            flash('your application was not successfully installed, Kindly contact your administrator')
            return redirect(url_for('index'))
      else:
           flash ('Program error. Please contact the developer') 


@app.route ('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    if request.method =='POST':
        if username != "admin" and password != "password" :
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))
        else: 
            return redirect(url_for('index'))    
    else:
        flash('We are experiencing a problem')
        return redirect(url_for('index'))       
    

@app.errorhandler(404)
def page_not_found(e):
    error = 'This page does not exist'
    return render_template( '404.html', error = error ) 
	

@app.errorhandler(500)
def internal_server_error(error):
    return 'Sorry we are currently experiencing an internal server error'


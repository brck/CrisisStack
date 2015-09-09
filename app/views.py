import os, subprocess , shlex , sys , threading 
from app import app , db , models , forms , APP_STATIC 
from flask import Flask, request, render_template, redirect , url_for , flash 

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', applicationset = models.ApplicationTable.query.filter_by(installed=True))

@app.route('/MyApplications')
def MyApplications():
    return render_template("presentapplications.html", presentapplications = models.ApplicationTable.query.filter_by(installed = True))

@app.route('/MyApplications/<int:app_id>', methods =['DELETE','GET'])
def myapplication(app_id):
  if request.method == 'GET':
     return render_template("applicationprofile.html", appentry = models.ApplicationTable.query.get(app_id))
  elif request.method == 'DELETE':
      if request.form['submit'] == "Delete Application":
          subprocess.call([{{appentry.uninstallscript}}])
          if ( subprocess.call(["echo $?"]) == 0):
               appentry.update().\
               values(installed = 'False') .\
               where(appentry.id == app_id)
               flash ('Your application will be deleted in the background.')
               return render_template("applicationprofile.html", appentry = models.ApplicationTable.query.get(app_id))
          else: 
              flash ('Your application was not successfuly deleted. Please try again ')
              return render_template("applicationprofile.html", appentry = models.ApplicationTable.query.get(app_id))
 
  else: 
          return render_template("applicationprofile.html", appentry = models.ApplicationTable.query.get(app_id))
                  

@app.route('/StoreApplications')
def Storeapplications():
    return render_template("StoreApplications.html", storeapplications = models.ApplicationTable.query.filter_by(installed= False), )	  

@app.route('/StoreApplications/<int:app_id>', methods = ['GET','POST'])
def storeapplication(app_id):
  if request.method =='GET':
      return render_template("applicationprofileinstall.html", storeappentry = models.ApplicationTable.query.get(app_id))      
  elif request.method == 'POST':
        if request.form['submit'] == "Install Application" :
            subprocess.call([{{storeappentry.installscript}}])
            if ( subprocess.call(["echo $?"]) == 0):
               appentry.update().\
               values(installed = 'True') .\
               where(appentry.id == app_id)
               flash('The installation process will run in the background. Kindly launch from Installed applications ')
            else: 
                pass 
        else:
            pass
  else: 
      return render_template("applicationprofileinstall.html", storeappentry = models.ApplicationTable.query.get(app_id))              


@app.route ('/login', methods=['GET'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    if username != "admin" and password != "password" :
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    return redirect(request.args.get('next') or url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    error = 'This page does not exist'
    return render_template( '404.html', error = error ) 
	

@app.errorhandler(500)
def internal_server_error(e):
	return 'Sorry we are currently experiencing an internal server error', 500
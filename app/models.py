
import os
import sys
import base64
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db 

class Person (db.Model):
         # Here we define db.columns for the table person
    # Notice that each db.column is also a normal Python instance attribute.
    __tablename__= 'PersonTable'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable = False)

    def __init__(self,id,name):
        self.id=id
        self.name=name

    def __repr__(self):
        return '<PersonTable %r>' % self.name

class DeveloperTable(db.Model):

    __tablename__='DeveloperTable'
    id = db.Column(db.Integer, primary_key=True)  
    developername = db.Column(db.String(250), nullable= False, unique = True)
    website = db.Column(db.String(250), nullable= False)
    email = db.Column(db.String(20), nullable= False)

    def __init__(self,id,name,website,email,address):
        self.id=id
        self.name=name
        self.website=website
        self.email=email

    def  __repr__(self):
            return '< DeveloperTable %r %r %r >' % (self.developername, self.website, self.email, self.address)   

class categoryTable(db.Model):
    __tablename__ = 'categoryTable'
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(250), nullable=False )

    def __init__(self): 
        self.id = id 
        self.name = name 
    
    def __repr__(self): 
        return '<categorytable, %r %r >' % (self.id, self.name)            

class ApplicationTable (db.Model):
    __tablename__ = 'ApplicationTable'
    ##Here we define colums for the application information table 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique = True)
    version = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False, unique = True)
    size = db.Column(db.Integer, nullable=False)
    developerId = db.Column(db.Integer, db.ForeignKey('DeveloperTable.id')) 
    developerName = db.relationship ('DeveloperTable', primaryjoin = "DeveloperTable.developername== DeveloperTable.id")  
    interactionPoints = db.Column(db.String(250), nullable = False)
    permission = db.Column(db.String(250), nullable = False)
    osVersion = db.Column(db.String(250), nullable = False)
    categoryId = db.Column(db.Integer, db.ForeignKey('categoryTable.id'),nullable=False)
    downloads = db.Column(db.Integer, nullable=False)
    launchurl = db.Column(db.String, nullable=False, unique= True)
    installscript = db.Column(db.String, nullable=False)
    installed = db.Column(db.Boolean,default= False, nullable= False,)
    uninstallscript = db.Column(db.String, nullable=False)


    def __init__(self, id,name,version,description,size,developerId,developerName,interactionPoints,permission,osVersion,categoryId,downloads,launchurl,installscript,installed,uninstallscript):
        self.id = id
        self.name = name
        self.version = version 
        self.description =  description
        self.size =  size
        self.developerId = developerId
        self.developerName = developerName
        self.interactionPoints = interactionPoints
        self.permission = permission
        self.osVersion = osVersion
        self.categoryId = categoryId
        self.downloads = downloads
        self.launchurl = launchurl
        self.installscript = installscript
        self.installed = installed
        self.uninstallscript = uninstallscript

    def __repr__(self):
        return '<ApplicationTable %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r >' % (self.id,self.name,self.version, self.description,self.size,self.developerId,self.developerName,self.icon,self.screenShotOne,self.screenShotTwo,self.screenShotThree,self.screenShotFour,self.video,self.interactionPoints,self.permission,self.osVersion,self.categoryId,self.downloads,self.launchurl,self.installscript,self.installed,self.uninstallscript)

class Address(db.Model):
    __tablename__='AddressTable'
    # Here we define db.columns for the table address.
    # Notice that each db.column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(250))
    street_number = db.Column(db.String(250))
    post_code = db.Column(db.String(250), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('DeveloperTable.id'))

    def __init__(self,id,street_name,street_number,post_code,person_id,person):
        self.id = id 
        self.street_name = name 
        self.street_number = street_number
        self.post_code = post_code
        self.person_id = person_id

    def __repr__(self):    
        return '<AddressTable , %r %r %r %r %r >' % (self.id , self.street_name , self.street_number , self.post_code ,self.person_id)

class applicationupdate(db.Model):
    __tablename__= 'applicationupdatetable'
    id = db.Column(db.Integer, nullable= False, primary_key=True)
    applicationid = db.Column(db.Integer, db.ForeignKey('ApplicationTable.id'))
    version = db.Column(db.Integer, nullable= False)
    updates = db.Column(db.String(250), nullable= False)

    def __init__(self,id,applicationid,version,updates):
        self.id = id
        self.applicationid = applicationid
        self.version = version
        self.updates = updates

    def __repr__(self):
        return '< applicationupdatetable, %r %r %r >' % (self.id , self.applicationid, self.version, self.updates)


        
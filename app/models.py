from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from .app import db


Base = declarative_base()


class User (db.Model):
    # We define db.columns for the users table
    # db.column is a normal python instance

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Users %r>' % self.email

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


association_table = Table(
    'dev_apps', Base.metadata,
    Column('application_id', Integer, ForeignKey('ApplicationTable.id')),
    Column('developer_id', Integer, ForeignKey('DeveloperTable.id'))
)


class Developer(db.Model):
    __tablename__ = 'DeveloperTable'

    id = db.Column(db.Integer, primary_key=True)
    developername = db.Column(db.String(250), nullable=False, unique=True)
    website = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    applications = relationship(
        "ApplicationTable", secondary=association_table)

    def __init__(self, id, name, website, email, address):
        self.id = id
        self.name = name
        self.website = website
        self.email = email

    def __repr__(self):
            return '< DeveloperTable %r %r %r >' % (
                self.developername, self.website, self.email, self.address)


class CategoryTable(db.Model):
    __tablename__ = 'app_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    applications = db.relationship(
        'ApplicationTable', backref='ApplicationTable', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<app_category, %r %r >' % (self.id, self.name)


class ApplicationTable (db.Model):
    __tablename__ = 'ApplicationTable'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey('CategoryTable.id'), nullable=False)
    name = db.Column(db.String(250), nullable=False, unique=True)
    version = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False, unique=True)
    size = db.Column(db.Integer, nullable=False)
    interactionPoints = db.Column(db.String(250), nullable=False)
    permission = db.Column(db.String(250), nullable=False)
    osVersion = db.Column(db.String(250), nullable=False)
    downloads = db.Column(db.Integer, nullable=False)
    launchurl = db.Column(db.String, nullable=False, unique=True)
    installscript = db.Column(db.String, nullable=False)
    installed = db.Column(db.Boolean, default=False, nullable=False,)
    uninstallscript = db.Column(db.String, nullable=False)

    def __init__(
        self, id, name, version, description, size, developerId,
        developerName, interactionPoints, permission, osVersion, categoryId,
            downloads, launchurl, installscript, installed, uninstallscript):

        self.id = id
        self.name = name
        self.version = version
        self.description = description
        self.size = size
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
        return '<ApplicationTable %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r >' % (
            self.id, self.name, self.version, self.description, self.size,
            self.developerId, self.developerName, self.icon,
            self.screenShotOne, self.screenShotTwo, self.screenShotThree,
            self.screenShotFour, self.video, self.interactionPoints,
            self.permission, self.osVersion, self.categoryId,
            self.downloads, self.launchurl, self.installscript,
            self.installed, self.uninstallscript)


class applicationupdate(db.Model):
    __tablename__ = 'applicationupdatetable'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    applicationid = db.Column(db.Integer, db.ForeignKey('ApplicationTable.id'))
    version = db.Column(db.Integer, nullable=False)
    updates = db.Column(db.String(250), nullable=False)

    def __init__(self, id, applicationid, version, updates):
        self.id = id
        self.applicationid = applicationid
        self.version = version
        self.updates = updates

    def __repr__(self):
        return '< applicationupdatetable, %r %r %r >' % (
            self.id, self.applicationid, self.version, self.updates)

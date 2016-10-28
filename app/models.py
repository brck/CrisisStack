from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import json
from flask_login import UserMixin
from flask import current_app
from . import db, login_manager


Base = declarative_base()


class User(UserMixin, db.Model):
    # We define db.columns for the users table
    # db.column is a normal python instance

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    developer = relationship('Developer', backref="developer", uselist=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Return an object representation of the user model
    def __repr__(self):
        return "<User(id='%s', email='%s', username='%s', admin='%s')>" % (
            self.id, self.email, self.username, self.admin)

    # Return a json object of the user model
    def to_json(self):
        return dict(
            id=self.id,
            email=self.email,
            username=self.username,
            admin=self.admin
        )

    # Receive a json object and convert it to a python dictionary
    # representing the user model
    def from_json(self, user_details):
        user = json.loads(user_details)
        self.email = user['name']
        self.username = user['username']
        self.password = user['password']
        self.admin = user['admin']


# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Applications category table model
class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    applications = db.relationship(
        'Application', backref='belongs_to', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<category, %r %r >' % (self.id, self.name)

    def to_json(self):
        return dict(
            id=self.id,
            name=self.name
        )

    def from_json(self, category_details):
        category = json.loads(category_details)
        self.name = category['name']


developer_apps = db.Table(
    'developer_apps',
    db.Column('application_id', db.Integer, db.ForeignKey('application.id')),
    db.Column('developer_id', db.Integer, db.ForeignKey('developer.user_id'))
)


class Developer(db.Model):
    __tablename__ = 'developer'

    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    website = db.Column(db.String(250), nullable=False)
    applications = db.relationship(
        "Application", secondary=developer_apps,
        backref=db.backref('developers'), lazy='dynamic')

    def __repr__(self):
        return '< developer %r %r %r >' % (
            self.name, self.website, self.email)

    def to_json(self):
        return dict(
            id=self.id,
            name=self.developername,
            website=self.website,
            email=self.email
        )

    def from_json(self, developer_details):
        developer = json.loads(developer_details)
        self.name = developer['name']
        self.website = developer['website']
        self.email = developer['email']


# Applications table model
class Application (db.Model):

    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    # Relationship to category table
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(250), nullable=False, unique=True)
    version = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False, unique=True)
    size = db.Column(db.Integer, nullable=False)
    interactionPoints = db.Column(db.String(250), nullable=False)
    permission = db.Column(db.String(250), nullable=False)
    osVersion = db.Column(db.String(250), nullable=False)
    downloads = db.Column(db.Integer, nullable=False)
    launchurl = db.Column(db.String(250), nullable=False, unique=True)
    installscript = db.Column(db.String(250), nullable=False)
    installed = db.Column(db.Boolean, default=False, nullable=False,)
    uninstallscript = db.Column(db.String(250), nullable=False)
    application_updates = db.relationship(
        'ApplicationUpdates', backref='app_updates', lazy='dynamic')
    application_assets = db.relationship(
        'ApplicationAssets', backref='assests', lazy='dynamic')

    def __init__(
        self, name, version, description, size, interactionPoints,
        permission, osVersion, category_id, downloads, launchurl,
            installscript, installed, uninstallscript):

        self.name = name
        self.version = version
        self.description = description
        self.size = size
        self.interactionPoints = interactionPoints
        self.permission = permission
        self.osVersion = osVersion
        self.category_id = category_id
        self.downloads = downloads
        self.launchurl = launchurl
        self.installscript = installscript
        self.installed = installed
        self.uninstallscript = uninstallscript

    def __repr__(self):
        return '<Application %r %r %r %r %r %r %r %r %r %r %r %r %r %r >' % (
            self.id, self.name, self.version, self.description, self.size,
            self.interactionPoints, self.permission, self.osVersion,
            self.category_id, self.downloads, self.launchurl,
            self.installscript, self.installed, self.uninstallscript)

    def to_json(self):
        return dict(
            id=self.id,
            category_id=self.developername,
            name=self.name,
            version=self.version,
            description=self.description,
            size=self.size,
            interactionPoints=self.interactionPoints,
            permission=self.permission,
            osVersion=self.osVersion,
            downloads=self.downloads,
            launchurl=self.launchurl,
            installscript=self.installscript,
            installed=self.installed,
            uninstallscript=self.uninstallscript
        )

    def from_json(self, application_details):
        application = json.loads(application_details)

        self.name = application['name']
        self.version = application['version']
        self.description = application['description']
        self.size = application['size']
        self.interactionPoints = application['interactionPoints']
        self.permission = application['permission']
        self.osVersion = application['osVersion']
        self.category_id = application['category_id']
        self.downloads = application['downloads']
        self.launchurl = application['launchurl']
        self.installscript = application['installscript']
        self.installed = application['installed']
        self.uninstallscript = application['uninstallscript']


class ApplicationUpdates(db.Model):

    __tablename__ = 'applicationupdates'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    version = db.Column(db.Integer, nullable=False)
    updates = db.Column(db.String(250), nullable=False)

    def __init__(self, application_id, version, updates):
        self.application_id = application_id
        self.version = version
        self.updates = updates

    def __repr__(self):
        return '< applicationupdates, %r %r %r >' % (
            self.id, self.application_id, self.version, self.updates)

    def to_json(self):
        return dict(
            id=self.id,
            application_id=self.application_id,
            version=self.version,
            updates=self.updates
        )

    def from_json(self, update_details):
        updates = json.loads(update_details)

        self.application_id = updates['application_id']
        self.version = updates['version']
        self.updates = updates['updates']


class ApplicationAssets(db.Model):

    __tablename__ = 'applicationassets'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    icon = db.Column(db.String(250), nullable=False, unique=True)
    screenShotOne = db.Column(db.String(250), unique=True)
    screenShotTwo = db.Column(db.String(250), unique=True)
    screenShotThree = db.Column(db.String(250), unique=True)
    screenShotFour = db.Column(db.String(250), unique=True)
    video = db.Column(db.String(250), unique=True)

    def __init__(
        self, application_id, icon, screenShotOne, screenShotTwo,
            screenShotThree, screenShotFour, video):
        self.application_id = application_id
        self.icon = icon
        self.screenShotOne = screenShotOne
        self.screenShotTwo = screenShotTwo
        self.screenShotThree = screenShotThree
        self.screenShotFour = screenShotFour
        self.video = video

    def __repr__(self):
        return '< applicationassets, %r %r %r >' % (
            self.id, self.app_id, self.version, self.updates)

    def to_json(self):
        return dict(
            id=self.id,
            application_id=self.application_id,
            screenShotOne=self.screenShotOne,
            screenShotTwo=self.screenShotTwo,
            screenShotThree=self.screenShotThree,
            screenShotFour=self.screenShotFour,
            video=self.video
        )

    def from_json(self, assets_details):
        assets = json.loads(assets_details)

        self.application_id = assets['application_id']
        self.screenShotOne = assets['screenShotOne']
        self.screenShotTwo = assets['screenShotTwo']
        self.screenShotThree = assets['screenShotThree']
        self.screenShotFour = assets['screenShotFour']
        self.video = assets['video']

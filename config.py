import os
basedir = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MYDIR = os.path.dirname(__file__)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rugged internet for people'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'app/static/scripts/install')
    APPLICATIONS_DIR = os.path.join(APP_ROOT, 'app/static/applications/')
    if not os.path.exists(APPLICATIONS_DIR):
        os.makedirs(APPLICATIONS_DIR)
    ROOT_DIR = APP_ROOT
    APP_TEMPLATE_ASSESTS = 'applications'
    DEFAULT_APPS_DIR = 'app/static/default_apps/'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev_db.db')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'crisis_stack.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

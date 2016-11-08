
import unittest
import uuid
from flask import current_app
from sqlalchemy.exc import IntegrityError
from app.models import User, Application, Developer, Category, ApplicationAssets
from app import create_app, db


class ContextTestCase(unittest.TestCase):
    """Create TestCase containing app context"""

    def __call__(self, result=None):
        try:
            self._pre_setup()
            super(ContextTestCase, self).__call__(result)
        finally:
            self._post_teardown()

    def _pre_setup(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_teardown(self):
        if getattr(self, '_ctx') and self._ctx is not None:
            self._ctx.pop()
        del self._ctx


class BaseTestCase(ContextTestCase):
    """Crisis Stack base test case."""

    def create_user_account(self):
        user = User.query.filter_by(email='admin@cs.com').first()
        if user is None:
            try:
                user = User(uuid=str(uuid.uuid4()), email='admin@cs.com',
                            username='admin', password='admin')
                db.session.add(user)
            except IntegrityError as e:
                db.session.rollback()
        return user

    def create_developer_account(self):
        user = self.create_user_account()
        developer = Developer.query.filter_by(user_id=user.id).first()
        if developer is None:
            try:
                developer = Developer(user_id=user.id, name='Awesome Devs',
                                      website='http://www.devs.com')

                db.session.add(developer)
            except IntegrityError as e:
                db.session.rollback()
        return developer

    def add_category(self):
        category = Category.query.filter_by(name='category').first()
        if category is None:
            try:
                category = Category(name='category', description='some description')
                db.session.add(category)
            except IntegrityError as e:
                db.session.rollback()
        return category

    def add_application(self):
        application = Application.query.filter_by(id=1).first()

        if application is None:
            developer = self.create_developer_account()
            new_category = self.add_category()

            try:
                application = Application(
                    category_id=new_category.id,
                    name='app_name',
                    version='1.0',
                    description='some great app',
                    size='1000',
                    permission='OS-Admin',
                    osVersion='Some OS',
                    developer_id=developer.user_id,
                    launchurl='http://www.testing.com')

                db.session.add(application)
            except IntegrityError as e:
                db.session.rollback()
        return application

    def add_assets(self):
        application = self.add_application()
        assets = ApplicationAssets.query.filter_by(application_id=application.id).first()
        if assets is None:
            try:
                assets = ApplicationAssets(
                    application_id=application.id,
                    icon='icon.png',
                    screenShotOne='browser.png',
                    screenShotTwo='browser.png',
                    screenShotThree='browser.png',
                    screenShotFour='browser.png',
                    video='video')

                db.session.add(assets)
            except IntegrityError as e:
                db.session.rollback()
        return application

    def setUp(self):

        db.create_all()

        self.create_user_account()
        self.create_developer_account()
        self.add_category()
        self.add_application()
        self.add_assets()

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

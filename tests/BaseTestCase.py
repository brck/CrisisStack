
import unittest
from flask import current_app
from app.models import User, Application, Developer, Category
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

    def user(self):
        return User(username='admin', email='admin@cs.com', password='admin')

    def developer(self):
        user = User(email='developer@devs.com', username='developer',
                    password='developer')

        db.session.add(user)
        db.session.flush()

        return Developer(user_id=user.id, name='Developers', website='http:www.devs.com')

    def category(self):
        return Category(name='Category', description='Some Fancy Category')

    def application(self):
        return Application(category_id=self.category.id, name='app_name',
                           version='1.0', description='some great app',
                           size='1000', permission='OS-Admin', osVersion='Some OS',
                           developer_id=self.developer.user_id, launchurl='http://www.app.com')

    def setUp(self):

        db.create_all()

        db.session.add(User(username='admin', email='admin@cs.com', password='admin'))
        # db.session.add(self.developer)
        # db.session.add(self.category)
        # db.session.add(self.application)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

import unittest
from flask import current_app
from app.models import User
from app import create_app, db


class CrisisStackTestCase(unittest.TestCase):
    """A base test case for crisis stack."""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.app = self.app.test_client()
        self.db = db
        self.db.create_all()

        if User.query.filter_by(username='admin').count() == 0:
            self.user = User(username='admin',
                            email='admin@cs.com',
                            password='admin')

            self.db.session.add(self.user)
            self.db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    if __name__ == '__main__':
        unittest.main()

# tests/test_auth.py

import unittest
import uuid
from flask import url_for, request
from app.models import User
from flask_login import current_user
from BaseTestCase import BaseTestCase


class TestUserModel(BaseTestCase):
    """
    Tests for user db table and model
    """

    def create_user(self, uuid, username, email, password, confirm, terms):
        return self.client.post(url_for("auth.create_user_account"), data=dict(
            uuid=uuid,
            email=email,
            username=username,
            password=password,
            confirm=confirm,
            accept_tos=terms
        ), follow_redirects=True)

    def test_user_creation_success(self):
        """_____User should be found in the database after creation"""

        with self.client:
            user_uuid = str(uuid.uuid4())
            response = self.create_user(user_uuid, 'testing', 'testing@cs.com',
                                        'testing', 'testing', True)

            self.assertIn(b'Your account has been created successfully', response.data)

            user = User.query.filter_by(email='testing@cs.com').count()
            self.assertTrue(user == 1)

    def test_incorrect_user_registeration(self):
        """_____Errors should be thrown during an incorrect user registration"""

        with self.client:
            user_uuid = str(uuid.uuid4())
            response = self.create_user(user_uuid, 'testing', 'testing.com',
                                        'testing', 'testing', True)
            self.assertIn(b'Please enter a valid email address.', response.data)
            self.assertIn(b'/user', request.url)

    def test_get_by_id(self):
        """_____User id should be correct for the current/logged in user"""

        with self.client:
            self.client.post('/login', data=dict(
                email="admin@cs.com", password='admin'
            ), follow_redirects=True)
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id == 20)

    def test_check_password(self):
        """_____Entered password should be correct after unhashing"""

        user = User.query.filter_by(email='admin@cs.com').first()
        self.assertTrue(user.verify_password('admin'))
        self.assertFalse(user.verify_password('another_admin'))


class TestUserViews(BaseTestCase):
    """
    Tests for user blueprint views
    """

    def test_login_page_loads(self):
        """_____Login page should load successfully"""

        response = self.client.get('/login')
        self.assertIn(b'Please login', response.data)

    def test_create_account_page_loads(self):
        """_____Create account page loads successfully"""

        response = self.client.get(url_for("auth.create_account"))
        self.assertTrue(b'Create Account' in response.data)

    def test_create_developer_account_page_loads(self):
        """_____Create developer account page loads successfully"""

        response = self.client.get(url_for("auth.create_developer_account"))
        self.assertTrue(b'website' in response.data)

    def test_correct_login(self):
        """_____Ensure login behaves correctly with correct credentials"""

        with self.client:
            response = self.login('admin@cs.com', 'admin')

            self.assertIn(b'Logout', response.data)
            self.assertTrue(current_user.username == "admin")
            self.assertTrue(current_user.is_active)

    def test_incorrect_login(self):
        """_____Ensure login behaves correctly with incorrect credentials"""

        with self.client:
            response = self.login('wrong.com', 'wrong')
            self.assertIn(b'Please login', response.data)

    def test_logout(self):
        """_____Ensure logout behaves correctly"""

        with self.client:
            self.login('admin@cs.com', 'admin')

            response = self.client.get('/logout', follow_redirects=True)

            self.assertTrue(b'Logout' not in response.data)
            self.assertFalse(current_user.is_active)
            self.assertTrue(current_user.is_anonymous)

    def test_logout_route_requires_login(self):
        """_____Ensure that logout page requires user login"""

        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please login', response.data)


if __name__ == '__main__':
    unittest.main()

import flask
from flask import url_for
from flask_login import current_user
import CrisisStackTest
from app.models import User


class AuthTests(CrisisStackTest.CrisisStackTestCase):

    def login(self, email, password):
        return self.app.post(
            url_for("auth.login"), data=dict(email=email, password=password),
            follow_redirects=True)

    def logout(self):
        return self.app.get('/auth/logout', follow_redirects=True)

    def create(self, username, email, password, confirm, terms):
        return self.app.post(url_for("auth.create_user_account"), data=dict(
            email=email,
            username=username,
            password=password,
            confirm=confirm,
            accept_tos=terms
        ), follow_redirects=True)

    def test_page_not_found(self):
        """====== Pages which dont exist should be directed to a 404 page"""
        response = self.app.get('/a-page-which-doesnt-exist')
        self.assertTrue(b'404' in response.data)

    def test_login_page_loads(self):
        """====== Login page loads successfully"""
        response = self.app.get(url_for("auth.login"))
        self.assertTrue(b'Please login' in response.data)

    def test_create_account_page_loads(self):
        """====== Create account page loads successfully"""
        response = self.app.get(url_for("auth.create_account"))
        self.assertTrue(b'Create Account' in response.data)

    def test_create_developer_account_page_loads(self):
        """====== Create developer account page loads successfully"""
        response = self.app.get(url_for("auth.create_developer_account"))
        self.assertTrue(b'website' in response.data)

    def test_user_creation_success(self):
        """====== User should be found in the database after creation"""
        with self.app as c:
            self.create('testing',
                'testing@cs.com',
                'testing',
                'testing',
                True)

            user = User.query.filter_by(email='testing@cs.com').count()
            self.assertTrue(user == 1)

    def test_login_success_session(self):
        """====== Successfull login should put user_name in session"""
        with self.app as c:
            response = self.login('admin@cs.com', 'admin')
            self.assertTrue(current_user.username == "admin")
            self.assertFalse(current_user.is_anonymous)

    # def test_index_page_loads_correctly(self):
    #     self.browser.get('http://localhost:5000')
    #     self.assertIn("Crisis Stack", self.browser.title)

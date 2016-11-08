# tests/test_main.py

import unittest
import uuid
from flask import url_for, request
from app.models import Category, Developer, Application, User, ApplicationAssets
from BaseTestCase import BaseTestCase


class TestMainModels(BaseTestCase):
    """
    Tests for main blueprint tables and models
    """

    pass


class TestMainViews(BaseTestCase):
    """
    Tests for main blueprint views
    """

    def test_page_not_found(self):
        """_____Pages which dont exist should be directed to a 404 page"""

        response = self.client.get('/a-page-which-doesnt-exist')
        self.assertTrue(b'404' in response.data)

    def test_home_page_loads(self):
        """_____Home page should load successfully"""

        response = self.client.get('/')
        self.assertIn(b'Installed Apps', response.data)

    def test_nav_links_display_for_logged_in_users(self):
        """_____Navigation Links should display for logged in users"""

        self.login('admin@cs.com', 'admin')
        response = self.client.get('/')
        self.assertIn(b'Add Category', response.data)

    def test_no_nav_links_for_anonymous_users(self):
        """_____No navigation links for anonymous users"""

        response = self.client.get('/')
        self.assertTrue(b'Add Category' not in response.data)

    def test_added_apps_are_displayed_in_home_page(self):
        """_____Added applications should be displayed on the home page"""

        app = self.add_application()
        response = self.client.get('/')
        self.assertTrue(app.name.encode() in response.data)

    def test_installed_apps_are_displayed(self):
        """_____Installed apps should be displayed in installed apps section"""

        app = self.add_application()
        response = self.install_app(app.id)
        self.assertIn(b'/launch_app?app_id=1', response.data)

    def test_added_categories_are_displayed(self):
        """_____Installed apps should be displayed in installed apps section"""

        category = self.add_category()
        response = self.client.get('/category')
        self.assertTrue(category.description.encode() in response.data)


if __name__ == '__main__':
    unittest.main()

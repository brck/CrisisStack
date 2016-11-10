# tests/test_main.py

import unittest
import uuid
from StringIO import StringIO
import os
import shutil
import io
from flask import url_for, request, current_app
from app.models import Category, Developer, Application, User, ApplicationAssets
from BaseTestCase import BaseTestCase


class TestMainModels(BaseTestCase):
    """
    Tests for main blueprint tables and models
    """
    def save_application(self, category_id, developer_id, version, description,
                         permission, osVersion, launchurl, app_file):
        return self.client.post(
            url_for("main.application"),
            content_type='multipart/form-data',
            data=dict(category_id=category_id, developer_id=developer_id,
                      version=version, description=description, permission=permission,
                      osVersion=osVersion, launchurl=launchurl, app_file=app_file),
            follow_redirects=True)

    def save_application_assets(self, screenshot1, screenshot2, screenshot3,
                                screenshot4, icon, video):
        developer = self.create_developer_account()
        category = self.add_category()

        with self.client:
            testfile_bytes = "fdjasdfjksjkadffgfgfgfgfgxsddsdsd"
            app_file = (StringIO(testfile_bytes), 'testing.sh')

            response = self.save_application(category.id, developer.user_id, '1.0',
                                             'some new great app', 'OS-Admin', 'Raspbian',
                                             'http://www.newapp.com', app_file)
            app = Application.query.filter_by(launchurl='http://www.newapp.com').first()

        return self.client.post(
            url_for("main.app_assets1", app_uuid=app.uuid),
            content_type='multipart/form-data',
            data=dict(screenshot1=screenshot1, screenshot2=screenshot2,
                      screenshot3=screenshot3, screenshot4=screenshot4,
                      icon=icon, video=video),
            follow_redirects=True)

    def add_app_assets(self):
        """
        Helper function to add an applications assets that returns a response
        received from add_assets route from view. The function uses test client
        of its calling function
        """
        developer = self.create_developer_account()
        category = self.add_category()

        testfile_bytes = "fdjasdfjksjkadffgfgfgfgfgxsddsdsd"
        screenshot1 = (StringIO(testfile_bytes), 'image1.png')
        screenshot2 = (StringIO(testfile_bytes), 'image2.png')
        screenshot3 = (StringIO(testfile_bytes), 'image3.png')
        screenshot4 = (StringIO(testfile_bytes), 'image4.png')
        icon = (StringIO(testfile_bytes), 'icon1.png')
        video = (StringIO(testfile_bytes), 'video1.mp4')

        return self.save_application_assets(screenshot1, screenshot2, screenshot3,
                                            screenshot4, icon, video)

    def save_category(self, name, description):
        return self.client.post(
            url_for("main.category"),
            data=dict(name=name, description=description),
            follow_redirects=True)

    def test_adding_new_applications(self):
        """_____Added application should be found in the database"""
        developer = self.create_developer_account()
        category = self.add_category()

        with self.client:
            testfile_bytes = "fdjasdfjksjkadffgfgfgfgfgxsddsdsd"
            app_file = (StringIO(testfile_bytes), 'testing.sh')

            response = self.save_application(category.id, developer.user_id, '1.0',
                                             'some new great app', 'OS-Admin', 'Raspbian',
                                             'http://www.newapp.com', app_file)
            app = Application.query.filter_by(launchurl='http://www.newapp.com')
            app_count = app.count()
            app_obj = app.first()

            self.assertTrue(app_count == 1)

            APPLICATIONS_DIR = current_app.config['APPLICATIONS_DIR']
            file_dir = os.path.join(APPLICATIONS_DIR, app_obj.uuid)
            file_path = os.path.join(file_dir, 'testing.sh')
            os.remove(file_path)
            shutil.rmtree(file_dir)

    def test_adding_applications_assets(self):
        """_____Added application should be found in the database"""
        response = self.add_app_assets()
        app_assets = ApplicationAssets.query.filter_by(screenShotOne='screenshot1.png').first()

        self.assertTrue('screenshot4.png' == app_assets.screenShotFour)

        APPLICATIONS_DIR = current_app.config['APPLICATIONS_DIR']
        file_dir = os.path.join(APPLICATIONS_DIR, app_assets.app_uuid)
        shutil.rmtree(file_dir)

    def test_adding_new_category(self):
        """_____Added category should be found in the database"""
        with self.client:
            response = self.save_category('Some Category', 'Great description')

            category = Category.query.filter_by(name='Some Category').count()
            self.assertTrue(category == 1)


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

    def test_applications_page_loads(self):
        """_____Applications page loads successfully"""
        response = self.client.get(url_for("main.application"))
        self.assertTrue(b'Application Details' in response.data)

    def test_added_apps_are_displayed_in_home_page(self):
        """_____Added applications should be displayed on the home page"""
        app = self.add_application()
        response = self.client.get('/')
        self.assertTrue(app.name.encode() in response.data)

    def test_app_info_page(self):
        """_____Applications info page should load successfully"""
        app = self.add_application()
        assets = self.add_assets()

        response = self.client.get(url_for('main.app_info1', app_uuid=app.uuid))
        self.assertTrue(app.name.encode() in response.data)
        self.assertTrue(app.uuid.encode() in response.data)

    def test_installed_apps_are_displayed(self):
        """_____Installed apps should be displayed in installed apps section"""
        app = self.add_application()
        response = self.install_app(app.uuid)
        self.assertIn(b'/launch_app?app_id=%s' % (str(app.uuid)), response.data)

    def test_app_categoty_page_loads(self):
        """_____Category page loads successfully"""
        response = self.client.get(url_for("main.category"))
        self.assertTrue(b'Category Description' in response.data)

    def test_added_categories_are_displayed(self):
        """_____Installed apps should be displayed in installed apps section"""
        category = self.add_category()
        response = self.client.get('/category')
        self.assertTrue(category.description.encode() in response.data)


if __name__ == '__main__':
    unittest.main()

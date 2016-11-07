import unittest
import uuid
from selenium import webdriver
from sqlalchemy.exc import IntegrityError
from app import db
from flask import url_for
import CrisisStackTest
from app.models import Category, Developer, Application, User, ApplicationAssets


class UserModelTestCase(CrisisStackTest.CrisisStackTestCase):
    def add_category(self):
        return Category(name='category', description='some description')

    def add_app_to_db(self):
        new_app = None
        developer = self.create_developer()

        try:
            new_category = self.add_category()
            db.session.add(new_category)
            db.session.flush()

            new_app = Application(
                category_id=new_category.id,
                name='app_name',
                version='1.0',
                description='some great app',
                size='1000',
                permission='OS-Admin',
                osVersion='Some OS',
                developer_id=developer.user_id,
                launchurl='http://www.testing.com')

            db.session.add(new_app)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()

        return new_app

    def create_new_user(self):
        user = None
        try:
            user = User(uuid=str(uuid.uuid4()),
                        email='developer@dev.com',
                        username='developer',
                        password='developer')
            db.session.add(user)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()

        return user

    def create_developer(self):
        developer = None
        user = User(uuid=str(uuid.uuid4()),
                    email='developer@dev.com',
                    username='developer',
                    password='developer')

        try:
            db.session.add(user)
            db.session.flush()

            developer = Developer(
                user_id=user.id,
                name='Awesome Devs',
                website='http://www.devs.com')

            db.session.add(developer)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()

        return developer

    def test_adding_category(self):
        """====== Successfull addition should have category  name in database"""
        new_category = self.add_category()
        db.session.add(new_category)
        db.session.commit()

        self.assertTrue(Category.query.filter_by(id=new_category.id))

    def test_adding_application(self):
        """====== Successfull addition should have application details in database"""

        new_app = self.add_app_to_db()
        self.assertTrue(Application.query.filter_by(id=new_app.id))

    def test_app_categoty_page_loads(self):
        """====== Category page loads successfully"""
        response = self.app.get(url_for("main.category"))
        self.assertTrue(b'Category Description' in response.data)

    def test_applications_page_loads(self):
        """====== Applications page loads successfully"""
        response = self.app.get(url_for("main.application"))
        self.assertTrue(b'Application Details' in response.data)

    def test_app_info(self):
        """====== Application info page should have details of selected app"""

        new_app = self.add_app_to_db()
        try:
            assets = ApplicationAssets(
                application_id=new_app.id,
                icon='icon.png',
                screenShotOne='browser.png',
                screenShotTwo='browser.png',
                screenShotThree='browser.png',
                screenShotFour='browser.png',
                video='video')

            db.session.add(assets)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()

        response = self.app.get(url_for('main.app_info', app_id=new_app.id))
        self.assertTrue(new_app.name.encode("utf-8") in response.data)

    def test_application_without_assets_is_inactive(self):
        """====== Applications without assets should be inactive"""

        new_app = self.add_app_to_db()
        app_assets = ApplicationAssets.query.filter_by(application_id=new_app.id).count()

        # user = User.query.filter_by(email='testing@cs.com').count()
        self.assertTrue(app_assets == 0)

    def test_active_applications_have_assets(self):
        """====== Applications with assets should be active"""

        new_app = self.add_app_to_db()

        try:
            assets = ApplicationAssets(
                application_id=new_app.id,
                icon='icon.png',
                screenShotOne='browser.png',
                screenShotTwo='browser.png',
                screenShotThree='browser.png',
                screenShotFour='browser.png',
                video='video')

            db.session.add(assets)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()

        app = Application.query.first()
        app_assets = ApplicationAssets.query.first()

        self.assertTrue(app.id, app_assets.application_id)

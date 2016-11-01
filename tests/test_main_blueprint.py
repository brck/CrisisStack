import unittest
from selenium import webdriver
from sqlalchemy.exc import IntegrityError
from app import db
from flask import url_for
import CrisisStackTest
from app.models import Category, Developer, Application


class UserModelTestCase(CrisisStackTest.CrisisStackTestCase):
    def add_category(self):
        return Category(name='category', description='some description')

    def test_adding_category(self):
        """====== Successfull addition should have category  name in database"""
        new_category = self.add_category()
        db.session.add(new_category)
        db.session.commit()

        self.assertTrue(Category.query.filter_by(id=new_category.id))

    def test_adding_application(self):
        """====== Successfull addition should have application details in database"""
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
                launchurl='http://www.testing.com')

            db.session.add(new_app)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()

        self.assertTrue(Application.query.filter_by(id=new_app.id))

    def test_app_categoty_page_loads(self):
        """====== Category page loads successfully"""
        response = self.app.get(url_for("main.category"))
        self.assertTrue(b'Category Description' in response.data)

    def test_applications_page_loads(self):
        """====== Applications page loads successfully"""
        response = self.app.get(url_for("main.application"))
        self.assertTrue(b'Application Details' in response.data)


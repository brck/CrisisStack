import unittest
from selenium import webdriver
from flask import current_app
from app.models import User
from app import create_app, db


class PagesLoadingCorrectly(unittest.TestCase):
    def setUp(self):
        self.browser=webdriver.Chrome("/usr/bin/chromedriver")
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
        self.browser.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page_loads_correctly(self):
        self.browser.get('http://localhost:5000')
        self.assertIn("Crisis Stack", self.browser.title)

    def test_categoty_page_populates_database(self):
        """Category page updates database successfully"""
        self.browser.get('http://localhost:5000/application')

        #find all form input fields via form name
        _inputs = self.browser.find_elements_by_xpath('//form[@name="signup-form"]//input')

        for input in _inputs:
            #print attribute name of each input element
            print id.get_attribute('name')

        self.assertIn("Crisis Stack", self.browser.title)

if __name__ == '__main__':
    unittest.main()


import unittest
from selenium import webdriver


class PagesLoadingCorrectly(unittest.TestCase):
    def setUp(self):
        self.browser=webdriver.Chrome("/usr/bin/chromedriver")

    def tearDown(self):
        self.browser.quit()

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


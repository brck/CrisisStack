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


if __name__ == '__main__':
    unittest.main()


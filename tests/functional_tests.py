from selenium import webdriver

browser=webdriver.Chrome("/usr/bin/chromedriver")

browser.get('http://localhost:5000')

assert "Crisis Stack" in browser.title

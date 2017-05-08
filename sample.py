from selenium import webdriver
from selenium.webdriver.common.keys import Keys



browser = webdriver.Firefox()
browser.get("https://www.google.com")
browser.quit()
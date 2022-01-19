from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import ActionChains
import time

driver = webdriver.Chrome("./chromedriver")
driver.get("http://127.0.0.1:8000")
driver.quit()

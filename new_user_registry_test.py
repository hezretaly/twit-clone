from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome("./chromedriver")
driver.get("http://127.0.0.1:8000")
driver.find_element_by_link_text('Sign up').click()

# Creating new user
driver.find_element_by_name("username").send_keys("Turkey")
driver.find_element_by_name("email").send_keys("turkey@turkey.com")
driver.find_element_by_name("password").send_keys("murkey")
driver.find_element_by_name("password2").send_keys("murkey")
driver.find_element_by_name("submit").send_keys(Keys.RETURN)

# Login
login_button = driver.find_element_by_link_text('Login')
login_button.click()
if driver.title.find("Sign in") == -1:
	print("how come not found?")
	driver.quit()

login_name = driver.find_element_by_name("username")
login_password = driver.find_element_by_name("password")
login_name.send_keys("Turkey")
login_password.send_keys("murkey")
login_password.send_keys(Keys.RETURN)

driver.quit()
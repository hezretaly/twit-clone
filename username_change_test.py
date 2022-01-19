# Username change(info. alteration)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome("./chromedriver")
driver.get("http://127.0.0.1:8000")
# Login
login_button = driver.find_element_by_link_text('Login')
login_button.click()
if driver.title.find("Sign in") == -1:
	print("how come not found?")
	driver.quit()

login_name = driver.find_element_by_name("username")
login_password = driver.find_element_by_name("password")
login_name.send_keys("Susan")
login_password.send_keys("Susan")
login_password.send_keys(Keys.RETURN)

# Name change locating
driver.find_element_by_link_text('Profile').click()
driver.find_element_by_link_text('Edit Profile').click()

# Name chage actions
username_elem = driver.find_element_by_name('username')
username_elem.clear()
username_elem.send_keys("Susanna")
username_elem.send_keys(Keys.RETURN)


driver.quit()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome("./chromedriver")
driver.get("http://127.0.0.1:8000")
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
# THIS FAR LOGIN PASSED SUCCESSFULLY
# Let's check it
if driver.title.find("Home Page") == -1:
	driver.quit()

# Now find search field and insert the search-word, 
# but first it should be in the Articles page
# there will be an expenation on why user should be in Articles page to search articles
driver.find_element_by_link_text('Articles').click()
serach_field = driver.find_element_by_name('q')
serach_field.send_keys('flask')
serach_field.send_keys(Keys.RETURN)

# This should've returned the articles that include 'falsk' in their
# header or body
# Let's check it
count = len(driver.find_elements_by_xpath('//table'))
if count < 2:
	print("fail: wrong number of articles")
	driver.quit()
# we check if it's equal two because there are
# two articles containing word 'flask' in them currently.
# there could be more intricate solution but for time 
# considirations I chose easier one


driver.quit()



# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
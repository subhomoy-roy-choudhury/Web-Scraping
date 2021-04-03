from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import sys

a=sys.argv[1]


PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)
web = str(a)+'/'
driver.get("https://pypi.org/project/"+str(web))

# assert "Python" in driver.title
elem = driver.find_element_by_id("pip-command")
print("########",elem.text)
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
time.sleep(2)
# assert "No results found." not in driver.page_source
driver.close()
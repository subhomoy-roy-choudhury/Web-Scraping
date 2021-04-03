from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup

val="machine"
a="https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText="+str(val)
page = requests.get(str(a))
print(a)
soup = BeautifulSoup(page.content, 'html.parser')

with open("results.html","w") as file:
    # print(soup.prettify())
    file.write(soup.prettify())
time.sleep(5)


# # assert "Python" in driver.title
# elem = driver.find_element_by_id("pip-command")
# print("########",elem.text)
# # elem.clear()
# # elem.send_keys("pycon")
# # elem.send_keys(Keys.RETURN)
# time.sleep(2)
# # assert "No results found." not in driver.page_source
# driver.close()
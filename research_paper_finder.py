from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


val = input("Enter your value: ") 
val = val.replace(" ","%20")
time.sleep(2)
if val is not None: 
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText="+str(val))
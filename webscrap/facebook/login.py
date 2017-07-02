from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def fb_login(userid,password):
    driver = webdriver.Firefox()
    driver.get('https://www.facebook.com')
    userElem = driver.find_element_by_id('email')
    passElem = driver.find_element_by_id('pass')
    userElem.send_keys(userid)
    passElem.send_keys(password)
    passElem.send_keys(Keys.RETURN)
    return webdriver

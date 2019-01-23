## Setup
	1. Run install.sh to autocreate all the folders, install dependenceies, and move files to them
	2. Create a simple cred phishing site based on client's SSO portal similar to https://portalhome.client.com
	3. Configure phishforward.py to point to the sites you want. You can test out the selection and login process by running phishphorward.py on your system and using the chromedriver instead of phantomJS.
	4. On your phishing site, make the form action /cgi-bin/submit.py
	5. run watchdog.py and leave it running while you phish. Might be helpful to make a service of some kind.
	6. Once you capture user's creds copy and paste the cookies into phishreplay.py , point it to the site, and run it

## Tips
I highly recommend getting pushover and putting your token in phishforward.py, this will alert you whenever a new submission occurs.

## Needed Updates:

Update to support pass-through so users will actually be authed to the site (and thus less suspicious)

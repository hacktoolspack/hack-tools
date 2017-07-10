#!/usr/bin/env python
# WebPwn3r is a Web Applications Security Scanner
# By Ebrahim Hegazy - twitter.com/zigoo0
# First demo conducted 12Apr-2014 @OWASP Chapter Egypt
# https://www.owasp.org/index.php/Cairo
import urllib
import re
import time
from urllib import FancyURLopener

class colors:
        def __init__(self):
                self.green = "\033[92m"
                self.blue = "\033[94m"
                self.bold = "\033[1m"
                self.yellow = "\033[93m"
                self.red = "\033[91m"
                self.end = "\033[0m"
ga = colors()

class UserAgent(FancyURLopener):
	version = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'

useragent = UserAgent()

class HTTP_HEADER:
    HOST = "Host"
    SERVER = "Server"

def headers_reader(url):
	# This function will print the server headers such as WebServer OS & Version.
	print ga.bold+" \n [!] Fingerprinting the backend Technologies."+ga.end
	opener = urllib.urlopen(url)
	if opener.code == 200:
		 print ga.green+" [!] Status code: 200 OK"+ga.end
	if opener.code == 404:
		 print ga.red+" [!] Page was not found! Please check the URL \n"+ga.end
		 exit()
	#Host = opener.headers.get(HTTP_HEADER.HOST)
	Server = opener.headers.get(HTTP_HEADER.SERVER)
	# HOST will split the HostName from the URL
	Host = url.split("/")[2]
	print ga.green+" [!] Host: " + str(Host) +ga.end
	print ga.green+" [!] WebServer: " + str(Server) +ga.end
	for item in opener.headers.items():
	    for powered in item:
		sig = "x-powered-by"		
		if sig in item:
		    print ga.green+ " [!] " + str(powered).strip() + ga.end

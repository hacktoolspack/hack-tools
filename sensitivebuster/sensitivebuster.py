#!/usr/bin/env python

#1-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==0
#0     _                   __           __       __                    			 1
#1   /' \            __  /'__`\        /\ \__  /'__`\                   		 0
#0  /\_, \    ___   /\_\/\_\ \ \    ___\ \ ,_\/\ \/\ \  _ ___           		 1
#1  \/_/\ \ /' _ `\ \/\ \/_/_\_<_  /'___\ \ \/\ \ \ \ \/\`'__\          	     0
#0     \ \ \/\ \/\ \ \ \ \/\ \ \ \/\ \__/\ \ \_\ \ \_\ \ \ \/                    1
#1      \ \_\ \_\ \_\_\ \ \ \____/\ \____\\ \__\\ \____/\ \_\                    0
#0       \/_/\/_/\/_/\ \_\ \/___/  \/____/ \/__/ \/___/  \/_/                    1
#1                  \ \____/ >> Exploit database separated by exploit            0
#0                   \/___/          type (local, remote, DoS, etc.)             1
#1                                                                               1
#0  [+] Site            : 1337day.com                                            0
#1  [+] Support e-mail  : submit[at]1337day.com                                  1
#0                                                                               0
#1               #########################################                       1
#0      we are Angel Injection and th3breacher  members of Inj3ct0r Team        1
#1               #########################################                       0
#0-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=1
# This was written for educational purpose and pentest only. 
# Use it at your own risk. Author will be not responsible for any damage!
# Coders      : th3breacher | Angel Injection
# Version     : 1
# Description : That's a Sensitive data buster , it has 5 modes : 
#				shell:It looks for known shells in a website
#				backup:It looks for Backups in a website
#				admin:It looks for admin pages
#				dir:It looks for known sensitive Directories
#				files:It looks for sensitive files
# Usage      :  Simply run ./sensitivebuster.py <http:url> -m <mode> -p <proxy>
#               the result will be logged in a .txt log file
# Tested on  :  linux(all) , Windows
# Special thanks to :  r0073r, r4dc0re, Sid3^effects, L0rd CrusAd3r, KedAns-Dz(1337day.com)
#                      CrosS ,Ataman, Versus71,satsura, mich4th3c0wb0y, FInnH@X, s3rver.exe (r00tw0rm.com)
#-------------------------------------|------------------------------------------#
import sys, time, os , httplib , socket
import urllib2 as u2

        
class logging:
	f=""
	def __init__(self,_logfile):
		self._logfile=_logfile
		self.f = open(self._logfile, "w")
		self.f.write("Sensitive finder logs \n")
	def writelog(self,_message):
		try:
			self.f.write(_message) # Write a string to a file
		except IOError:
   	 		pass	
   	def close(self):
   		self.f.close()


def proxycheck(_httpproxy,_proxy):
	try:
	  if _proxy:
	    print "[+] Testing Proxy..."
	    h2 = httplib.HTTPConnection(_httpproxy)
	    h2.connect()
	    print "[+] Proxy:",_httpproxy
	    return 1
	except(socket.timeout):
	  print "[-] Proxy Timed Out"
	  sys.exit()
	  pass
	except(NameError):
	  print "[-] Proxy Not Given"
	  sys.exit()
	  pass
	except:
	  print "[-] Proxy Failed"
	  sys.exit()
	  pass

def timer():
  now = time.localtime(time.time())
  return "["+time.asctime(now)+"]"

def getWordlistLength(_wordlist):
        num_lines = sum(1 for line in open(_wordlist))
        return num_lines

def urlcheck(_url):
	try:
	       	print ("[!] Checking website " + _url + "...")
	       	req = u2.Request(_url)
	       	u2.urlopen(req)
	       	print "[!] " +_url+" appears to be Online.\n"
   	except:
	        print("[-] Server offline or invalid URL")
	        sys.exit()

def printbanner():
	 print """
	  _________                    .__  __  .__              
	 /   _____/ ____   ____   _____|__|/  |_|__|__  __ ____  
	 \_____  \_/ __ \ /    \ /  ___/  \   __\  \  \/ // __ \ 
	 /        \  ___/|   |  \\\\___ \|  ||  | |  |\   /\  ___/ 
	/_______  /\___  >___|  /____  >__||__| |__| \_/  \___  >
	        \/     \/     \/     \/                       \/ 
	  __________                __                           
	  \______   \__ __  _______/  |_  ___________            
	   |    |  _/  |  \/  ___/\   __\/ __ \_  __ \           
	   |    |   \  |  /\___ \  |  | \  ___/|  | \/           
	   |______  /____//____  > |__|  \___  >__|              
	          \/           \/            \/           

         				V 1.0
	+ -- --=[ by Angel Injection and Th3breacher]
"""

if __name__=='__main__':

	shellwordlist="shell.1337"
	backupwordlist="backups.1337"
	adminwordlist="admins.1337"
	dirwordlist="dir.1337" 
	fileswordlist="files.1337"
	wordlist=""
	proxy = "None"
	proxy_supp=0
	count = 0
	mode = 0
	logging_support=1
	printbanner()
 
	if len(sys.argv) < 4 or len(sys.argv) > 7:
		print "Usage:"   + sys.argv[0] + " <http:url> -m <mode> -p <proxy> "
		print "Example:" + sys.argv[0] + " http://host.com  -m shell -p 127.0.0.1:8118"
		exit()

	for arg in sys.argv:
		if arg == '-h':
			print "Usage:"   + sys.argv[0] + " <http:url> -m <mode> -p <proxy> "
			print "Example:" + sys.argv[0] + " http://host.com  -m shell -p 127.0.0.1:8118"
			sys.exit(1)
		elif arg == '-p':
			proxy = sys.argv[count+1]
   			proxy_supp=1
   		elif arg == "-m":
   			mode = sys.argv[count+1]
  		count += 1

  	site = sys.argv[1]
	if site[:4] != "http":
  		site = "http://"+site
	if site.endswith("--"):
  		site = site.rstrip('--')
	if site.endswith("/*"):
  		site = site.rstrip('/*')
	urlcheck(site)

	if mode == "shell":
		wordlist=shellwordlist
	elif mode == "backup":
		wordlist=backupwordlist
	elif mode == "admin":
		wordlist=adminwordlist
	elif mode == "dir": 
		wordlist=dirwordlist 
	elif mode == "files": 
		wordlist=fileswordlist 	
	else :
		print("[x] Mode not specified")
		exit()

	if not os.access(wordlist, os.F_OK):
		print(  "[x] File " + wordlist + " does not exist or "
			+ "you are not permitted to access to the file")
		exit()

	proxycheck(proxy,proxy_supp)
	print timer(),"[+] ["+mode+" Searching]"
	print "[+] Host:", site
	print "[+] Wordlist " + wordlist + " has " + str(getWordlistLength(wordlist)) + " words\n\n"

	if proxy_supp != 0:
	    proxy_handler = u2.ProxyHandler({'http': 'http://'+proxy+'/'})
	    opener = u2.build_opener(proxy_handler)
	    u2.install_opener(opener)
  	else:
		pass

	if logging_support !=0:
		filename = site.replace ("http://","")
		filename2 = site.replace ("/","")
		logging_session=logging(filename2+".txt")
	else:
		pass

	with open(wordlist) as comfile:
		for line in comfile:
			line = line.strip("\r\n")
			req = u2.Request(sys.argv[1] + "/" + line)
			try:
				u2.urlopen(req)
			except u2.HTTPError as hr:
				if hr.code == 404:
					print mode+": " + line.ljust(50,' ') + "[Not found]"
			except u2.URLError as ur:
				print "URL error:", ur.args
				exit()
			except ValueError as vr:
				print "Value error:", vr.args
				exit()
			except:
				print "Unknown exception: exit..."
				exit()
			else:
				print mode+": " + line.ljust(50,' ') + "[OK]"
				if logging_support !=0:
				   logging_session.writelog(mode+": " + line.ljust(50,' ') + "[OK]\n")
				else:
					pass
			try:
				pass
			except KeyboardInterrupt as kierr:
				print "\nInterrupted by user: (CTRL+C or Delete)"
				exit()
	logging_session.close()
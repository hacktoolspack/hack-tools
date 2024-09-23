#!/usr/bin/python
""" 
Common Gateway Interface (CGI) scanner
CGIfuzzer.py by gunslinger_
This was written for educational purpose and pentest only. Use it at your own risk.
Author will not responsible for any damage
Special thanks to devilzc0de crew : mywisdom, petimati, peneter, flyff666, rotlez, 7460, xtr0nic, devil_nongkrong, cruzen and all devilzc0de family
"""
import socket
import urllib2
import sys
import httplib

__author__ = "Gunslinger_"
__version__= "v1.0"
__date__   = "Saturday, 20 February 2010 $ 9:10 AM"
log 	   = "cgifuzzer.log"
filelog    = open(log, "a")
cgilist    = "cgilist"
slash      = "/"
http       = "http://"
target     = "None"
counter    = 0
try:
	preventstrokes = open("cgilist", "r")
	linez 	       = preventstrokes.readlines()
	count          = 0 
	countpath      = len(linez)
	while count < len(linez): 
		linez[count] = linez[count].strip() 
		count += 1 
except(IOError): 
  	print "\n[-] Error: Check your cgilist path\n"
	file.write("\n[-] Error: Check your cgilist path\n")
  	sys.exit(1)
myhead     = """
   _|_|_|    _|_|_|  _|_|_|    _|_|                                                    
 _|        _|          _|    _|      _|    _|  _|_|_|_|  _|_|_|_|    _|_|    _|  _|_|  
 _|        _|  _|_|    _|  _|_|_|_|  _|    _|      _|        _|    _|_|_|_|  _|_|      
 _|        _|    _|    _|    _|      _|    _|    _|        _|      _|        _|        
   _|_|_|    _|_|_|  _|_|_|  _|        _|_|_|  _|_|_|_|  _|_|_|_|    _|_|_|  _|     
   
   Programmer 		: %s
   Version    		: %s
   Date version release : %s  
   Ready to Scan %s CGI path on your site target""" % (__author__, __version__, __date__, countpath)

helpcomm   = """
Usage: ./cgifuzzer.py [options]
Options: -t, --target    <hostname/ip>   |   Target to fuzzing the CGI 
         -h, --help      <help>          |   print this help
"""
  	
def help():
	print myhead
	print helpcomm
	filelog.write(myhead)
	filelog.write(helpcomm)
	sys.exit(1)
	
def main(line):
	global counter
	global target
	conn = httplib.HTTPConnection(target)
	conn.request("GET",slash+line)
	r1 = conn.getresponse()
	target = target.replace("http","")
	print "[-] Checking path : http://%s%s%s" % (target, slash, line)
	print "[-] Status : %s %s " % (r1.status, r1.reason)
	filelog.write("[-] Checking path : http://%s%s%s\n" % (target, slash, line))	
	filelog.write("[-] Status : %s %s\n" % (r1.status, r1.reason)) 
	counter+=1
	if counter == len(linez)/2:
		print "[+] Cgifuzzer on halfway done..."
		print "[+] Please be patient..."	
		filelog.write("[+] Cgifuzzer on halfway done...\n")
		filelog.write("[+] Please be patient...\n")
	if counter == len(linez):
		print "[+] Cgifuzzer done...\n"
		filelog.write("[+] Cgifuzzer done...!\n")	
	
for arg in sys.argv:
	if len(sys.argv) <=1:
		help()
        if arg.lower() == '-h' or arg.lower() == '--help':
		help()
       	if arg.lower() == '-t' or arg.lower() == '--target':
		target = sys.argv[int(sys.argv[1:].index(arg))+2]  
		
if __name__ == '__main__':
	for line in linez :
		main(line.replace("\n",""))
	filelog.close()
		

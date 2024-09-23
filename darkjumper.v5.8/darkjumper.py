#!/usr/bin/python
import sys
import urllib2
import httplib
import os
import re
import time
import sgmllib
import threading
import pickle
import urllib
import random
import warnings
import StringIO
import string
warnings.filterwarnings(action="ignore", message=".*(sets) module is deprecated", category=DeprecationWarning)
import sets
from ftplib import FTP
from socket import *
from var import *
from adminpath import *


"""Clear Monitor"""
if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	SysCls = 'clear'
	hapuslogreverse='rm -rf *.log'
else:
	SysCls = 'cls'
	hapuslogreverse='del *.log'

os.system(SysCls)
os.system(hapuslogreverse)	
		
#this class taken from linkscanner by asit_dhal( lipun4u[at]gmail[dot]com )		
class MyParser(sgmllib.SGMLParser): 
    "A simple parser class." 
    def parse(self, s): 
        "Parse the given string 's'." 
        self.feed(s) 
        self.close() 
    def __init__(self, verbose=0): 
        "Initialise an object, passing 'verbose' to the superclass." 
        sgmllib.SGMLParser.__init__(self, verbose) 
        self.hyperlinks = [] 
    def start_a(self, attributes): 
        "Process a hyperlink and its 'attributes'." 
        for name, value in attributes: 
            if name == "href": 
                self.hyperlinks.append(value) 
    def get_hyperlinks(self): 
        "Return the list of hyperlinks." 
        return self.hyperlinks 
 #end of linkscanner class

def cleanup(s):
   return filter(lambda x: x not in '    \n', s)

dan=cleanup(dan)

def reversemode():
	import socket
	global threadz
	global jumlah
	global udah
	print darkjumperface2  
	filelog = open(log, "a")
	filelog.write (darkjumperface2)
	try:
		reverse=socket.gethostbyaddr(target)
		ip=str(reverse[2])
		ip = ip[2:-2]
	except KeyboardInterrupt:
		print "\n[-] Exiting darkjumper..."
		sys.exit(1)
	except socket.herror:
		ip = "Unknown"
	print "[+] Target hostname : "+target
	print "[+] Target IP       :",ip
	print "[+] Use proxy       : "+proxy
	print "[+] Verbocity       :",verbocity
	print "[+] Time Starting   : %s" % time.strftime("%X")
	print "[+] Trying reverse your target's ip..."
	time.sleep(1)
	print "[+] Please wait..."
	filelog.write ("\n[+] Target set :"+target) 
        filelog.write ("\n[+] Trying reverse your target's ip...")
        filelog.write ("\n[+] please wait...")
	jumlah=0
	trik=0
	threadz=1
	threadzx=str(threadz)
	threadzx=threadzx+ekstensi
	url=machine+target
	print "-" * 30
	try:
		udah="belum"
		if proxy != "None":
			proxyHandler = urllib2.ProxyHandler({'http' : 'http://' + proxy + '/'})
			opener = urllib2.build_opener(proxyHandler)
			opener.addheaders = [("User-Agent", random.choice(ouruseragent))]
			response = opener.open(url)
		else:
			headers = { 'User-Agent' : random.choice(ouruseragent) }
			values = {'host' : target}
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data, headers)
			response = urllib2.urlopen(req)
        	parser = MyParser()
		dax=response.read()
		parser.parse(dax) 
		links = parser.get_hyperlinks()
		file = open(threadzx, "w")
 	 	filerev2 = open(filerev, "a")
	 	for l in links:
               		if saring in l and udah<>"ya":
	            		if saringan[1 in range(int(9))] not in l: 		
		       			if trik>50:
		         			file.close()
			 			trik=0
			 			threadz=threadz+1
                         			threadzx=str(threadz)
			 			threadzx=threadzx+ekstensi
			 			file = open(threadzx, "w")
	                		 	l=l.replace('/whois/','http://')
						if l=="http://":
						      udah="ya"
						if l<>"http://":
						      print l
						      file.write(l) 
						      file.write("\n")
						      filerev2.write(l)
						      filerev2.write("\n")
						      jumlah=jumlah+1
						      trik=trik+1
					else:
						 l=l.replace('/whois/','http://')
						 if l=="http://":
				 			udah="ya"
						 if l<>"http://":
			   				print l
						 file.write(l) 
						 file.write("\n")
						 filerev2.write(l)
						 filerev2.write("\n")
						 jumlah=jumlah+1
						 trik=trik+1
		print "-" * 30
		print "[+] Found :",jumlah," Domains hosted at this IP"
		print "-" * 30
	        filelog.close()
	except KeyboardInterrupt:
		print "\n[-] Exiting darkjumper..."
		sys.exit(1)
	except(IOError),msg: 
		 print "[!] Error in connecting site "
		 print "[!] Please check internet connections !" 
		 sys.exit(1)  

# sqli scan
def sqli_scan(line):
	global line2
	global saringhttp
	saringhttp="http://"
	pisah="/"
	pisah=str(pisah)
        f = open(tmpsudah, "r")
        text = f.read()
	f.close()
	if line not in text:
	  print "-" * 30
	  print "[+] Starting SQLI Scanning Thread at :"+line
	  print "-" * 30
 	  if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	  	sqlicom = "python devilzc0de.py -sqli %s " % line
		#"""Uncoment if you want run more faster"""
	    	#sqlicom=sqlicom.rstrip('/r/n')
	    	#sqlicom=sqlicom.rstrip()
	    	#sqlicom=sqlicom+dan       
	  else:
	     	sqlicom = "devilzc0de.py -sqli %s " % line
	     		
	  if verbocity:		
		print ("[+] Running command :"+sqlicom)
	  os.system(sqlicom)
	  filelog = open(tmpsudah, "a")
          filelog.write ("\n"+line)
	  filelog.close()  

#sub sqli scan
def sqli_scan_sub(linez):
	global line2
	global saringhttp
	saringhttp="http://"
	pisah="/"
	pisah=str(pisah)
        f = open(tmpsudah0, "r")
        text = f.read()
	f.close()
	linez.replace("'", "");
	if linez not in text:      
		print "-" * 30
		print "[+] Starting SQLI Scanning Thread at subpage url : "+linez
		print "-" * 30
 		if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	  		sqlicom = "python devilzc0de.py -sqlisub "+linez
			#"""Uncomment if you want run more faster"""
	  		#sqlicom=sqlicom.rstrip('/r/n')
	   		#sqlicom=sqlicom.rstrip()
	   		#sqlicom=sqlicom+dan          
	  	else:  
	     		sqlicom = "devilzc0de.py -sqlisub "+linez
	if verbocity:		
		print ("[+] Running command :"+sqlicom)
	os.system(sqlicom)
	filelog = open(tmpsudah0, "a")
        filelog.write ("\n"+linez+"\n")
	filelog.close()  
	
# blind sql scan		
def blind_scan(line):	
	global sqlicom
	f = open(tmpsudah2, "r")
        text = f.read()
	f.close()
	if line not in text:
		print "-" * 30
		print "[+] Starting Blind SQLI Scanning Thread at : "+line
		print "-" * 30
 		if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	      		sqlicom = "python devilzc0de.py -blind %s " % line
	    		"""Uncomment if you want run more faster"""
	  		#sqlicom=sqlicom.rstrip('/r/n')
	   		#sqlicom=sqlicom.rstrip()
	   		#sqlicom=sqlicom+dan
		else:
	      		sqlicom = "devilzc0de.py -blind %s " % line
       	if verbocity:		
		print ("[+] Running command :"+sqlicom)
 	os.system(sqlicom)
	filelog = open(tmpsudah2, "a")
        filelog.write ("\n"+line)
	filelog.close()  
	
# rfi scan
def rfi_scan(line):
	global sqlicom
       	f = open(tmpsudah3, "r")
        text = f.read()
	f.close()
	if line not in text:
  		print "-" * 30
		print "[+] Starting RFI Scanning Thread at : "+line
		print "-" * 30
		if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	      		sqlicom = "python devilzc0de.py -rfi %s " % line
	    		#"""Uncomment if you want run more faster"""
	  		#sqlicom=sqlicom.rstrip('/r/n')
	   		#sqlicom=sqlicom.rstrip()
	   		#sqlicom=sqlicom+dan
		else:
	      		sqlicom = "devilzc0de.py -rfi %s " % line
	if verbocity:		
		print ("[+] Running command :"+sqlicom)
	os.system(sqlicom)
	filelog = open(tmpsudah3, "a")
        filelog.write ("\n"+line)
	filelog.close()  
	
#lfi scan
def lfi_scan(line):
		global sqlicom
		f = open(tmpsudah4, "r")
		text = f.read()
		f.close()
		if line not in text:
			print "-" * 30
			print "[+] Starting LFI Scanning Thread at : "+line
			print "-" * 30
			if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
				sqlicom = "python devilzc0de.py -lfi %s " % line
			else:
				sqlicom = "devilzc0de.py -lfi %s " % line
				#"""Uncomment if you want run more faster"""
	  			#sqlicom=sqlicom.rstrip('/r/n')
	   			#sqlicom=sqlicom.rstrip()
	   			#sqlicom=sqlicom+dan
	   	if verbocity:		
			print ("[+] Running command :"+sqlicom)
		os.system(sqlicom)
		filelog = open(tmpsudah4, "a")
		filelog.write ("\n"+line)
		filelog.close()  

#rce scan
def rce_scan(line):
		global sqlicom
		f = open(tmpsudah4, "r")
		text = f.read()
		f.close()
		if line not in text:
			print "-" * 30
			print "[+] Starting RCE Scanning Thread at : "+line
			print "-" * 30
			if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
				sqlicom = "python devilzc0de.py -rce %s " % line
			else:
				sqlicom = "devilzc0de.py -rce %s " % line
				#"""Uncomment if you want run more faster"""
	  			#sqlicom=sqlicom.rstrip('/r/n')
	   			#sqlicom=sqlicom.rstrip()
	   			#sqlicom=sqlicom+dan
	   	if verbocity:		
			print ("[+] Running command :"+sqlicom)
		os.system(sqlicom)
		filelog = open(tmpsudah4, "a")
		filelog.write ("\n"+line)
		filelog.close()  
# cgi scan		
def cgi_scan(target):
	import urllib2, socket
	try:
		reverse=socket.gethostbyaddr(target)
		ip=str(reverse[2])
		ip = ip[2:-2]
	except KeyboardInterrupt:
		print "\n[-] Exiting darkjumper..."
		sys.exit(1)
	except socket.herror:
		ip = "Unknown"
	print "[+] Target hostname : "+target
	print "[+] Target IP       :",ip
	print "[+] Use proxy       : "+proxy
	print "[+] Verbocity       :",verbocity
	print "[+] Time Starting   : %s" % time.strftime("%X")
	print "[+] Try to getting Common Gateway Interface path"
	print "[+] Please wait..."
	print "-"*40
	awalan="http://"
	if awalan not in target :
		targetx=awalan+target
	else:
                targetx=target	
        if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
		cgirun = "python darkcgi.py --target %s" % target
	else:
		cgirun = "darkcgi.py --target %s" % target
       	if verbocity:		
		print ("[+] Running command :"+cgirun)
 	os.system(cgirun)		
	
# enumerate scan
def enumerasi():
	print "[+] Testing enumerator"
	global jum
	global jumlah
	jum = sys.argv[count+5]
	bisa1="Forbidden"	
	global hasilrev
	print "[-] Checking whether user enumeration is possible or not..."
	targa="http://"+target+"/"+usercheck
	print "[-] Checking :"+targa
	response=urllib.urlopen(targa)
        hasilrev = response.read()
	if bisa1 in hasilrev:
		counter = 1
		print "[!] Server has an user enumeration vulnerability !"
    		print "[!] Please wait... checking possible user enumeration at : "+target+"\n"
    		filelog = open(log, "a")
    		filelog.write ("\n----------------------------------------")
    		filelog.write ("\n[!] Please wait... checking possible user enumeration at : "+target+"")
    		filelog.write ("\n----------------------------------------")
    		filelog.close()
    		f = open(filerev,'r')
    		for line in f.readlines() :
      			lineold=line	    
      			line=line.replace("http://","")
      			line=line.replace("www.","")
      			line=line.replace(".","")
      			line=line.replace("/","")
      			if jum=="4":
				line=line[:4]    
			elif jum=="5":
				line=line[:5]    
      			elif jum=="6":
				line=line[:6]    
      			elif jum=="7":
				line=line[:7]      	    
      			elif jum=="8":
				line=line[:8]   
      			elif jum=="None" :
				line=line[:4 in range(8)] 
      			newline="http://"+target+"/~"+line
      			conn = httplib.HTTPConnection(target)
      			conn.request("GET","/~"+line)
      			r1 = conn.getresponse()
      			if verbocity:
      				print "\n------------------------------------------------------------------"
				print jum+" chars Possible user: "+line+" ,substring taken from site: "+lineold
	     			print "Status :", r1.status, r1.reason # If 500 error, don't worry... it's still guessing and work enough !
      			print "[-] Checking user : "+line	
      			if counter == jumlah/10:
      				print "[+] 10% done..."	
      				print "[+] Please be patient..."   
      			elif counter == jumlah/5:
      				print "[+] 20% done..."	
      				print "[+] Please be patient..."   
      			elif counter == jumlah/4:
      				print "[+] 25% done..."	
      				print "[+] Please be patient..."  
      			elif counter == jumlah/2:
      				print "[+] 50% done..."	
      				print "[+] Please be patient..."
      			elif counter == jumlah:
      				print "[+] Done !"
      				sys.exit(1)
      			response2=urllib.urlopen(newline)
      			if r1.status == 301 or r1.status == 200:
				print "[!] W00t !!! found possible user : "+line
				print "[!] Check this out : "+newline
				print "[!] Possible user saved at darkjumper.log"
				filelog = open(log, "a")
	  			filelog.write ("\n[!] W00t !!! found possible user: "+line)
	  			filelog.write ("\n[!] Check this out:"+newline)
	  			filelog.close()
				filelog = open(kamus, "a")
				filelog.write ("\n"+line)
				filelog.close()
			if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
				autobrute = "./ftpbrute.py -t "+target+" -u "+line+" -w "+kamus
			else:
				autobrute = "ftpbrute.py -t "+target+" -u "+line+" -w "+kamus
				if verbocity:
					print "Running autoftpbruteforce !!"
				if autobruteforce:
					os.system(autobrute)	   
			counter+=1     
      		else:
			pass
			
      		f.close()
  	else:
		print "[!]Sorry dude ! The server is configured well, you can not guess user(s) here !"

def injection_scan():
	global target
	global jumlah
	global threadz
	global theVar
	global mode
	global mywisdom
	jumlahx=str(jumlah)
	threadzx=str(threadz)
	print """
----------------------------------------
[+] Starting Full Scan to find vulnerabilities on website(s) at the same server as %s
[+] Total Scanning Thread : %s
[+] Total Target(s) to scan on this server : %s
[+] Working please wait 
----------------------------------------""" % (target, threadzx, jumlahx)
	filelog = open(log, "a")
	filelog.write ("""
----------------------------------------
[+] Starting Full Scan to find vulnerabilities on website(s) at the same server as %s
[+] Total Scanning Thread : %s
[+] Total Target(s) to scan on this server : %s
[+] Working please wait 
----------------------------------------""" % (target, threadzx, jumlahx))
	filelog.close()
	theVar=1
	mywisdom = 1
	saringan="https"
	ekstensi=".log"
	linez="-"
	if theVar<threadz:
		theVarx=str(theVar)
		logrev=theVarx+ekstensi
		file=open(logrev, 'r')
		for line in file:
			if saringan not in line:
			      print "[+] Injection scan mode applied to:"+line
			      sqli_scan(line)
			      blind_scan(line)
		theVar = theVar + 1
	else:
		theVarx=str(theVar)
		logrev=theVarx+ekstensi
		file=open(logrev, 'r')
		for line in file:
			if saringan not in line:
				print "[+] Injection scan mode applied to:"+line
		      		sqli_scan(line)
		      		blind_scan(line)
		
		theVar = theVar + 1

def inclusion_scan():
	global target
	global jumlah
	global threadz
	global theVar
	global mode
	global mywisdom
	jumlahx=str(jumlah)
	threadzx=str(threadz)
	print """
----------------------------------------
[+] Starting Full Scan to find vulnerabilities on website(s) at the same server as %s
[+] Total Scanning Thread : %s
[+] Total Target(s) to scan on this server : %s
[+] Working please wait 
----------------------------------------""" % (target, threadzx, jumlahx)
	filelog = open(log, "a")
	filelog.write ("""
----------------------------------------
[+] Starting Full Scan to find vulnerabilities on website(s) at the same server as %s
[+] Total Scanning Thread : %s
[+] Total Target(s) to scan on this server : %s
[+] Working please wait 
----------------------------------------""" % (target, threadzx, jumlahx))
	filelog.close()
	theVar=1
	mywisdom = 1
	myguns = 1
	saringan="https"
	ekstensi=".log"
	linez="-"
	if theVar<threadz:
		theVarx=str(theVar)
		logrev=theVarx+ekstensi
		file=open(logrev, 'r')
		for line in file:
			if saringan not in line:
			      print "[+] File Inclusion scan mode applied to:"+line
			      rfi_scan(line)
			      lfi_scan(line)
		theVar = theVar + 1
	else:
		theVarx=str(theVar)
		logrev=theVarx+ekstensi
		file=open(logrev, 'r')
		for line in file:
			if saringan not in line:
				print "[+] File Inclusion scan mode applied to:"+line
				rfi_scan(line)
			      	lfi_scan(line)
			      	rce_scan(line)
		theVar = theVar + 1
		
def full_scan():
	global target
	global jumlah
	global threadz
	global theVar
	global mode
	global mywisdom
	jumlahx=str(jumlah)
	threadzx=str(threadz)
	print """
----------------------------------------
[+] Starting Full Scan to find vulnerabilities on website(s) at the same server as %s
[+] Total Scanning Thread : %s
[+] Total Target(s) to scan on this server : %s
[+] Working please wait 
----------------------------------------""" % (target, threadzx, jumlahx)
	filelog = open(log, "a")
	filelog.write ("""
----------------------------------------
[+] Starting Full Scan to find vulnerabilities on website(s) at the same server as %s
[+] Total Scanning Thread : %s
[+] Total Target(s) to scan on this server : %s
[+] Working please wait 
----------------------------------------""" % (target, threadzx, jumlahx))
	filelog.close()
	theVar=1
	mywisdom = 1
	myguns = 1
	saringan="https"
	ekstensi=".log"
	linez="-"
	if theVar<threadz:
		theVarx=str(theVar)
		logrev=theVarx+ekstensi
		file=open(logrev, 'r')
		for line in file:
			if saringan not in line:
			      print "[+] Injection scan mode applied to:"+line
			      sqli_scan(line)
			      blind_scan(line)
			      rfi_scan(line)
			      lfi_scan(line)
		theVar = theVar + 1
	else:
		theVarx=str(theVar)
		logrev=theVarx+ekstensi
		file=open(logrev, 'r')
		for line in file:
			if saringan not in line:
				print "[+] Injection scan mode applied to:"+line
		      		sqli_scan(line)
		      		blind_scan(line)
				rfi_scan(line)
			      	lfi_scan(line)
			      	rce_scan(line)
		theVar = theVar + 1

def portscan():
	import socket
	global target
	try:
		reverse=socket.gethostbyaddr(target)
		ip=str(reverse[2])
		ip = ip[2:-2]
	except KeyboardInterrupt:
		print "\n[-] Exiting darkjumper..."
		sys.exit(1)
	except socket.herror:
		ip = "Unknown"
	print "[+] Target hostname : "+target
	print "[+] Target IP       :",ip
	print "[+] Use proxy       : "+proxy
	print "[+] Verbocity       :",verbocity
	print "[+] Time Starting   : %s" % time.strftime("%X")
	print "[+] Scanning open port on",target
	print "[+] Please wait until finish !"
	from socket import AF_INET, SOCK_STREAM		
    	for port in range(int(sys.argv[5].split('-')[0]), int(sys.argv[5].split('-')[1])+1):
		try:
	    		socket(AF_INET, SOCK_STREAM).connect((target, port)); 
	    		print "[!] Port ",port, "is open !"
	    	except KeyboardInterrupt:
			print "\n[-] Exiting darkjumper..."
			sys.exit(1)
		except: 
			if verbocity:
	    			print "[-]port ",port,"is close !"
	    		pass		

def checkip():
	print "[+] Checking your ip or proxy"
	print "[+] Please wait !"
	sitechecker = "http://my-addr.com/your-ip-and-city-country-isp-latitude-longitude/geo-ip-region-lookup/my_geo.php"
	if proxy != "None":
		proxyHandler = urllib2.ProxyHandler({'http' : 'http://'+proxy+'/'})
		opener = urllib2.build_opener(proxyHandler)
		response = opener.open(sitechecker)
		myip = re.findall("""<b>IP</b></td><td class='td_val'>(.*?)</td></tr>""", response)
		mycontinent =  re.findall("""<td class='td_var'>CONTINENT CODE</td>
<td class='td_val'>(.*?)</td>
""", response)
		countrycode =  re.findall("""<td class='td_var'>COUNTRY CODE</td>
<td class='td_val'>(.*?)</td>
""", response)
		countryname =  re.findall("""<td class='td_var'>COUNTRY NAME</td>
<td class='td_val'>(.*?)</td>
""", response)
		regioncode =  re.findall("""<td class='td_var'>REGION CODE</td>
<td class='td_val'>(.*?)</td>
</tr>
""", response)
		regionname =  re.findall("""<td class='td_var'>REGION NAME</td>
<td class='td_val'>(.*?) <font color='red'>&lt;- it's your region</font></td>
""", response)
		city =  re.findall("""<td class='td_var'>CITY</td>
<td class='td_val'>(.*?) <font color='red'>&lt;- it's your city</font></td>
""", response)
		latitude = re.findall("""<td class='td_var'>LATITUDE</td>
<td class='td_val'>(.*?)</td>
""",response)
		longitude = re.findall("""<td class='td_var'>LONGITUDE</td>
<td class='td_val'>(.*)</td>
""",response)
		provider = re.findall("<td class='td_val'>(.*)<font color='red'>&lt;- it's your provider</font></td>",response)
		mytrace = [myip, mycontinent, countrycode, regionname, regioncode, city, latitude, longitude, provider]
		print "[+] Your IP          : ",mytrace[0]
		print "[+] Your Continent   : ",mytrace[1]
		print "[+] Your Countrycode : ",mytrace[2]
		print "[+] Your Regionname  : ",mytrace[3]
		print "[+] Your Regioncode  : ",mytrace[4]
		print "[+] Your City        : ",mytrace[5]
		print "[+] Your Latitude    : ",mytrace[6]
		print "[+] Your Longitude   : ",mytrace[7]
		print "[+] Your Provider    : ",mytrace[8]
	else:
		req = urllib2.Request(sitechecker)
		req.addheaders = [("User-Agent", random.choice(ouruseragent))]
		opener = urllib2.urlopen(req)
		response = opener.read()
		myip = re.findall("<b>IP</b></td><td class='td_val'>(.*?)</td></tr>", response)
		mycontinent =  re.findall("""<td class='td_var'>CONTINENT CODE</td>
<td class='td_val'>(.*?)</td>
""", response)
		countrycode =  re.findall("""<td class='td_var'>COUNTRY CODE</td>
<td class='td_val'>(.*?)</td>
""", response)
		countryname =  re.findall("""<td class='td_var'>COUNTRY NAME</td>
<td class='td_val'>(.*?)</td>
""", response)
		regioncode =  re.findall("""<td class='td_var'>REGION CODE</td>
<td class='td_val'>(.*?)</td>
</tr>
""", response)
		regionname =  re.findall("""<td class='td_var'>REGION NAME</td>
<td class='td_val'>(.*?) <font color='red'>&lt;- it's your region</font></td>
""", response)
		city =  re.findall("""<td class='td_var'>CITY</td>
<td class='td_val'>(.*?) <font color='red'>&lt;- it's your city</font></td>
""", response)
		latitude = re.findall("""<td class='td_var'>LATITUDE</td>
<td class='td_val'>(.*?)</td>
""",response)
		longitude = re.findall("""<td class='td_var'>LONGITUDE</td>
<td class='td_val'>(.*)</td>
""",response)
		provider = re.findall("<td class='td_val'>(.*)<font color='red'>&lt;- it's your provider</font></td>",response)
		mytrace = [myip, mycontinent, countrycode, regionname, regioncode, city, latitude, longitude, provider]
		print "[+] Your IP          : ",mytrace[0]
		print "[+] Your Continent   : ",mytrace[1]
		print "[+] Your Countrycode : ",mytrace[2]
		print "[+] Your Regionname  : ",mytrace[3]
		print "[+] Your Regioncode  : ",mytrace[4]
		print "[+] Your City        : ",mytrace[5]
		print "[+] Your Latitude    : ",mytrace[6]
		print "[+] Your Longitude   : ",mytrace[7]
		print "[+] Your Provider    : ",mytrace[8]
		
def headerinfo():
	import urllib2, socket
	try:
		reverse=socket.gethostbyaddr(target)
		ip=str(reverse[2])
		ip = ip[2:-2]
	except KeyboardInterrupt:
		print "\n[-] Exiting darkjumper..."
		sys.exit(1)
	except socket.herror:
		ip = "Unknown"
	print "[+] Target hostname : "+target
	print "[+] Target IP       :",ip
	print "[+] Use proxy       : "+proxy
	print "[+] Verbocity       :",verbocity
	print "[+] Time Starting   : %s" % time.strftime("%X")
	print "[+] Try to getting http header info..."
	time.sleep(1)
	print "[+] Please wait..."
	print "-"*40
	response = urllib2.urlopen("http://"+target)
	print response.info()	
	print "-"*40
	
def adminpath():
	import urllib2, socket
	reverse=socket.gethostbyaddr(target)
	try:
		reverse=socket.gethostbyaddr(target)
		ip=str(reverse[2])
		ip = ip[2:-2]
	except KeyboardInterrupt:
		print "\n[-] Exiting darkjumper..."
		sys.exit(1)
	except socket.herror:
		ip = "Unknown"
	print "[+] Target hostname : "+target
	print "[+] Target IP       :",ip
	print "[+] Use proxy       : "+proxy
	print "[+] Verbocity       :",verbocity
	print "[+] Time Starting   : %s" % time.strftime("%X")
	print "[+] Scanning admin path disclosure..."
	time.sleep(1)
	print "[+] Please wait..."
	print "-"*40
	try:
		for admin in admin_path:
			admin = admin.replace("\n","")
			admin = "/" + admin
			connection = httplib.HTTPConnection(target)
			connection.request("GET",admin)
			r1 = connection.getresponse()
			print "http:/%s%s %s %s" % (target, admin, r1.status, r1.reason)
	except KeyboardInterrupt:
		print "\n[-] Exiting darkjumper..."
		sys.exit(1)
	except:
		pass	
	print "-"*40

def daemonizeinfo():
	global target
	import urllib2, socket
	try:
		reverse=socket.gethostbyaddr(target)
		ip=str(reverse[2])
		ip = ip[2:-2]
	except KeyboardInterrupt:
		print "\n[-] Exiting darkjumper..."
		sys.exit(1)
	except socket.herror:
		ip = "Unknown"
	print "[+] Target hostname : "+target
	print "[+] Target IP       :",ip
	print "[+] Use proxy       : "+proxy
	print "[+] Verbocity       :",verbocity
	print "[+] Time Starting   : %s" % time.strftime("%X")
	print "[+] Try to getting daemon info..."
	time.sleep(1)
	print "[+] Please wait..."
	print "-"*40
	http="http://"
	if http in target:
		target = target.replace(http,"")
        if verbocity:
        	print "[+] Running daemoninfo.pl"	
	cgiscan="perl daemoninfo.pl %s" % target
	os.system(cgiscan)

def converter():
	inputtype = raw_input("[-] Input data to encode : ")
	print "[+] Hex is :"
	print "0x"+inputtype.encode("hex")
	print "[+] Base64 is: "
	print "0x"+inputtype.encode("base64")
	print "[+] DONE !"
	
def anonymousftp():
	import socket
	global target
	try:
		reverse=socket.gethostbyaddr(target)
		ip=str(reverse[2])
		ip = ip[2:-2]
	except KeyboardInterrupt:
		print "\n[-] Exiting darkjumper..."
		sys.exit(1)
	except socket.herror:
		ip = "Unknown"
	print "[+] Target hostname : "+target
	print "[+] Target IP       :",ip
	print "[+] Use proxy       : "+proxy
	print "[+] Verbocity       :",verbocity
	print "[+] Time Starting   : %s" % time.strftime("%X")
	print "[+] Trying to check ftp anonymous access..."
	http="http://"
	if http in target:
		target = target.replace(http,"")
	try:
		ftp = FTP(target)
		ftp.login()
		ftp.retrlines('LIST')
		print "[!] Anonymous login successfuly !"
		ftp.quit()
	except Exception, e:
        	print "[-] Anonymous login unsuccessful..."
		pass	
	except KeyboardInterrupt:
		print "\n[-] Anonymous checking skipped..."
		sys.exit(1)	    		
def main():
	global target
	for arg in sys.argv:
		if len(sys.argv) <= 1:
			print darkjumperface1
			filelog = open(log, "a")
			filelog.write (darkjumperface1)
			filelog.close()
			sys.exit(1)
		if arg.lower() == '-h' or arg.lower() == '--help':
			print optiondarkjumper
			filelog = open(log, "a")
			filelog.write (optiondarkjumper)
			sys.exit(1)
		elif arg.lower() == '-t' or arg.lower() == '--target':
                	target = sys.argv[int(sys.argv.index(arg))+1]
                elif arg.lower() == '-p' or arg.lower() == '--proxy':
                	proxy = sys.argv[int(sys.argv.index(arg))+1]	
        	elif arg.lower() == '-m' or arg.lower() == '--mode':
        		global l
                	mode = sys.argv[int(sys.argv.index(arg))+1]
			if mode=="reverseonly":
				reversemode()
				print "[+] DONE !"
			elif mode=="injection":
				reversemode()
				injection_scan()  
    				threadzx=str(threadz)
    				print "[+] DONE !"
			elif mode=="inclusion":
				reversemode()
				inclusion_scan()
				threadzx=str(threadz)
				print "[+] DONE !" 
			elif mode=="full":
				reversemode()
				full_scan()
				cgi_scan(target)
        			threadzx=str(threadz)
				print "[+] DONE !"
			elif mode=="enum":
				reversemode()	
    				enumerasi()
			elif mode=="portscan":
				print darkjumperface2
				portscan()
			elif mode=="cgidirs":
				print darkjumperface2
#				reversemode()
				cgi_scan(target)
			elif mode=="headerinfo":
				print darkjumperface2
				headerinfo()
				print "[+] DONE !"
			elif mode=="scanadminpath":
				print darkjumperface2
				adminpath()
			elif mode=="daemoninfo":
				print darkjumperface2
				daemonizeinfo()	
				print "[+] DONE !"
			elif mode=="converter":
				print darkjumperface2
				converter()	
			elif mode=="checkip":
				print darkjumperface2
				checkip()
			elif mode=="ftpanon":
				print darkjumperface2
				anonymousftp()
				print "[+] DONE !"
			else:
				print darkjumperface2
				print "[!] "+mode+" mode is NOT in [option]"
				print "[!] -h or --help to get option..."
			
"""define proxy & verbocity & autobruteforcing & check IP mode"""
proxy = "None"
verbocity = False
autobruteforce = False
for arg in sys.argv:
	if arg.lower() == '-p' or arg.lower() == '--proxy':
                proxy = sys.argv[int(sys.argv.index(arg))+1]
	elif arg.lower() == '-v' or arg.lower() == '--verbocity':
                verbocity = True
        elif arg.lower() == '-a' or arg.lower() == '--autobruteforce':
                autobruteforce = True
"""End define proxy & verbocity & autobruteforcing & check IP mode"""

if __name__ == '__main__':
	main()

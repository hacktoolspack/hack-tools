#!/usr/bin/python

import urllib,sys,os,sgmllib 

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
gajebo=" Error "

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
nemu="-" 
ceksqli="'"
filename="sub2.txt"
log="darkjumperlog.txt"
kres="#"
slash="/"
http="http://"
php="php"
shtml="shtml"
asp="asp"
mailto="mailto"
js="javascript"
tanya="?"
samadengan="=" 
print "\n\n\t\tsub page scannning for darkjumper.py \n by: mywisdom \n idea taken from lipun4u[at]gmail[dot]com" 
print "\t\t------------------------" 
 
appname = os.path.basename(sys.argv[0]) 
 
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
            if name == "src": 
                self.hyperlinks.append(value) 
 
    def get_hyperlinks(self): 
        "Return the list of hyperlinks." 
 
        return self.hyperlinks 
 
 
 
if len(sys.argv) not in [2,]: 
    print "Usage : " + appname + " <url> " 
    print "e.g. : " + appname + " www.google.com " 
    sys.exit(1) 
elif "-h"  in sys.argv: 
    print "Usage : " + appname + " <url> " 
    print "e.g. : " + appname + " www.google.com " 
    sys.exit(1) 
elif "--help" in sys.argv: 
    print "Usage : " + appname + " <url> " 
    print "e.g. : " + appname + " www.google.com " 
    sys.exit(1) 
 
 
 
site = sys.argv[1].replace("http://","") 
site = "http://" + site.lower() 
 
print "Target : " + site
filelog = open(filename, "a")
filelog.close()  
 
try: 
    site_data = urllib.urlopen(site) 
    parser = MyParser() 
    parser.parse(site_data.read()) 
except(IOError),msg: 
    print "Error in connecting site ", site 
    print msg 
    sys.exit(1) 
links = parser.get_hyperlinks() 
print "Total no. of hyperlinks : " + str(len(links)) 
print "" 
z=1
for l in links: 
    z=z+1
    if z>100:
	     sys.exit(1)
		  	
    if kres not in l and js not in l and mailto not in l:
    	  if php in l or asp in l or shtml in l:	
	      l=l.replace("'", "")
	      st=site.split("/")
              ly="http://"+st[2]+"/"+l
              if tanya in ly and samadengan in ly:
	         ly2=ly+ceksqli
		 print "[-]Checking sqli at:"+ly2     
		 response=urllib.urlopen(ly2)
                 htmlsqli = response.read()  
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
			print "[+]W00t !! Found "+ tipe+ " Bug at:"+ly2
			print "[+]Possible server's hole saved at darkjumperlog.txt"
			filelog = open(log, "a")
			filelog.write ("\n[+]W00t !! Found "+ tipe+ " Bug at:"+ly2) 
			    
	       
              filelog = open(filename, "a")
              filelog.write ("\n"+ly+"\n")
              filelog.close()  


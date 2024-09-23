#!/usr/bin/python
__developer__ = "mywisdom & gunslinger_"
__version__   = "5.8"
__date__      = "Wednesday, 24 Feb 2010 $ 9:13 PM "

#variabel 
global acak
global mywisdom
global subpages
global niktoscan
global hasilrev
global startport
global proxy
#include sub pages ?
subpages="yes"
#include sub pages ?
niktoscan="yes"
machine="http://www.ip-adress.com/reverse_ip/"
hypertext="http://"
mode="None"
stoper = 1
a=1
count=0
log="darkjumper.log"
tmpreverse = "reversetmp.html"
tmpsudah="sitealready.txt"
tmpsudah2="sitealready2.txt"
tmpsudah3="sitealready3.txt"
tmpsudah4="sitealready4.txt"
tmpsudah0="sitealready0.txt"
tmpalreadysubcek="tmpalreadysubcek.txt"
tmpalreadysub="tmpalreadysubcek.txt"
filerev="reverse.txt"
usercheck="~root"
filelog = open(tmpsudah, "w")
filelog.write ("-")
filelog.close()  
filelog = open(tmpsudah2, "w")
filelog.write ("-")
filelog.close()  
filelog = open(tmpsudah3, "w")
filelog.write ("-")
filelog.close()  
filelog = open(tmpsudah4, "w")
filelog.write ("-")
filelog.close()  
filelog = open(tmpsudah0, "w")
filelog.write ("-")
filelog.close()  
zubpagez="subpage.txt"
filelog = open(zubpagez, "w")
filelog.write ("-")
filelog.close()  
tmpcek="tmpcek.txt"
filelog = open(tmpcek, "w")
filelog.write ("-")
filelog.close()  
filelog = open(tmpalreadysubcek, "w")
filelog.write ("-")
filelog.close()  
theVar = 1
ekstensi=".log"
mywisdom=1
jum = "None"
dan=str(' &')
kamus = "wordlist"
saring="whois"
saringan=['http://www.ip-adress.com/',
	'http://www.addthis.com/bookmark.php',
	'http://www.addthis.com/bookmark.php',
	'http://www.thumbshots.com',
	'http://www.addthis.com/bookmark.php',
	'http://www.advancedregistryfix.com',
	'http://www.proxyfire.net',
	'http://www.hideyouripaddress.net',
	'http://www.twitter.com/ipadress',
	'http://www.ip2location.com']
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
darkjumperface1 = '''
################################################################
#       .___             __          _______       .___        # 
#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    # 
#    / __ |\__  \\\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   # 
#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   # 
#   \____ |(______/__|  |__|_ \\\_____>\_____  /\_____|\____\   # 
#        \/                  \/             \/                 # 
#                   ___________   ______  _  __                # 
#                 _/ ___\_  __ \_/ __ \ \/ \/ /                # 
#                 \  \___|  | \/\  ___/\     /                 # 
#                  \___  >__|    \___  >\/\_/                  # 
#      est.2007        \/            \/   forum.darkc0de.com   # 
################################################################
Darkjumper.py version %s                                      
Developed by         : %s 
Date version release : %s      
Dedicated to darkc0de.com, devilzc0de.org,jatimcrew.org,flash-crew.com, jasakom.com, h4cky0u.org and 0c0de.com
---------------------------------------------------------------------------------------------------------------

Usage : ./darkjumper.py [option]
	-h or --help for get help   
''' % (__version__, __developer__, __date__)
darkjumperface2 = '''
################################################################
#       .___             __          _______       .___        # 
#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    # 
#    / __ |\__  \\\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   # 
#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   # 
#   \____ |(______/__|  |__|_ \\\_____>\_____  /\_____|\____\   # 
#        \/                  \/             \/                 # 
#                   ___________   ______  _  __                # 
#                 _/ ___\_  __ \_/ __ \ \/ \/ /                # 
#                 \  \___|  | \/\  ___/\     /                 # 
#                  \___  >__|    \___  >\/\_/                  # 
#      est.2007        \/            \/   forum.darkc0de.com   # 
################################################################
Darkjumper.py version %s                                      
Developed by         : %s 
Date version release : %s
Dedicated to darkc0de.com, devilzc0de.org,jatimcrew.org,flash-crew.com, jasakom.com, h4cky0u.org and 0c0de.com''' % (__version__, __developer__, __date__)
optiondarkjumper = '''
################################################################
#       .___             __          _______       .___        # 
#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    # 
#    / __ |\__  \\\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   # 
#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   # 
#   \____ |(______/__|  |__|_ \\\_____>\_____  /\_____|\____\   # 
#        \/                  \/             \/                 # 
#                   ___________   ______  _  __                # 
#                 _/ ___\_  __ \_/ __ \ \/ \/ /                # 
#                 \  \___|  | \/\  ___/\     /                 # 
#                  \___  >__|    \___  >\/\_/                  # 
#      est.2007        \/            \/   forum.darkc0de.com   # 
################################################################
Darkjumper.py version %s help module
Developed by : %s
Date release : %s
This tool will try to find every website that host at the same server at your target
Then check for every vulnerability of each website that host at the same server
Vulnerable check including : sqli, blind, lfi, rfi, rce
---------------------------------------------------------------------------------------------------------------
Usage : ./darkjumper.py -t [target] -m [option] 
	Available [option] :
		reverseonly				| Only reverse target no checking bug
		injection				| Checking for sqli and blind sqli on every web that host at the same target server
		inclusion				| Checking for lfi, rfi, rce on every web that host at the same target server
		full					| Checking for sqli, blind sqli, lfi, rfi, rce on every web that host at the same target server
		cgidirs					| Scanning cgidirs on the target server
		enum [number] 				| Guessing possible user enumeration on server (4-8 chars user enumeration)
		portscan [startport]-[endport]		| Scanning open port at your target
		headerinfo				| Show http header info at your target (grabing banner host target)
		daemoninfo				| Show what's running daemon at your target 
		scanadminpath				| Scanning disclosure admin path at your target
		converter				| Simple data encoder to hex & base64 (usefull for injection) 
		checkip					| Use IP or proxy checker (Usefull for checking your ip or proxy)
		ftpanon					| Checking target for anonymous file transfer protocol (ftp) access
		
	Additional option : 
		-p [proxyaddress:port]			| Use proxy
		-v					| Use verbose mode
		-a					| Use Autobruteforcer after enumeration	
		
Please report bug or check update at <http://sourceforge.net/projects/darkjumper/>	
---------------------------------------------------------------------------------------------------------------''' % (__version__, __developer__, __date__)

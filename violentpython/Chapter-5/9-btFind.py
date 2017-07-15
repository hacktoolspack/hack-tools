import time
from bluetooth import *
from datetime import datetime

def findTgt(tgtName):
    foundDevs = discover_devices(lookup_names=True)
    for (addr, name) in foundDevs:
        if tgtName == name:
            print '[*] Found Target Device ' + tgtName
            print '[+] With MAC Address: ' + addr
            print '[+] Time is: '+str(datetime.now())


tgtName = 'TJ iPhone'
while True:
    print '[-] Scanning for Bluetooth Device: ' + tgtName
    findTgt(tgtName)
    time.sleep(5)


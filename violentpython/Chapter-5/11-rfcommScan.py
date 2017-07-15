#!/usr/bin/python
# -*- coding: utf-8 -*-

from bluetooth import *


def rfcommCon(addr, port):
    sock = BluetoothSocket(RFCOMM)
    try:
        sock.connect((addr, port))
        print '[+] RFCOMM Port ' + str(port) + ' open'
        sock.close()
    except Exception, e:
        print '[-] RFCOMM Port ' + str(port) + ' closed'


for port in range(1, 30):
    rfcommCon('00:16:38:DE:AD:11', port)

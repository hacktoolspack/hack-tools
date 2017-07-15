#!/usr/bin/python
# -*- coding: utf-8 -*-

import obexftp

try:
    btPrinter = obexftp.client(obexftp.BLUETOOTH)
    btPrinter.connect('00:16:38:DE:AD:11', 2)
    btPrinter.put_file('/tmp/ninja.jpg')
    print '[+] Printed Ninja Image.'
except:

    print '[-] Failed to print Ninja Image.'

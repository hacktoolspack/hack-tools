#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,httplib
import socket,sys
fobj = open('redis.txt','r')
fileHandle = open('vul.txt','a+')  
payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
s = socket.socket()
socket.setdefaulttimeout(10)
for target in fobj:
    ip = target.strip()
    try:
        port = 6379
        s.connect((ip, port))
        s.send(payload)
        recvdata = s.recv(1024)
        if recvdata and 'redis_version' in recvdata:
            fileHandle.write(target)
            print 'server is vulerable'
    except:
        pass

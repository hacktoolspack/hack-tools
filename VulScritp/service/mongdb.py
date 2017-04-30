#!/usr/bin/python

import pymongo
import random

fobj = open('27017.txt','r')
fileHandle = open('vul.txt','a+')
for target in fobj:
	ip_addr = target.strip()
	try:
		print target.strip()
		conn = pymongo.MongoClient(ip_addr, 27017, socketTimeoutMS=3000)
		print "ok"
		fileHandle.write(target)
	except Exception, e:
		print "can't conn"

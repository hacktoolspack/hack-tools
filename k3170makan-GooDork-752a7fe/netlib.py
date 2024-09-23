#!/usr/bin/python
import urllib
import urllib2
import urlparse
import httplib
import sys
import socket
"""Netlib
The object incharge of all the HTTP redtape.
*later version will include proxy support
"""
class netlib:
	def __init__(self):
		self.httplib_inst = httplib.HTTP()
	"""Return the html requested from host
	"""
	def getPage(self,url):
		sys.stderr.write("Opening Page: %s" % (url))
		parsed = urlparse.urlparse(url)
		self.httplib_inst = httplib.HTTP(parsed.netloc)
		self.httplib_inst.putrequest('GET',parsed.path)
		self.httplib_inst.putheader('Host',parsed.netloc)
		self.httplib_inst.putheader('Accept','text/html')
		self.httplib_inst.putheader('User-agent','Internet Explorer 6.0')
		try:
			self.httplib_inst.endheaders()
			code,msg,headers = self.httplib_inst.getreply()
		except socket.error,e:
			return (False,'')
		try:
			sys.stderr.write("\n\n%s\n%s\n" % (code.replace("\r",""),msg))
		except:
			sys.stderr.write("\n\n%s %s\n" % (code,msg))
		sys.stderr.write("%s" % (headers))
		sys.stderr.write("---------------------------\n")
		html = self.httplib_inst.getfile().read()
		return (True,html)
	"""Return the html from a google search
	"""
	def googleSearch(self,query):
		#f = open("Sample.html","w")
		sys.stderr.write('Searching >>%s<<' % (query))
		parsed = ''
		if query == '':
			return (True,'')
		self.httplib_inst = httplib.HTTP('www.google.com')
		self.httplib_inst.putrequest('GET','/search?num=500&q='+query)
		self.httplib_inst.putheader('Host','www.google.com')
		self.httplib_inst.putheader('Accept','text/html')
		self.httplib_inst.putheader('User-agent','Internet Explorer 6.0')
		try:
			self.httplib_inst.endheaders()
			code,msg,headers = self.httplib_inst.getreply()
		except socket.error,e:
			return (False,'')
		sys.stderr.write("\n\n\n")
		sys.stderr.write("%s\n%s" % (code,msg))
		sys.stderr.write("%s \n" % (headers))
		html = self.httplib_inst.getfile().read()
		#for i in html:
		#	f.write(i)
		#f.flush()
		return (True,html)
if __name__ == "__main__":
	nt = netlib()
	print nt.googleSearch('site:.nasa.gov')

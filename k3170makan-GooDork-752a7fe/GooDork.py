#!/usr/bin/python
import sys
import netlib
import Operator
import getopt
class GooDork:
	def __init__(self):
		self.operator = Operator.Operator()
		self.links = []
		return
	def run(self):
		results = []
		if len(sys.argv[1:]) == 0:
			self.usage()
			sys.exit()
		links = self.operator.goosearch(sys.argv[1])
		self.links = links
		if len(sys.argv[2:]) == 0:
			print "Results:"
			for i,link in enumerate(links):
				 print "%d:%s" % (i+1,link)
			sys.exit()
		try:
			opts,args = getopt.getopt(sys.argv[2:],"b:a:u:t:")
			print opts
		except getopt.GetoptError,e:
			self.usage()
			sys.exit()
		for opt,arg in opts:
			if opt == '-b':
				#print "intext:",arg
				results+=self.intext(arg)
			elif opt == '-a':
				#print "inanchor:",arg
				results+=self.inanchor(arg)
			elif opt == '-t':
				#print "intitle:",arg
				results+=self.intitle(arg)
			elif opt == '-u':
				print "inurl:",arg
				results+=self.inurl(arg)
		results = set(results) #I just OR the results for now
		if len(results) != 0:
			print "Results of %s" % (sys.argv[1:])
			for index,result in enumerate(results):
				print "%d:%s" % (index+1,result)
		else:
			print "No Results match your regex"
		
	def usage(self):
		print """.::GooDork::. 2.0

Usage: ./GooDork [dork] {-b[pattern]|-t[pattern]|-a[pattern]}

dork			-- google search query
pattern			-- a regular expression to search for
-b			-- search the displayable text of the dork results for 'pattern'
-t			-- search the title of the dork results for 'pattern'
-a			-- search in the anchors of the dork results for 'pattern'

e.g ./GooDork site:.edu -bStudents #returns urls to all pages in the .edu domain displaying 'Students'
"""
	def inurl(self,pattern):
		sys.stderr.write("searching for %s in links\n" % pattern)
		return [link for link in self.links if self.operator.inurl(pattern,link)]
	def intext(self,pattern):
		sys.stderr.write("searching for %s in text\n" % pattern)
		return [link for link in self.links if self.operator.intext(pattern,link)]
	def intitle(self,pattern):
		sys.stderr.write("searching for %s in title\n" % pattern)
		return [link for link in self.links if self.operator.intitle(pattern,link)]
	def inanchor(self,pattern):
		sys.stderr.write("searching for %s in anchor\n" % pattern)
		return [link for link in self.links if self.operator.inanchor(pattern,link)] #<-- this is when im lazy!
if __name__ == "__main__":
	try:
		dork = GooDork()
		dork.run()
	except KeyboardInterrupt:
		print "User stopped dork"

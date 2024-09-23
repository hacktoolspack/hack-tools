#!/usr/bin/python
import re
import sys
import urlparse
from bs4 import BeautifulSoup as soup
import netlib
import URLStripper
class Operator:
	"""
		Operator: the object that does all of dorks dirty work for it
			*applies URLStripper calls
			*applies all the neccesary netlib calls
			*performs the dorks
				>inurl,intext....
			and returns them to Dork, where all the boolean logic will be performed
	"""
	def __init__(self):
		self.netlib = netlib.netlib()
		self.stripper = URLStripper.URLStripper()
	"""Get the HTML of the page from the supplied url
		url --- the Resource locator of the page

		returns a single str containing the HTML
	"""
	def getHTML(self,url):
		page = self.netlib.getPage(url)
	#	print page[1]
		if page[0] == False:
			sys.stderr.write("Problem fetching page...[%s]" % (url))
			return False
		return page[1]
	"""Google Search the given query

		returns the links that google replied with corresponding to the query
	"""
	def goosearch(self,query):
		page = self.netlib.googleSearch(query)
		if page[0] == False:
			sys.stderr.write("Problem fetching page...[%s]" % (url))
			return False
		links = self.stripper.strip(page[1])
		return links
	"""Search the displayable text of a page for a given regex pattern
			pattern
		url --- the Resource locator of the page
		pattern  --- the regex pattern to apply

		returns True if the regex form appears in the page
		returns False if it does not
	"""
	def intext(self,pattern,url):
		html = self.getHTML(url)
		if html == False:
			return html
		#now we search the text of the page
		try:
			for string in soup(html).strings:
				#print string
				if re.search(pattern,string) != None:
					return True
		except: #this happend when the file is not HTML!, I'm gonna fix this later , so you can search SQL/XML files aswell
			return re.search(pattern,html) != None #there i fix!!
		return False
	"""Search the url supplied for the given regex pattern
		url		 --- the Resource locator to search
		pattern   --- the regex pattern to apply

		returns True if the pattern does appear in the url supplied
		returns False if not
	"""
	def inurl(self,pattern,url):
		 #i should let them just use regex!, need to read up on python regex
		#print "re.search(%s,%s)" % (pattern,url)
		res = re.search(pattern,url)
		#print res
		return res != None
	"""Search the title tag of a page for the given regex pattern
		url --- the Resource locator (URL) to the page
		pattern --- the regex pattern to apply

		returns True if the regex does appear in the title of the page
		returns False if it does not
	"""
	def intitle(self,pattern,
					url):
		html = self.getHTML(url)
		try:
			title = soup(html).title
		except:
			return False
		return re.search(pattern,title.string) != None
	def inanchor(self,pattern,
					 url):
		html = self.getHTML(url)
		if html == False:
			return html
		try:
			anchors = soup(html).findAll("a")
			for anchor in anchors:
				href = anchor.get("href")
				if self.inurl(pattern,href):
					print "anchor found! [",href,"]"
					return True,href
		except:
			return False
		return False
	"""This has yet to be implemented
		I hope to be able to have users supply a dork and return have Operator return all the URLs 'related' to the urls from the dork query
		e.g
			dork .php?*wp-content*=* -related
		will return all the URLS that are related to the results returned from the dork
	"""
	def related(self): #this is gonna take a lil thought to apply properly, will be quite powerful!
		return
	"""This has yet to be implemented
		This will apply the regex pattern to the domain of the given url string
	"""
	def site(self,url,
				pattern):
		return
	#def cache(self):
	#	return
	"""Search the <input> tags of a page for the supplied regex pattern 
		in the vales of the supplied attribute
		e.g
		 "	ininput(example.com,type,hidden) " will return True if the are input tags 
			where the attribute type is set to hidden i.e <input type=hidden>
		 "	-ininput [\w]=[\d] " will return True if there are any input tags
			where any attributes set to integer data  i.e <input abcdefgh123456709=1>

		url --- the Resource locator to the page
		attr --- the name of the attribute
		pattern --- the regex pattern to be applied
		
		returns True if the pattern does appear in the value of the attribute of the input tags
		returns False if it does not
	"""
	def ininput(self,url
					,attr,pattern):
		return
	"""the same as above but applied to the <form> tag
	"""
	def inform(self,url,
				  attr,pattern):
		return
	"""the same as above but applied to the <img> tag
	
	*PROTIP: this will help you find sites that have been XSSed
	"""
	def inimg(self,url,
				 attr,pattern):
		return
	"""Search the contents of the script tags on a page for the supplied pattern
		url --- the Resouce locator of the page
		pattern -- the regex to be applied to the tag
	Returns True if the pattern was found the contents of the script tag
	Returns False if not
	*PROTIP: this will help you find sites that have been XSSed
	"""
	def inscript(self,url,
					 pattern):
		return
	def inscript_tag(self,url,
						  pattern):
		return
	#I used these methods to test the implementations ;)
	def inanchor_(self,html,pattern):
		f = open(html,"r")
		html = f.read()
		anchors = soup(html).findAll("a")
		for anchor in anchors:
			if re.search(pattern,str(anchor.get("href"))) != None:
				print "Found :",anchor
				return True
		return False
	def intext_(self,html,pattern):
		f = open(html,"r")
		html = f.read()
		for string in soup(html).strings:
			if re.search(pattern,string) != None:
				print "Found :",string
				return True
		return False
if __name__ == "__main__":
	op = Operator()
	op.inanchor_(sys.argv[1],sys.argv[2])

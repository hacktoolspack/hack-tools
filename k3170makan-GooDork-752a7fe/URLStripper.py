#!/usr/bin/python
import urlparse
import re
import sys
#from BeautifulSoup import BeautifulSoup as soup
from bs4 import BeautifulSoup as soup
class URLStripper:
	def __init__(self):
		return
	def strip(self,page):
		self.page = page
		results_wrapper = soup(self.page).find("div",{"id":"ires"})
		if len(results_wrapper) < 1:
			return []
		results_list = results_wrapper.ol
		list_items = results_list.findAll("li",{"class":"g"})
		if len(list_items) == 0:
			return
		#now all thats left is to get the goodies from list_itesm
		results = []
		for li in list_items:
			anchor = li.h3.a.get('href') #we have the link, now we need to cut away all the google trash attached to it
			anchor = str(anchor[7:].split("&sa=")[0])
			if re.search('http://',anchor) != None:
				results.append(anchor)
		return results
if __name__ == "__main__":
	f = open(sys.argv[1],"r")
	f = f.read()
	urls = URLStripper(f,'')
	urls.strip()

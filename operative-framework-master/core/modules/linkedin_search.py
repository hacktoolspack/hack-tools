#!/usr/bin/env	python
#description:Linkedin employee search module#

from colorama import Fore,Back,Style
from core import load

import os,sys
import urllib
import requests
import re,string

class module_element(object):

	def __init__(self):
		self.title = "Linkedin gathering : \n"
		self.require = {"enterprise":[{"value":"","required":"yes"}],"limit_search":[{"value":"","required":"yes"}]}
		self.export = []
		self.export_file = ""
		self.export_status = False

	def show_options(self):
                load.show_options(self.require)

	def export_data(self, argv=False):
                load.export_data(self.export, self.export_file, self.export_status, self.title, argv)
	
	def set_options(self,name,value):
	        load.set_options(self.require, name, value)

	def check_require(self):
                load.check_require(self.require)

	def get_options(self,name):
		if name in self.require:
			return self.require[name][0]["value"]
		else:
			return False

	def set_agv(self, argv):
		self.argv = argv

	def run_module(self):
		ret = self.check_require()
		if ret == False:
			print Back.YELLOW + Fore.BLACK + "Please set the required parameters" + Style.RESET_ALL
		else:
			self.main()

	def main(self):
		userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
		quantity = "100"
		server = "www.google.com"
		word = self.get_options("enterprise")
		limit = int(self.get_options("limit_search"))
		counter = 0
		result = ""
		totalresults = ""
		print Fore.GREEN + "Search Linkedin research" + Style.RESET_ALL
		url="http://"+ server + "/search?num=" + str(limit) + "&start=0&hl=en&meta=&q=site%3Alinkedin.com/in%20" + word
		r=requests.get(url)
		result = r.content
		if result != "":
			regex = re.compile('">[a-zA-Z0-9._ -]* \| LinkedIn')
			output = regex.findall(result)
			if len(output) > 0:
				for line in output:
					if line.strip() != "":
						if " | LinkedIn" in line and '">' in line:
							people = line.strip().replace(' | LinkedIn','').replace('">','')
							print Fore.BLUE + "* "+ Style.RESET_ALL + people
							self.export.append(people)
			else:
				print Fore.RED + "Nothing on linkedin." + Style.RESET_ALL
		else:
			print Fore.RED + "Can't get response" + Style.RESET_ALL



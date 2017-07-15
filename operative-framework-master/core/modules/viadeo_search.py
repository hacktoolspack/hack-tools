#!/usr/bin/env	python
#description:Viadeo employee search module#

from colorama import Fore,Back,Style
from core import load

import os,sys
import urllib
import re,string
import requests

class module_element(object):

	def __init__(self):
		self.title = "Viadeo gathering : \n"
		self.require = {"enterprise":[{"value":"","required":"yes"}],"limit":[{"value":"","required":"no"}]}
		self.export = []
		self.export_file = ""
		self.export_status = False

	def set_agv(self, argv):
		self.argv = argv

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

	def run_module(self):
		ret = self.check_require()
		if ret == False:
			print Back.YELLOW + Fore.BLACK + "Please set the required parameters" + Style.RESET_ALL
		else:
			self.main()

	def main(self):
		server = "www.google.fr"
		limit = 100
		if self.get_options('limit') != '':
			limit = int(self.get_options('limit'))
		url = "http://"+server+"/search?num="+str(limit)+"&start=10&hl=en&meta=&q=site%3Afr.viadeo.com/fr/profile/%20"+self.get_options('enterprise')
		r=requests.get(url)
		results = r.content
		regex = re.compile("\>fr\.viadeo\.com\/fr\/profile\/(.*?)\<\/cite")
		output = regex.findall(results)
		if len(output) > 0:
			print Fore.GREEN + "Viadeo result : "+ Style.RESET_ALL
			for line in output:
				if line.strip() != "":
					print Fore.BLUE + "* " + Style.RESET_ALL + line.strip()
					self.export.append(line.strip())
		else:
			print Fore.RED + "* "+Style.RESET_ALL + "No result found"



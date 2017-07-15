#!/usr/bin/env	python
#description:Get domain with email#

from colorama import Fore,Back,Style
from core import load

import os,sys
import requests
import re
import string

class module_element(object):

	def __init__(self):
		self.title = "Email whois gathering : \n"
		self.require = {"email":[{"value":"","required":"yes"}]}
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
		headers = {
    		'User-Agent': 'Mozilla/5.0'
    	}
		email = self.get_options('email')
		url = "https://whoisology.com/search_ajax/search?action=email&value="+email+"&page=1&section=admin"
		output = ""
		try:
			output = requests.get(url,headers=headers)
			output = output.content
		except:
			print Fore.RED + "Can't open url" + Style.RESET_ALL
		if output != "":
			regex = re.compile('whoisology\.com\/(.*?)">')
			finded = regex.findall(output)
			if len(finded) > 0:
				for line in finded:
					if line.strip() != "":
						if line not in self.export and "." in line:
							self.export.append(line)
							print "- "+Fore.GREEN + line + Style.RESET_ALL
			else:
				print Fore.YELLOW + "Empty domain result for email : "+email +Style.RESET_ALL




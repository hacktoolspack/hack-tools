#!/usr/bin/env	python
#Display header information#

from colorama import Fore,Back,Style
from core import load

import os,sys
import requests

class module_element(object):

	def __init__(self):
		self.title = "Header retrieval : \n"
		self.require = {"website":[{"value":"","required":"yes"}]}
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
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'en-US,en;q=0.8',
		'Connection': 'keep-alive'}
		website = self.get_options('website')
		loaded = 0
		if not "://" in website:
			website = "http://" + website
		print Fore.YELLOW + Style.DIM + "Try load '" + str(website) +"'"+ Style.RESET_ALL
		try:
			req = requests.get(website)
			loaded = 1
			print Fore.GREEN + Style.DIM + "[OK] successfully '" + str(website) +"'"+ Style.RESET_ALL
		except:
			print Fore.RED + "Can't load url '"+str(website)+"'" + Style.RESET_ALL
		if loaded == 1:
			print Fore.YELLOW + Style.DIM + "[wait] header recovery..." + Style.RESET_ALL
			headers = req.headers
			if len(headers) > 0:
				for line in headers:
					lines = line + " : " + headers[line]
					if not lines in self.export:
						print Fore.GREEN + "-" + Style.RESET_ALL + str(lines)
						self.export.append(lines)
			else:
				print Fore.RED + "Header is empty'"+str(website)+"'" + Style.RESET_ALL



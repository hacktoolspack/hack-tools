#!/usr/bin/env	python
#description:	Read/Search common file#

from colorama import Fore,Back,Style
from core import load

import os,sys
import requests

class module_element(object):

	def __init__(self):
		self.title = "Common file : \n"
		self.require = {"website":[{"value":"","required":"yes"}]}
		self.export = []
		self.export_file = ""
		self.export_status = False
		self.common_file = ['/robots.txt']

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
		print Fore.YELLOW + "* check if url is stable" + Style.RESET_ALL
		website = self.get_options('website')
		action = 0
		if "http//" in website:
			website = website.replace('http//','http://')
			if website[-1:] == "/":
				website = website[:-1]
		try:
			requests.get(website)
			action = 1
			print Fore.GREEN + "* website / url is stable" + Style.RESET_ALL
		except:
			print Fore.RED + "* website / url not found" + Style.RESET_ALL
		for line in self.common_file:
			complet_url = website + line
			req = requests.get(complet_url)
			if req.status_code == 200:
				print Fore.GREEN  + "* common file found : " + line + Style.RESET_ALL
				print Fore.BLUE   + "* reading file : " + complet_url + Style.RESET_ALL
				source = req.content
				source = source.split('\n')
				for ligne in source:
					if ligne.strip() != "":
						print "* "+ligne.strip()
				self.export.append(complet_url)




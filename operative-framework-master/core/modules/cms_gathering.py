#!/usr/bin/env	python
#description:Check if CMS is used (wordpress,joomla,magento)#

from colorama import Fore,Back,Style
from core import load

import os,sys
import requests

class module_element(object):

	def __init__(self):
		self.title = "CMS gathering : \n"
		self.require = {"website":[{"value":"","required":"yes"}]}
		self.export = []
		self.export_file = ""
		self.export_status = False
		self.cms = {
			"wordpress":['/wp-includes/','/wp-admin/'],
			"magento":['/frontend/default/','/static/frontend/'],
			"joomla":['/administrator/','/templates/']
		}
		self.status_code = [200,403,301,302]

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
		start = 0
		website = self.get_options('website')
		if "http//" in website:
			website = website.replace('http//','http://')
		print "* Checking for " + Fore.BLUE + website + Style.RESET_ALL
		if website[-1:] == "/":
			website = website[:-1]
		try:
			requests.get(website)
			print Fore.GREEN + "* url is stable" + Style.RESET_ALL
			start = 1
		except:
			print Fore.RED + "* url schema not correct" + Style.RESET_ALL
		if start == 1:
			for line in self.cms:
				print "* checking " + str(line)
				for path in self.cms[line]:
					complet_url = website + path
					req = requests.get(complet_url)
					if req.status_code in self.status_code:
						print Fore.GREEN + "* possible using " + str(line) + " with : " + str(complet_url) + Style.RESET_ALL
						self.export.append(complet_url + " ("+str(line)+")")

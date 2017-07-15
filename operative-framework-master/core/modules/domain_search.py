#!/usr/bin/env	python
#description:Search enterprise domain name#

from colorama import Fore,Back,Style
from core import load

import os,sys
import urllib

class module_element(object):

	def __init__(self):
		self.title = "Domain gathering : \n"
		self.require = {"enterprise":[{"value":"","required":"yes"}]}
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
        	domain_list = []
        	load_name = self.get_options("enterprise")
        	print Style.BRIGHT + Fore.BLUE + "Search domain name for "+load_name + Style.RESET_ALL
        	start_with = ["www.","http://","https://"]
        	end_with   = [".com",".fr",".org",".de",".eu"]
        	for line in start_with:
                	for end_line in end_with:
                        	domain = line + str(load_name) + end_line
                        	try:
                                	return_code = urllib.urlopen(domain).getcode()
                                	return_code = str(return_code)
                                	if return_code != "404":
                                        	domain_list.append(domain)
                                        	print Fore.GREEN + "- "+Style.RESET_ALL + domain
                        	except:
                                	Back.YELLOW + Fore.BLACK + "Can't get return code" + Style.RESET_ALL
		if len(domain_list) > 0:
			for domain in domain_list:
				self.export.append(domain)
		else:
			print Fore.RED + "No domain found" + Style.RESET_ALL



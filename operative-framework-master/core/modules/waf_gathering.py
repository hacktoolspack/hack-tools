#!/usr/bin/env	python
#description:WAF information gathering : need wafw00f#

from colorama import Fore,Back,Style
from core import load

import os,sys
import urllib
import subprocess
import re,string

class module_element(object):

	def __init__(self):
		self.title = "Web Application Firewall gathering : \n"
		self.require = {"domain":[{"value":"","required":"yes"}]}
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
		try:
		    response = subprocess.check_output(["wafw00f", self.get_options("domain")])
		    if "is behind a" in response:
		    	regex = re.compile("is behind a(.*)")
		    	result = regex.findall(response)
		    	print Fore.GREEN + "* " + Style.RESET_ALL + "Firewall found"
		    	print Fore.BLUE + "* "  + Style.RESET_ALL + result[0].strip()
		    	self.export.append(result[0].strip())
		    else:
		    	print Fore.RED + "* "  + Style.RESET_ALL + "Can't get firewall with wafw00f"
		except OSError as e:
		    if e.errno == os.errno.ENOENT:
		        print e
		    else:
		        # Something else went wrong while trying to run `wget`
		        raise



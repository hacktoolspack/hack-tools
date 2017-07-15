#!/usr/bin/env	python
#description:SSL/TLS information gathering (sslyze)#

from colorama import Fore,Back,Style
from core import load

import os,sys
import urllib
import subprocess

class module_element(object):

	def __init__(self):
		self.title = "SSL/TLS gathering : \n"
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
		domain = self.get_options('domain')
		if "://" in domain:
			domain = domain.split("://")[1]
		if domain[:-1] == "/":
			domain = domain[-1]
		try:
		    response = subprocess.check_output(["sslyze", "--regular", domain])
		    if response != "":
		    	explode = response.split('\n')
		    	for line in explode:
		    		self.export.append(line)
		    		print Fore.BLUE + "* " + Style.RESET_ALL + line
		    else:
		    	print Fore.RED + "* "  + Style.RESET_ALL + "Can't get SSL/TLS with sslyze"
		except OSError as e:
		    if e.errno == os.errno.ENOENT:
		        print e
		    else:
		        # Something else went wrong while trying to run `sslyze`
		        raise



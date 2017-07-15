#!/usr/bin/env	python
#description:Reverse ip domain check (Yougetsignal)#

from colorama import Fore,Back,Style
from core import load

import os,sys
import urllib
import requests
import json

class module_element(object):

	def __init__(self):
		self.title = "Reverse ip gathering : \n"
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
	def is_array(self,var):
		return isinstance(var, (list, tuple))

	def main(self):
		content = ""
		url = "http://domains.yougetsignal.com/domains.php"
		try:
			r = requests.post(url, data = {'remoteAddress':self.get_options('domain')})
			content = r.json()
		except:
		 	print Fore.RED + "Can't send requests" + Style.RESET_ALL
		print Fore.GREEN + "Search information for : " + self.get_options('domain') + Style.RESET_ALL
		if content != "":
			for line in content:
				value = ""
				if self.is_array(content[line]):
					print "------------------------------"
					self.export.append("domain listing... : ")
					for content_array in content[line]:
						if self.is_array(content_array):
							value = "-----" + content_array[0]
							print Fore.BLUE + "* " + Style.RESET_ALL + content_array[0]
						else:
							value = "-----" + content_array
							print Fore.BLUE + "* " + Style.RESET_ALL + content_array
						self.export.append(value)
					print "------------------------------"
				else:
		 			print line + " : " + content[line]
		 			value = line + " : " + content[line]
		 		self.export.append(value)
		else:
			print Fore.YELLOW + "" + Style.RESET_ALL






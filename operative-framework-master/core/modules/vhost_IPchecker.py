#!/usr/bin/env	python
#description:Reverse IP domain check (BING)#

from colorama import Fore,Back,Style
from bs4 import BeautifulSoup
from core import load

import os,sys
import urllib
import requests

class module_element(object):

	def __init__(self):
		self.title = "Reverse ip gathering (BING) : \n"
		self.require = {"ip_address":[{"value":"","required":"yes"}]}
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
		server = "www.bing.com"
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
		server_ip = self.get_options('ip_address')
		url = "http://"+server+"/search?q=ip%3a"+str(server_ip)
		print Fore.YELLOW +  Style.DIM + "[wait] try loading url..." + Style.RESET_ALL
		try:
			req = requests.get(url,headers=headers)
			html = req.content
		except:
			print Fore.RED + "[error] Can't load url. " + Style.RESET_ALL
		soup = BeautifulSoup(html,"html.parser",from_encoding="utf-8")
		parsing = soup.findAll('cite')
		for link in parsing:
			website = link.text.encode('ascii', 'ignore')
			if " " in website:
				website = website.split(' ')[0]
			if "/" in website:
				website = website.split('/')[0]
			if "	" in website:
				website = website.split('	')[0]
			if not website in self.export:
				self.export.append(website)
			print Fore.GREEN + "> " + Style.RESET_ALL + website



#!/usr/bin/env	python
#description:Extract url on website domain#

from colorama import Fore,Back,Style
from bs4 import BeautifulSoup
from core import load

import os,sys
import time
import requests

class module_element(object):

	def __init__(self):
		self.title = "Url gathering : \n"
		self.require = {"website_url":[{"value":"","required":"yes"}],"page_limit":[{"value":"100","required":"no"}]}
		self.export = []
		self.export_file = ""
		self.export_status = False
		self.already = []
		self.linked = []
		self.current_load = 1

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

	def parse_domain(self, url):
		if "://" in url:
			url = url.split('://')[1]
		if "." in url:
			url = url.split('.',1)[0]
		return url

	def extract_url(self, url):
		next_page = ""
		nexts = 0
		try:
			req = requests.get(url)
			nexts = 1
		except:
			print Fore.YELLOW + "* Can't open " + str(url) + Style.RESET_ALL
		if nexts == 1:
			if url[-1:] == "/":
				url = url[:-1]
			if url not in self.already and self.parse_domain(self.get_options('website_url')) in url:
				html = req.content
				soup = BeautifulSoup(html, "html.parser")
				link_count = len(soup.findAll('a'))
				print Fore.YELLOW + "* Load : " + str(url) + " with " + str(link_count) + " total link" + Style.RESET_ALL
				for a in soup.findAll('a'):
					try:
						if a['href'] != "":
							total_link = a['href']
							if total_link[:1] == "?":
								total_link = url + "/" + str(total_link)
							if total_link[:1] == "/":
								total_link = url + total_link
							elif total_link[:2] == "//":
								total_link = total_link.replace('//',url + "/")
							elif total_link[:1] == "#":
								total_link = url + "/" + total_link
							elif "://" not in total_link[:8]:
								total_link = url + "/" + total_link
							if "mailto:" not in total_link:
								if total_link not in self.export_file and a['href'] not in self.linked:
									if total_link != "":
										self.export.append(total_link)
								self.linked.append(a['href'])
					except:
						err = 1
				if self.current_load <= int(self.get_options('page_limit')):
					if len(self.export) > 0:
						next_page = self.export[self.current_load]
						if next_page != "":
							self.current_load += 1
							self.extract_url(next_page)
				else:
					return True
	def main(self):
		nexts = 0
		website = self.get_options('website_url')
		if "http//" in website:
			website = website.replace('http//','http://')
		print Fore.GREEN + "* Check if " + str(website) + " is stable" + Style.RESET_ALL
		try:
			req = requests.get(website)
			nexts = 1
		except:
			print Fore.RED + "* Website url is not stable" + Style.RESET_ALL
		if nexts == 1:
			self.extract_url(website)


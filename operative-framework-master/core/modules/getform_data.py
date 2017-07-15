#!/usr/bin/env	python
#description:	Get all form parameters (BETA)#

from colorama import Fore,Back,Style
from core import load

import os,sys
import requests
import re
import time

class module_element(object):

	def __init__(self):
		self.title = "extract form gathering : \n"
		self.require = {"url_list_file":[{"value":"","required":"yes"}],"sqlmap_format":[{"value":"false","required":"no"}]}
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

	def get_form_information(self, form, url):
		form = form.replace("'",'"')
		if "://" in url:
			domain_info = url.split('://')
			if "/" in domain_info[1]:
				domain = domain_info[0] + "://" + domain_info[1].split("/",1)[0]
			else:
				domain = url
		if 'method="' in form:
			method = form.split('method="')[1].split('"')[0]
		else:
			method = ""
		if 'action="' in form:
			action = form.split('action="')[1].split('"')[0]
			if action[:1] == "/":
				action = domain + action
			elif action[:1] == "?" or action == "#":
				action = domain + "/" + action
			elif "://" not in total_link[:8]:
				action = domain + "/" + action
		else:
			action = ""
		array = {'action':str(action),'method':str(method)}
		return array

	def main(self):
		current = 0
		total_form = 0
		current_form = 0
		file_link = self.get_options('url_list_file')
		sqlmap_format = self.get_options('sqlmap_format')
		print Fore.GREEN + "* try to load file url" + Style.RESET_ALL
		if os.path.isfile(file_link):
			total_link = len(open(file_link).read().split('\n'))-1
			for line in open(file_link):
				try:
					current += 1
					line = line.strip()
					if line != "":
						if "- " in line:
							line = line.split("- ")[1]
						sys.stdout.write('\r' + Fore.BLUE + "* total open url ("+str(current)+"/"+str(total_link)+") "+ Style.RESET_ALL + "|" + Fore.YELLOW + " total form exported: ("+str(total_form) + ")" + Style.RESET_ALL)
						req = requests.get(line)
						html = req.content
						if "<form" in html:
							regex = re.compile("\<form[\s]{0,}(.*?)\>(.*?)\<\/form\>",re.S)
						else:
							regex = re.compile("\<FORM[\s]{0,}(.*?)\>(.*?)\<\/form\>",re.S)
						output = regex.findall(html)
						nb_form = len(output)
						if nb_form > 0:
							for form in output:
								form_information = self.get_form_information(form[0], line)
								if "<input" in form[1]:
									regex =  re.compile("\<input(.*?)\>", re.S)
								else:
									regex =  re.compile("\<INPUT(.*?)\>", re.S)
								out_input = regex.findall(form[1])
								if len(out_input) > 0:
									total_line = ""
									for inputs in out_input:
										inputs = inputs.replace("'",'"')
										inputs = inputs.strip()
										if 'name="' in inputs:
											input_name = inputs.split('name="')[1].split('"')[0]
										else:
											input_name = ""
										if 'value="' in inputs:
											input_value = inputs.split('value="')[1].split('"')[0]
										else:
											input_value = ""
										if input_name != "":
											total_line = total_line + "&"+str(input_name)+"="+str(input_value)
									if sqlmap_format.lower() == "true" and form_information['action'] != "":
										if form_information['method'].lower() == "post":
											sqlmap = "sqlmap -u '"+str(form_information['action'])+"' --data='"+str(total_line)+"'"
										else:
											if total_line[:1] == "&":
												total_line = '?' + total_line[1:]
											sqlmap = "sqlmap -u '"+str(form_information['action'])+str(total_line) +"'"
										self.export.append(sqlmap)
									else:
										export_format = "url: " + str(form_information['action']) + " method: " + str(form_information['method']) + " input: " + str(total_line)
										self.export.append(export_format)
								current_form += 1
								total_form = total_form + nb_form
				except:
					errors = 1
				time.sleep(0.3)
				sys.stdout.flush()
			print "..."
		else:
			Fore.RED + "* can't open file : " + str(file_link) + Style.RESET_ALL



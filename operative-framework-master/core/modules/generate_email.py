#!/usr/bin/env	python
#description:Generate email with employee list#

from colorama import Fore,Back,Style
from core import load

import os,sys
import urllib

class module_element(object):

	def __init__(self):
		self.title = "Email generator : \n"
		self.require = {"filename":[{"value":"","required":"yes"}]}
		self.export = []
		self.export_file = ""
		self.export_status = False
		self.domain = [
						'@gmail.com','@hotmail.com','@yahoo.com','@hotmail.fr',
						'@yahoo.fr','yandex.ru']

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

	def generate_email(self, name_last):
		email_list = []
		for domain in self.domain:
			email_first = name_last[1]+"."+name_last[0]+domain
			email_list.append(email_first)
			email_second= name_last[0]+"."+name_last[1]+domain
			email_list.append(email_second)
			email_third = name_last[1]+"-"+name_last[0]+domain
			email_list.append(email_third)
			email_four  = name_last[0]+"-"+name_last[1]+domain
			email_list.append(email_four)
			email_five  = name_last[0]+name_last[1]+domain
			email_list.append(email_five)
			email_six   = name_last[1]+name_last[0]+domain
			email_list.append(email_six)
		for email in email_list:
			self.export.append(email)


	def main(self):
		view = 0
		if os.path.exists(self.get_options('filename')):
			file_open = open(self.get_options('filename')).read()
			if "Viadeo gathering :" in file_open:
				print Fore.GREEN + "* "+Style.RESET_ALL + "Viadeo find..."
				view = 1
				explode_viadeo = file_open.split('Viadeo gathering :')[1]
				explode_viadeo = explode_viadeo.split('\n')
				for employee in explode_viadeo:
					if "-" in employee:
						employee = employee.split('-')[1].strip()
						if "." in employee:
							name_last = employee.split('.')
							self.generate_email(name_last)
			if "Linkedin gathering :" in file_open:
				print Fore.GREEN + "* "+Style.RESET_ALL + "Linkedin find..."
				view = 1
				explode_linkedin = file_open.split('Linkedin gathering :')[1]
				explode_linkedin = explode_linkedin.split('-')
				for employee in explode_linkedin:
					if "-" in employee:
						employee = employee.split('-')
						for line in employee:
							if " " in employee:
								name_last = employee.split(' ')
								self.generate_email(name_last)
				if view == 0:
					print Fore.YELLOW + "Please run Linkedin,Viadeo search module and export"+Style.RESET_ALL
				elif view==1:
					print Fore.GREEN + "* "+Style.RESET_ALL + "All email generated please use :export"



		else:
			print Fore.RED + self.get_options('filename')+Style.RESET_ALL+" Not valid file"



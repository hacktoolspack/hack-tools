#!/usr/bin/env	python

import os,sys
from core import menu
from colorama import Fore,Back,Style

class export(object):
	def __init__(self):
		self.export_type = ""
		self.module_name = ""
		self.export_module = ""
		self.report_array = []
		self.output_name = ""
		self.total_report = False
		self.module_class = ""
		self.extension = "txt"

	def set_export_name(self,export_name):
		self.output_name = export_name
		self.module_class.set_export(export_name)

	def set_module_name(self,name):
		self.module_name = name
		self.module_class.set_name(name)

	def set_report_value(self,value):
		self.report_array = value
		self.module_class.set_report(value)

	def set_total(self,value):
		self.total_report = value
		self.module_class.set_total(value)

	def set_export_type(self,export_type):
		self.export_type = export_type
		self.export_module = menu.menu_export[export_type.upper()]
		try:
			mod = __import__(self.export_module.replace("/","."), fromlist=['export_module'])
			self.module_class = mod.export_module()
			self.extension = self.module_class.extension
		except:
			print Fore.RED + "Can't read export module '" + str(self.export_module) + "'" + Style.RESET_ALL
			sys.exit()
	def begin(self):
		try:
			self.module_class.begin_file()
			return True
		except:
			return False

	def now(self):
		try:
			self.module_class.core_file()
			return True
		except:
			return False

	def end(self):
		try:
			self.module_class.end_file()
			return True
		except:
			return False
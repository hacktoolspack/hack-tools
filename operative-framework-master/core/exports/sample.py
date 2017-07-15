#!/usr/bin/env	python

import os,sys

class export_module(object):
	def __init__(self):
		self.export_name = ""     # File Output Name
		self.export_array = []    # exported data 
		self.total_report = False # int numbers of data
		self.module_name = ""     # Current module name (e.g: WHOIS)
		self.extension = ""       # Output file extension

	def set_export(self,file):
		self.export_name = file

	def set_report(self,value):
		self.export_array = value

	def set_total(self,total_report):
		self.total_report = total_report

	def set_name(self,module_name):
		self.module_name = module_name

	def parse_title(self):
		export_name = self.module_name
		if ":" in export_name:
			export_name= export_name.replace(':', '')
		if '(' in export_name:
			export_name = export_name.replace('(','')
			export_name = export_name.replace(')','')
		export_name = export_name.strip()
		if " " in export_name:
			export_name = export_name.replace(' ', '-')
		self.module_name = export_name

	def begin_file(self):
		# first line of document (if needed).
		return True

	def end_file(self):
		# end line of document (if needed).
		return True

	def core_file(self):
		# Core of export process
		return True
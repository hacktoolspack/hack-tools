#!/usr/bin/env	python
# -*- coding: utf-8 -*-

import os,sys
import json

class export_module(object):
	def __init__(self):
		self.finaly = []
		self.export_name = ""     # File Output Name
		self.export_array = []    # Exported data 
		self.total_report = False # Int numbers of data
		self.module_name = ""     # Current module name (e.g: WHOIS)
		self.extension = "json"   # Output file extension

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
		self.finaly = {"operative-report":{"result":[]}}
		return True

	def end_file(self):
		with open("export/"+self.export_name, 'a+') as outfile:
			json.dump(self.finaly,outfile)
		return True

	def core_file(self):
		self.parse_title()
		if len(self.export_array) > 0:
			nb = 0
			count = len(self.export_array)
			module = str(self.module_name)
			first = {"name":module,"count":str(count),"result":[]}
			for element in self.export_array:
				if not element in first["result"]:
					first["result"].append(element)
			self.finaly["operative-report"]["result"].append(first)
		# Core of export process
		return True
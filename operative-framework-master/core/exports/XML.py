#!/usr/bin/env	python

import os,sys

class export_module(object):
	def __init__(self):
		self.export_name = ""     # File Output Name
		self.export_array = []    # Exported data
		self.total_report = False # Int numbers of data
		self.module_name = ""     # Current module name (e.g: WHOIS)
		self.extension = "xml"    # Output file extension

	def set_export(self,file):
		self.export_name = file

	def set_report(self,value):
		self.export_array = value

	def set_total(self,total_report):
		self.total_report = total_report

	def set_name(self,module_name):
		self.module_name = module_name

	def begin_file(self):
		#first line of XML document.
		self.export_name = self.export_name
		file_open = open("export/" + self.export_name,'a+')
		file_open.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		file_open.write('<operative-framework-report>\n')
		file_open.close()

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

	def end_file(self):
		#end of line
		export_name = self.export_name
		file_open = open("export/" + export_name,'a+')
		file_open.write('</operative-framework-report>')
		file_open.close()

	def core_file(self):
		# Core of export process
		self.parse_title()
		export_name = self.module_name
		output_name = self.export_name
		export_array = self.export_array
		total_report = self.total_report
		first_open = 0
		if len(export_array) > 0:
			nb = 1
			export_name_first = "<report"+str(total_report)+">"
			export_name_end = "</report"+str(total_report)+">"
			file_open = open("export/"+output_name,'a+')
			file_open.write(export_name_first+"\n")
			file_open.write("	<name>"+export_name+"</name>\n")
			file_open.write("	<count>"+str(len(export_array))+"</count>\n")
			for line in export_array:
				if "-" in line[0]:
					line = line[0].replace('-','')
				line = "<value"+str(nb)+">"+line.strip()+"</value"+str(nb)+">"
				file_open.write("	"+line+"\n")
				nb+=1
			file_open.write(export_name_end +"\n")
#!/usr/bin/env	python
#description:	Forensics module for SQL database#

from colorama import Fore,Back,Style
from core import load

import os,sys
import urllib
import string
import re

class module_element(object):

	def __init__(self):
		self.title = "Database gathering : \n"
		self.require = {"nb_result":[{"value":"200","required":"no"}]}
		self.export = []
		self.export_file = ""
		self.argv = ""
		self.export_status = False
		self.current_db = ""
		self.current_db_name = ""
		self.finded = 0
		self.result = []
		self.nb_result = 0

	def set_agv(self, argv):
		self.argv = argv

	def show_options(self):
                load.show_options(self.require)

	def export_data(self):
                load.export_data_search_db(self.export, self.export_file, self.export_status, self.title)
	
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

	def select_db(self, user_input):
			if user_input in self.argv:
				if ".sql" in user_input and "core/dbs" in user_input:
					self.current_db_name = user_input.strip().split('core/dbs/')[1].split('.sql')[0]
				else:
					self.current_db_name = user_input.strip().split('.sql')[0]
				self.current_db = open(user_input.strip()).read()
			else:
				print Fore.RED + "Database not found in list please use :show_db" + Style.RESET_ALL

	def show_table_db(self):
		if self.current_db != "":
			regex = re.compile("CREATE[\s]{0,}TABLE[\s]{0,}[\`]{1}(.*)[\`]{1}")
			output = regex.findall(self.current_db)
			if len(output) < 1:
				print "######################"
				print "#   no table found	#"
				print "######################"
			else:
				print "##############################"
				for line in output:
					line = "#  - "+line
					if len(line) < 30:
						while len(line) < 29:
							line = line + " "
						line = line + "#"
					print line
				print "##############################"
		else:
			print Fore.RED + "Database no selected please use :select dbname" + Style.RESET_ALL

	def show_columns_db(self, table_name):
		if self.current_db != "":
			regex = re.compile("CREATE[\s]{0,}TABLE[\s]{0,}[\`]{1}"+table_name+"[\`]{1}[\s]{0,}[\(](.*?)[\;]",re.S)
			output = regex.findall(self.current_db)
			if len(output) < 1:
				print "######################"
				print "# no columns found   #"
				print "######################"
			else:
				print "##################################################"
				for lines in output:
					explode = lines.split('\n')
					for line in explode:
						if line.strip()[:1] != ")" and line.strip() != "":
							if "`" in line.strip():
								line = line.split('`')[1].split('`')[0]
							line = "# - "+line.strip()
							if len(line) < 50:
								while len(line) < 49:
									line = line + " "
								line = line + "#"
							if "," in line:
								line = line.replace(',','')
							if line.strip() != "":
								print line
				print "##################################################"
		else:
			print Fore.RED + "Database no selected please use :select dbname" + Style.RESET_ALL

	def get_value_db(self, user_input):
			if self.current_db != "":
				explode = user_input.split(' ')
				if len(explode) < 3:
					print Fore.RED + "Please use correct usage :get <table> <value>" + Style.RESET_ALL
				else:
					table_name = explode[1].strip()
					data = explode[2].strip()
					print Fore.GREEN + "Search " + Style.BRIGHT + data + Style.RESET_ALL + Fore.GREEN +" in " + Style.BRIGHT + table_name + Style.RESET_ALL + Fore.GREEN + "..." + Style.RESET_ALL
					regex_value = re.compile("INSERT[\s]{0,}INTO[\s]{0,}[`]"+table_name+"[\`].*?VALUES(.*?)\;",re.S)
					output = regex_value.findall(self.current_db)
					if len(output) > 0:
						for line in output:
							line = line.strip()
							if line != "":
								if '(' in line:
									line = line.replace('(','')
									if ");" in line:
										line = line.split(');')[0]
									elif ")," in line:
										line = line.replace('),',')nxl,')
								if "'" in line:
									line = line.replace('\'','')
								if "," in line:
									get_all = line.split(')nxl,')
									if len(get_all) > 0:
										for information in get_all:
											for nexline in information.split(','):
												if data in nexline:
													if self.nb_result != int(self.get_options('nb_result')):
														self.nb_result += 1
														self.export_search(information.split(','), data)
													else:
														break
						if self.finded == 0:
							print Fore.RED + "No result found" + Style.RESET_ALL
						else:
							self.finded = 0
							self.result = []
					else:
						print Fore.YELLOW + "No entrie found for this table" + Style.RESET_ALL
			else:
				print Fore.RED + "Database no selected please use :select dbname" + Style.RESET_ALL


	def export_search(self, get_all, word):
		if self.finded == 0:
			print "------------------------------------"
		self.finded = 1
		nb_result = len(get_all)
		if get_all not in self.result:
			count = 0
			for line in get_all:
				if ")" in line:
					line = line.replace(')','')
				if line.strip() != "":
					count += 1
					if word in line.strip():
						string = Fore.RED + Style.BRIGHT + word + Style.RESET_ALL
						line = line.replace(word,string)
					print "data "+str(count)+": "+line.strip()
			print "------------------------------------"
			self.result.append(get_all)


	def main(self):
		action = 0
		while action == 0:
			if self.current_db == "":
				prompt = "operative ("+Fore.YELLOW+"module"+Style.RESET_ALL+":"+Fore.RED+"running"+Style.RESET_ALL+") > "
			else:
				prompt = "operative ("+Fore.YELLOW+"module"+Style.RESET_ALL+":"+Fore.RED+"running"+Style.RESET_ALL+":"+Fore.GREEN+self.current_db_name+Style.RESET_ALL+") > "
			user_input = raw_input(prompt)
			if ":" in user_input:
				user_input = user_input.replace(':','')
			if user_input == "quit":
				action = 1
			elif user_input == "help":
				print """:select <dbs>		Select current database
:show_db		Show databases list
:show_table		Show tables listing
:show_columns <table>	Show columns from table
:get <table> <value>	Seach value in table
:quit			Exit module"""
			elif user_input == "show_db":
				for line in self.argv:
					print "- "+Fore.GREEN+line+Style.RESET_ALL
			elif "select" in user_input:
				self.select_db(user_input.split('select')[1].strip())
			elif user_input == "show_table":
				self.show_table_db()
			elif "show_columns" in user_input:
				user_input = user_input.split('show_columns')[1].strip()
				self.show_columns_db(user_input)
			elif "get " in user_input:
				self.get_value_db(user_input)

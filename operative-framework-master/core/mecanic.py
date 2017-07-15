#!/usr/bin/env	python
# -*- coding: utf-8 -*-

import sys,os
import time
import glob
import urllib
import string
import random
import json
from colorama import Fore,Back,Style
from core import export

total_dbs = []
total_report = 0

def load(name):
	if "use" in name:
		load_module(name)
	else:	
		globals()[name]()

def exit_operative():
	sys.exit()

def banner():
	version = "1.0b"
	print """                               __  _          
  ____  ____  ___  _________ _/ /_(_)   _____ 
 / __ \/ __ \/ _ \/ ___/ __ `/ __/ / | / / _ \\
/ /_/ / /_/ /  __/ /  / /_/ / /_/ /| |/ /  __/
\____/ .___/\___/_/   \__,_/\__/_/ |___/\___/ 
    /_/ """+Fore.RED+"Version: "+Style.RESET_ALL+version+" | "+Fore.RED+"Twitter: "+Style.RESET_ALL+"""@graniet75"""
	print Fore.YELLOW + "        If you don't know how run it use :help\n" + Style.RESET_ALL

def use_module(module, argv=False):
	action = 0
	module_class = ""
	module_name = module.split(".py")[0]
	while action == 0:
		try:
			user_input = raw_input("$ operative ("+Fore.YELLOW+module_name+Style.RESET_ALL+") > ")
		except:
			print "..."
			action = 1
			break
		
		if ":" in user_input[:1]:
			user_input = user_input[1:]
		if module_class == "":
			module_path = module_name.replace("/",".")
			mod = __import__(module_path, fromlist=['module_element'])
			module_class = mod.module_element()
		if argv != False:
			module_class.set_agv(argv)
		if user_input == "show options":
			module_class.show_options()
		elif "set" in user_input and "=" in user_input:
			value = user_input.split(" ",1)[1].split("=")
			module_class.set_options(value[0],value[1])
		elif user_input == "help":
			print """:show options		Show module options
:set option=value	Set value from element
:run			Run current  module
:export			Export module return data
:quit			Exit current module"""
		elif user_input == "quit":
			break
		elif user_input == "clear":
			os.system('clear')
		elif user_input == "run":
			module_class.run_module()
		elif user_input == "export":
			module_class.export_data()
	print Fore.YELLOW + "Stop module : " + module_name + "..." + Style.RESET_ALL

def load_module(name):
	if "use " in name:
		module = name.split("use")[1].strip() + ".py"
		module = "core/modules/" + module
		if os.path.exists(module):
			print Fore.GREEN + "Loading : " + module + Style.RESET_ALL
			use_module(module)
		else:
			print Back.RED + "Module not found" + Style.RESET_ALL

def show_module():
	if os.path.exists("core/modules/"):
		list_module = glob.glob("core/modules/*.py")
		for module in list_module:
			if ".py" in module:
				module_name = module.split(".py")[0]
				module_name = module_name.replace('core/modules/','')
			if "__init__" not in module:
				description = "No module description found"
				if "#description:" in open(module).read():
					description = open(module).read().split("#description:")[1]
					description = description.split("#")[0]
				print Fore.BLUE + " * "+ Style.RESET_ALL  + module_name + "		" + description
	else:
		print Back.RED + Fore.BLACK + "Modules directory not found"+ Style.RESET_ALL
def show_help():
	print """:modules		Show module listing
:campaign 		Start Gath/Fingerprint campaign
:new_module		Generate a new module class
:helper			Use helper class
:load_db		Load SQL database
:search_db		Search information on database
:use <module>		Use module
:update			Update operative framework
:clear			Clear current screen
:help			Show this bullet & close
:quit			Close operative framework"""

def update_framework():
	print Fore.GREEN + "[information] checking update..." + Style.RESET_ALL
	try:
		os.system('git pull')
		print Fore.YELLOW + "[warning] please reboot a framework" + Style.RESET_ALL
	except:
		print Fore.RED + "[error] can't start update please use <git pull>" + Style.RESET_ALL

def clear_screen():
	os.system('clear')

def generate_session(name):
	time_day = time.strftime("%Y-%m-%d")
	file_open = open("."+time_day,"w")
	file_open.write("name=" + name + "#")
	file_open.close()
	print Fore.GREEN + "Session generated " + Style.RESET_ALL

def search_dbs():
	if len(total_dbs) > 0:
		use_module('core/modules/search_db.py',total_dbs)
	else:
		print Fore.RED + "Please before use :load_db"+ Style.RESET_ALL

def check_session(name):
	time_day = time.strftime("%Y-%m-%d")
	if not os.path.exists("."+time_day):
		generate_session(name)
	elif os.path.exists("."+time_day):
		user_input = raw_input(Fore.YELLOW + "operative (overwrite old session?) [Y/n] " + Style.RESET_ALL)
		if user_input == "" or user_input == "Y" or user_input == "y":
			generate_session(name)		

def set_enterprise():
	user_input = raw_input("operative (enterprise name) > ")
	check_session(user_input)
	run_enterprise()

def run_enterprise():
	time_day = time.strftime("%Y-%m-%d")
	if os.path.exists("."+time_day):
		file_open = open("."+time_day).read()
		print Fore.GREEN + "New session set for : " + file_open.split("name=")[1].split("#")[0] + Style.RESET_ALL
	else:
		print Fore.RED + "Please run <set> for make session" + Style.RESET_ALL

def get_current():
	filename = "."+time.strftime("%Y-%m-%d")
	if os.path.exists(filename):
		content = open(filename).read()
		return content.split("name=")[1].split("#")[0]
	else:
		set_enterprise()
		get_current()

def load_db():
	global total_dbs
	count = 1
	if not os.path.isdir("core/dbs/"):
		print Fore.RED + "core/dbs/ folder not found" + Style.RESET_ALL
		return False
	else:
		file_dbs = glob.glob("core/dbs/*.sql")
		if len(file_dbs) < 1:
			print Fore.YELLOW + "core/dbs/ No dbs found" + Style.RESET_ALL
			return False
		else:
			file_nb = len(file_dbs)
		print "Load "+str(file_nb)+" databases..."
		for line in file_dbs:
			if line not in total_dbs:
				print "Load database : "+Fore.GREEN + line + Style.RESET_ALL
				total_dbs.append(line)
			else:
				print "Already loaded : "+Fore.YELLOW + line + Style.RESET_ALL

def start_campaign():
	if os.path.isfile('config.json'):
		with open('config.json') as json_file:
			data_json = json.load(json_file)
		check_modules_exists(data_json)
		check_require(data_json)
		load_campaign_(data_json)
	else:
		print Fore.RED + "Can't locate a config.json" + Style.RESET_ALL

def generate_module_class():
	action = 0
	if os.path.isfile('core/modules/sample_module.py'):
		while action == 0:
			module_name = raw_input('(operative) New module name > ')
			if module_name != "":
				if ".py" in module_name:
					module_name = module_name.split('.py')[0]
				if not os.path.isfile('core/modules/'+module_name+'.py'):
					module_description = raw_input('(operative) New module description > ')
					if module_name != "":
						new_module_file = open('core/modules/'+module_name+'.py','w')
						sample_module_source = open('core/modules/sample_module.py').read()
						if "#description:" in sample_module_source:
							sample_module_source = sample_module_source.replace('#description:Module sample#',
																				'#description:'+str(module_description)+"#")
						new_module_file.write(sample_module_source)
						new_module_file.close()
						print Fore.GREEN + "Module as been written '"+str('core/modules/'+module_name+'.py')+"'" + Style.RESET_ALL
						print "Now add argument on self.require & write your code in main(), Good luck"
						action = 1
					else:
						print Fore.RED + "- " + Style.RESET_ALL + "Please enter a description"

			else:
				print Fore.RED + "- " + Style.RESET_ALL + " Please enter new module name..."

	else:
		print Fore.RED + "-" + Style.RESET_ALL + " Can't find sample_module file"
		sys.exit()

def use_helper(user_input):
	if not " " in user_input.strip():
		if os.path.exists('core/helpers/'):
			print Fore.YELLOW + " !" + Style.RESET_ALL + " use helper with :helper helper_name"
			for helper in glob.glob('core/helpers/*.py'):
				if not "__init__" in helper:
					helper_source = open(helper).read()
					helper_description = "No helper description"
					helper_name = helper.split('core/helpers/')[1].split('.py')[0]
					if "#description:" in helper_source:
						helper_description = helper_source.split('#description:')[1].split('#')[0]
					print Fore.BLUE + " * " + Style.RESET_ALL + str(helper_name) + "		" + str(helper_description)
		else:
			print Fore.RED + "- " + Style.RESET_ALL + "Helper folder not found"
	else:
		helper_name = user_input.strip().split(' ')[1]
		if not "core/helpers/" in helper_name:
			helper_name = "core/helpers/" + str(helper_name)
		if os.path.isfile(str(helper_name) + ".py"):
			try:
				module_path = helper_name.replace("/", ".")
				mod = __import__(module_path, fromlist=['helper_class'])
				helper_class = mod.helper_class()
				action = 0
				while action == 0:
					try:
						user_put = raw_input('operative helper ('+Fore.YELLOW+helper_name+Style.RESET_ALL+') > ')
					except:
						print "..."
						action = 1
						break
					if ":" in user_put:
						user_put = user_put.replace(':','')
					if user_put == "show options":
						helper_class.show_options()
					elif user_put == "resume":
						helper_class.get_resume()
					elif user_put == "run":
						helper_class.run_module()
					elif "set" in user_put and "=" in user_put:
						value = user_put.split(" ", 1)[1].split("=")
						helper_class.set_options(value[0], value[1])
					elif user_put == "help":
						print """:show options		Show module options
:set option=value	Set value from element
:resume			Get helper resume
:run			Run current  module
:quit			Exit current module"""
					elif "quit" == user_put:
						break
			except:
				print Fore.RED + "- " + Style.RESET_ALL + "Can't load helper"

		else:
			print Fore.RED + "- " + Style.RESET_ALL + "Helper not found"

def check_modules_exists(modules):
	for item in modules["campaign"]["modules"]:
		module_name = item['name']
		if not os.path.isfile('core/modules/' + module_name + '.py'):
			print Fore.RED + "Can't load a 'core/modules/"+module_name+".py'" + Style.RESET_ALL
			sys.exit()
def check_require(config):
	require_modules = []
	for item in config['campaign']['modules']:
		for item_require in item['require']:
			if item_require != '' and not item_require in require_modules:
				require_modules.append(item_require)
	for item in config['campaign']['required']:
		if not item['name'] in require_modules:
			print Fore.RED + Style.DIM + "can't locate requirement : " + item['name'] + Style.RESET_ALL
			sys.exit()
		if item['value'] == "":
			print Fore.RED + Style.DIM + "required value can't be null" + Style.RESET_ALL
			sys.exit()
def load_campaign_(config):
	global total_report
	action = 0
	first_use = 0
	module = __import__("core.export", fromlist=['export'])
	export_module = module.export()
	export_module.set_export_type(config['campaign']['export'])
	extension = export_module.extension
	while action == 0:
		export_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))+ "." + extension
		if not os.path.isfile("export/" + export_name):
			export_module.set_export_name(export_name)
			if export_module.begin() == True:
				first_use = 1
			action = 1
	requirement = config['campaign']['required']
	modules = config['campaign']['modules']
	for module in modules:
		require_module = module['require']
		module_path = "core/modules/"+module['name']+".py"
		if os.path.isfile(module_path):
			print Fore.GREEN + Style.DIM + "[load] " + module_path + Style.RESET_ALL
			mod = __import__(module_path.replace("/",".").split('.py')[0], fromlist=['module_element'])
			module_class = mod.module_element()
			for item_required in require_module:
				for item_requirement in requirement:
					if item_requirement['name'] == item_required:
						required = item_requirement['value']
				module_class.set_options(item_required,required)
				print Fore.BLUE + Style.DIM + "[setup] argument " + item_required + ":" + required + Style.RESET_ALL
			module_class.run_module()
			if len(module_class.export) > 0:
				total_report += 1
			export_module.set_module_name(module_class.title)
			export_module.set_report_value(module_class.export)
			export_module.set_total(total_report)
			export_value = export_module.now()
			if export_value == False:
				module_class.export_data(export_name) # modules export function
	if first_use == 1:
		export_module.end()
	print Fore.GREEN + "Report written here 'export/"+export_module.output_name+"'" + Style.RESET_ALL

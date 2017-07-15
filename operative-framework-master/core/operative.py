#!/usr/bin/env	python
# -*- coding: utf-8 -*-

import sys,os
import time
from core import menu
from core import mecanic
from colorama import Fore,Back,Style

def loading():
	red_bold = Style.BRIGHT + Fore.RED
	reset = Style.RESET_ALL
	loading = "loading the fingerprinting framework"
	action = 0
	while action < 1:
		for i,char in enumerate(loading):
			if i == 0:
				print "%s%s%s%s" %(red_bold,char.upper(),reset,loading[1:])
			elif i == 1:
				old_loading = loading[0].lower()
				print "%s%s%s%s%s" %(old_loading,red_bold,char.upper(),reset,loading[2:])
			elif i == i:
				old_loading = loading[-0:i].lower()
				print "%s%s%s%s%s" %(old_loading,red_bold,char.upper(),reset,loading[i+1:])
			time.sleep(0.1)
			os.system('clear')
		action += 1
	return True

def shortcut_loading():
	for line in sys.argv:
		if line in menu.menu_shortcut:
			mecanic.load(menu.menu_shortcut[line])
			sys.exit()

def user_put():
	shortcut_loading()
        loading() # Comment to omit loading
	mecanic.banner()
	shortcut_loading()
	action = 0
	while action == 0:
		try:
			user_input = raw_input("$ operative > ")
		except:
			print "..."
			sys.exit()
		if ":" in user_input:
				user_input = user_input.replace(':','')
		if user_input in menu.menu_list:
			mecanic.load(menu.menu_list[user_input])
		if "use " in user_input:
			mecanic.load(user_input)
		if "helper" in user_input:
			mecanic.use_helper(user_input)
		

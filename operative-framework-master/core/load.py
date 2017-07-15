#!/usr/bin/env	python

from colorama import Fore,Back,Style
import os, sys

def show_options(require):
    #print Back.WHITE + Fore.WHITE + "Module parameters" + Style.RESET_ALL
    for line in require:
        if require[line][0]["value"] == "":
	    value = "No value"
	else:
	    value = require[line][0]["value"]
	if require[line][0]["required"] == "yes":
	    if require[line][0]["value"] != "":
	        print Fore.GREEN+Style.BRIGHT+ "+ " +Style.RESET_ALL+line+ ": " +value
	    else:
	        print Fore.RED+Style.BRIGHT+ "- " +Style.RESET_ALL+line+ "(" +Fore.RED+ "is_required" +Style.RESET_ALL+ "):" +value
	else:
	    if require[line][0]["value"] != "":
		print Fore.GREEN+Style.BRIGHT+ "+ " +Style.RESET_ALL+line + ": " +value
	    else:
		print Fore.WHITE+Style.BRIGHT+ "* " +Style.RESET_ALL+line + "(" +Fore.GREEN+ "optional" +Style.RESET_ALL+ "):" +value
    #print Back.WHITE + Fore.WHITE + "End parameters" + Style.RESET_ALL

def export_data(export, export_file, export_status, title, argv):
    if len(export) > 0:
        if export_file == "":
	    if argv == False:
	        user_input = raw_input("operative (export file name ?) > ")
	    else:
		user_input = argv
	    if os.path.exists("export/"+user_input):
		export_file = "export/"+user_input
	    elif os.path.exists(user_input):
		export_file = user_input
	    else:
	        print Fore.GREEN + "Writing " + user_input + " file" + Style.RESET_ALL
		export_file = "export/"+user_input
	    export_data(export, export_file, export_status, title, argv)
	elif export_status == False:
	    file_open = open(export_file,"a+")
	    file_open.write(title)
	    for line in export:
	        file_open.write("- " + line +"\n")
	    print Fore.GREEN + "File writed : " + export_file + Style.RESET_ALL
	    file_open.close()
	    export_status = True
	else:
	    print Back.YELLOW + Fore.BLACK + "Module empty result" + Style.RESET_ALL


def export_data_search_db(export, export_file, export_status, title):
    if len(export) > 0:
        if export_file == "":
	    user_input = raw_input("operative (export file name ?) > ")
	    if os.path.exists("export/"+user_input):
	        export_file = "export/"+user_input
	    elif os.path.exists(user_input):
	        export_file = user_input
	    else:
	        print Fore.GREEN + "Writing " + user_input + " file" + Style.RESET_ALL
		export_file = "export/"+user_input
	    export_data(export, export_file, export_status, title)
	elif export_status == False:
	    file_open = open(export_file,"a+")
	    file_open.write(title)
	    for line in export:
	        file_open.write("- " + line +"\n")
	    print Fore.GREEN + "File writed : " + export_file + Style.RESET_ALL
	    file_open.close()
	    export_status = True
    else:
        print Back.YELLOW + Fore.BLACK + "Module empty result" + Style.RESET_ALL


def set_options(require, name, value):
    if name in require:
        require[name][0]["value"] = value
    else:
        print Fore.RED + "Option not found" + Style.RESET_ALL

def check_require(require):
    for line in require:
        for option in require[line]:
            if option["required"] == "yes":
                if option["value"] == "":
                    return False
    return True


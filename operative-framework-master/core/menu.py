#!/usr/bin/env	python

import sys

menu_list = {	
	"quit":"exit_operative",
	"modules":"show_module",
	"help":"show_help",
	"set":"set_enterprise",
	"run":"run_enterprise",
	"load_db":"load_db",
	"search_db":"search_dbs",
        "update":"update_framework",
	"clear":"clear_screen",
	"search_domain":"domain_module",
	"campaign":"start_campaign",
	"new_module":"generate_module_class"
}

menu_shortcut = {
	"--campaign":"start_campaign",
	"--update":"update_framework",
	"--modules":"show_module",
	"--version":"banner",
	"--generate_module":"generate_module_class"
}

menu_export = {
	"XML":"core/exports/XML",
	"JSON":"core/exports/JSON",
	"HTML":"core/exports/HTML"
}


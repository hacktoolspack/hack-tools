#!/usr/bin/env  python
#description:Check syntax for operative framework modules#
# -*- coding: utf-8 -*-

import os,sys
from colorama import Fore, Style, Back
from core import load

class helper_class(object):

    def __init__(self):
        self.resume  = {
            'Name': 'Module Class Syntax checker',
            'Desc': 'Check syntax for operative framework modules',
            'Author': 'Tristan Granier'
        }
        self.param_type = []
        self.require = {"module_path": [{"value": "", "required": "yes"}],"param_monitor":[{"value":"True/False", "required": "no"}]}

    def set_agv(self, argv):
        self.argv = argv

    def get_resume(self):
        print Fore.YELLOW + "Name          " + Style.RESET_ALL + ": " + self.resume['Name']
        print Fore.YELLOW + "Description   " + Style.RESET_ALL + ": " + self.resume['Desc']
        print Fore.YELLOW + "Author        " + Style.RESET_ALL + ": (c) " + self.resume['Author']

    def show_options(self):
        load.show_options(self.require)

    def set_options(self, name, value):
	load.set_options(self.require, name, value)

    def check_require(self):
        load.check_require(self.require)

    def get_options(self, name):
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

    def reload_main(self):
        user_put = raw_input('(operative) Reload module ? [Y/n]')
        if user_put == "" or user_put == "Y" or user_put == "y":
            self.run_module()

    def param_monitor(self, module_current):
        for line in module_current.require:
            if not line in self.param_type:
                action = 0
                while action == 0:
                    type_of_param = raw_input('(' + Fore.YELLOW + str(line) + Style.RESET_ALL + ") [INTEGER/STRING/ALL] : ")
                    if str(type_of_param).lower() == "str" or str(type_of_param).lower() == "string":
                        self.param_type.append({'name':str(line),'param':[{'type':'STRING'}]})
                        action = 1
                    elif str(type_of_param).lower() == "int" or str(type_of_param).lower() == "integer":
                        self.param_type.append({'name':str(line),'param':[{'type':'INTEGER'}]})
                        action = 1
                    elif str(type_of_param).lower() == "all":
                        self.param_type.append({'name':str(line),'param':[{'type':'ALL'}]})
                        action = 1
                    else:
                        print Fore.YELLOW + "Please enter correct parameter" + Style.RESET_ALL


    def main(self):
        module_name = self.get_options('module_path')
        param_monitor = self.get_options('param_monitor')
        success = 0
        if os.path.isfile(module_name):
            if "/" in module_name:
                module_path = module_name.replace("/", ".")
                module_path = module_path.replace('.py','')
                try:
                    mod = __import__(module_path, fromlist=['module_element'])
                    module_class = mod.module_element()
                    success = 1
                    if success == 1:
                        if str(param_monitor) == "true" or str(param_monitor) == "True":
                            self.param_monitor(module_class)
                        print "------------------------"
                        try:
                            success = 0
                            print Fore.YELLOW + "Information: " + Style.RESET_ALL + " :show options"
                            module_class.show_options()
                            success = 1
                            print "+ status: " + Fore.GREEN + "OK" + Style.RESET_ALL
                            if success == 1:
                                try:
                                    success = 0
                                    print Fore.YELLOW + "Information: " + Style.RESET_ALL + " :set options=value"
                                    if len(self.param_type) > 0:
                                        for line in self.param_type:
                                            base_value = ""
                                            #print str(line['name']) + Fore.BLUE + " => " + Style.RESET_ALL + str(line['param'][0]['type'])
                                            if str(line['param'][0]['type']) == "STRING":
                                                base_value = "DEBUGSYNTAX"
                                            elif str(line['param'][0]['type']) == "INTEGER":
                                                base_value = 123
                                            elif str(line['param'][0]['type']) == "ALL":
                                                base_value = "D3BUG_S1NT4X"
                                            module_class.set_options(str(line['name']), str(base_value))
                                            for line in module_class.require:
                                                print "* " + str(line) + Fore.BLUE + " => " + Style.RESET_ALL + module_class.require[line][0]["value"]
                                    else:
                                        for line in module_class.require:
                                            print "- set " + str(line)
                                            module_class.set_options(line,'val_debug')
                                    print "+ status: " + Fore.GREEN + "OK" + Style.RESET_ALL
                                    success = 1
                                except Exception, e:
                                    print "- status: " + Fore.RED + "ERROR" + Style.RESET_ALL
                                    print str(e)
                                    self.reload_main()
                            if success == 1:
                                try:
                                    success = 0
                                    print Fore.YELLOW + "Information: " + Style.RESET_ALL + " :run"
                                    module_class.run_module()
                                    print "+ status: " + Fore.GREEN + "OK" + Style.RESET_ALL
                                    success = 1
                                except Exception,e:
                                    print "- status: " + Fore.RED + "ERROR" + Style.RESET_ALL
                                    print str(e)
                                    self.reload_main()
                                if success == 1:
                                    print Fore.GREEN + "Your module seem be OK" + Style.RESET_ALL
                                    print "------------------------"


                        except Exception,e:
                            print "- status: " + Fore.RED + "ERROR" + Style.RESET_ALL
                            print str(e)
                            self.reload_main()
                except Exception,e:
                    print "- status: " + Fore.RED + "ERROR" + Style.RESET_ALL
                    print str(e)
                    self.reload_main()
            else:
                Fore.RED + "- " + Style.RESET_ALL + "Please use full relative path of module"
        else:
            print Fore.RED + "- " + Style.RESET_ALL + "Please enter correct module path"

from functions import *
"""Telnet Fuzzer"""
PROPERTY={}
PROPERTY['PROTOCOL']="TNET"
PROPERTY['NAME']=": Telnet Fuzzer"
PROPERTY['DESC']="Fuzz a Telnet server"
PROPERTY['AUTHOR']='localh0t'

class FuzzerClass:
	def fuzzer(self):
		fuzzTCP()
		fuzzUser("USER")
		fuzzPass("test","USER","PASS")
		exitProgram(2)
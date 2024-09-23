from functions import *
"""TCP Fuzzer"""
PROPERTY={}
PROPERTY['PROTOCOL']="TCP"
PROPERTY['NAME']=" : TCP Fuzzer "
PROPERTY['DESC']="Send garbage to a TCP connection "
PROPERTY['AUTHOR']='localh0t'

class FuzzerClass:
	def fuzzer(self):
		fuzzTCP()
		exitProgram(2)
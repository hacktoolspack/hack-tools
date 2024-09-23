from functions import *
"""UDP Fuzzer"""
PROPERTY={}
PROPERTY['PROTOCOL']="UDP"
PROPERTY['NAME']=" : UDP Fuzzer "
PROPERTY['DESC']="Send garbage to a UDP connection "
PROPERTY['AUTHOR']='localh0t'

class FuzzerClass:
	def fuzzer(self):
		fuzzUDP()
		exitProgram(2)
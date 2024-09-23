from functions import *
"""SSH Fuzzer"""
PROPERTY={}
PROPERTY['PROTOCOL']="SSH"
PROPERTY['NAME']=" : SSH Fuzzer "
PROPERTY['DESC']="Fuzz an SSH server "
PROPERTY['AUTHOR']='localh0t'

# Generic SSH-1.99-OpenSSH_3.4 header, for key exchange purporses
header = ["\x53\x53\x48\x2d\x31\x2e\x39\x39\x2d\x4f\x70\x65\x6e\x53\x53\x48\x5f\x33\x2e\x34\x0a\x00\x00\x4f\x04\x05\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xde"]

class FuzzerClass:
	def fuzzer(self):
 		fuzzTCP()
		sock = createSocketTCP(0,0)
		fuzzCommands(sock,header,0,"SingleCommand")
		exitProgram(2)
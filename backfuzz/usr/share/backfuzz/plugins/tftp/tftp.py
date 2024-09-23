from functions import *
from binascii import unhexlify as unhex

"""TFTP Fuzzer"""
PROPERTY={}
PROPERTY['PROTOCOL']="TFTP"
PROPERTY['NAME']=": TFTP Fuzzer"
PROPERTY['DESC']="Fuzz an TFTP Server "
PROPERTY['AUTHOR']='localh0t'

# Stages
stage_1 = [(" (Read request)" , "0x0001"), (" (Write request)" , "0x0002")]
stage_2 = [(" (Data)" , "0x0003")]
stage_3 = [(" (Error)" , "0x0005")]

# Stuff
null = (" (NULL Byte)", "0x00")
mode = (" (Mode)", "netascii")
somefile = (" (File)", "inexistent.file")
block = (" (Block Number)", "0x0001")
error_opcodes = [(" (Not defined, see error message)" , "0x0000"), (" (File not found)" , "0x0001"),
				 (" (Access violation)" , "0x0002"), (" (Disk full or allocation exceeded)" , "0x0003"),
				 (" (Illegal TFTP operation)" , "0x0004"), (" (Unknown transfer ID)" , "0x0005"),
				 (" (File already exists)" , "0x0006"), (" (No such user)" , "0x0007")]

class FuzzerClass:
	def fuzzer(self):
		fuzzUDP()
		# Stage 1
		for opcode in stage_1:
			printCommand(opcode[0])
			for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
				payloadCount(length)
				pattern = createPattern(length)
				payload = unhex(opcode[1][2:]) + pattern + unhex(null[1][2:]) + mode[1] + unhex(null[1][2:])
				spattern = opcode[1] + opcode[0] + " + " + pattern + somefile[0] + " + " + null[1] + null[0] + " + " + mode[1] + mode[0] +  " + " + null[1] + null[0]
				sock = createSocketUDP(spattern,length)
				sendDataUDP(sock,payload,spattern,length,1)
			printCommand("(Mode) with" + opcode[0])
			for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
				payloadCount(length)
				pattern = createPattern(length)
				payload = unhex(opcode[1][2:]) + somefile[1] + unhex(null[1][2:]) + pattern + unhex(null[1][2:])
				spattern = opcode[1] + opcode[0] + " + " + somefile[1] + somefile[0] +  " + " + null[1] + null[0] + " + " + pattern + mode[0] + " + " + null[1] + null[0]
				sock = createSocketUDP(spattern,length)
				sendDataUDP(sock,payload,spattern,length,1)
		# Stage 2
		for opcode in stage_2:
			printCommand(opcode[0])
			for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
				payloadCount(length)
				pattern = createPattern(length)
				payload = unhex(opcode[1][2:]) + unhex(block[1][2:]) + pattern + unhex(null[1][2:])
				spattern = opcode[1] + opcode[0] + " + " + block[1] + block[0] + " + " + pattern + opcode[0] + " + " + null[1] + null[0]
				sock = createSocketUDP(spattern,length)
				sendDataUDP(sock,payload,spattern,length,1)

		# Stage 3
		for opcode in stage_3:
			for error_opcode in error_opcodes:
				printCommand(opcode[0] + " with" + error_opcode[0])
				for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
					payloadCount(length)
					pattern = createPattern(length)
					payload = unhex(opcode[1][2:]) + unhex(error_opcode[1][2:]) + pattern + unhex(null[1][2:])
					spattern = opcode[1] + opcode[0] + " + " + error_opcode[1] + error_opcode[0] + " + " + pattern + " (Error String)" + " + " + null[1] + null[0]
					sock = createSocketUDP(spattern,length)
					sendDataUDP(sock,payload,spattern,length,1)
		exitProgram(2)
from functions import *
"""SMTP Fuzzer"""
PROPERTY={}
PROPERTY['PROTOCOL']="SMTP"
PROPERTY['NAME']=": SMTP Fuzzer"
PROPERTY['DESC']="Fuzz an SMTP server"
PROPERTY['AUTHOR']='localh0t'

stage_1 = ['HELO','EHLO']
stage_2 = ['MAIL From:']
stage_3 = ['VRFY','EXP','AUTH PLAIN']
stage_4 = ['RCPT To:']
stage_5 = ['SIZE=', 'DATA']
special_stages = ['AUTH LOGIN','AUTH CRAM-MD5','AUTH CRAM-SHA1']

class FuzzerClass:
	def fuzzer(self):
		(username,password) = createUser()
		# Stage 0
		fuzzTCP()
		# Stage 1
		sock = createSocketTCP(0,0)
		fuzzCommands(sock,stage_1,0,"SingleCommand")
		# Stage 2
		sock = createSocketTCP(0,0)
		sendCredential(sock,"HELO","localh0t")
		sendCredential(sock,"AUTH LOGIN","")
		sendDataTCP(sock,base64.b64encode(username),0,0)
		sendDataTCP(sock,base64.b64encode(password),0,0)
		fuzzCommands(sock,stage_2,0,"Email")
		# Stage 3
		sock = createSocketTCP(0,0)
		sendCredential(sock,"HELO","localh0t")
		sendCredential(sock,"AUTH LOGIN","")
		sendDataTCP(sock,base64.b64encode(username),0,0)
		sendDataTCP(sock,base64.b64encode(password),0,0)
		fuzzCommands(sock,stage_3,0,"SingleCommand")
		# Stage 4
		sock = createSocketTCP(0,0)
		sendCredential(sock,"HELO","localh0t")
		sendCredential(sock,"AUTH LOGIN","")
		sendDataTCP(sock,base64.b64encode(username),0,0)
		sendDataTCP(sock,base64.b64encode(password),0,0)
		sendCredential(sock,"MAIL From:","backfuzz@localh0t.com.ar")
		fuzzCommands(sock,stage_4,0,"Email")
		# Stage 5
		sock = createSocketTCP(0,0)
		sendCredential(sock,"EHLO","localh0t")
		sendCredential(sock,"AUTH LOGIN","")
		sendDataTCP(sock,base64.b64encode(username),0,0)
		sendDataTCP(sock,base64.b64encode(password),0,0)
		sendCredential(sock,"MAIL From:","<backfuzz@localh0t.com.ar>")
		sendCredential(sock,"RCPT To:","<null@fuzz.com>")
		fuzzCommands(sock,stage_5,0,"SingleCommand")
		# Special Stages
		for command in special_stages:
			printCommand(command)
			for length in range(globalvars.minim, globalvars.maxm+1 ,globalvars.salt):
			 	pattern = base64.b64encode(createPattern(length))	
			 	payloadCount(length)	
 				sock = createSocketTCP(pattern,length)
 				sendCredential(sock,"EHLO","localh0t")
				sendCredential(sock,command,"")
				if command == 'AUTH LOGIN':
					sendDataTCP(sock,pattern,length,0)
				sendDataTCP(sock,pattern,length,1)
		exitProgram(2)
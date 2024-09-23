from functions import *
"""IMAP Fuzzer"""
PROPERTY={}
PROPERTY['PROTOCOL']="IMAP"
PROPERTY['NAME']=": IMAP Fuzzer"
PROPERTY['DESC']="Fuzz an IMAP server"
PROPERTY['AUTHOR']='localh0t'

user_stage = ['. login']
pass_stage = ['. login anonymous@test.com']
stage_1 = ['. list ""','. lsub ""', '. status INBOX','. examine','. select','. create','. delete', '. rename INBOX','. fetch 1','. store 1 flags', '. copy 1:2','. subscribe','. unsubscribe','. getquotaroot','. getacl']
stage_2 = ['. list', '. status','. rename','. fetch','. store 1','. copy','. lsub']
stage_3 = ['. store']

class FuzzerClass:
	def fuzzer(self):
		(username,password) = createUser()
		# Stage 0
		fuzzTCP()
		# User Stage
		sock = createSocketTCP(0,0)
		fuzzCommands(sock,user_stage,"test","DoubleCommand")
		# Pass Stage
		sock = createSocketTCP(0,0)
		fuzzCommands(sock,pass_stage,0,"SingleCommand")
		# Stage 1
		login = ". login " + str(username)
		sock = createSocketTCP(0,0)
		sendCredential(sock,login,password)
		fuzzCommands(sock,stage_1,0,"SingleCommand")
		# Stage 2
		sock = createSocketTCP(0,0)
		sendCredential(sock,login,password)
		fuzzCommands(sock,stage_2,1,"DoubleCommand")
		# Stage 3
		sock = createSocketTCP(0,0)
		sendCredential(sock,login,password)
		fuzzCommands(sock,stage_3,"+flags NonJunk","DoubleCommand")
		exitProgram(2)
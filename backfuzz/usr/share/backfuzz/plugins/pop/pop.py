from functions import *
"""POP3 Fuzzer"""
PROPERTY={}
PROPERTY['PROTOCOL']="POP3"
PROPERTY['NAME']=": POP3 Fuzzer"
PROPERTY['DESC']="Fuzz an POP3 server"
PROPERTY['AUTHOR']='localh0t'

commands = ['STAT','LIST','RETR','DELE','RSET','TOP','TOP 1','RPOP','RPOP test','APOP','APOP test']

class FuzzerClass:
	def fuzzer(self):
		(username,password) = createUser()
		fuzzTCP()
		fuzzUser("USER")
		fuzzPass(username,"USER","PASS")
		sock = createSocketTCP(0,0)
		sendCredential(sock,"USER",username)
		sendCredential(sock,"PASS",password)
		fuzzCommands(sock,commands,0,"SingleCommand")
		exitProgram(2)




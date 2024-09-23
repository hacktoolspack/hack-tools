from functions import *
"""FTP Fuzzer"""
PROPERTY={}
PROPERTY['PROTOCOL']="FTP"
PROPERTY['NAME']=" : FTP Fuzzer "
PROPERTY['DESC']="Fuzz an FTP server "
PROPERTY['AUTHOR']='localh0t'

commands = ['ABOR','ACCT','ALLO','APPE','AUTH','CWD','CDUP','DELE','FEAT','HELP','HOST','LANG','LIST',
			'MDTM','MKD','MLST','MODE','NLST','NLST -al','NOOP','OPTS','PASV','PORT','PROT','PWD','REIN',
			'REST','RETR','RMD','RNFR','RNTO','SIZE','SITE','SITE CHMOD','SITE CHOWN','SITE EXEC','SITE MSG',
			'SITE PSWD','SITE ZONE','SITE WHO','SMNT','STAT','STOR','STOU','STRU','SYST','TYPE','XCUP',
			'XCRC','XCWD','XMKD','XPWD','XRMD']


class FuzzerClass:
	def fuzzer(self):
		(username,password) = createUser()
		fuzzTCP()
		fuzzUser("USER")
		fuzzPass(username,"USER","PASS")
		sock = createSocketTCP(0,0)
		sendCredential(sock,"USER",username)
		sendCredential(sock,"PASS",password)
		for command in commands:
			printCommand(command)
			for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
				payloadCount(length)
				pattern = createPattern(length)
				pattern = addCommandPattern(command,0,pattern)
				sock = createSocketTCP(pattern,length)
				sendCredential(sock,"USER",username)
				sendCredential(sock,"PASS",password)
				sendDataTCP(sock,pattern,length,1)
		exitProgram(2)
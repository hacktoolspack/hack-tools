from functions import *
"""HTTP Fuzzer"""
PROPERTY={}
PROPERTY['PROTOCOL']="HTTP"
PROPERTY['NAME']=": HTTP Fuzzer"
PROPERTY['DESC']="Fuzz an HTTP server"
PROPERTY['AUTHOR']='localh0t'

commands = ['GET' , 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE', 'TRACE', 'CONNECT']

headers = [
			'User-Agent:',
			'Accept:',
			'Accept-Language:',
			'Accept-Encoding:',
			'Connection:',
			'Referer:',
			'Cookie:',
			'Cache-Control:',
			'X-Forwared-For:',
			'Content-Type:',
			'Content-Length:',
			'If-Modified-Since:',
]

class FuzzerClass:
	def fuzzer(self):
		# VHOST define
		try:
			vhost = raw_input("[!] VHOST you want to use in fuzzer request's (Host:) (default fuzzingh0t.com)> ")
		except KeyboardInterrupt:
			exitProgram(6)
		if vhost == '':
			vhost = "fuzzingh0t.com"
		else:
			pass
		# Stage 0
		fuzzTCP()
		# Commands Stage
		for command in commands:
			printCommand(command)
			for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
				payloadCount(length)
				pattern = createPattern(length)
				pattern = addDoubleCommandNoSpace(command + " /","HTTP/1.0 \r\n",pattern)
				sock = createSocketTCP(pattern,length)
				sendDataTCP(sock,pattern,length,1)
		# Host Stage
		for command in commands:
			printCommand(command + " => Host: stage")
			for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
					payloadCount(length)
					pattern = createPattern(length)
					pattern = addCommandPattern("Host:",0,pattern + "\r\n")
					sock = createSocketTCP(pattern,length)
					sendCredential(sock,command + " /","HTTP/1.1")
					sendDataTCP(sock,pattern,length,1)
		# Headers Stage
		for command in commands:
			printCommand(command + " => headers stage")
			for header in headers:
				printCommand(command + " with " + header)
				for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
					payloadCount(length)
					pattern = createPattern(length)
					pattern = addCommandPattern(header,0,pattern + "\r\n")
					sock = createSocketTCP(pattern,length)
					sendCredential(sock,command + " /","HTTP/1.1")
					sendCredential(sock,"Host:",vhost)
					sendDataTCP(sock,pattern,length,1)
		# Data Stage
		for command in commands:
			printCommand(command + " => DATA stage")
			for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
				payloadCount(length)
				pattern = createPattern(length) + "\r\n"
				sock = createSocketTCP(pattern,length)
				sendCredential(sock,command + " /","HTTP/1.1")
				sendCredential(sock,"Host:",vhost)
				sendCredential(sock,"Content-Length:",str((len(pattern) -2)) + "\n")
				sendDataTCP(sock,pattern,length,1)
		exitProgram(2)
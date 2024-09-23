import sys,socket,select,time,errno,base64,random,globalvars

#################################################################################################################################

# Write "pattern" to "file"

def fileWrite(file,pattern):
	try:
		fileHandle = open(file, 'w')
		fileHandle.write(pattern)
		fileHandle.close()
	except:
		print "\n[-] Invalid directory or directory doesn't exist"
		exitProgram(4)

# ----------------------------------------------------------------------------------------------------------------------------- #

# Prints "message" and do keyboard input unless Ctrl-C

def fileInput(message):
	print message + "\n"
	user_input = ''
	try:
		while(1):
			user_input = user_input + raw_input()
			user_input = user_input + "\n"
	except KeyboardInterrupt:
			return user_input

###################################################################################################################################

# Creates a payload with ("user" + PAYLOAD) and sends the data to a TCP socket, iterating with the given minim, maxm & salt params

def fuzzUser(user):
	printCommand(user)
	for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
		payloadCount(length)			
		pattern = createPattern(length)
		pattern = addCommandPattern(user,0,pattern) 
		sock = createSocketTCP(pattern,length)
		sendDataTCP(sock,pattern,length,1)

# ----------------------------------------------------------------------------------------------------------------------------- #

# First, sends ("user" + "username") as an authentication pattern. Then creates a payload with ("passwd" + PAYLOAD) and sends 
# the data to the same TCP socket, iterating with the given minim, maxm & salt params

def fuzzPass(username,user,passwd):
	printCommand(passwd)
	for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
		payloadCount(length)
		pattern = createPattern(length)
		pattern = addCommandPattern(passwd,0,pattern)
		sock = createSocketTCP(pattern,length)
		sendCredential(sock,user,username)
		sendDataTCP(sock,pattern,length,1)

#################################################################################################################################

# Simply it create and fuzz a TCP socket, iterating with the given minim, maxm & salt params

def fuzzTCP():
		printCommand("TCP Socket")
		for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
			payloadCount(length)			
			pattern = createPattern(length)
			sock = createSocketTCP(pattern,length)
			sendDataTCP(sock,pattern,length,1)

# ----------------------------------------------------------------------------------------------------------------------------- #

# Simply it create and fuzz a UDP socket, iterating with the given minim, maxm & salt params

def fuzzUDP():
		printCommand("UDP Socket")
		for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
			payloadCount(length)			
			pattern = createPattern(length)
			sock = createSocketUDP(pattern,length)
			sendDataUDP(sock,pattern,pattern,length,1)

#################################################################################################################################

# Some different kinda of fusion-pattern's functions, pretty intuitive

def addCommandPattern(command,endcommand,pattern):
    return (str(command) + " " + str(pattern))

def addCommandNoSpace(command,endcommand,pattern):
    return (str(command) + str(pattern))

def addCommandPatternEmail(command,endcommand,pattern):
    return (str(command) + " " + "backfuzz@" + str(pattern) + ".com")
 
def addDoubleCommand(command,endcommand,pattern):
    return (str(command) + " " + str(pattern) + " " + str(endcommand))

def addDoubleCommandNoSpace(command,endcommand,pattern):
    return (str(command) + str(pattern) + " " + str(endcommand))

# ----------------------------------------------------------------------------------------------------------------------------- #

# It uses a given alive TCP socket "sock", a given list of "commands" (like ['STAT','LIST', etc]), an optional ending "endcommand"
# (to use like COMMAND + PATTERN + ENDCOMMAND), and a "type" ("SingleCommand", "Email", "DoubleCommand"  etc.).
# The main idea of this function is to expand the command's posible combination's, and use a proper one while fuzzing a particular
# combination. It iterate's with the given minim, maxm & salt params

def fuzzCommands(sock,commands,endcommand,type):
	for i in range(0,len(commands)):
		printCommand(commands[i])
		for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
			payloadCount(length)
			pattern = createPattern(length)
			Switch = { 
			"SingleCommand":addCommandPattern,
			"SingleCommandNoSpace":addCommandNoSpace,
			"Email":addCommandPatternEmail,
			"DoubleCommand":addDoubleCommand,
			"DoubleCommandNoSpace":addDoubleCommandNoSpace 
			}
 			pattern = Switch[type](commands[i],endcommand,pattern)
			if i == (len(commands) - 1) and (length+globalvars.salt) > globalvars.maxm:
				sendDataTCP(sock,pattern,length,1)
			else:
				sendDataTCP(sock,pattern,length,0)


#################################################################################################################################

# Create's a new TCP socket and returns it. If it's not possible to create the socket, something has happened, do some checks and
# return the propper payload with the showPayload() function, given "pattern" and "length" for that

def createSocketTCP(pattern,length):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(globalvars.timeout)
		sock.connect((globalvars.host, globalvars.port))
		return sock
	except KeyboardInterrupt:
		exitProgram(6)
	except socket.error, err:
		error = err[0]
		if error == errno.ECONNREFUSED:
			print "[!] We got a connection refused, the service almost certainly crashed"
			showPayload(pattern,length)
	except:
		print "[!] Another socket error, the service almost certainly crashed"
		showPayload(pattern,length)

# ----------------------------------------------------------------------------------------------------------------------------- #

# It uses a given alive TCP socket "sock", and send's the pattern "pattern" to the same socket. If it's not possible to send
# the data through the socket, something has happened, do some checks and return the propper payload with the showPayload() 
# function, given "pattern" and "length" for that. Optionally you can specify to close the socket after sending the data or not.

def sendDataTCP(sock,pattern,length,close):
	try:
		time.sleep(globalvars.timeout)
		sock.settimeout(globalvars.timeout)
		pattern = pattern + "\r\n"
		sock.send(pattern)
		sock.recv(4096)
		if close == 1:
			sock.close()
		else:
			pass
	except KeyboardInterrupt:
		exitProgram(6)
	except socket.error, err:
		error = err[0]
		if error == errno.EPIPE:
			print "\n[!] We got a broken pipe, that is a *possible* crash. Checking if it really crashed ..."
			check_conn = createSocketTCP(pattern,length)
			print "[!] The service has not really crashed, continuing fuzzing ...\n"
		if error == errno.ECONNREFUSED:
			print "\n[!] We got a connection refused, the service almost certainly crashed"
			showPayload(pattern,length)
	except:
		print "[!] Another socket error, the service almost certainly crashed"
		showPayload(pattern,length)

#################################################################################################################################

# Create's a new UDP socket and returns it. If it's not possible to create the socket, something has happened, do some checks and
# return the propper payload with the showPayload() function, given "pattern" and "length" for that (yes, I know that UDP is
# definitely not real "connection" oriented, but only for convention)

def createSocketUDP(pattern,length):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.settimeout(globalvars.timeout)
		sock.connect((globalvars.host, globalvars.port))
		return sock
	except KeyboardInterrupt:
		exitProgram(6)
	except socket.error, err:
		error = err[0]
		if error == errno.ECONNREFUSED:
			print "\n[!] We got a connection refused, the service almost certainly crashed"
			showPayload(pattern,length)
	except:
		print "[!] Another socket error, the service almost certainly crashed"
		showPayload(pattern,length)

# ----------------------------------------------------------------------------------------------------------------------------- #

# It uses a given UDP socket "sock", and send's the pattern "pattern" to the same socket. If it's not possible to send
# the data through the socket, something has happened, do some checks and return the propper payload with the showPayload() 
# function, given "pattern" and "length" for that. Optionally you can specify to close the socket after sending the data or not.

def sendDataUDP(sock,pattern,spattern,length,close):
	try:
		time.sleep(globalvars.timeout)
		sock.settimeout(globalvars.timeout)
		sock.send(pattern)
		sock.recv(4096)
		if close == 1:
			sock.close()
		else:
			pass
	except KeyboardInterrupt:
		exitProgram(6)
	except socket.error, err:
		error = err[0]
		if error == errno.ECONNREFUSED:
			print "\n[!] We got a connection refused, the service almost certainly crashed"
			showPayload(spattern,length)
	except:
		print "[!] Another socket error, the service almost certainly crashed"
		showPayload(spattern,length)

#################################################################################################################################

# Send's a "command" + "login" data to a given alive socket, for login purposes.

def sendCredential(sock,command,login):
	try:
		data = str(command) + " " + str(login) + "\r\n"
		sock.send(data)
	except:
		exitProgram(5)

# ----------------------------------------------------------------------------------------------------------------------------- #

# If not "username" / "password" given, use a default one

def checkDefaultUser(username,password):
	if username == '':
		username = "anonymous"
	if password == '':
		password = "anonymous@test.com"
	else:
		pass
	return username,password

# ----------------------------------------------------------------------------------------------------------------------------- #

# Specify a new "username" / "password" combination.

def createUser():
	try:
		username = raw_input("[!] Insert username (default: anonymous)> ")
		password = raw_input("[!] Insert password (default: anonymous@test.com)> ")
	except KeyboardInterrupt:
		exitProgram(6)
	return checkDefaultUser(username,password)

#################################################################################################################################

# Show payload details, with the correct "pattern" and "length"

def showPayload(pattern,length):
	print "\n#####################################################################################################################################"
	print "\nPayload details:\n================\n"
	print "Host: " + globalvars.host
	print "Port: " + str(globalvars.port)
	print "Type: " + globalvars.plugin_use
	print "Connection refused at: " + str(length)
	if globalvars.show_pattern:
		print "\nPayload:\n========\n"
		print pattern
	print "\n#####################################################################################################################################"
	exitProgram(4)

# ----------------------------------------------------------------------------------------------------------------------------- #

def printCommand(command):
	print "\n[!] " + str(command) + " fuzzing ...\n"

# ----------------------------------------------------------------------------------------------------------------------------- #

def payloadCount(pos):
	print "MIN: " + str(globalvars.minim) + " MAX: " + str(globalvars.maxm) + " Giving it with: " + str(pos)

# ----------------------------------------------------------------------------------------------------------------------------- #

# Exit code's

def exitProgram(code):
	if code==1:
		sys.exit("\n[!] Exiting help ...")
	if code==2:
		sys.exit("\n[!] End of fuzzing, exiting ...")
	if code==3:
		sys.exit("\n[-] Check your arguments, exiting with errors ...")
	if code==4:
		sys.exit("\n[!] Exiting ...")
	if code==5:
		sys.exit("\n[-] Error sending credentials, exiting ...")
	if code==6:
		sys.exit("\n[!] Keyboard Interrupt, exiting ...")

#################################################################################################################################

# Colors for terminal
class colors:
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	RED = '\033[91m'
	ENDC = '\033[0m'

# ----------------------------------------------------------------------------------------------------------------------------- #

# Convert a str variable "convert" to int

def strToInt(convert,typeParam):
	try:
		value = int(convert)
		return value
	except:
		print "Number given in " + typeParam + " is invalid"
		exitProgram(3)

# ----------------------------------------------------------------------------------------------------------------------------- #

# Convert a str variable "convert" to float

def strToFloat(convert,typeParam):
	try:
		value = float(convert)
		return value
	except:
		print "Number given in " + typeParam + " is invalid"
		exitProgram(3)

# ----------------------------------------------------------------------------------------------------------------------------- #

def checkMinMax(min,max):
	if min >= max:
		print "\n[-] MIN >= MAX"
		exitProgram(3)

# ----------------------------------------------------------------------------------------------------------------------------- #

# Some check's for invalid pattern's-flavour's

def checkFlavour(flavour):
	flavour_list = ["Cyclic", "CyclicExtended", "Single", "FormatString"]
	if flavour not in flavour_list:
		print "\n[-] Pattern-Flavour " + str(flavour) + " doesn't exist, check help"
		exitProgram(3)

#################################################################################################################################

# Create's a single pattern, with the given "size"
def createPatternSingle(size):
	return "A" * size

# ----------------------------------------------------------------------------------------------------------------------------- #

# Create's a format-string-like pattern, with the given "size"

def createPatternFormat(size):
	pattern = ''
	for cont in range(1,size+1):
		pattern += "%" + random.choice('snx')
	return pattern

# ----------------------------------------------------------------------------------------------------------------------------- #

# Taken from mona.py / http://redmine.corelan.be/projects/mona , Copyright (c) 2011, Corelan GCV
# Create's a cyclic pattern, with the given "size"

def createPatternCyclic(size):
	
	char1="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	char2="abcdefghijklmnopqrstuvwxyz"
	char3="0123456789"

	if globalvars.pattern_flavour == "CyclicExtended":
		char3 += ",.;+=-_!&()#@'({})[]%"	# ascii, 'filename' friendly
	
	charcnt=0
	pattern=""
	max=int(size)
	while charcnt < max:
		for ch1 in char1:
			for ch2 in char2:
				for ch3 in char3:
					if charcnt<max:
						pattern=pattern+ch1
						charcnt=charcnt+1
					if charcnt<max:
						pattern=pattern+ch2
						charcnt=charcnt+1
					if charcnt<max:
						pattern=pattern+ch3
						charcnt=charcnt+1
	return pattern

# ----------------------------------------------------------------------------------------------------------------------------- #

# Switch between the different pattern's

def createPattern(size):
	
	Switch = { 
			"Cyclic":createPatternCyclic,
			"CyclicExtended":createPatternCyclic,
			"Single":createPatternSingle,
			"FormatString":createPatternFormat,
			}
	
	pattern = Switch[globalvars.pattern_flavour](size)
	return pattern

#################################################################################################################################

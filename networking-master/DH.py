import socket, json, threading
import SocketServer as socketserver
from random import randint

def is_prime(number):
	if 0 <= number <= 2:
		return False
	primes = []
	for i in range(number + 1):
		primes.append(True)
	primes[0] = False
	primes[1] = False
	for i in range(number + 1):
		if primes[i] is True:
			j = 2 * i
			while j <= number:
				primes[j] = False
				j += i
	return primes[number] is True

def rand_prime(size):
	prime = 1
	while not is_prime(prime):
		prime = randint(0,size)
	return prime

def multinv(modulus, value):
	x, lastx = 0, 1
	a, b = modulus, value
	while b:
		a, q, b = b, a // b, a % b
		x, lastx = lastx - q * x, x
	result = (1 - lastx * modulus) // value
	if result < 0:
		result += modulus
	assert 0 <= result < modulus and value * result % modulus == 1
	return result

class DH:
	def __init__(self):
		self.privatePrime = rand_prime(2000)
		self.sharedPrime = rand_prime(2000)
		self.base = rand_prime(2000)
		self.key = int()
	def calcPublicSecret(self):
		return (self.base ** self.privatePrime) % self.sharedPrime
	def calcSharedSecret(self, privSecret):
		self.key = (privSecret ** self.privatePrime) % self.sharedPrime

class ServerSocket(socketserver.BaseRequestHandler):
	def initDiffieHellman(self):
		if self.request.recv(1024).decode() != "connected":
			print("Error while connecting")
		publicSecret = self.__dh.calcPublicSecret()
		step1 = "{"
		step1 += "\"dh-keyexchange\":"
		step1 += "{"
		step1 += "\"step\": {},".format(1)
		step1 += "\"base\": {},".format(self.__dh.base)
		step1 += "\"prime\": {},".format(self.__dh.sharedPrime)
		step1 += "\"publicSecret\": {}".format(publicSecret)
		step1 += "}}"
		self.request.send(step1.encode())
		step2 = self.request.recv(1024)
		if self.__debugflag:
			print(step2)
		jsonData = json.loads(step2.decode())
		jsonData = jsonData["dh-keyexchange"]
		publicSecret = int(jsonData["publicSecret"])
		self.__dh.calcSharedSecret(publicSecret)

	def handle(self):
		self.__debugflag = self.server.conn
		self.__dh = DH()
		self.initDiffieHellman()
		globals()["h_"+self.client_address[0].replace(".","")] = str(self.__dh.key)

def start_server(debugflag=False):
	try:
		server = socketserver.ThreadingTCPServer(("", 50000), ServerSocket)
		server.conn = debugflag
		print "[DAEMON] Hellman Server Started"
		server.serve_forever()
	except:
		pass

class ClientSocket:
	def __init__(self, debugflag=False):
		self.__dh = DH()
		self.__debugflag = debugflag
	def initDiffieHellman(self, socket):
		socket.send("connected".encode())
		step1 = socket.recv(5000)
		if self.__debugflag:
			print(step1)
		jsonData = json.loads(step1.decode())
		jsonData = jsonData["dh-keyexchange"]
		self.__dh.base = int(jsonData["base"])
		self.__dh.sharedPrime = int(jsonData["prime"])
		publicSecret = int(jsonData["publicSecret"])
		calcedPubSecret = str(self.__dh.calcPublicSecret())
		step2 = "{"
		step2 += "\"dh-keyexchange\":"
		step2 += "{"
		step2 += "\"step\": {},".format(2)
		step2 += "\"publicSecret\": {}".format(calcedPubSecret)
		step2 += "}}"
		socket.send(step2.encode())
		self.__dh.calcSharedSecret(publicSecret)

	def start_client(self, ip):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((ip, 50000));
			self.initDiffieHellman(sock)
		finally:
			sock.close()
			globals()["h_"+ip.replace(".","")] = str(self.__dh.key)

def hellman():
	try:
		daemon = threading.Thread(target=start_server)
		daemon.daemon = True
		daemon.name = "hellman_server"
		daemon.start()
	except:
		pass

def client(serv):
	try:
		client = ClientSocket()
		client.start_client(serv)
	except:
		pass

def hellman_client(target):
	try:
		daemon = threading.Thread(target=client,args=(target,))
		daemon.daemon = True
		daemon.start()
	except:
		pass

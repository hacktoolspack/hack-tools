from binascii import hexlify
import os, socket, sys, threading, traceback, SocketServer, logging, paramiko, time, argparse
from Crypto.PublicKey import RSA
from paramiko.py3compat import b, u

parser = argparse.ArgumentParser(description='Create A Honeypot For Hackers')
parser.add_argument('-r', "--random", help='Create new keypairs constantly',action="store_true")
args = parser.parse_args()
ran = args.random

def new_key():
	key = RSA.generate(2048)
	with open("rsa.key", 'w') as content_file:
		os.chmod("rsa.key", 0600)
		content_file.write(key.exportKey('PEM'))
	pubkey = key.publickey()
	with open("pub.key", 'w') as content_file:
		content_file.write(pubkey.exportKey('OpenSSH'))

if ran:
	new_key()

try:
	import console
	console.set_color(1,1,0)
	console.set_font("Menlo",10)
	print """
	   __ __                             __ 
	  / // /__  ___  ___ __ _____  ___  / /_
	 / _  / _ \/ _ \/ -_) // / _ \/ _ \/ __/
	/_//_/\___/_//_/\__/\_, / .__/\___/\__/ 
	                   /___/_/ """
	console.set_color()
	console.set_font()
except:
	print """
	   __ __                             __ 
	  / // /__  ___  ___ __ _____  ___  / /_
	 / _  / _ \/ _ \/ -_) // / _ \/ _ \/ __/
	/_//_/\___/_//_/\__/\_, / .__/\___/\__/ 
	                   /___/_/ """       

PORT = 2222
LOG_FILE = "Honeypot.log"
msg1 = "\t[1;90;43m-=-=- Honeypot v1.3.3 -=-=-\r\n"
DENY_ALL = False
PASSWORDS = [
"root",
"password",
"test"
]

def deepscan(target,f=None):
	data = str(socket.gethostbyaddr(target))
	data = data.replace(",","").replace("[","").replace("]","").replace("(","").replace(")","").replace("'","")
	data = data.split()
	d1 = "-Name: "+data[0]
	d2 = "-FQDN: "+data[1]
	d3 = "-Provider: "+data[2]
	print d1
	print d2
	print d3
	print ""
	f.write("-"+target+"\n")
	f.write(d1+"\n")
	f.write(d2+"\n")
	f.write(d3+"\n\n")

def deepscan2(target,chan):
	data = str(socket.gethostbyaddr(target))
	data = data.replace(",","").replace("[","").replace("]","").replace("(","").replace(")","").replace("'","")
	data = data.split()
	d1 = "-Name: "+data[0]
	d2 = "-FQDN: "+data[1]
	d3 = "-Provider: "+data[2]
	chan.send("   "+d1+"\r\n")
	chan.send("   "+d2+"\r\n")
	chan.send("   "+d3+"\r\n")

logger = logging.getLogger("access.log")
logger.setLevel(logging.INFO)
lh = logging.FileHandler(LOG_FILE)
logger.addHandler(lh)

host_key = paramiko.RSAKey(filename="rsa.key")

print "\nKey: " + u(hexlify(host_key.get_fingerprint()))
print ""

class Server(paramiko.ServerInterface):
	def __init__(self, client_address):
		self.event = threading.Event()
		self.client_address = client_address
	
	def check_channel_request(self, kind, chanid):
		if kind == "session":
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
	
	def check_auth_password(self, username, password):
		logger.info("-=-=- %s -=-=-\nUser: %s\nPassword: %s\n" % (self.client_address[0], username, password))
		
		print " IP: %s\n User: %s\n Pass: %s\n" % (self.client_address[0], username, password)
			
		if DENY_ALL == True:
			return paramiko.AUTH_FAILED
		f = open("blocked.dat","r")
		data = str(f.readlines()).find(self.client_address[0])
		if data > 1:
			if ran:
				new_key()
			return paramiko.PasswordRequiredException
		else:
			f = open("blocked.dat","a")
			deepscan(self.client_address[0],f)
		paramiko.OPEN_FAILED_CONNECT_FAILED
		if (username == "root") and (password in PASSWORDS):
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED
	
	def check_channel_shell_request(self, channel):
		self.event.set()
		return True
	
	def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
		return True

class SSHHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		try:
			t = paramiko.Transport(self.connection)
			t.add_server_key(host_key)
			server2 = Server(self.client_address)
			try:
				t.start_server(server=server2)
			except paramiko.SSHException:
				print "*** SSH Failed"
			except KeyboardInterrupt:
				pass
			except:
				pass
			
			chan = t.accept(20)
			if chan is None:
				t.close()
				return
			server2.event.wait(10)
			if not server2.event.is_set():
				t.close()
				return
			
			chan.send(msg1)
			for i in range(101):
				chan.send("\r\t     Loading "+str(i)+" of 100    ")
				time.sleep(0.001)
			chan.send("\r\n\r\n   Congrats All Cerious Hackers!\r\n   You have all walked into a Honeypot!\r\n   You will now be blocked from joining \r\n   this server and your IP address\r\n   information has been reported into the\r\n   following report:\r\n\r\n")
			deepscan2(self.client_address[0],chan)
			
			chan.send("\r\n\r\n\r\n\tNow GTFO my Honeypot")
			chan.close()
			
		except Exception as e:
			print("*** Caught exception: " + str(e.__class__) + ': ' + str(e))
			traceback.print_exc()
		finally:
			try:
				t.close()
			except:
				pass

sshserver = SocketServer.ThreadingTCPServer(("192.168.1.68", PORT), SSHHandler)
sshserver.serve_forever()

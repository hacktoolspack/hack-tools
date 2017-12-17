from binascii import hexlify
import os, socket, sys, threading, traceback, SocketServer, logging, paramiko, time, argparse, random
from time import gmtime, strftime
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
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8",80))
	hostip = s.getsockname()[0]
except:
	hostip = "127.0.0.1"
LOG_FILE = "Honeypot.log"
DENY_ALL = False

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
		f = open("blocked.dat").read()
		if self.client_address[0] in f:
			if ran:
				new_key()
			return paramiko.OPEN_FAILED_UNKNOWN_CHANNEL_TYPE
		else:
			f = open("blocked.dat","a")
			deepscan(self.client_address[0],f)
		paramiko.OPEN_FAILED_CONNECT_FAILED
		if (username == "root"):
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
			
			authid = "root",hostip
			ip = self.client_address[0]
			user = "%s@%s ~$ " % (authid[0], ip)
			
			fh = """
			         ___           ___              
			        /\__\         /\  \             
			       /:/ _/_        \:\  \            
			      /:/ /\__\        \:\  \           
			     /:/ /:/  /    ___ /::\  \          
			    /:/_/:/  /    /\  /:/\:\__\         
			    \:\/:/  /     \:\/:/  \/__/         
			     \::/__/       \::/__/              
			      \:\  \        \:\  \              
			       \:\__\        \:\__\             
			        \/__/unny     \/__/oney\r\n
			""".replace("\n","\r\n")
			chan.send(fh)
			
			def keyspeed(calm=False):
				if calm:
					time.sleep(random.choice([0.10,0.07,0.08,0.09,0.6]))
				else:
					time.sleep(random.choice([0.14,0.07,0.06,0.09]))
			
			def cmdline(msg,chill=False):
				for _ in msg:
					if _ == ".":
						time.sleep(0.13)
					if _ == " ":
						pass
					if _ == "!":
						pass
					else:
						keyspeed(chill)
					chan.send(_)
					if _ == "!":
						time.sleep(1)

			chan.send(user)
			time.sleep(2)
			ctime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
			for _ in "sudo rootload.sh\r\n":
				chan.send(_)
				keyspeed()
			time.sleep(0.7)
			chan.send("Loading")
			for i in "... ":
				chan.send(i)
				time.sleep(0.4)
			time.sleep(1)
			chan.send("%s Rooted!\r\n" % authid[1])
			keyspeed()
			chan.send("Accepting Reverse Shell from %s" %ip)
			user = "root@localhost ~$ "
			for i in "... ":
				chan.send(i)
				time.sleep(0.4)
			chan.send("\r\n")
			time.sleep(1)
			chan.send(user)
			time.sleep(2)
			cmdline("echo Hello! A reverse shell has been installed on your terminal!\r\n",True)
			chan.send("Hello! A reverse shell has been installed on your terminal!\r\n")
			time.sleep(0.1)
			chan.send(user)
			time.sleep(1)
			cmdline("echo Your root password is also compromised!\r\n",True)
			time.sleep(0.2)
			chan.send("Your root password is also compromised!\r\n")
			chan.send(user)
			time.sleep(1)
			cmdline("echo \"You got owned!\"\r\n")
			time.sleep(0.2)
			chan.send("\"You got owned!\"\r\n")
			chan.send(user)
			time.sleep(2)
			cmdline("ls -al")
			time.sleep(0.5)
			months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
			if int(ctime.split()[0][5:].split("-")[0]) <= 9:
				month = ctime[5:].split()[0][:5].split("-")[0][1:]
			else:
				month = ctime.split()[0][5:].split("-")[0]
			month = months[int(month)-1] + " " +ctime[5:].split()[1][:5]
			chan.send("\r\n-rw-r----- root root    289372 %s rootload.sh\r\n" %month)
			chan.send("-rw-r--rx- root root      1281 %s hacked.md\r\n" %month)
			chan.send("drw-r--rx- root root   2721281 Nov 11:34 notporn\r\n")
			chan.send("-rw-r---r- root root     63782 Oct  9:53 doggo.jpg\r\n")
			chan.send(user)
			time.sleep(3)
			cmdline("echo ummm...\r\n",True)
			time.sleep(0.13)
			chan.send("ummm...\r\n")
			chan.send(user)
			time.sleep(1)
			cmdline("rm ./notporn\r\n")
			chan.send("Are you sure you want to remove './notporn'? y/n ")
			time.sleep(0.2)
			cmdline("y\r\n")
			chan.send(user)
			cmdline("rm ./rootload.sh\r\n")
			chan.send("Are you sure you want to remove './rootload.sh'? y/n ")
			time.sleep(0.2)
			cmdline("y\r\n")
			chan.send(user)
			cmdline("ls -al",True)
			chan.send("\r\n-rw-r--rx- root root      1281 %s hacked.md\r\n" %month)
			chan.send("-rw-r---r- root root     63782 Oct  9:53 doggo.jpg\r\n")
			chan.send(user)
			time.sleep(2)
			cmdline("echo gtfo!\r\n")
			chan.send("gtfo!\r\n")
			deepscan2(self.client_address[0],chan)
			chan.close()
			
		except Exception as e:
			print("*** Caught exception: " + str(e.__class__) + ': ' + str(e))
		finally:
			try:
				t.close()
			except:
				pass

sshserver = SocketServer.ThreadingTCPServer((hostip, PORT), SSHHandler)
sshserver.serve_forever()

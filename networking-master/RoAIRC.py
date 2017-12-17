import sys, time, threading, RoA, string, random, socket
from random import randint
from binascii import hexlify
import DH

Ro = RoA.RoA(False)
port = 50000
key = "savsecro"*4
user = "[%s] " %raw_input("Username: ")
 
try:
	socket.setdefaulttimeout(2)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("8.8.8.8", 53))
	ip = sock.getsockname()[0]
	sock.close()
except Exception as e:
	ip = "127.0.0.1"
socket.setdefaulttimeout(1000)

def header(b="",c=""):
	head = ip,b,c
	return str(head) + "\x0f"

def encrypt(msg,key):
	roa_out = Ro.encrypt(msg,key)
	return str(roa_out)
	
def decrypt(roa_in):
	try:
		roa_in = eval(roa_in)
		decrypted = Ro.decrypt(roa_in[0],roa_in[1],roa_in[2])
		return decrypted
	except Exception as e:
		pass

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def encryption_handler(packet,key):
	p = packet.replace(key,"!!!key!!!")
	p = p.replace(key[16:],"!!!sub!!!")
	return p

def daemon_hound():
	while 1:
		data = s.recv(5000)
		if eval(data.split("\x0f")[0])[1] == "direct" and ip in data:
			try:
				DH.hellman_client(eval(data.split("\x0f")[0])[2])
				v = "h_"+eval(data.split("\x0f")[0])[0].replace(".","")
				time.sleep(1)
				exec "globals()['%s'] = DH.%s" % (v,v)
				while 1:
					globals()[v] = int(globals()[v])*32+6**2
					if len(str(globals()[v])) >= 32:
						break
				globals()[v] = str(globals()[v])[:32]
			except:
				pass
			globals()["stop"] = True
		
		elif eval(data.split("\x0f")[0])[2] == "dm" and eval(data.split("\x0f")[0])[1] == ip:
			print
			print decrypt(data.replace("!!!key!!!",globals()[v]).replace("!!!sub!!!",globals()[v][16:]).split("\x0f")[1])
		
		else:
			data = data.split("\x0f")
			d = decrypt(data[1])
			if d != None:
				print "\n"+d

daemon = threading.Thread(target=daemon_hound)
daemon.daemon = True
daemon.start()
print "[DAEMON] SNIFFING"
time.sleep(0.5)
DH.hellman()
time.sleep(0.5)
stop = False

while 1:
	try:
		msg = raw_input("\n=> ")
	except:
		break
	if len(msg) == 0:
		msg = "0"
	data = header() + encrypt(user+msg,key)
	d_host = raw_input("HOST => ")
	direct = header("direct",d_host)
	if len(d_host) > 7:
		data = direct
	if len(msg) > 0:
		s.sendto(data, ("255.255.255.255", port))
	if len(d_host) > 7:
		while not stop:
			time.sleep(0.5)
	if len(d_host) > 7:
		v = str("h_"+d_host.replace(".",""))
		exec "globals()['%s'] = DH.%s" % (v,v)
		while 1:
			globals()[v] = int(globals()[v])*32+6**2
			if len(str(globals()[v])) >= 32:
				break
		globals()[v] = str(globals()[v])[:32]
		msg = raw_input("[%s] => " %d_host)
		pack = encrypt("[Direct]" + user+msg,globals()[v])
		pack = encryption_handler(pack,globals()[v])
		s.sendto(header(d_host,"dm")+pack,("255.255.255.255", port))
	time.sleep(1)
	stop = False

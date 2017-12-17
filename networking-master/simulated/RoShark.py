import sys, random, time, string, socket, console
console.set_font("Menlo",20)
console.set_color(0,0,1)
sys.stdout.write("\n\t\t\tWire")
console.set_color(1,1,1)
sys.stdout.write("|\\")
console.set_color(0,0,1)
sys.stdout.write("Shark\n")
console.set_color()
console.set_font()
time.sleep(3)
console.set_font("Menlo",int(sys.argv[1]))
hx = "0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","0","0","0","F","F"
def nodes(am=14):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	except:
		ip = random.choice("192.168.1.0","10.0.0.0")
	ip = ip.split(".")
	ip[3] = ""
	ips = []
	for i in range(am):
		nip = ".".join(ip[:4]) + str(random.choice(range(100)))
		ips.append(nip)
	return ips

def dst(am=14):
	ips = []
	for i in range(am):
		nip = str(random.choice(range(22,194))) + "." + str(random.choice(range(22,194))) + "." + str(random.choice(range(22,194))) + "." + str(random.choice(range(22,194)))
		ips.append(nip)
	ips.append("www.google.com")
	return ips

def newmac():
	mac = ""
	for i in range(12):
		mac = mac + random.choice(hx)
		if str(i) in "1.3.5.7.9".split("."):
			mac = mac + ":"
	return mac

def signal():
	types = "TCP","DNS","ARP","HTTP","UDP"
	types = random.choice(types)
	if types == "TCP":
		sig = "62216 > http "
		if random.choice([0,1]) == 1:
			sig = "http > 62216 "
		sig = types + " " + sig + random.choice(["FIN ","ACK ","SYN "]) + "Seq=" + random.choice(["0 ","1 "]) + "Win=" + str(random.choice(range(100,1000))) + " Len=0"
		if "ACK" in sig:
			sig = sig + " Ack=" + str(random.choice(range(10,1000)))
		if "SYN" in sig:
			sig = sig + " MSS=" + str(random.choice(range(100,1000)))
		return sig
	if types == "DNS":
		sig = "DNS Started Query "
		if random.choice([0,1]) == 1:
			sig = sig + "Response CNAME " + str(random.choice(dst())) + " A " + str(random.choice(dst()))
		else:
			sig = sig + "A " + str(random.choice(dst()))
		return sig
	if types == "ARP":
		sig = "ARP " + random.choice(dst()) + " is at " + newmac()
		return sig
	if types == "HTTP":
		sig = "GET / HTTP/1.1 Host: " + random.choice(dst()) + ":" + random.choice(["80","443","8080"])
		if random.choice([0,1]) == 1:
			sig = "POST / HTTP/ Host: " + random.choice(dst()) + ":" + str(random.choice([80,443,8080]))
		return sig
	if types == "UDP":
		sig = "UDP Source Port: " + str(random.choice(range(10000,50000))) + " Destination Port: " + str(random.choice(range(22,2222)))
		return sig

def rocap():
	no = 0
	start = time.time()
	print " No | Src          | Dst        | Sec | Info "
	time.sleep(random.choice(range(1,6)))
	while 1:
		no = no + 1
		ip = random.choice(nodes())
		sig = signal()
		elapsed = time.time() - start
		stamp = "Time: %s" % (elapsed)
		print " ",str(no),"",ip,">",random.choice(dst()),str(elapsed)[:4]+"s","-",sig
		if no < 5:
			time.sleep(0.4)
		if no > 5 and no < 10:
			time.sleep(0.05)
		else:
			time.sleep(0.09)
		if no > 35:
			no = 0

try:
	rocap()
except:
	console.set_font()
	pass

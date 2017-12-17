import cb, time, struct, sys, random, string

try:
	import console
	console.set_color(0.0,0.2,1)
	print """
  _____       _     _____ _         
 |     |___ _| |___| __  | |_ _ ___ 
 |   --| . | . | -_| __ -| | | | -_|
 |_____|___|___|___|_____|_|___|___|
                    _____ 
             _   __/ ___/ 
            | | / / __ \ 
            | |/ / /_/ / 
            |___/\____/ 

	"""
	console.set_color()
	console.set_font()
except:
	print """
  _____       _     _____ _         
 |     |___ _| |___| __  | |_ _ ___ 
 |   --| . | . | -_| __ -| | | | -_|
 |_____|___|___|___|_____|_|___|___|
                    _____ 
             _   __/ ___/
            | | / / __ \ 
            | |/ / /_/ / 
            |___/\____/ 

	"""

try:
	import printbyte
except:
	class printbyte (object):
		def byte_pbyte(data):
			if len(str(data)) > 1:
				msg = list(data)
				s = 0
				for u in msg:
					u = str(u).encode("hex")
					u = "\\x"+u
					msg[s] = u
					s = s + 1
				msg = "".join(msg)
			else:
				msg = data
				msg = str(msg).encode("hex")
				msg = "\\x"+msg
			return msg

shell = False
verbose = True
devices = []
responses = []
sim_names = False
blacklist = "none", "None", "unknown", "", "Unknon"

def ani_load(msg,amt=5,tm=0.1,rng=(1,3)):
	for t in range(random.randint(rng[0],rng[1])):
		for _ in range(1,amt):
			sys.stdout.write("\r"+msg+"."*_+"     ")
			time.sleep(tm)
	print 

class BlueBorne (object):
	def did_update_state(self):
		pass

	def did_discover_peripheral(self, p):
		if "" in p.uuid and str(p.name) not in blacklist and p.name not in devices:
			print "\n"+"="*36+"\n"
			if verbose:
				print "[+] Discovered " + str(p.name)
			self.peripheral = p
			cb.connect_peripheral(p)
	
	def did_disconnect_peripheral(self,p,error):
		try:
			print "[-] %s Disconnected" %(p.name)
			self.peripheral.cancel_peripheral_connection(p)
		except:
			pass
	
	def did_connect_peripheral(self, p):
		print "[+] Connected " + p.name
		p.discover_services()

	def did_discover_services(self, p, error):
		if not sim_names:
			devices.append(p.name)
		responses = []
		print 
		for s in p.services:
			if "" in s.uuid:
				if verbose:
					print "[+] Service " + s.uuid
				p.discover_characteristics(s)
		print
	
	def did_discover_characteristics(self, s, error):
		for c in s.characteristics:
			if "" in c.uuid:
				if verbose:
					print "[+] Characteristic " + c.uuid
					if shell:
						ani_load("[+] Generating Payload")
				if shell:
					self.peripheral.write_characteristic_value(c,shell,True)
					print "Payload -> %s//%s" %(self.peripheral.name[:6], c.uuid[:6])
				try:
					self.peripheral.read_characteristic_value(c)
					self.peripheral.set_notify_value(c, True)
					
				except Exception as e:
					pass
	
	def did_update_value(self, c, error):
		if c.uuid not in responses:
			print "[*] Checking Response For %s" %c.uuid[:6]
			try:
				if len(c.value) == 10 and "\x70" in c.value:
					ten = False
					resp = str(c.value)
				if str(c.uuid) == "2A24":
					resp = str(c.value)
				elif len(c.value) == 1:
					resp = eval(printbyte.byte_pbyte(c.value).replace("\\x","0x"))
				elif ten:
					resp = printbyte.byte_pbyte(c.value)
				print "[%]",resp
				print
			except Exception as e:
				try:
					print "[-] No Response"
					print
				except:
					pass
				pass
			responses.append(c.uuid)
	
	def did_write_value(self,c,error):
		try:
			print "[+] Payload Finished %s\n[=] Scanning Info On %s" %(c.uuid[:6],self.peripheral.name[:6])
		except:
			pass
	
cb.set_central_delegate(BlueBorne())
ani_load("[*] Scanning For Devices",5,0.15,(6,8))
cb.scan_for_peripherals()

try:
	while True: time.sleep(0.1)
except KeyboardInterrupt:
	cb.reset()
	cb.stop_scan()

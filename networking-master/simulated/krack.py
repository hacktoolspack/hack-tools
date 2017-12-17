"""
 _____             _   
|  |  |___ ___ ___| |_ 
|    -|  _| .'|  _| '_|
|__|__|_| |__,|___|_,_|-zero-all-tk.py

This is a simulated program just to visualize display outputs.
This is NOT the exploit for the program Krack!

An attacker within range of a victim can exploit these weaknesses using key reinstallation attacks (KRACKs). Concretely, attackers can use this novel attack technique to read information that was previously assumed to be safely encrypted.	This can be abused to steal sensitive information such as credit card numbers, passwords, chat messages, emails, photos, and so on. The attack works against all modern protected Wi-Fi networks. Depending on the network configuration, it is also possible to inject and manipulate data. For example, an attacker might be able to inject ransomware or other malware into websites.

Key Reinstallation Attacks

Mathy Vanhoef KRACK (c) 2017

"""

import random, socket, time, string
from time import gmtime, strftime

try:
	import sys
	import console
	console.set_font("Menlo",9.6)
	if sys.platform != "ios":
		sys.exit()
except:
	print "Pythonista 3 App is required to run this program"
	sys.exit()

def green():
	console.set_color(0.3,0.7,0)

def yellow():
	console.set_color(0.7,0.6,0)

def noc():
	console.set_color()
noc()

print "\n\t===[ KRACK Attacks against Linux/Android by Mathy Vanhoef ]===\n"
time.sleep(2)

def line_probe(stage=1):
		if stage == 3:
			if random.randint(0,3) == 3:
				probe = " Null(seq=%s, sleep=0)" % random.randint(70,90)
			else:
				probe = " EncryptedData(seq=%s, IV=%s)" %(random.randint(60,90),random.randint(1,90))
		if stage == 2:
			if random.randint(0,4) == 1:
				probe = " Null(seq=%s, sleep=0)" % random.randint(70,90)
			else:
				probe = " Auth(seq=%s, status=0)" %random.randint(1,10)
		if stage == 4:
			probe = " EAPOL-Msg3(seq=%s, reply=%s) -- MiTM'ing" %(random.randint(0,1),random.randint(2,5))
		if stage == 1:
			probe = " ProbeResp(seq=%s, sleep=0)" % (random.choice([8261,7293,2581,9392,5283,8948,8271,2782,7262,3682,21,25,38,39,8282,6278,10,11,12,13,15,16,17,18,19,8032,9277,9261,92729,7282,6288,9827,8287,7261,7942,5147,8232,9927,7282]))
		return probe

def rmac(end=False):
	mac = ""
	for _ in range(6):
		for _ in range(2):
			mac += random.choice(list(string.hexdigits.upper()))
		mac += ":"
	if end:
		return mac
	return mac[:17]

pmac = ("ff:"*6)[:17],rmac()
umac = rmac(),rmac(),pmac[1]

def line_signal(r=False):
	line = strftime("[%H:%M:%S] ", gmtime())
	segment = "%s channel" %(random.choice(["Real","Rogue","Real", "Real","Real","Real","Real","Real", "Real","Real"]))
	if "Real" in segment:
		segment += " : "
		line += segment
		line += random.choice(umac)
		line += " -> "
		line += random.choice(pmac)
		line += ":"
	else:
		segment += ": "
		line += segment
		line += random.choice(umac[:2])
		line += " -> "
		line += random.choice(pmac[1:])
		line += ":"
	return line

def start_sim():
	print strftime("[%H:%M:%S] ", gmtime())+ "Note: Remember to disable your own network before running this."
	print strftime("[%H:%M:%S] ", gmtime())+ "Note: Keep >1 meter between both interfaces."
	time.sleep(2)
	green()
	print strftime("[%H:%M:%S] ", gmtime())+ "Target network %s detected on channel 6" %pmac[1]
	time.sleep(random.randint(1,3))
	print strftime("[%H:%M:%S] ", gmtime())+ "Will create rogue AP to channel 1"
	time.sleep(1)
	noc()
	print strftime("[%H:%M:%S] ", gmtime())+ "Setting MAC Address of SavLan to %s"%pmac[1]
	time.sleep(1)
	print strftime("[%H:%M:%S] ", gmtime())+ "Giving the rogue hostapd one second to initialize...."
	time.sleep(random.randint(1,3))
	green()
	print strftime("[%H:%M:%S] ", gmtime())+ "Injected 4 CSA Beacon Pairs (moving stations to channel 1)"
	time.sleep(random.randint(1,2))
	yellow()
	print strftime("[%H:%M:%S] ", gmtime())+ "Rogue hostapad: nl80211: send_mlme * d = %s noack=0 freq=0 nocck=0 chanok=0 wait_time=0 fc=0xc0 (wLAN_FC_STYPE_DEAUTH) nlmode=3" %pmac[0]
	time.sleep(random.randint(1,3))
	green()
	print strftime("[%H:%M:%S] ", gmtime())+"Rogue channel: injection Disassociation to %s" % pmac[1]
	noc()
	time.sleep(1.5)
	
	for _ in range(2):
		print line_signal() + " QoS-Null(seq %s, sleep=0)" % random.randint(800,1000)
	
	time.sleep(random.randint(2,3))
	for _ in range(random.randint(50,75)):
		print line_signal(True) + line_probe()
		time.sleep(random.choice([0.12,0.09,0.1]))
	
	yellow()
	print line_signal() + " Auth(seq=%s, status=0)" %random.randint(1,10)
	time.sleep(1)
	print strftime("[%H:%M:%S] ", gmtime())+ "Client %s is connecting on real channel. Injectinf CSA beacon to try to correct." %umac[2]
	time.sleep(3)
	green()
	for _ in range(2):
		print strftime("[%H:%M:%S] ", gmtime())+ "Injected 1 CSA beacon pairs (moving stations to channel 1)"
		time.sleep(2)
	
	noc()
	for _ in range(3):
		print line_signal(True) + line_probe(4)
		time.sleep(random.choice([0.32,0.29,0.31]))
	
	green()
	print "\tEstablished MiTM position against client %s (moved to state 2)"%umac[2]
	time.sleep(2)
	noc()
	
	for _ in range(3):
		print line_signal(True)+line_probe(4)
	green()
	print "\tNot Forwarding EAPIO msg3 (1 unique now queued)"
	noc()
	time.sleep(2.3)
	print line_signal() + " QoS-Null(seq %s, sleep=0)" % random.randint(800,1000)
	print line_signal(True) + line_probe(4)
	
	green()
	print "\tGot 2nd unique EAPIL msg3. Will forward both these Msg3's seperated by a forged msg1."
	time.sleep(1)
	print "\t==> Performing key reinstallation attack!"
	time.sleep(3)
	noc()
	
	for _ in range(random.randint(9,12)):
		print line_signal(True)+line_probe(3)
		time.sleep(random.choice([0.32,0.29,0.31]))
	print line_signal(True)+" EncryptedData(seq=4, IV=1)"
	green()
	print "\tSUCCESS! Nonce reuse detected (IV=1), with usage of all-zero encryption key."
	time.sleep(2)
	print "\tNow MiTM'ing the victim using our malicious AP."
	time.sleep(3)
	noc()
	
	for _ in range(random.randint(100,200)):
		print line_signal(True)+line_probe(random.choice([1,3,3]))
		time.sleep(random.choice([0.12,0.09,0.1]))

start_sim()
console.set_font()

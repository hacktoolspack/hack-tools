"""

_____/\\\\\\\\\__________________        
 ___/\\\///////\\\________________       
  __\/\\\_____\/\\\________________      
   __\///\\\\\\\\\/_______/\\\\\____     
    ___/\\\///////\\\____/\\\///\\\__    
     __/\\\______\//\\\__/\\\__\//\\\_   
      _\//\\\______/\\\__\//\\\__/\\\__  
       __\///\\\\\\\\\/____\///\\\\\/___ 
        ____\/////////________\/////_____

8o Scanner is a Multi-API information gathering tool developed to provide quick access to information on target sites or domains. More APIs coming soon!

SavSec 8o (c) 2017
@Russian_Otter (c) 2017

Formatting:
	Tab: 2
	Encoding: UTF-8
	Python: 2.7.11
	iOS & PC Support

License:
	MIT License
	
"""

import shodan, sys, time, socket, argparse, json, requests, socket
from urllib2 import urlopen

hidden = True
iOS = False
ZoneTransfer = True
print

class Censys:
	
	def __init__(self, ip, uid, secret):
		self.API_URL = "https://www.censys.io/api/v1"
		self.UID = uid
		self.SECRET = secret
		self.ip = ip

	def search(self,pages=1):
		page = 1
		while page <= pages:
			params = {'query' : self.ip, 'page' : page}
			res = requests.post(self.API_URL + "/search/ipv4", json = params, auth = (self.UID, self.SECRET))
			payload = res.json()
			for r in payload['results']:
				ip = r["ip"]
				proto = r["protocols"]
				print "[Censys] IP: %s" %ip
				print "[Domain] %s" %socket.getfqdn(ip)
				time.sleep(0.005)
				print
			pages = payload['metadata']['pages']
			page += 1

	def view(self, server):
		res = requests.get(self.API_URL + ("/view/ipv4/%s" % server), auth = (self.UID, self.SECRET))
		payload = res.json()
		try:
			ip = "[ "+payload["ip"]+" ]"
			print "=" *len(ip)
			print ip
			print "=" *len(ip)
			for _ in payload["location"]:
				print "[%s] %s" %(_.upper().replace("_"," "),payload["location"][_])
			for _ in payload["autonomous_system"]:
				print "[%s] %s" %(_.upper().replace("_"," "),payload["autonomous_system"][_])
			if "80" in payload:
				for _ in payload["80"]["http"]["get"]["metadata"]:
					print "[%s] %s" %(_.upper().replace("_"," "),payload["80"]["http"]["get"]["metadata"][_])
		except Exception as e:
			print e
			pass
		print

def search(query,multi=False):
	try:
		result = api.search(query)
		for service in result["matches"]:
			time.sleep(0.05)
			if "200" in service["data"]:
				print "\n-",service["ip_str"],"-"
				if multi:
					try:
						adv = Censys(service["ip_str"],CENSYS_ID,CENSYS_API_KEY)
						adv.view(service["ip_str"])
					except Exception as e:
						print e
				try:
					print "[Device]", service["product"]
				except:
					pass
				if service["os"]:
					print "[OS]",service["os"]
				if service["location"]["country_code"]:
					print "[Country]",service["location"]["country_code"]
				if service["location"]["city"]:
					print "[City]",service["location"]["city"]
				if service["isp"]:
					print "[ISP]",service["isp"]
				if ZoneTransfer:
					AXFR = urlopen("http://api.hackertarget.com/zonetransfer/?q=%s"%service["ip_str"]).read()
					print "[AXFR Info]"
					print AXFR
				print "[Information]"
				print service["data"].replace("\r\n\r\n","\n").split("<")[0].replace("\r","")
		print
	except Exception as e:
		error = "Error: %s" % e
		if str(e) == "Invalid API key":
			print error
			if iOS:
				sys.stdout.write("[")
				console.write_link("Shodan Signup","https://account.shodan.io/register")
				print "]"
				sys.stdout.write("[")
				console.write_link("Censys Signup","https://www.censys.io/register")
				print "]"
			else:
				print "https://account.shodan.io/register"
				print "https://www.censys.io/register"
		else:
			print error
		pass

if not hidden:
	id = hash(SHODAN_API_KEY)
	cip = hash(CENSYS_API_KEY)
else:
	id = "Ro"

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("shodan.io",443))
	s.close()
except:
	print "\n[Offline]"
	sys.exit()

def menu(value):
	value = str(value)
	if value.lower() == "auth":
		if not SHODAN_API_KEY:
			print "[Shodan] Unauthenticated"
		else:
			print "[Shodan] Authenticated"
		if not CENSYS_API_KEY:
			print "[Censys] Unauthenticated"
		else:
			print "[Censys] Authenticated"
		print
	if value.lower() == "about":
		print "8oScanner is a Multi-API program used for scanning one or many domains using popular network-based API methods!"
		print "8o supports both iOS and PC!"
		print "Current APIs:"
		print "https://shodan.io"
		print "https://censys.io"
		print "https://hackertarget.com/zone-transfer/"
		print
		print "Options:"
		print "Shodan - Shodan API Query"
		print "Censys - Censys Domain Query"
		print "All - Combines both Shodan & Censys in a Multi-API Query"
		print
	if value.lower() == "quit":
		sys.exit()
	if value.lower() == "back":
		return "break"
	if value.lower() == "shodan":
		return "Shodan"
	if value.lower() == "censys":
		return "Censys"
	if value.lower() == "all":
		return "Shosys"
	if value.lower() == "direct":
		return "Direct"

parser = argparse.ArgumentParser(description = "8oScanner Authentication")
parser.add_argument("-s", "--shodan-api", help="Shodan API Key",default=None)
parser.add_argument("-c", "--censys-api", help="Censys API Key",default=None)
parser.add_argument("-ci", "--censys-id", help="Censys API ID",default=None)

args = parser.parse_args()
CENSYS_API_KEY = args.censys_api
CENSYS_ID = args.censys_id
SHODAN_API_KEY = args.shodan_api
api = shodan.Shodan(SHODAN_API_KEY)
censys_active = True
shodan_active = True
if len(str(SHODAN_API_KEY)) < 5:
	shodan_active = False
if len(str(CENSYS_API_KEY)) < 5:
	censys_active = False
	
if sys.platform == "ios":
	import console
	time.sleep(1)
	console.set_font("Menlo",40)
	console.set_color(0.8,0,0)
	print "  8o\r",
	console.set_color()
	print "Shodan"
	console.set_font()
	iOS = True
	if CENSYS_API_KEY:
		time.sleep(1)
		console.set_font("Arial Rounded MT Bold",40)
		console.set_color(0.8,0.3,0)
		print "     C \r",
		console.set_font("Menlo",40)
		console.set_color(0.5,0.5,0.55)
		print "censys"
		console.set_font()
		console.set_color()
		time.sleep(1)
	else:
		time.sleep(1)

print "\nCommands:"
print "[QUIT, AUTH, SHODAN, CENSYS, ABOUT, ALL, BACK, DIRECT]\n"

mode = "Menu"
while 1:
	try:
		if mode == "Shodan" and shodan_active:
			while 1:
				if iOS:
					sys.stdout.write("\n[")
					console.write_link("Shodan","https://shodan.io")
					sys.stdout.write("-%s]" %id)
					q = raw_input(" >>> ")
				else:
					q = raw_input("\n[Shodan-%s] >>> "%id)
				if len(q) > 1:
					i = menu(q)
					if i is "break":
						mode = "Menu"
						break
					if i is "Shodan":
						mode = i
						break
					if i is "Censys":
						mode = i
						break
					if i is "Shosys":
						mode = i
						break
					if i is "Direct":
						mode = i
						break
					print "[Shodan] Starting Search For %s" %q
					time.sleep(0.5)
					print "[Shodan] Querying API...\n"
					time.sleep(1)
					search(q)
		elif mode == "Censys" and censys_active:
			while 1:
				if iOS:
					sys.stdout.write("\n[")
					console.write_link("Censys","https://censys.io")
					sys.stdout.write("-%s]" %id)
					q = raw_input(" >>> ")
				else:
					q = raw_input("\n[Censys-%s] >>> "%cid)
				if len(q) > 1:
					i = menu(q)
					if i is "break":
						mode = "Menu"
						break
					if i is "Shodan":
						mode = i
						break
					if i is "Censys":
						mode = i
						break
					if i is "Shosys":
						mode = i
						break
					if i is "Direct":
						mode = i
						break
					print "[Censys] Starting Search For %s" %q
					time.sleep(0.5)
					print "[Censys] Querying API...\n"
					time.sleep(1)
					censys = Censys(q,CENSYS_ID,CENSYS_API_KEY)
					censys.search()
		elif mode == "Menu":
			while 1:
				a = raw_input("[Menu] >>> ")
				i = menu(a)
				if i is "break":
					mode = "Menu"
					break
				if i is "Shodan":
					mode = i
					break
				if i is "Censys":
					mode = i
					break
				if i is "Shosys":
					mode = i
					break
				if i is "Direct":
					mode = i
					break
		elif mode == "Shosys":
			while 1:
				a = raw_input("[Multi-API] >>> ")
				i = menu(a)
				if i is "break":
					mode = "Menu"
					break
				if i is "Shodan":
					mode = i
					break
				if i is "Censys":
					mode = i
					break
				if i is "Shosys":
					mode = i
					break
				if i is "Direct":
					mode = i
					break
				search(a,True)
		elif mode == "Direct":
			while 1:
				a = raw_input("[Direct] >>> ")
				i = menu(a)
				if i is "break":
					mode = "Menu"
					break
				if i is "Shodan":
					mode = i
					break
				if i is "Censys":
					mode = i
					break
				if i is "Shosys":
					mode = i
					break
				if i is "Direct":
					mode = i
					break
				a = socket.gethostbyname((a))
				censys = Censys(a,CENSYS_ID,CENSYS_API_KEY)
				censys.view(a)
		else:
			mode = "Menu"
	except Exception as e:
		break

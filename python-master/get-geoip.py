#!/usr/bin/python
# by ..:: crazyjunkie ::.. 2014

def main():
	def mapi():
		print("Getting GEO IP")
		ip = urllib.urlopen('http://www.telize.com/geoip').read()
		print(ip)
	mapi()
main()

#Telize.com is awesome go there they have more API's

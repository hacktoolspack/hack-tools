#!/usr/bin/python
#     __                                           _             __   _    
#    / /_  __  __   ______________ _____  __  __  (_)_  ______  / /__(_)__ 
#   / __ \/ / / /  / ___/ ___/ __ `/_  / / / / / / / / / / __ \/ //_/ / _ \
#  / /_/ / /_/ /  / /__/ /  / /_/ / / /_/ /_/ / / / /_/ / / / / ,< / /  __/
# /_.___/\__, /   \___/_/   \__,_/ /___/\__, /_/ /\__,_/_/ /_/_/|_/_/\___/ 
#       /____/                         /____/___/                          
#
###############################################################################
 Download huge collections of wordlist:#
http://ul.to/folder/j7gmyz#
##########################################################################

####################################################################
 Need daylie updated proxies?#
http://j.mp/Y7ZZq9#
################################################################

######################################################
#### Hash Crack ######
###################################################
#Attempts to crack hash ( md5, sha1, sha256, sha384, sha512) against any givin wordlist.


import os, sys ,hashlib

if len(sys.argv) != 4:
	print " \n by ..:: crazyjunkie ::.."
	print "\n\nUsage: ./hash.py <hash algorithm > <hash> <wordlist>"
	print "\n Example: /hash.py <md5 or sha1 or sha256 or sha384 or sha512> <hash> <wordlist>"
	sys.exit(1)
	
algo=sys.argv[1]
pw = sys.argv[2]
wordlist = sys.argv[3]
try:
  words = open(wordlist, "r")
except(IOError): 
  print "Error: Check your wordlist path\n"
  sys.exit(1)
words = words.readlines()
print "\n",len(words),"words loaded..."
file=open('cracked.txt','a')
if algo == 'md5':
	for word in words:
		hash = hashlib.md5(word[:-1])
		value = hash.hexdigest()
		if pw == value: 
			print "Password is:",word,"\n"
			file.write("\n Cracked Hashes\n\n")
			file.write(pw+"\t\t")
			file.write(word+"\n")
if algo == 'sha1':
	for word in words:
		hash = hashlib.sha1(word[:-1])
		value = hash.hexdigest()
		if pw == value: 
			print "Password is:",word,"\n"
			file.write("\n Cracked Hashes\n\n")
			file.write(pw+"\t\t")
			file.write(word+"\n")
if algo == 'sha256':
	for word in words:
		hash = hashlib.sha256(word[:-1])
		value = hash.hexdigest()
		if pw == value: 
			print "Password is:",word,"\n"
			file.write("\n Cracked Hashes\n\n")
			file.write(pw+"\t\t")
			file.write(word+"\n")

if algo == 'sha384':
	for word in words:
		hash = hashlib.sha384(word[:-1])
		value = hash.hexdigest()
		if pw == value: 
			print "Password is:",word,"\n"
			file.write("\n Cracked Hashes\n\n")
			file.write(pw+"\t\t")
			file.write(word+"\n")
	
	
if algo == 'sha512':
	for word in words:
		hash = hashlib.sha512(word[:-1])
		value = hash.hexdigest()
		if pw == value: 
			print "Password is:",word,"\n"
			file.write("\n Cracked Hashes\n\n")
			file.write(pw+"\t\t")
			file.write(word+"\n")

#!/usr/bin/python
#Attempts to crack hash against any givin wordlist.
#by ..:: crazyjunkie ::.. 2014

import md5, base64, sys

if len(sys.argv) != 3:
  print "Usage: ./md5crack.py <hash> <wordlist>"
  sys.exit(1)
  
pw = sys.argv[1]
wordlist = sys.argv[2]
try:
  words = open(wordlist, "r")
except(IOError): 
  print "Error: Check your wordlist path\n"
  sys.exit(1)
words = words.readlines()
print "\n",len(words),"words loaded..."
hashes = {}
for word in words:
  hash = md5.new()
  hash.update(word[:-1])
  value = hash.hexdigest()
  hashes[word[:-1]] = value
for (key, value) in hashes.items():
  if pw == value: 
    print "Password is:",key,"\n"

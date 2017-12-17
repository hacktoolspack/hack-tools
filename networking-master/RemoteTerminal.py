import socket, time, os, threading, sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	BIND_IP = s.getsockname()[0]
	BIND_PORT = 2000
	s.close()
except:
	sys.exit()

def handle_client(client_socket):
	while 1:
		request = client_socket.recv(1024)
		try:
			if str(request) == "exit":
				sys.exit()
		except:
			pass
		try:
			exec(str(request))
		except:
			pass

def tcp_server():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((BIND_IP, BIND_PORT))
	server.listen(5)
	print"[*] Listening on %s:%d" % (BIND_IP, BIND_PORT)
	
	while 1:
		client, addr = server.accept()
		print "[*] Accepted connection from: %s:%d" %(addr[0], addr[1])
		client_handler = threading.Thread(target=handle_client, args=(client,))
		client_handler.start()

if __name__ == '__main__':
	tcp_server()

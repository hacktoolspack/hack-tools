from LoggingProxyHTTPHandler import LoggingProxyHTTPHandler
import BaseHTTPServer
import sys
import socket
try:
	from objc_util import *
except:
	pass

def main(args):
	try:
		port = int(args[1])
	except IndexError:
		port = 8000
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8",80))
		ip = s.getsockname()[0]
	except:
		ip = "0.0.0.0"
		print "No Connection"
	try:
		CNCopyCurrentNetworkInfo = c.CNCopyCurrentNetworkInfo
		CNCopyCurrentNetworkInfo.restype = c_void_p
		CNCopyCurrentNetworkInfo.argtypes = [c_void_p]
		wifiid = ObjCInstance(CNCopyCurrentNetworkInfo(ns('en0')))
		wifiid = wifiid["SSID"]
	except:
		wifiid = "[Your WiFi]"
	server_address = (ip, port)
	print "Started Proxy",ip,port
	print "\nTo Start Logging:"
	print "Settings>WiFi>%s>HTTP Proxy>Manual>\nHost: %s\nPort: %s\nAuthentication: OFF\n" %(wifiid,ip,port)
	httpd = BaseHTTPServer.HTTPServer(server_address, LoggingProxyHTTPHandler)
	httpd.serve_forever()

if __name__ == '__main__':
	sys.exit(main(sys.argv))

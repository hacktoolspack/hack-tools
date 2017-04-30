#!/usr/bin/env python

import socket
import signal
import sys
import threading
import time
import SocketServer
import Util
import argparse
import os

LOG_FILE = 'log.txt'
filebusy = False;

"""
Append the provided line to the log file (log.txt) or
just generate the log string
"""
def log(line):

   if logToFile:
      global filebusy
      while filebusy:
         time.sleep(0.5) # wait 500 ms
      filebusy = True

   logStr = Util.formatTimeMS(Util.getCurrTime()) + ': '+ line

   if logToFile:
      with open(LOG_FILE, 'a') as logFile:
         logFile.write(logStr + '\n')
      filebusy = False

   return logStr

"""
Shut down gracefully.
"""
def shutdown(signum, frame):
   if 'server' in globals():
      server.shutdown()

   print '\nServer shut down'

   sys.exit(0)

"""
Handles the Clients connecting to the Server.
"""
class ClientRequestHandler(SocketServer.BaseRequestHandler):
   def handle(self):
      logLine = 'Received connection request from ' + str(self.client_address)
      print log(logLine)

      # keep the connection open while data is still being sent
      while True:
         try:
            rcvdStr = Util.recieve(self.request)

            if len(rcvdStr) < 1:
               break

            print log(str(self.client_address) + ' ' + rcvdStr)
         except socket.error as msg:
            log(str(msg))
            break

"""
Class for a threaded TCP server
"""
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
   pass


"""
The Target Server simply runs a threaded TCP server on the specifed port.
Once clients connect, it continues to accept data from them until they stop.
"""
if __name__ == '__main__':
   # handle arguments
   parser = argparse.ArgumentParser(description='Start Server.')

   parser.add_argument('-p', '--port', dest='port', action='store', \
      type=int, required=False, help='The port on which to run the server. \
      Default is 8080.', default=8080)

   parser.add_argument('-f', dest='logToFile', action='store_true')

   args = parser.parse_args()
   port = args.port
   logToFile = args.logToFile

   # invalid port
   if port <= 1024:
      parser.print_help()
      sys.exit(0)

   print 'Initializing Server...\n'

   signal.signal(signal.SIGINT, shutdown)

   # clear old log file
   if logToFile and os.path.isfile(LOG_FILE):
      os.remove(LOG_FILE)

   # set up the server, and start listening on the specified port
   HOST, PORT = socket.gethostname(), port
   server = ThreadedTCPServer((HOST, PORT), ClientRequestHandler)
   server.allow_reuse_address
   ip, serverPort = server.server_address

   # Start a thread with the server -- that thread will then start one
   # more thread for each request
   serverThread = threading.Thread(target=server.serve_forever)
   # Exit the server thread when the main thread terminates
   serverThread.daemon = True
   serverThread.start()

   print 'Server is listening on port', port, 'in thread:', serverThread.name
   print '\nUse Ctrl+C to stop server at anytime\n'

   # keep the main thread running, can be stopped with ctrl+c
   while True:
      time.sleep(60)

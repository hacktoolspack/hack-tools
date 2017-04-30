#!/usr/bin/env python

import time
import datetime

EOF = '\n'
MASTER_PASSPHRASE = 'gits#9sac'
BOT_PASSPHRASE    = 'standalone'
CODE_00 = '00' # send current time

"""
   Receive msg from the provided connection.
   The length of the msg can be specified if known, otherwise
   default is 2048 chars.
"""
def recieve(connection, MSGLEN = 2048):
   recvdStr = [] # stores received substrings
   recvdStrLen = 0 # keep track of how much of the msg is received

   # keep receiving data until MSGLEN is reached or EOF is found
   while recvdStrLen < MSGLEN:
      recvdSubstring = connection.recv(MSGLEN - recvdStrLen)

      # empty string signals connection was closed
      if recvdSubstring == '':
         break 

      # check received substring 
      left, middle, right = recvdSubstring.partition(EOF)

      if left == EOF: # first char is an EOF
         break
      elif middle == EOF: # found EOF, only use left substring
         recvdStr.append(left)
         break
      else: # no EOF, keep receiving until MSGNLEN is received 
         recvdStr.append(recvdSubstring)
         recvdStrLen += len(recvdSubstring)

   # return final string
   return ''.join(recvdStr)

"""
Send a msg to the provided connection.
"""
def send(connection, msg):
   sendStr = msg + EOF
   connection.send(msg + EOF)

"""
Get the current time in milliseconds.
"""
def getCurrTime():
   return int(time.time() * 1000) # time in milliseconds

"""
Format the provided time in milliseconds to a human readable String.
"""
def formatTimeMS(timeMS):
   return str(datetime.datetime.fromtimestamp(float(timeMS)/1000)\
         .strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

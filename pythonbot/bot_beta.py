import socket, getpass, random, platform, uuid, signal, time, os, sys, urllib2, unicodedata, json
from subprocess import Popen, PIPE, STDOUT
from time import strftime, sleep

version = "BETA1.0"

server = 'irc.freenode.net'
port = 6667
channel = '##medusa'
admin = 'thesquash'
nick = "[MEDUSA-TESTBOT]"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))

data = irc.recv(4096)
print data

irc.send('NICK %s\r\n' % nick )
irc.send('USER %s %s %s :%s\r\n' % (nick, nick, nick, nick))
irc.send('JOIN %s\r\n' % channel)

while True:
    data = irc.recv(4096)
    print data
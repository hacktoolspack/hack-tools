import pantheradesktop.kernel
import sys
import os

class udosArgsParsing (pantheradesktop.argsparsing.pantheraArgsParsing):
    """ 
        Arguments parser extension
    """
    
    description = "UDoS for GNU/Linux - Universal DoS and DDoS testing tool"
    
    def fork(self, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        '''This forks the current process into a daemon.
        The stdin, stdout, and stderr arguments are file names that
        will be opened and be used to replace the standard file descriptors
        in sys.stdin, sys.stdout, and sys.stderr.
        These arguments are optional and default to /dev/null.
        Note that stderr is opened unbuffered, so
        if it shares a file with stdout then interleaved output
        may not appear in the order that you expect.
        '''
    
        # Do first fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)   # Exit first parent.
        except OSError as e:
            sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
            sys.exit(1)
    
        # Decouple from parent environment.
        os.chdir("/")
        os.umask(0)
        os.setsid()
    
        # Do second fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)   # Exit second parent.
        except OSError as e:
            sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )
            sys.exit(1)
    
        # Now I am a daemon!
    
        # Redirect standard file descriptors.
        si = open(stdin, 'r')
        so = open(stdout, 'a+')
        se = open(stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        
    def debug(self, data=''):
        self.app.logging.silent = False
        
    def bindMode(self, data=''):
        self.app.mode = "bind"
        
    def selectTarget(self, target=''):
        self.app.target = target
        
    def selectPort(self, port=''):
        self.app.destPort = port
        
    def packetSize(self, bytes=''):
        self.app.packetSize = int(bytes)
        
    def run(self, data=''):
        self.app.run = True
        
    def stop(self, data=''):
        self.app.stopBefore = True
        
    def client(self, data=''):
        self.app.mode = 'client'
        self.app.clients = data.replace(' ', '').split(',')
        
    def setSocket(self, socketName=''):
        if not socketName in ('tcp', 'udp', 'rfc', 'http'):
            print("Unknown socket type. Please specify one of following socket types: tcp, udp, rfc, http")
            self.app.pa_exit()
        
        self.app.socketType = socketName
        
    def version(self, data=''):
        print("udos 2.0")
    
    def addArgs(self):
        """ Add application command-line arguments """
    
        self.createArgument('--fork', self.fork, 1, 'Fork to background', action='store_true')
        self.createArgument('--run', self.run, 1, 'Execute run on remote server (to be used with --client argument)', action='store_true')
        self.createArgument('--stop', self.stop, 1, 'Stop previous job', action='store_true')
        self.createArgument('--debug', self.debug, 1, 'Debugging mode', action='store_true')
        self.createArgument('--socket', self.setSocket, '', 'use TCP or UDP connection over ethernet/wireless, default TCP, available TCP, UDP, RFC (bluetooth)')
        self.createArgument('--client', self.client, 1, 'Connect to comma separated client addresses')
        self.createArgument('--server', self.bindMode, 1, 'turn into a server mode that handles instructions', action='store_true')
        self.createArgument('--target', self.selectTarget, '', 'target adress (bluetooth mac or ip adress over ethernet/wireless)')
        self.createArgument('--port', self.selectPort, 80, 'destination port')
        self.createArgument('--bytes', self.packetSize, 80, 'number of bytes to send in one packet')
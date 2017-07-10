#!/usr/bin/python
from src.main import *
from src.header import *

from core.protocols import *
from core.xmpp import *
from core.web import *

class Bruteforce(object):
    def __init__(self, service, username, wordlist, address, port, delay, proxy):
        
        self.service = service
        self.username = username
        self.wordlist = wordlist
        self.address = address 
        self.port = port
        self.delay = delay
        self.proxy = proxy
        
        self.get_args(self.service, self.username, self.wordlist, self.address, self.port, self.delay, self.proxy)
        
        print choice(headers)
        print (G + "[*] Username: %s " % self.username) + W
        sleep(0.5)
        print (G + "[*] Wordlist: %s " % self.wordlist) + W
        sleep(0.5)
        if os.path.exists(self.wordlist) == False:
            print R + "[!] Wordlist not found! [!]" + W
            exit()
        print (C + "[*] Service: %s "  % self.service) + W
        if self.service is None:
            print R + "[!] No service provided! [!]" + W
        if self.proxy is not None:
            print (C + "[*] Proxy file: %s " % self.proxy) + W
            print O + "Checking if proxies are active...\n" + W
            self.proxyServer(self.proxy)
        sleep(0.5)
        
    def get_args(self, service, username, wordlist, address, port, delay, proxy):
        parser = argparse.ArgumentParser(description='Bruteforce framework written in Python')
        required = parser.add_argument_group('required arguments')
        required.add_argument('-s', '--service', dest='service', help="Provide a service being attacked. Several protocols and services are supported")
        required.add_argument('-u', '--username', dest='username', help='Provide a valid username for service/protocol being executed')
        required.add_argument('-w', '--wordlist', dest='password', help='Provide a wordlist or directory to a wordlist')
        parser.add_argument('-a', '--address', dest='address', help='Provide host address for specified service. Required for certain protocols')
        parser.add_argument('-p', '--port', type=int, dest='port', help='Provide port for host address for specified service. If not specified, will be automatically set')
        parser.add_argument('-d', '--delay', type=int, dest='delay', help='Provide the number of seconds the program delays as each password is tried')
        parser.add_argument('--proxy', dest='proxy', help="Providing a proxy for anonymization and avoiding time-outs")

        args = parser.parse_args()

        man_options = ['username', 'password']
        for m in man_options:
            if not args.__dict__[m]:
                print R + "[!] You have to specify a username AND a wordlist! [!]" + W
                exit()

        self.service = args.service
        self.username = args.username
        self.wordlist = args.password
        self.address = args.address
        self.port = args.port
        self.delay = args.delay
        self.proxy = args.proxy

        if self.delay is None:
            self.delay = 1
        
    def proxyServer(proxy):
        proxy = open(proxy, 'r')
        for i in proxy.readlines():
            proxyaddr = i.strip("\n")
            try:
                proxies = {"http" : "http://" + str(proxyaddr) }
                r = requests.get("http://google.com", proxies=proxies)
                print G + "[v]" + W + (" Proxy %s is found! " % proxyaddr)
            except requests.exceptions.ProxyError:
                print R + "[X]" + W + (" Proxy %s is NOT found!" % proxyaddr)
                
            proxy.close()
    

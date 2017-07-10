#!/usr/bin/python
'''
brut3k1t - main application that calls upon dependencies and 
    other libraries / modules
'''

from src.brut3k1t import *

def main():
    os.system("rm -rf tmp/") # delete tmp if created from previous usage
    
    b = Bruteforce(service=None, username=None, wordlist=None, address=None, port=None, delay=1, proxy=None)
    
    protocols = ["ssh", "ftp", "smtp", "telnet"]
    web = ["instagram", "twitter", "facebook"]
    
    if b.service in protocols:
        ProtocolBruteforce(b.service, b.address, b.username, b.wordlist, b.port, b.delay)
    elif b.service in web:
        if b.address or b.port:
            print R + "[!] NOTE: You don't need to provide an address OR port [!]" + W
            exit(1)
        WebBruteforce(b.service, b.username, b.wordlist, b.delay)
    elif b.service == 'xmpp':
        xmppBruteforce(b.address, b.port, b.username, b.wordlist, b.delay)
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print R + "\n[!] Keyboard Interrupt detected! Killing program... [!]" + W
        exit(1)

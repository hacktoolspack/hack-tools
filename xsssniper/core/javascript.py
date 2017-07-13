#/usr/bin/env python

import hashlib
from core.packages.clint.textui import colored 

class Javascript:
    """
    Used to represent a Javascript file and the result o it's
    analysis
    """

    def __init__(self, link, body, js_hash=None, is_embedded=False):
        self.link = link
        self.body = body
        self.is_embedded = is_embedded
        
        # javascript fingerprinting
        self.js_hash = js_hash
        if self.js_hash is None:
            self.js_hash = hashlib.md5(self.body).hexdigest()

        self.sources = []
        self.sinks = []

    def addSource(self, line, pattern):
        s = (line, pattern)
        self.sources.append(s)

    def addSink(self, line, pattern):
        s = (line, pattern)
        self.sinks.append(s)
    
    def printResult(self):
        if len(self.sources) > 0 | len(self.sinks) > 0:
            print " |--[!] Javascript: %s" % self.link
            if self.is_embedded:
                print " |   |- Type: embedded"
            print " |   |--[+] # Possible Sources: " + colored.green("%s" % len(self.sources))
            for s in self.sources:
                print " |   |   |--[Line: %s] %s" % (s[0], s[1])
            print " |   |"
            print " |   |--[+] # Possible Sinks: " + colored.green("%s" % len(self.sinks))
            for s in self.sinks:
                print " |   |   |--[Line: %s] %s" % (s[0], s[1])
            print " |   |"
            

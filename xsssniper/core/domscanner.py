try:
    from mechanize import Request, urlopen, URLError, HTTPError,ProxyHandler, build_opener, install_opener, Browser
except ImportError:
    print "\n[X] Please install mechanize module:"
    print "    http://wwwsearch.sourceforge.net/mechanize/\n"
    exit()

import re
import random
import threading
from lxml import etree
import os

from core.javascript import Javascript

SOURCES_RE = re.compile("""/(location\s*[\[.])|([.\[]\s*["']?\s*(arguments|dialogArguments|innerHTML|write(ln)?|open(Dialog)?|showModalDialog|cookie|URL|documentURI|baseURI|referrer|name|opener|parent|top|content|self|frames)\W)|(localStorage|sessionStorage|Database)/""")
SINKS_RE = re.compile("""/((src|href|data|location|code|value|action)\s*["'\]]*\s*\+?\s*=)|((replace|assign|navigate|getResponseHeader|open(Dialog)?|showModalDialog|eval|evaluate|execCommand|execScript|setTimeout|setInterval)\s*["'\]]*\s*\()/""")

class DOMScanner(threading.Thread):
    def __init__(self, engine, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.engine = engine

        self.errors = {}
        self.results = []
        self.javascript = []
        self.whitelisted_js = []
        self.whitelist = []

        self.browser = Browser()
        self._setProxies()
        self._setHeaders()
        self._getWhitelist()

    def _setHeaders(self):
        if self.engine.getOption('ua') is not None:
            if self.engine.getOption('ua') is "RANDOM":
                self.browser.addheaders = [('User-Agent', random.choice(USER_AGENTS))]
            else:
                self.browser.addheaders = [('User-Agent', self.engine.getOption('ua'))]
        if self.engine.getOption("cookie") is not None:
            self.browser.addheaders = [("Cookie", self.engine.getOption("cookie"))]
    
    def _setProxies(self):
         if self.engine.getOption('http-proxy') is not None:
            self.browser.set_proxies({'http': self.engine.getOption('http-proxy')})

    def _addError(self, key, value):
        if self.errors.has_key(key):
            self.errors[key].append(value)
        else:
            self.errors[key] = [value]

    def _getWhitelist(self):
        path = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(path, "../lib/whitelist.xml")
        f = open(path, "rb")
        xml = f.read()
        root = etree.XML(xml)

        for element in root.iterfind("javascript"):
            el = {
                'hash' : element.find("hash").text,
                'description': element.find("description").text,
                'reference': element.find("reference").text
                }
            self.whitelist.append(el)
        
    def _parseJavascript(self, target):
        if self.engine.getOption("ua") is "RANDOM": self._setHeaders() 
        
        url = target.getFullUrl()
        
        try:
            to = 10 if self.engine.getOption('http-proxy') is None else 20
            response = self.browser.open(url, timeout=to) #urlopen(req, timeout=to)
            
        except HTTPError, e:
            self._addError(e.code, target.getAbsoluteUrl())
            return
        except URLError, e:
            self._addError(e.reason, target.getAbsoluteUrl())
            return
        except:
            self._addError('Unknown', target.getAbsoluteUrl())
            return
        else:
            embedded = []
            linked = []
            # Parse the page for embedded javascript 
            response = response.read()
            index = 0
            intag = False
            inscript = False
            insrc = False
            ek = 0
            lk = 0

            while index <= len(response)-1:
                if response[index:index+7].lower() == "<script":
                    intag = True
                    index += 7
                    continue
                if response[index:index+4].lower() == "src=" and intag:
                    insrc = True
                    linked.append("")
                    index += 4
                    continue
                if (response[index] == "\"" or response[index] == "'") and insrc:
                    index += 1
                    continue
                if (response[index] == "\" " or 
                    response[index] == "' ") and insrc:
                    insrc = False
                    lk += 1
                    index += 2
                    continue
                if (response[index] == "\">" or
                    response[index] == "'>") and insrc and intag:
                    insrc = False
                    intag = False
                    lk += 1
                    index += 2
                    continue
                if response[index] == " " and insrc:
                    insrc = False
                    lk += 1
                    index += 1
                    continue
                if response[index] == ">" and insrc and intag:
                    insrc = False
                    intag = False
                    inscript = True
                    embedded.append("")
                    lk += 1
                    index += 1
                    continue
                if response[index] == ">" and intag:
                    intag = False
                    inscript = True
                    embedded.append("")
                    index += 1
                    continue
                if response[index:index+9].lower() ==  "</script>" and inscript:
                    inscript = False
                    ek += 1
                    index += 9
                    continue
                if inscript:
                    embedded[ek] += response[index]
                if insrc:
                    linked[lk] += response[index]

                index += 1

            # Parse the linked javascripts
            new_linked = []
            for link in linked:
                if link == "": continue
                if link[0:len(target.getBaseUrl())] == target.getBaseUrl():
                    new_linked.append(link)
                    continue
                elif (link[0:7] == "http://" or 
                     link[0:4] == "www." or
                     link[0:8] == "https://" or
                     link[0:2] == "//"):
                    if link[0:2] == "//":
                        link = "http:" + link
                    new_linked.append(link)
                    continue
                elif link[0] == "/":
                    new_linked.append(target.getBaseUrl() + link)
                    continue
                else:
                    new_linked.append(target.getBaseUrl() + "/" + link)
             
            # Remove duplicates
            linked = list(set(new_linked))
            
            # Return all javascript retrieved
            # javascript = [ [target, content], ... ]
             
            for link in linked:
                try:
                    to = 10 if self.engine.getOption('http-proxy') is None else 20
                    response = self.browser.open(link, timeout=to)
                except HTTPError, e:
                    self._addError(e.code, link)
                    continue
                except URLError, e:
                    self._addError(e.reason, link)
                    continue
                except:
                    self._addError('Unknown', link)
                    continue
                else:
                    j = Javascript(link, response.read())
                    self.javascript.append(j)
                    
            for r in embedded:
                if r is not "": 
                    j = Javascript(target.getAbsoluteUrl(), r, True)
                    self.javascript.append(j)
     
    def _analyzeJavascript(self):
         for js in self.javascript:
             #print "\n[+] Analyzing:\t %s" % js.link

             # Check if the javascript is whitelisted
             # and eventually skip the analysis
             skip = False
             for wl in self.whitelist:
                 if wl["hash"] == js.js_hash:
                     self.whitelisted_js.append(wl)
                     skip = True
                     break

             if skip:
                 continue


             for k, line in enumerate(js.body.split("\n")):
                for pattern in re.finditer(SOURCES_RE, line):
                    for grp in pattern.groups():
                        if grp is None: continue
                        js.addSource(k, grp) 
                        #print "[Line: %s] Possible Source: %s" % (k, grp)
                for pattern in re.finditer(SINKS_RE, line):
                    for grp in pattern.groups():
                        if grp is None: continue
                        js.addSink(k, grp) 
                        #print "[Line: %s] Possible Sink: %s" % (k, grp)

    def run(self):
        """ Main code of the thread """
        while True:
            try:
                target = self.queue.get(timeout = 1)
            except:
                try:
                    self.queue.task_done()
                except ValueError:
                    pass
            else:
                
                self._parseJavascript(target)
                self._analyzeJavascript()
                
                # Scan complete
                try:                
                    self.queue.task_done()
                except ValueError:
                    pass

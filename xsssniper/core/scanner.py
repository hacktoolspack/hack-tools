#!/usr/bin/env python 

try:
    from mechanize import Request, urlopen, URLError, HTTPError,ProxyHandler, build_opener, install_opener, Browser
except ImportError:
    print "\n[X] Please install mechanize module:"
    print "    http://wwwsearch.sourceforge.net/mechanize/\n"
    exit()

import random
import threading
import string

from core.constants import USER_AGENTS
from core.result import Result
from core.target import Target
from core.payload import Payload

class Scanner(threading.Thread):
    def __init__(self, engine, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.engine = engine

        self.results = []
        self.errors = {}

    def _addError(self, key, value):
        if self.errors.has_key(key):
            self.errors[key].append(value)
        else:
            self.errors[key] = [value]

    def processResponse(self, response, payload):
        """
        Given a response object it search and return XSS injection.

        How it works: we parse the response sequentially
        looking for the seed while keeping
        a state of the current position to determine if we have
        a valid injection and where.

        This is based on ratproxy XSS scanning technique so
        all the props to @lcamtuf for this.
        """
        
        # It only works for payloads of type taint (temporary)
        if payload.taint:
            htmlstate = 0
            htmlurl = 0
            index = 0
            result = []

            # Building the taint and the response
            # I want everything lowercase because I don't want to handle 
            # cases when the payload is upper/lowercased by the webserver
            seed_len = payload.seed_len
            seed = payload.seed

            # htmlstate legend:
            # - 1 index is in tag
            # - 2 index is inside double quotes
            # - 4 index is inside single quotes
            # - 8 index is inside html comment
            # - 16 index is inside cdata
            while index <= len(response)-1:
                # Exit cases for a match against the taint
                # If conditions are a little messy...
                # TODO: utf-7 xss
                if response[index:index+seed_len] == seed:
                    # XSS found in tag
                    # <tag foo=bar onload=...>
                    # type 1
                    if htmlstate == 1 and response[index+seed_len:index+seed_len+seed_len+1] == " " + seed + "=":
                        index = index + seed_len
                        result.append([1, "Payload found inside tag"])
                        continue

                    # XSS found in url
                    # <tag src=foo:bar ...>
                    # type 2
                    if htmlurl and response[index+seed_len:index+seed_len+seed_len+1] == ":" + seed:
                        index = index + seed_len
                        result.append([2, "Payload found inside url tag"])
                        continue

                    # XSS found freely in response
                    # <tag><script>...
                    # type 3
                    if htmlstate == 0 and response[index+seed_len:index+seed_len+seed_len+1] == "<" + seed:
                        index  = index + seed_len
                        result.append([3, "Payload found free in html"])
                        continue

                    # XSS found inside double quotes
                    # <tag foo="bar"onload=...>
                    # type 4
                    if (htmlstate == 1 or htmlstate == 2) and response[index+seed_len:index+seed_len+seed_len] == "\"" + seed:
                        index = index + seed_len
                        result.append([4, "Payload found inside tag escaped from double quotes"])
                        continue

                    # XSS found inside single quotes
                    # <tag foo='bar'onload=...>
                    # type 5
                    if (htmlstate == 1 or htmlstate == 4) and response[index+seed_len:index+seed_len+seed_len] == "'" + seed:
                        index  = index + seed_len
                        result.append([5, "Payload found inside tag escaped from single quotes"])
                        continue

                else:
                    # We are in a CDATA block
                    if htmlstate == 0 and response[index:index+9] == "<![CDATA[":
                        htmlstate = 16
                        index = index + 9
                        continue

                    if htmlstate == 16 and response[index:index+3] == "]]>":
                        htmlstate = 0
                        index = index + 3
                        continue

                    # We are in a html comment
                    if htmlstate == 0 and response[index:index+4] == "<!--":
                        htmlstate = 8
                        index = index + 4
                        continue

                    if htmlstate == 8 and response[index:index+3] == "-->":
                        htmlstate = 0
                        index = index + 3
                        continue

                    # We are in a tag
                    if htmlstate == 0 and response[index] == "<" and (response[index+1] == "!" or response[index+1] == "?" or response[index+1].isalpha()):
                        htmlstate = 1
                        index = index + 1
                        continue

                    if htmlstate == 1 and response[index] == ">":
                        htmlstate = 0
                        htmlurl = 0
                        index = index + 1
                        continue

                    # We are inside a double quote
                    if htmlstate == 1 and response[index] == '"' and response[index-1] == '=':
                        htmlstate = 2
                        index = index + 1
                        continue

                    if (htmlstate == 1 or htmlstate == 2) and response[index] == '"':
                        htmlstate = 1
                        index = index + 1
                        continue

                    # We are inside a single quote
                    if htmlstate == 1 and response[index] == '\'' and response[index-1] == '=':
                        htmlstate = 4
                        index = index + 1
                        continue

                    if (htmlstate == 1 or htmlstate == 4) and response[index] == '\'':
                        htmlstate = 1
                        index = index + 1
                        continue

                    # We are inside an url
                    if htmlstate == 1 and response[index-1] == " " and response[index:index+5] == "href=":
                        htmlurl = 1
                        index = index + 5 
                        continue

                    if htmlstate == 1 and response[index-1] == " " and response[index:index+5] == "src=":
                        htmlurl = 1
                        index = index + 4
                        continue

                    # In case the url isn't correctly closed
                    if htmlurl == 1: 
                        htmlurl = 0

                # Move on
                index = index +1

            # End of response parsing
            return result

        else:
            # No a taint payload
            return None
            
    def _performInjections(self, target):
        # Check every parameter 
        for k, v in target.params.iteritems():
            pl = Payload(taint=True)
            url, data = target.getPayloadedUrl(k, pl.payload)
            
            # In case of proxy 
            if self.engine.getOption('http-proxy') is not None:
                proxy = ProxyHandler({'http': self.engine.getOption('http-proxy')})
                opener = build_opener(proxy)
                install_opener(opener)
            # Some headers
            if self.engine.getOption('ua') is not None:
                if self.engine.getOption('ua') is "RANDOM":
                    headers = {'User-Agent': random.choice(USER_AGENTS)}
                else:
                    headers = {'User-Agent': self.engine.getOption('ua')}
            else:
                headers = {}
            if self.engine.getOption("cookie") is not None:
                headers["Cookie"] = self.engine.getOption("cookie")

            # Build the request
            req = Request(url, data, headers)
            try:
                to = 10 if self.engine.getOption('http-proxy') is None else 20
                response = urlopen(req, timeout=to)
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
                result = self.processResponse(response.read().lower(), pl)
                for r in result:
                    self.results.append(Result(target, k, pl, r))

    def _checkStoredInjections(self):
        for r in self.results:
            # At this state injections in Result obj are not
            # compacted yet so it will only be 1st injected param
            url, data = r.target.getPayloadedUrl(r.first_param, "")
            
            # In case of proxy 
            if self.engine.getOption('http-proxy') is not None:
                proxy = ProxyHandler({'http': self.engine.getOption('http-proxy')})
                opener = build_opener(proxy)
                install_opener(opener)
            
            # Some headers
            if self.engine.getOption('ua') is not None:
                if self.engine.getOption('ua') is "RANDOM":
                    headers = {'User-Agent': random.choice(USER_AGENTS)}
                else:
                    headers = {'User-Agent': self.engine.getOption('ua')}
            else:
                headers = {}
            if self.engine.getOption("cookie") is not None:
                headers["Cookie"] = self.engine.getOption("cookie")

            # Build the request
            req = Request(url, data, headers)
            try:
                to = 10 if self.engine.getOption('http-proxy') is None else 20
                response = urlopen(req, timeout=to)
            except HTTPError, e:
                self._addError(e.code, r.target.getAbsoluteUrl())
                continue 
            except URLError, e:
                self._addError(e.reason, r.target.getAbsoluteUrl())
                continue
            except:
                self._addError('Unknown', r.target.getAbsoluteUrl())
                continue
            else:
                result = self.processResponse(response.read().lower(), r.first_pl)
                
                if len(result) is not 0:
                    # looks like it's stored
                    oldinjtype = r.injections[r.first_param]
                    oldinjtype[0][0][0] = "stored"
                    r.injections[r.first_param] = oldinjtype
    
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
                # No GET/POST parameters? Skip to next url 
                if len(target.params) == 0:
                    # print "[X] No paramaters to inject"
                    self.queue.task_done()
                    continue
               
                self._performInjections(target)
                self._checkStoredInjections()
                                
                # Scan complete
                try:                
                    self.queue.task_done()
                except ValueError:
                    pass

#!/usr/bin/env python

try:
    from mechanize import Request, urlopen, URLError, HTTPError,ProxyHandler, build_opener, install_opener, Browser
except ImportError:
    print "\n[X] Please install mechanize module:"
    print "    http://wwwsearch.sourceforge.net/mechanize/\n"
    exit()

from collections import defaultdict
import random
import threading

from core.constants import USER_AGENTS
from core.target import Target

class Crawler(threading.Thread):
    def __init__(self, engine, queue, crawl_links = False, crawl_forms = False):
        threading.Thread.__init__(self)
        self.engine = engine
        self.queue = queue

        self.results = []
        self.errors = {}

        self.crawl_links = crawl_links
        self.crawl_forms = crawl_forms

        self.browser = Browser()
        self._setProxies()
        self._setHeaders()

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

    def _crawlLinks(self, target):
        # If UA is RANDOM we need to refresh browser's headers
        if self.engine.getOption("ua") is "RANDOM": self._setHeaders()
        
        try: self.browser.open(target.getAbsoluteUrl())
        except HTTPError, e:
            self._addError(e.code, target.getAbsoluteUrl())
            return False 
        except URLError, e:
            self._addError(e.reason, target.getAbsoluteUrl())
            return False
        except:
            self._addError('Unknown', target.getAbsoluteUrl())
            return False
        else:
            try:
                links = self.browser.links()
            except:
                print "[X] Can't retrieve links"
                return False

            new_targets = []

            for link in links:
                if link.url.startswith(target.getBaseUrl()):
                    # Local Absolute url
                    new_targets.append(link.url)
                    continue
                elif link.url.startswith("/"):
                    # Local Relative url, starting with /
                    link.url = target.getBaseUrl() + link.url
                    new_targets.append(link.url)
                    continue
                elif link.url.startswith("http://") or link.url.startswith("www."):
                    # Absolute external links starting with http:// or www.
                    continue
                else:
                    # Everything else, should only be local urls not starting with /
                    # If it's not the case they'll return 404 - i can live with that
                    link.url = target.getBaseUrl() + "/" + link.url
                    new_targets.append(link.url)

            # Remove duplicate links
            new_targets = set(new_targets)
            #print "[-] Found %s unique URLs" % len(new_targets)

            # Build new targets
            for t in new_targets:
                self.results.append(Target(t))

    def _crawlForms(self, target):
        # If UA is RANDOM we need to refresh browser's headers
        if self.engine.getOption("ua") is "RANDOM": self._setHeaders()

        try: self.browser.open(target.getAbsoluteUrl())
        except HTTPError, e:
            self._addError(e.code, target.getAbsoluteUrl())
            return False 
        except URLError, e:
            self._addError(e.reason, target.getAbsoluteUrl())
            return False
        except:
            self._addError('Unknown', target.getAbsoluteUrl())
            return False
        else:
            try: 
                forms = self.browser.forms()
            except:
                print "[X] Can't retrieve forms"
                return False

            for form in forms:
                form_data = form.click_request_data()
                
                if form.method is "POST" and form_data[1] is None:
                    # If the post form has no data to send
                    continue
                elif form.method is "GET" and form_data[1] is not None:
                    # GET forms
                    nt = Target(form_data[0]+"?"+form_data[1], method = form.method, data = None)
                    self.results.append(nt)
                else:
                    nt = Target(form_data[0], method = form.method, data = form_data[1])
                    self.results.append(nt)


    def run(self):
        while True:
            try:
                target = self.queue.get(timeout = 1)
            except:
                try:
                    self.queue.task_done()
                except ValueError:
                    pass
            else:

                if self.crawl_links:
                    self._crawlLinks(target)
                if self.crawl_forms:
                    self._crawlForms(target)

                # task done    
                try:
                    self.queue.task_done()
                except ValueError:
                    pass  

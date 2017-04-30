#!/usr/bin/env python
#
# Load proxy from command line or text file
#

import os

def load_proxy(self):
    self.proxy_index = 0
    self.args.proxy_on = False
    self.proxy_list = []

    if self.args.proxy:
        for proxy_item in self.args.proxy.split(','):
            proxy_item = proxy_item.strip()
            if len(proxy_item) >= 7 and proxy_item.find(':') > 0:
                self.proxy_list.append(proxy_item)

        if self.proxy_list:
            self.args.proxy_on = True
        else:
            raise Exception('Invalid proxy Server! Feed sth like 127.0.0.1:8080')

    # Load HTTP proxies from file
    if self.args.proxylist:
        if not os.path.exists(self.args.proxylist):
            raise Exception('Proxy list file not found!')

        with open(self.args.proxylist, 'r') as inFile:
            while True:
                line = inFile.readline().strip()
                if len(line) < 1: break
                if line.find(':') > 0 and len(line) >= 7 and line[line.find(':')+1:].strip().isdigit():
                    self.proxy_list.append(line)

        if self.proxy_list:
            self.args.proxy_on = True
        else:
            raise Exception('Fail to load HTTP proxies from file: no valid proxies in file')

    if self.args.debug and self.proxy_list:
        self.lock.acquire()
        print '[Proxy servers loaded]\n'
        print self.proxy_list
        print '\n' + '*' * self.console_width
        self.lock.release()

    if self.args.checkproxy and not self.proxy_list:
        raise Exception('No proxy servers found, use -proxy or -proxylist to feed some.')

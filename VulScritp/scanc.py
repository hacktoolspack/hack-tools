#!/usr/bin/env python
# -*- coding:utf-8 -*-

# @Author: IcySun

import requests,urllib2,urllib
import socket, json,sys,re

class scanC():

    def use(self):
        print '#' * 50
        print u'\t\t C段扫描'
        print '\t\t\t Code By: IcySun'
        print '\t python scanc.py www.xxx.com(ip) '
        print '#' * 50

    def ipChk(self,in_put):
       pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
       if re.match(pattern, in_put):
          return True
       else:
          return False

    def www2ip(self,name):  
        try:
            result = socket.getaddrinfo(name, None)
            return result[0][4][0]
        except:
            return 0

    def scan(self,ip):
        payload = {'action':'query','ip':ip}
        test_data_urlencode = urllib.urlencode(payload)
        req = urllib2.Request(url = weburl,data = test_data_urlencode)
        try:
            res_data = urllib2.urlopen(req,timeout = 3)
            con = json.loads(res_data.read())
            if isinstance(con['list'],list):
                if len(con['list']) != 0:
                    print ip,con['list'][0]
                    with open('c.txt','a+') as c:
                        c.write(ip+'  '+con['list'][0]+'\n')
            else :
                for (d,x) in con['list'].items():
                    print ip,str(x)
                    with open('c.txt','a+') as c:
                        c.write(ip+'  '+str(x)+'\n')
        except socket.timeout, e:
            pass
        except urllib2.URLError,e:
            pass

def main():
    global weburl
    s = scanC()
    weburl = 'http://www.144118.com/api/Cclass.php'
    if len(sys.argv) != 2:
        s.use()
        sys.exit()
    in_put = sys.argv[1]
    if s.ipChk(in_put):
        ip1 = re.match(r"^\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.+",in_put).group(0)
        for i in xrange(1,255):
            ip = ip1 + str(i)
            s.scan(ip)

    else:
        ip1 = re.match(r"^\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.+",s.www2ip(in_put)).group(0)
        for i in xrange(1,255):
            ip = ip1 + str(i)
            s.scan(ip)

if __name__ == '__main__':
    main()

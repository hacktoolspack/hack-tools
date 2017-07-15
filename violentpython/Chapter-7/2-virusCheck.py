#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import httplib
import time
import os
import optparse
from urlparse import urlparse


def printResults(url):

    status = 200
    host = urlparse(url)[1]
    path = urlparse(url)[2]

    if 'analysis' not in path:
        while status != 302:
            conn = httplib.HTTPConnection(host)
            conn.request('GET', path)
            resp = conn.getresponse()
            status = resp.status
            print '[+] Scanning file...'
            conn.close()
            time.sleep(15)

    print '[+] Scan Complete.'
    path = path.replace('file', 'analysis')
    conn = httplib.HTTPConnection(host)
    conn.request('GET', path)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()

    reResults = re.findall(r'Detection rate:.*\)', data)
    htmlStripRes = reResults[1].\
      replace('&lt;font color=\'red\'&gt;', '').\
      replace('&lt;/font&gt;', '')
    print '[+] ' + str(htmlStripRes)


def uploadFile(fileName):

    print "[+] Uploading file to NoVirusThanks..."
    fileContents = open(fileName,'rb').read()

    header = {'Content-Type': 'multipart/form-data; \
      boundary=----WebKitFormBoundaryF17rwCZdGuPNPT9U'}
            
    params = "------WebKitFormBoundaryF17rwCZdGuPNPT9U"
    params += "\r\nContent-Disposition: form-data; "+\
      "name=\"upfile\"; filename=\""+str(fileName)+"\""
    params += "\r\nContent-Type: "+\
      "application/octet stream\r\n\r\n"
    params += fileContents
    params += "\r\n------WebKitFormBoundaryF17rwCZdGuPNPT9U"
    params += "\r\nContent-Disposition: form-data; "+\
      "name=\"submitfile\"\r\n"
    params += "\r\nSubmit File\r\n"
    params +="------WebKitFormBoundaryF17rwCZdGuPNPT9U--\r\n"
    conn = httplib.HTTPConnection('vscan.novirusthanks.org')
    conn.request("POST", "/", params, header)
    response = conn.getresponse()
    location = response.getheader('location')
    conn.close()
    return location


def main():

    parser = optparse.OptionParser('usage %prog -f <filename>')
    parser.add_option('-f', dest='fileName', type='string',\
      help='specify filename')
    (options, args) = parser.parse_args()
    fileName = options.fileName

    if fileName == None:
        print parser.usage
        exit(0)
    elif os.path.isfile(fileName) == False:
        print '[+] ' + fileName + ' does not exist.'
        exit(0)
    else:
        loc = uploadFile(fileName)
        printResults(loc)


if __name__ == '__main__':
    main()


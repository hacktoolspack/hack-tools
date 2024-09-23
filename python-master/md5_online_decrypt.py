#!/usr/bin/python
# This was written for educational purpose only. Use it at your own risk.
# Author will be not responsible for any damage!
#      __                                           _             __   _    
#     / /_  __  __   ______________ _____  __  __  (_)_  ______  / /__(_)__ 
#    / __ \/ / / /  / ___/ ___/ __ `/_  / / / / / / / / / / __ \/ //_/ / _ \
#   / /_/ / /_/ /  / /__/ /  / /_/ / / /_/ /_/ / / / /_/ / / / / ,< / /  __/
#  /_.___/\__, /   \___/_/   \__,_/ /___/\__, /_/ /\__,_/_/ /_/_/|_/_/\___/ 
#        /____/                         /____/___/                          
#
###############################################################################
# Download huge collections of wordlist:#
#http://ul.to/folder/j7gmyz#
##########################################################################
#
####################################################################
# Need daylie updated proxies?#
#http://j.mp/Y7ZZq9#
################################################################
#
######################################################
#### MD5 Hash Cracker online | offline ######
###################################################

import sys
import time
import urllib2
import urllib 
import re
import hashlib

if len(sys.argv) < 2:
  print '\nUsage:'
  print '\t%s --online [hash..] ' % sys.argv[0]
  print '\t%s --offline [hash..] [dictionary..]'  % sys.argv[0]
  sys.exit(1)

def banner():
  print '''

	|-----------------------------------------------------------------|
        | [#] MD5 Hash Cracker (online | offline)                         |
        | [#] pastebin.com: gelbeseiten				          |
        | [#] Written by: ..:: crazyjunkie ::..                           |
        |-----------------------------------------------------------------|

'''

option   = sys.argv[1]
passwd   = sys.argv[2]

if option == '--online':
  if len(passwd) != 32: 
    print '\n[*] Error: "%s" doesn\'t seem to be a valid MD5 hash "32 bit hexadecimal"' % passwd
  else:
    try:
      banner()
      def myaddr():
        site = 'http://md5.my-addr.com/'
        rest = 'md5_decrypt-md5_cracker_online/md5_decoder_tool.php'
        para = urllib.urlencode({'md5':passwd})
        req  = urllib2.Request(site+rest)
        try:
          fd   = urllib2.urlopen(req, para)
          data = fd.read()
          match= re.search('(Hashed string</span>: )(\w+.\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError:  print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      myaddr()

      def victorov():
        try:
          site = 'http://www.victorov.su/'
          para = 'md5/?md5e=&md5d=%s' % passwd
          req  = urllib2.Request(site+para)
          req.add_header
          opener = urllib2.urlopen(req)
          data = opener.read()
          match = re.search('(<b>)(.+[^>])(</b>)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError:  print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      victorov()
      
      def md5crack():
        site = 'http://www.md5crack.com/'
        rest = 'crackmd5.php'
        para = urllib.urlencode({'term':passwd})
        req = urllib2.Request(site+rest)
        try: 
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search('(Found: md5)(..)(\w+.\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(3))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error seems to be down' % site
      md5crack()
  

      def rednoize():
        site = 'http://md5.rednoize.com/'
        para = 'p&s=md5&q=%s&_=' % passwd
        try:
          req = urllib2.urlopen(site+'?'+para)
          data = req.read()
          if not len(data): print '[-] site: %s\t\t\tPassword: Not found' %site
          else: print '[-] site: %s\t\t\tPassword: %s' % (site, data)
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      rednoize()

      def md5pass():
        site = 'http://www.md5pass.info/'
        para = urllib.urlencode({'hash':passwd, 'get_pass':'Get+Pass'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search('(Password - <b>)(\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      md5pass()

      def md5decryption():
        site = 'http://md5decryption.com/'
        para = urllib.urlencode({'hash':passwd,'submit':'Decrypt+It!'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search(r'(Decrypted Text: </b>)(.+[^>])(</font><br/><center>)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      md5decryption()


      def bigtrapeze():
        site = 'http://www.bigtrapeze.com/'
        rest = 'md5/index.php?query=%s' % passwd
        req = urllib2.Request(site+rest)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.2)\
        Gecko/20100316 AskTbSPC2/3.9.1.14019 Firefox/3.6.2')
        try:
          opener = urllib2.build_opener()
          data = opener.open(req).read()
          match = re.search('(=> <strong>)(\w+.\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      bigtrapeze()

      def cloudcracker():
        site = 'http://www.netmd5crack.com/'
        para = 'cgi-bin/Crack.py?InputHash=%s' % passwd
        try:
          req = urllib.urlopen(site+para)
          data = req.read()
          match = re.search(r'<tr><td class="border">[^<]+</td><td class="border">\
          (?P<hash>[^>]+)</td></tr></tbody></table>', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(hash))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      cloudcracker()


      def hashcracking():
        site = 'http://md5.hashcracking.com/'
        rest = 'search.php'
        para = 'md5=%s' % passwd
        try:
          req = urllib2.urlopen(site+rest+'?'+para)
          data = req.read()
          match = re.search('(is)(.)(\w+.\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(3))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      hashcracking()

      def cloudcracker():
        site = 'http://www.cloudcracker.net/'
        para = urllib.urlencode({'inputbox':passwd, 'submit':'Crack+MD5+Hash!'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search('(this.select)(....)(\w+=")(\w+.\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s\n' % (site, match.group(4))
          else: print '[-] site: %s\t\t\tPassword: Not found\n' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      cloudcracker()
    except KeyboardInterrupt: print '\nTerminated by user ...'
    
elif option == '--offline':
  banner()
  try:
    def offline():
      print '[+] This opertaion will take some time, be patient ...' 
      dictionary = sys.argv[3]
      dic = {}
      shooter = 0
      try:
        f = open(dictionary, 'rb')
        start = time.time()
        for line in f:
          line = line.rstrip()
          dic[line] = hashlib.md5(line).hexdigest()
        for k in dic.keys(): 
          if passwd in dic[k]:
            stop = time.time()
            global spent
            spent = stop - start
            print '\n[-] Hash: %s\t\tData: %s\t\tTime: %.f seconds' % (dic[k], k, spent)
            shooter += 1
        if shooter == 0:  print "\n[*]Password not found in [%s] try the online cracker\n" % dictionary
        f.close()
      except IOError: print '\n[*] Erorr: %s doesn\'t exsit \n' % dictionary
    offline()
  except KeyboardInterrupt: print '\nTerminated by user ...'
  
else: pass

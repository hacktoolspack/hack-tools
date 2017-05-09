#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fiht --<fiht@qq.com>
  Purpose: 找出Mongo中存在sql注入的链接
  Created: 2016年06月26日
"""
import requests

from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
lisu = []
#----------------------------------------------------------------------
def get_info(host):
    """get some infomation of a host"""
    req = ''
    try:
        req = requests.get(host,timeout=10)
        req.encoding = req.apparent_encoding    
        result = re.findall(re.compile('<title>(.*?)</title>',re.L),req.text)
        return result[0]
    except Exception as e:
        print(e)
        return None
#----------------------------------------------------------------------
def fuck():
    """其实她叫main"""
    db = MongoClient('nofiht.ml')['from_tecent']
    for i in db.url.find({'injection':1}):
        if urlparse(i['url'])[1] not in lisu:
            lisu.append(urlparse(i['url'])[1])
            #print(i['url'])
            print(i['url'],get_info(i['url']))
if __name__ == '__main__':
    fuck()
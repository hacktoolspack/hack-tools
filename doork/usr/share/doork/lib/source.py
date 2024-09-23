#!/usr/bin/env python

"""
Copyright (c) 2014 tilt (https://github.com/AeonDave/tilt)
See the file 'LICENSE' for copying permission
"""

import core
from lib.logger import logger
from bs4 import BeautifulSoup

def get_dork_from_exploit_db(value):
    url = 'https://www.exploit-db.com/ghdb/'
    html = core.get_html_from_url(url+str(value))
    if html:
        parser = BeautifulSoup(html.decode('utf-8'), 'html.parser')
        table = parser.find('table',{'class' : 'category-list'})
        if table != None:
            data = table.find('a').get_text().strip()
            if len(data)==0:
                return " "
            return data
        else:
            msg = "exploit-db returned error"
            logger.debug(msg)
            return False
    else:
        msg = "exploit-db returned badly"
        logger.debug(msg)
        return False

def check_exploit_db(num):
    max_errors = 10
    error_pages=0
    while (error_pages < max_errors):
        if (get_dork_from_exploit_db(num+error_pages)):
            break
        else:
            error_pages +=1
    if (error_pages < max_errors):
        return error_pages
    else:
        return False
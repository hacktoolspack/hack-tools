#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from anonBrowser import *


def google(search_term):
    ab = anonBrowser()

    search_term = urllib.quote_plus(search_term)
    response = ab.open('http://ajax.googleapis.com/'+\
      'ajax/services/search/web?v=1.0&q='+ search_term)
    print response.read()

google('Boondock Saint')


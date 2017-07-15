#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib
from anonBrowser import *

class reconPerson:

    def __init__(self,first_name,last_name,\
      job='',social_media={}):
        self.first_name = first_name
        self.last_name = last_name
        self.job = job
        self.social_media = social_media

    def __repr__(self):
        return self.first_name + ' ' +\
          self.last_name + ' has job ' + self.job

    def get_social(self, media_name):
        if self.social_media.has_key(media_name):
            return self.social_media[media_name]

        return None

    def query_twitter(self, query):
        query = urllib.quote_plus(query)
        results = []
        browser = anonBrowser()
        response = browser.open(\
          'http://search.twitter.com/search.json?q='+ query)
        json_objects = json.load(response)
        for result in json_objects['results']:
            new_result = {}
            new_result['from_user'] = result['from_user_name']
            new_result['geo'] = result['geo']
            new_result['tweet'] = result['text']
            results.append(new_result)

        return results


ap = reconPerson('Boondock', 'Saint')
print ap.query_twitter(\
  'from:th3j35t3r since:2010-01-01 include:retweets')


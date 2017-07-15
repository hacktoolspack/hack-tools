#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib
import optparse
from anonBrowser import *

def get_tweets(handle):
    query = urllib.quote_plus('from:' + handle+\
      ' since:2009-01-01 include:retweets')
    tweets = []
    browser = anonBrowser()
    browser.anonymize()

    response = browser.open('http://search.twitter.com/'+\
      'search.json?q='+ query)

    json_objects = json.load(response)
    for result in json_objects['results']:
        new_result = {}
        new_result['from_user'] = result['from_user_name']
        new_result['geo'] = result['geo']
        new_result['tweet'] = result['text']
        tweets.append(new_result)

    return tweets


def load_cities(cityFile):
    cities = []
    for line in open(cityFile).readlines():
	city=line.strip('\n').strip('\r').lower()
	cities.append(city)
    return cities

def twitter_locate(tweets,cities):
    locations = []
    locCnt = 0
    cityCnt = 0
    tweetsText = ""

    for tweet in tweets:
        if tweet['geo'] != None:
            locations.append(tweet['geo'])
	    locCnt += 1 

	tweetsText += tweet['tweet'].lower()

    for city in cities:
	if city in tweetsText:
	    locations.append(city)
	    cityCnt+=1
   
    print "[+] Found "+str(locCnt)+" locations "+\
      "via Twitter API and "+str(cityCnt)+\
      " locations from text search."
    return locations


def main():

    parser = optparse.OptionParser('usage %prog '+\
     '-u <twitter handle> [-c <list of cities>]')
    
    parser.add_option('-u', dest='handle', type='string',\
      help='specify twitter handle')
    parser.add_option('-c', dest='cityFile', type='string',\
      help='specify file containing cities to search')

    (options, args) = parser.parse_args()
    handle = options.handle
    cityFile = options.cityFile

    if (handle==None):
	print parser.usage
	exit(0)

    cities = []
    if (cityFile!=None):
    	 cities = load_cities(cityFile)
    tweets = get_tweets(handle)
    locations = twitter_locate(tweets,cities)
    print "[+] Locations: "+str(locations)

if __name__ == '__main__':
    main()



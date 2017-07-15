#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import optparse
import os
import sqlite3


def printDownloads(downloadDB):
    conn = sqlite3.connect(downloadDB)
    c = conn.cursor()
    c.execute('SELECT name, source, datetime(endTime/1000000,\
    \'unixepoch\') FROM moz_downloads;'
              )
    print '\n[*] --- Files Downloaded --- '
    for row in c:
        print '[+] File: ' + str(row[0]) + ' from source: ' \
            + str(row[1]) + ' at: ' + str(row[2])


def printCookies(cookiesDB):
    try:
        conn = sqlite3.connect(cookiesDB)
        c = conn.cursor()
        c.execute('SELECT host, name, value FROM moz_cookies')

        print '\n[*] -- Found Cookies --'
        for row in c:
            host = str(row[0])
            name = str(row[1])
            value = str(row[2])
            print '[+] Host: ' + host + ', Cookie: ' + name \
                + ', Value: ' + value
    except Exception, e:
        if 'encrypted' in str(e):
            print '\n[*] Error reading your cookies database.'
            print '[*] Upgrade your Python-Sqlite3 Library'


def printHistory(placesDB):
    try:
        conn = sqlite3.connect(placesDB)
        c = conn.cursor()
        c.execute("select url, datetime(visit_date/1000000, \
          'unixepoch') from moz_places, moz_historyvisits \
          where visit_count > 0 and moz_places.id==\
          moz_historyvisits.place_id;")

        print '\n[*] -- Found History --'
        for row in c:
            url = str(row[0])
            date = str(row[1])
            print '[+] ' + date + ' - Visited: ' + url
    except Exception, e:
        if 'encrypted' in str(e):
            print '\n[*] Error reading your places database.'
            print '[*] Upgrade your Python-Sqlite3 Library'
            exit(0)


def printGoogle(placesDB):
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()
    c.execute("select url, datetime(visit_date/1000000, \
      'unixepoch') from moz_places, moz_historyvisits \
      where visit_count > 0 and moz_places.id==\
      moz_historyvisits.place_id;")

    print '\n[*] -- Found Google --'
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'google' in url.lower():
            r = re.findall(r'q=.*\&', url)
            if r:
                search=r[0].split('&')[0]
                search=search.replace('q=', '').replace('+', ' ')
                print '[+] '+date+' - Searched For: ' + search


def main():
    parser = optparse.OptionParser("usage %prog "+\
      "-p <firefox profile path> "
                              )
    parser.add_option('-p', dest='pathName', type='string',\
      help='specify skype profile path')

    (options, args) = parser.parse_args()
    pathName = options.pathName
    if pathName == None:
        print parser.usage
        exit(0)
    elif os.path.isdir(pathName) == False:
        print '[!] Path Does Not Exist: ' + pathName
        exit(0)
    else:

        downloadDB = os.path.join(pathName, 'downloads.sqlite')
        if os.path.isfile(downloadDB):
            printDownloads(downloadDB)
        else:
            print '[!] Downloads Db does not exist: '+downloadDB

        cookiesDB = os.path.join(pathName, 'cookies.sqlite')
        if os.path.isfile(cookiesDB):
            pass
            printCookies(cookiesDB)
        else:
            print '[!] Cookies Db does not exist:' + cookiesDB

        placesDB = os.path.join(pathName, 'places.sqlite')
        if os.path.isfile(placesDB):
            printHistory(placesDB)
            printGoogle(placesDB)
        else:
            print '[!] PlacesDb does not exist: ' + placesDB


if __name__ == '__main__':
    main()


#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import optparse
import os


def printProfile(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute("SELECT fullname, skypename, city, country, \
      datetime(profile_timestamp,'unixepoch') FROM Accounts;")

    for row in c:
        print '[*] -- Found Account --'
        print '[+] User           : '+str(row[0])
        print '[+] Skype Username : '+str(row[1])
        print '[+] Location       : '+str(row[2])+','+str(row[3])
        print '[+] Profile Date   : '+str(row[4])


def printContacts(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute("SELECT displayname, skypename, city, country,\
      phone_mobile, birthday FROM Contacts;")

    for row in c:
        print '\n[*] -- Found Contact --'
        print '[+] User           : ' + str(row[0])
        print '[+] Skype Username : ' + str(row[1])

        if str(row[2]) != '' and str(row[2]) != 'None':
            print '[+] Location       : ' + str(row[2]) + ',' \
                + str(row[3])
        if str(row[4]) != 'None':
            print '[+] Mobile Number  : ' + str(row[4])
        if str(row[5]) != 'None':
            print '[+] Birthday       : ' + str(row[5])


def printCallLog(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute("SELECT datetime(begin_timestamp,'unixepoch'), \
      identity FROM calls, conversations WHERE \
      calls.conv_dbid = conversations.id;"
              )
    print '\n[*] -- Found Calls --'

    for row in c:
        print '[+] Time: '+str(row[0])+\
          ' | Partner: '+ str(row[1])


def printMessages(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute("SELECT datetime(timestamp,'unixepoch'), \
              dialog_partner, author, body_xml FROM Messages;")
    print '\n[*] -- Found Messages --'

    for row in c:
        try:
            if 'partlist' not in str(row[3]):
                if str(row[1]) != str(row[2]):
                    msgDirection = 'To ' + str(row[1]) + ': '
                else:
                    msgDirection = 'From ' + str(row[2]) + ' : '
                print 'Time: ' + str(row[0]) + ' ' \
                    + msgDirection + str(row[3])
        except:
            pass


def main():
    parser = optparse.OptionParser("usage %prog "+\
      "-p <skype profile path> ")
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
        skypeDB = os.path.join(pathName, 'main.db')
        if os.path.isfile(skypeDB):
            printProfile(skypeDB)
            printContacts(skypeDB)
            printCallLog(skypeDB)
            printMessages(skypeDB)
        else:
            print '[!] Skype Database '+\
              'does not exist: ' + skpeDB


if __name__ == '__main__':
    main()

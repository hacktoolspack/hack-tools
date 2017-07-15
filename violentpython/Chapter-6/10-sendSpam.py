#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
import optparse

from email.mime.text import MIMEText
from twitterClass import *
from random import choice

def sendMail(user,pwd,to,subject,text):

    msg = MIMEText(text)
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = subject

    try:
    	smtpServer = smtplib.SMTP('smtp.gmail.com', 587)
    	print "[+] Connecting To Mail Server."
    	smtpServer.ehlo()
    	print "[+] Starting Encrypted Session."
    	smtpServer.starttls()
    	smtpServer.ehlo()
    	print "[+] Logging Into Mail Server."
    	smtpServer.login(user, pwd)
    	print "[+] Sending Mail."
    	smtpServer.sendmail(user, to, msg.as_string())
    	smtpServer.close()
        print "[+] Mail Sent Successfully."

    except:
	print "[-] Sending Mail Failed."


def main():

    parser = optparse.OptionParser('usage %prog '+\
      '-u <twitter target> -t <target email> '+\
      '-l <gmail login> -p <gmail password>')

    parser.add_option('-u', dest='handle', type='string',\
      help='specify twitter handle')

    parser.add_option('-t', dest='tgt', type='string',\
      help='specify target email')

    parser.add_option('-l', dest='user', type='string',\
      help='specify gmail login')

    parser.add_option('-p', dest='pwd', type='string',\
      help='specify gmail password')


    (options, args) = parser.parse_args()
    handle = options.handle
    tgt = options.tgt
    user = options.user
    pwd = options.pwd

    if handle == None or tgt == None\
      or user ==None or pwd==None:
        print parser.usage
        exit(0)


    print "[+] Fetching tweets from: "+str(handle)
    spamTgt = reconPerson(handle)
    spamTgt.get_tweets()
    print "[+] Fetching interests from: "+str(handle)
    interests = spamTgt.find_interests()
    print "[+] Fetching location information from: "+\
      str(handle)
    location = spamTgt.twitter_locate('mlb-cities.txt')


    spamMsg = "Dear "+tgt+","

    if (location!=None):
	randLoc=choice(location)
	spamMsg += " Its me from "+randLoc+"."	

    if (interests['users']!=None):
	randUser=choice(interests['users'])
	spamMsg += " "+randUser+" said to say hello."

    if (interests['hashtags']!=None):
	randHash=choice(interests['hashtags'])
	spamMsg += " Did you see all the fuss about "+\
          randHash+"?"

    if (interests['links']!=None):
	randLink=choice(interests['links'])
	spamMsg += " I really liked your link to: "+\
          randLink+"."

    spamMsg += " Check out my link to http://evil.tgt/malware"
    print "[+] Sending Msg: "+spamMsg

    sendMail(user, pwd, tgt, 'Re: Important', spamMsg)

if __name__ == '__main__':
    main()


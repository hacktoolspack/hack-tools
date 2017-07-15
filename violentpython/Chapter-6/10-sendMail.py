#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText


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
user = 'username'
pwd = 'password'

sendMail(user, pwd, 'target@tgt.tgt',\
  'Re: Important', 'Test Message')


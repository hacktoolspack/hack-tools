#!/usr/bin/python

## concrete.py
## File contains for standard passive modules
## Calls the cmsvulns module 

import string, sys
from modules import cmsvulns
from modules import client

bold = '\033[1m'
normal = '\033[0m'

## Dection function
def detect(target, dir, ssl):
    try:
        if ssl == True: ## Enables SSL

            ## Gets the data from the client.https_get module
            data = client.https_get(target, dir)

        else: ## Uses plain-text HTTP

            ## Get the data from teh client.http_get modules
            data = client.http_get(target, dir)

        ## Reads each line in the new data variable
        for line in string.split(data, '\n'):

            ## Get the line containing the generator tag
            if 'generator' in line:
                ver = line.split("\"")
                version = ver[3].split(" ")

                ## Checks the generator tag contains the concrete5 name
		if version[0] == 'concrete5':
                    if len(version) == 3:

                        ## concrete5 cms found attempts to print the version found
                        print bold, "[+] Found", version[0], version[1], version[2], normal, "via generator tag"

                        ## Runs the cmsvulns.vulns check module against the version
                        cmsvulns.vulncheck(version[2])
                        break

                    else: ## CMS dislclosed but with no version information

                        ## Prints found installation and breaks out of 'if' statements
                        print bold, "[+] Found", version[0], "installation", normal
		        break

		else: ## CMS found is not concrete5

                    ## Prints to screen conrete5 not found and quits
		    print bold, "[-] Not running concrete5!", normal
		    sys.exit(0)

        ## Generator tag not found and searches for the concrete5 base directory
        if not "/concrete/css/" in data:

            ## concrete5 found found an exits
            print bold, "[-] concrete5 installation not detected", normal
            sys.exit(0)

    except Exception, IndexError:
        print IndexError
	pass

    except Exception, error:
	print error
	sys.exit(1)


## The concrete5 enumerate module
def enumerate(target, dir, ssl):

    ## Runs all of the non-aggressive enumeration modules
    fullpath(target, dir, ssl)
    userenum(target, dir, ssl)


## Module to detect full path disclosure vulnerabilities
def fullpath(target, dir, ssl):

    try:
        if ssl == True: ## Enables SSL
            data = client.https_get(target, dir + "concrete/blocks/content/editor_config.php")

        else: ## Uses plain-text HTTP
            data = client.http_get(target, dir + "concrete/blocks/content/editor_config.php")

        for line in string.split(data, '\n'):
            if 'Fatal error' in line:
                line = line.split(" ")
                line = line[8]
                length = len(line)
                length = length - 4
                fpd = line[3:length]

                print bold, "\n [+] Full Path Disclosure found!\r", normal
                print "", fpd, normal, "\r"
				
                if ssl == True:
                    print " https://" + target + dir + "concrete/blocks/content/editor_config.php\n"
                else:
                    print " http://" + target + dir + "concrete/blocks/content/editor_config.php\n"

    except Exception, error:
        print error


## Module to discover disclosed usernames
def userenum(target, dir, ssl):

    try:
        if ssl == True:
            data = client.https_get(target, dir + "index.php/members")
        else:
            data = client.http_get(target, dir + "index.php/members")

        for line in string.split(data, '\n'):
            if 'member-username' in line:
                user = line.split(">")
                user = user[2]
                user = user.split("<")
                user = user[0]
                print bold + "\r [+] Found username: " + normal + user
       	
    except Exception, error:
        print error

#!/usr/bin/env python

"""
Copyright (c) 2016 tilt (https://github.com/AeonDave/doork)
See the file 'LICENSE' for copying permission
"""

import sys, getopt, logging, os

from lib import update
from lib import actions
from lib.logger import logger

# Doork Setup

try:
    options, args = getopt.getopt(sys.argv[1:], 't:wvhguo:', ['target=','wordlist', 'version', 'help', 'updateghdb',  'update', 'output'])
except getopt.GetoptError:
    actions.showhelp()
    sys.exit(1)

target=None
wordlist=None
output=None

for opt, arg in options:
    if opt in ('-h', '--help'):
        actions.showhelp()
        sys.exit(0)
    elif opt in ('-v', '--version'):
        actions.header()
        sys.exit(0)
    elif opt in ('-g', '--updateghdb'):
        actions.header()
        update.update_ghdb()
        sys.exit(0)
    elif opt in ('-u', '--update'):
        actions.header()
        update.update()
        sys.exit(0)
    elif opt in ('-t', '--target'):
        target = arg
    elif opt in ('-w', '--wordlist'):
        wordlist = arg
    elif opt in ('-o', '--output'):
        output = arg
    else:
        actions.header()
        actions.showhelp()
        sys.exit(1)

if not target:
    actions.header()
    actions.showhelp()
    msg = "[-] ERROR: You must provide a target."
    logger.error(msg)
    sys.exit(1)

def main():
    if output:
        handler = logging.FileHandler(output)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        
    logger.info('-----Start-----')

    if target and wordlist:

        if os.path.isfile(wordlist):
            msg = "File exist"
            logger.debug(msg)
            logger.info('[*] Starting dork scanner from'+ wordlist +' on '+ target)
            actions.scan_wordlist(target, wordlist)
            logger.info('[*] Scan completed')
        else:
            msg = "[-] ERROR: File not exist."
            logger.error(msg)
            sys.exit(1)
            
    else:
        logger.info('[*] Starting dork scanner on '+ target)
        actions.scan(target)
        logger.info('[*] Scan completed')

    if output:
        logger.info('[+] File log written: ' + output)
        
    logger.info('-----End-----\n')

if __name__ == '__main__':
    actions.header()
    main()
    sys.exit(0)

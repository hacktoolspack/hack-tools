#!/usr/bin/env python

"""
Copyright (c) 2016 tilt (https://github.com/AeonDave/doork)
See the file 'LICENSE' for copying permission
"""

import sys, os, core, settings

from lib.logger import logger

__version__ = settings.VERSION
__author__ = settings.AUTHOR

def header():
    os.system("clear")

    print ""
    print "         =============================================== "
    print "        |  Doork v{0}\t\t\t\t|".format(__version__)
    print "        |  by {0}\t\t\t\t\t|".format(__author__)
    print "         =============================================== "
    print ""
    print """
    
    
                                .+MNa+...
                               .MMMMMMMMMMMNa+...
               ...............'JMMMNMMNMNNMMMMMMMMMNa+...
              JMMMMMMMMMMMMNM|`JMMNMMNMMMMNMNMMNMMMMMMMMMN.
             .MMNMMMMMMMMMMMM' JMNMMNMMNMMMNMNMMNMNNMNMMNMF
             JMNMM             JMMMMNMNMNMNMMMNMMNMMNMNMMNF
             JMMNM             JMNMMMNMMMNMMNMMNMMMMMNMMNMF
             JMNMM             JMNMNMMNMMNMNMNMMNMNNMMNMMMF
             JMMNM             JMMMMNMMNMMNMMMNMMNMMNMMNMNF
             JMNMN             JMNMMNMNMNMMNMMNMMNMMMNMMNMF
             JMMNM             JMNMMMNMMMNMMNMMNMMNMNMMNMMF
             JMNMM             JMMNMMNMMNMMNMNMMNMMNMMNMMNF
             JMMNM             JMMMNMMNMMNMMNMMNMNMMNMMNMMF
             JNMMN             JMNMMNMMNMMNMMNMMNMMNMNMMNMF
             JMNMM             JMMNMMNMMNMMNMMNMMNMMNMMNMMF
             JMMNM             JMMMNMMNMMNMMNMMNMMNMMNMMNMF
             JMNMM             JMNMMM"7UMNMMNMMNMMNMMNMMNMF
             JMNMM             JMMNM'   dMNMMNMMNMMNMMNMMNF
             JNMMN             JMMMM.   JMMNMMNMMNMMNMMNMMF
             JMMNM             JMNMMN,..MNMMNMNMNMNMMNMMNMF
             JMNMM             JMNMNMNMMNMNMMNMMMNMMNMNMMNF
             JMMNM             JMMMMNMMNMMMNMMNMMNMNMMNMMMF
             JMMNM             JMNMMMNMMNMNMNMMNMMNMMNMNMNF
             JMNMM             JMMNMNMMNMMMNMMNMNMMNMMMMNMF ,o.  ,o
             JNMMM             JMNMMMNMMNMMNMMNMMNMMNMNMMMF ]8[ dP'
             JMMNM             JMMMNMMNMMNMMNMMNMMNMMNMNMMF ]8d8P
             JMNMM             JMNMMNMMNMNMNMNMMNMMNMMMNMNF ]88b.
             JMMNM             JMMNMMNMMNMMMNMMNMMNMNMNMMMF ]8[`8o
             JMNMM             JMMMMNMNMMNMMNMMNMMNMMNMMNMF ]8[  Y8
             JMNMMMMMMNMMMMMM| JMNMMNMMNMMNMMNMMNMMNMMMNMMF
              7MNMNNMMMMNMNMN\ JMNMMNMMNMMNMNMNMMNMMNMNMM@
                 ''''''''''''' ! JMMNMMNMMNMMNMMMNMMMH9"^ 
                               ,MNMMNMNMMNMH9"^ 
                                .THH9"^ 
    
    """

def showhelp():
    print """
    Usage: python doork.py [Target] [Options] [Output]

    Target:
        -t, --target target       Target URL (e.g. "www.site.com")
    Options:
        -w, --wordlist            Select custom wordlist (each line is a dork)
        -h, --help                Show basic help message
        -v, --version             Show program's version number
        -u, --update              Update program from repository
    Output:
        -o, --output file         Print log on a file

    Examples:
        python doork.py -t google.com -o log.log
        python doork.py -u
    """

def scan(target):

    if core.is_valid_url(target):
        msg = "Host Validation OK"
        logger.debug(msg)
        msg = "[+] Url Accepted"
        logger.info(msg)
        msg = "[*] Performing scan"
        logger.info(msg)
        try:
            core.scan(target, settings.WORDLISTFILE)
        except Exception,e: 
            print str(e)
            msg = "[-] ERROR"
            logger.error(msg)

    else:
        msg =  "[-] ERROR: You must provide a valid target. Given: "+ target
        showhelp()
        logger.error(msg)
        sys.exit(1)
 

def scan_wordlist(target, wordlist):
    
    if core.is_valid_url(target):
        msg = "Host Validation OK"
        logger.debug(msg)
        msg = "[+] Url Accepted"
        logger.info(msg)
        msg = "[*] Performing scan"
        logger.info(msg)
        try:
            core.scan(target, wordlist)
        except:
            msg = "[-] ERROR"
            logger.error(msg)

    else:
        msg =  "[-] ERROR: You must provide a valid target. Given: "+ target
        showhelp()
        logger.error(msg)
        sys.exit(1)
        

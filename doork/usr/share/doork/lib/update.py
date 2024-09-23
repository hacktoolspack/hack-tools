#!/usr/bin/env python

"""
Copyright (c) 2016 tilt (https://github.com/AeonDave/doork)
See the file 'LICENSE' for copying permission
"""

import sys, os, settings, source, codecs
from lib.logger import logger
from subprocess import PIPE
from subprocess import Popen
from lib.settings import ROOTDIR
from lib.settings import PLATFORM

retry = 0

def update():
    if not os.path.exists(os.path.join(ROOTDIR, ".git")):
        msg = "[-] Not a git repository. Please checkout the repository from GitHub (e.g. git clone https://github.com/AeonDave/doork.git)"
        logger.error(msg)
    if PLATFORM == 'nt':
        msg = "[-] Please checkout the repository from GitHub with GitHub for Windows (e.g. https://windows.github.com)"
        logger.warning(msg)
        msg = "[*] Repository at https://github.com/AeonDave/doork.git"
        logger.info(msg)
    else:
        msg = "[*] Updating Doork from latest version from the GitHub Repository\n" 
        logger.info(msg)
        Popen("git stash", shell=True, stdout=PIPE, stderr=PIPE)
        Popen("git stash drop", shell=True, stdout=PIPE, stderr=PIPE)
        process = Popen("git pull origin master", shell=True, stdout=PIPE, stderr=PIPE)
        process.communicate()
        success = not process.returncode
                
        if success:
            msg = "[+] Updated!\n"
            logger.info(msg)
            sys.exit(0)
        else:
            msg = "[-] Error!\n" 
            logger.error(msg)
            sys.exit(1)  
            
def update_ghdb():
    global retry
    msg = "Starting ghdb update"
    logger.debug(msg)
    msg = "[*] Updating Database"
    logger.info(msg)
    try:
        fname = settings.WORDLISTFILE
        with open(fname, 'r') as f:
            content = f.readlines()
        f.close()
        num = len(content)+1
        while True:
            dork = source.get_dork_from_exploit_db(num)
            if dork:
                retry = 0
                with codecs.open(fname, 'a', "utf-8") as f:
                    f.write(dork+"\n")
                f.close()
                msg = "[+] Loaded " + dork
                logger.info(msg)
            else:
                check = source.check_exploit_db(num)
                if check:
                    cont = 0
                    while(cont < check):
                        with codecs.open(fname, 'a', "utf-8") as f:
                            space = " "
                            f.write(space+"\n")
                        f.close()
                        cont +=1
                    num += check -1
                else:
                    break
            num += 1
        msg = "Database update ok"
        logger.debug(msg)
        msg = "[+] Database is up to date"
        logger.info(msg)
        sys.exit(1)
    except SystemExit:
        msg = "End update"
        logger.debug(msg)
    except:
        retry +=1
        msg = "Database update error"
        logger.debug(msg)
        msg = "[-] ERROR: Database update error"
        logger.error(msg)
        if (retry<3):
            msg = "[*] Retrying update"
            logger.info(msg)
            update_ghdb()
        else:
            msg = "[-] CRITICAL ERROR: Maybe Exploit-db or network is donwn"
            logger.error(msg)
            sys.exit(1)

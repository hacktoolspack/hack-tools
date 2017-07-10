import argparse
import random
import sys
import getpass
from urllib2 import HTTPError

# Pointers
from lib.pointers import run_proxy_finder
from lib.pointers import run_xss_scan
from lib.pointers import run_sqli_scan
from lib.pointers import run_dork_checker
from lib.pointers import run_hash_cracker
from lib.pointers import run_hash_verification
from lib.pointers import run_port_scan

# Shell
from lib.shell import pybelt_shell

# Settings
from lib.core.settings import LOGGER
from lib.core.settings import VERSION_STRING
from lib.core.settings import WORDLIST_LINKS
from lib.core.settings import CLONE_LINK
from lib.core.settings import create_wordlist
from lib.core.settings import hide_banner
from lib.core.settings import integrity_check
from lib.core.settings import update_pybelt
from lib.core.settings import prompt
from lib.core.settings import verify_py_version


if __name__ == '__main__':

    opts = argparse.ArgumentParser()
    opts.add_argument('-d', '--dork-check', metavar='DORK', dest="dorkcheck",
                      help="Provide a Google dork to check for possible injectable sites")
    opts.add_argument('-c', '--hash-crack', metavar="HASH", dest="hash", nargs=1,
                      help="Specify a hash to crack and a hash type, IE: -c <HASH>:md5 (default all)")
    opts.add_argument('-p', '--port-scan', metavar="HOST", dest="portscan",
                      help="Provide a host to scan for open ports")
    opts.add_argument('-s', '--sqli-scanner', metavar="URL", dest="sqliscan",
                      help="Provide a URL to scan for SQL injection flaws")
    opts.add_argument("-v", '--verify-hash', metavar="HASH", dest="hashcheck",
                      help="Verify a given hash type. (MD5, WHIRLPOOL, SHA256, etc..)")
    opts.add_argument("-f", "--find-proxies", action="store_true", dest="proxysearch",
                      help="Attempt to find some proxies automatically")
    opts.add_argument('-x', '--xss', metavar="URL", dest="xssScan",
                      help="Check if a URL is vulnerable to XSS")
    opts.add_argument('-sl', '--sql-list', metavar="FILE", dest="sqliList",
                      help="Pass a file path with URLS to scan for SQLi vulnerabilities")
    opts.add_argument('-xl', '--xss-list', metavar="FILE", dest="xssList",
                      help="Pass a file path with URLS to scan for XSS vulnerabilities"),
    opts.add_argument('-dl', '--dork-list', metavar="FILE", dest="dorkList",
                      help="Pass a file containing dorks to search check"),
    opts.add_argument('-vhl', '--verify-hash-list', metavar="FILE", dest="verifyHashFile",
                      help="Pass a file of hashes to verify the has type of each hash")

    opts.add_argument("--proxy", metavar="PROXY", dest="configProxy",
                      help="Configure the program to use a proxy when connecting")
    opts.add_argument('--banner', action="store_true", dest="banner",
                      help="Hide the banner")
    opts.add_argument('-l', '--legal', action="store_true", dest="legal",
                      help="Display the legal information")
    opts.add_argument('--version', action="store_true", dest="version",
                      help="Show the version number and exit")
    opts.add_argument('--update', action="store_true", dest="update",
                      help="Update the program to the latest version")
    opts.add_argument('--rand-wordlist', action="store_true", dest="random_wordlist",
                      help="Create a random wordlist to use for dictionary attacks"),
    opts.add_argument('--rand-agent', action="store_true", dest="randomUserAgent",
                      help="Use a random user agent from a file list")

    opts.add_argument('--anon', metavar="ANON", dest="anonLvl",
                      help=argparse.SUPPRESS)
    opts.add_argument('--hash-list', metavar="FILE", dest="hashList",
                      help=argparse.SUPPRESS)
    opts.add_argument('--tamper', metavar="SCRIPT", dest="tamper",
                      help=argparse.SUPPRESS)
    args = opts.parse_args()

    hide_banner(hide=True if args.banner else False,
                legal=True if args.legal else False) if args.version is False else hide_banner(hide=True)

    LOGGER.info("Checking program integrity..")

    try:
        if not verify_py_version():
            LOGGER.fatal("You must have Python version 2.7.x to run this program.")
            exit(1)
        integrity_check()
    except HTTPError:
        check_fail = "Integrity check failed to connect "
        check_fail += "you are running a non verified "
        check_fail += "Pybelt, this may or may not be insecure. "
        check_fail += "Suggestion would be to re-download Pybelt from "
        check_fail += "{}"
        LOGGER.error(check_fail.format(CLONE_LINK))
        answer = prompt("Would you like to continue anyways[y/N] ")
        if answer.upper().startswith("Y"):
            pass
        else:
            err_msg = "Please download the latest version from "
            err_msg += "{}"
            LOGGER.critical(err_msg.format(CLONE_LINK))

    try:
        if len(sys.argv) == 1:  # If you failed to provide an argument
            prompt = pybelt_shell.PybeltConsole()  # Launch the shell
            prompt.prompt = "{}@pybelt > ".format(getpass.getuser())
            info_message = "You have failed to provide a flag so you have been "
            info_message += "redirected to the Pybelt Console. For available "
            info_message += "flags type: 'run -hh', to see help type: 'help' "
            info_message += "to exit the console type: 'quit'"
            try:
                prompt.cmdloop(LOGGER.info(info_message))
            except TypeError as e:
                LOGGER.info("Terminating session...")
                exit(0)

        if args.update is True:  # Update the program
            update_pybelt()

        if args.version is True:  # Show the version number and exit
            hide_banner(hide=True)
            LOGGER.info(VERSION_STRING)
            sys.exit(0)

        if args.random_wordlist is True:  # Create a random wordlist
            LOGGER.info("Creating a random wordlist..")
            create_wordlist(random.choice(WORDLIST_LINKS))
            LOGGER.info("Wordlist created, resuming process..")

        if args.proxysearch is True:  # Find some proxies
            run_proxy_finder()

        if args.hashcheck is not None:  # Check what hash type you have
            run_hash_verification(args.hashcheck)

        if args.verifyHashFile is not None:
            run_hash_verification(None, hash_ver_file=args.verifyHashFile)

        if args.sqliscan is not None:  # SQLi scanning
            run_sqli_scan(args.sqliscan)

        if args.sqliList is not None:  # SQLi file scanning
            run_sqli_scan(None, url_file=args.sqliList)

        if args.dorkcheck is not None:  # Dork checker, check if your dork isn't shit
            run_dork_checker(args.dorkcheck, dork_file=args.dorkList, proxy=args.configProxy)

        if args.dorkList is not None:
            run_dork_checker(None, dork_file=args.dorkList, proxy=args.configProxy)

        if args.hash is not None:  # Try and crack a hash
            run_hash_cracker(args.hash)

        if args.portscan is not None:  # Scan a given host for open ports
            run_port_scan(args.portscan)

        if args.xssScan is not None:  # Scan a URL for XSS vulnerabilities
            run_xss_scan(args.xssScan, args.configProxy, args.randomUserAgent)

        if args.xssList is not None:  # Run a through a file list for XSS vulns
            run_xss_scan(None, url_file=args.xssList)

    except KeyboardInterrupt:  # Why you abort me?! :c
        LOGGER.error("User aborted.")

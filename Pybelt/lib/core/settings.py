import os
import sys
import uuid
import re
import logging
import random
import time
import urllib2
import base64
from colorlog import ColoredFormatter

log_level = logging.INFO
logger_format = "[%(log_color)s%(asctime)s %(levelname)s%(reset)s] %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(log_level)
formatter = ColoredFormatter(logger_format, datefmt="%I:%M:%S")
stream = logging.StreamHandler()
stream.setLevel(log_level)
stream.setFormatter(formatter)
LOGGER = logging.getLogger('pybeltConfig')
LOGGER.setLevel(log_level)
LOGGER.addHandler(stream)

# Full path to everything
PATH = os.getcwd()

# Current version <major><minor><patch><commit>
VERSION = "1.0.12.27"

# Coloring for the version string
TYPE_COLORS = {"dev": 33, "stable": 92}

# Type of version that the program is in "dev" or "stable"
VERSION_STRING = "\033[92m{}\033[0m(\033[{}m\033[1mdev\033[0m)".format(VERSION, TYPE_COLORS["dev"]) if len(
    VERSION) >= 4 else \
    "\033[92m{}\033[0m(\033[{}m\033[1mstable\033[0m)".format(VERSION, TYPE_COLORS["stable"])

# Basic legal disclaimer
LEGAL_DISC = "[!] legal disclaimer: This program is intended for learning purposes, any malicious intent is on you, " \
             "it is the end users responsibility to obey all laws, regulations, and rules of your respective country " \
             "or place of origin. For further information about this please see the legal information file under " \
             "lib/text_files or run the --legal flag"
LONG_LEGAL_DISCLAIMER = open("lib/text_files/legal.txt").read()

# Random saying to display on the banner
SAYING = random.choice(["The Hackers ToolBelt..",
                        "The Hackers Blackbelt..",
                        "The Hackers Multi-Tool..",
                        "The Hackers Gerber..",
                        "The Hackers Best Friend..",
                        "Hacking Made Easy.."])

# URLs to make the program work
PROXY_URL = "http://proxy.tekbreak.com/100/json"
CLONE_LINK = "https://github.com/ekultek/pybelt.git"
MD5_CHECKSUM_URL = "https://raw.githubusercontent.com/Ekultek/Pybelt/master/docs/checksum.md5"

# Random common column names, and random user agents
RANDOM_COMMON_COLUMN = random.choice(open("{}/lib/text_files/common_columns.txt".format(PATH)).readlines())
RANDOM_USER_AGENT = random.choice(open("{}/lib/text_files/agents.txt".format(PATH)).readlines()).strip()

# Search query regex to make sure the URLS have a GET parameter
QUERY_REGEX = re.compile(r"(.*)[?|#](.*){1}\=(.*)")

# Regex to match an IP and port given like so: 127.0.0.1:445
IP_PORT_REGEX = re.compile(r"((\d{1,3}.){3}\d{1,3}:\d+)")

# Regex to match errors thrown by the database
SQLI_ERROR_REGEX = {
    # PostgreSQL
    re.compile(r"PostgreSQL.*ERROR"): "PostgreSQL", re.compile(r"Warning.*\Wpg_.*"): "PostgreSQL",
    re.compile(r"valid PostgreSQL result"): "PostgreSQL", re.compile(r"Npgsql\."): "PostgreSQL",

    # MS SQL Server
    re.compile(r"Driver.* SQL[\-_ ]*Server"): "MS SQL Server", re.compile(r"OLE DB.* SQL Server"): "MS SQL Server",
    re.compile(r"(\W|\A)SQL Server.*Driver"): "MS SQL Server", re.compile(r"Warning.*mssql_.*"): "MS SQL Server",
    re.compile(r"(\W|\A)SQL Server.*[0-9a-fA-F]{8}"): "MS SQL Server", re.compile(r"(?s)Exception.*\WSystem\.Data\.SqlClient\."): "MS SQL Server",
    re.compile(r"(?s)Exception.*\WRoadhouse\.Cms\."): "MS SQL Server",

    # MS Access
    re.compile(r"Microsoft Access Driver"): "MS Access", re.compile(r"JET Database Engine"): "MS Access",
    re.compile(r"Access Database Engine"): "MS Access",

    # Oracle
    re.compile(r"\bORA-[0-9][0-9][0-9][0-9]"): "Oracle", re.compile(r"Oracle error"): "Oracle",
    re.compile(r"Oracle.*Driver"): "Oracle", re.compile(r"Warning.*\Woci_.*"): "Oracle",
    re.compile(r"Warning.*\Wora_.*"): "Oracle",

    # IBM DB2
    re.compile(r"CLI Driver.*DB2"): "IBM DB2", re.compile(r"DB2 SQL error"): "IBM DB2",
    re.compile(r"\bdb2_\w+\("): "IBM DB2",

    # SQLite
    re.compile(r"SQLite/JDBCDriver"): "SQLite", re.compile(r"SQLite.Exception"): "SQLite",
    re.compile(r"System.Data.SQLite.SQLiteException"): "SQLite", re.compile(r"Warning.*sqlite_.*"): "SQLite",
    re.compile(r"Warning.*SQLite3::"): "SQLite", re.compile(r"\[SQLITE_ERROR\]"): "SQLite",

    # Sysbase
    re.compile(r"(?i)Warning.*sybase.*"): "Sysbase", re.compile(r"Sybase message"): "Sysbase",
    re.compile(r"Sybase.*Server message.*"): "Sysbase",

    # MySQL
    re.compile(r"SQL syntax.*MySQL"): "MySQL", re.compile("Warning.*mysql_.*"): "MySQL",
    re.compile(r"valid MySQL result"): "MySQL", re.compile(r"MySqlClient\."): "MySQL",
}

# Regex to match syntax
SYNTAX_REGEX = re.compile(r"\W+$")

# Regex to match an IP address
IP_ADDRESS_REGEX = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|"
                              r"25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|"
                              r"2[0-4][0-9]|25[0-5])$")

# Regex to match any given URL
URL_REGEX = re.compile(
    r'(?i)\b((?:[a-z][\w-]+:(?:|[a-z0-9%])|'
    r'www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4})'
    r'(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+'
    r'(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'
    r'"]))'
)

# Regex to match hash types, these are the only supported hashing types right now
HASH_TYPE_REGEX = {
    re.compile(r"^[a-f0-9]{32}(:.+)?$", re.IGNORECASE):  ["MD5", "MD4", "MD2", "Double MD5",
                                                          "LM", "RIPEMD-128", "Haval-128",
                                                          "Tiger-128", "Skein-256(128)", "Skein-512(128",
                                                          "Lotus Notes/Domino 5", "Skype", "ZipMonster",
                                                          "PrestaShop"],
    re.compile(r"^[a-f0-9]{64}(:.+)?$", re.IGNORECASE):  ["SHA-256", "RIPEMD-256", "SHA3-256", "Haval-256",
                                                          "GOST R 34.11-94", "GOST CryptoPro S-Box",
                                                          "Skein-256", "Skein-512(256)", "Ventrilo"],
    re.compile(r"^[a-f0-9]{128}(:.+)?$", re.IGNORECASE): ["SHA-512", "Whirlpool", "Salsa10",
                                                          "Salsa20", "SHA3-512", "Skein-512",
                                                          "Skein-1024(512)"],
    re.compile(r"^[a-f0-9]{56}$", re.IGNORECASE):        ["SHA-224", "Haval-224", "SHA3-224",
                                                          "Skein-256(224)", "Skein-512(224)"],
    re.compile(r"^[a-f0-9]{40}(:.+)?$", re.IGNORECASE):  ["SHA-1", "Double SHA-1", "RIPEMD-160",
                                                          "Haval-160", "Tiger-160", "HAS-160",
                                                          "LinkedIn", "Skein-256(160)", "Skein-512(160)",
                                                          "MangoWeb Enhanced CMS"],
    re.compile(r"^[a-f0-9]{96}$", re.IGNORECASE):        ["SHA-384", "SHA3-384", "Skein-512(384)",
                                                          "Skein-1024(384)"],
    re.compile(r"^[a-f0-9]{16}$", re.IGNORECASE):        ["MySQL323", "DES(Oracle)", "Half MD5",
                                                          "Oracle 7-10g", "FNV-164", "CRC-64"],
    re.compile(r"^\*[a-f0-9]{40}$", re.IGNORECASE):      ["MySQL5.x", "MySQL4.1"],
    re.compile(r"^[a-f0-9]{48}$", re.IGNORECASE):        ["Haval-192", "Tiger-192", "SHA-1(Oracle)",
                                                          "XSHA (v10.4 - v10.6)"],
    re.compile(r"^\$[\w.]{1}\$\w+\$\S{22}$", re.IGNORECASE): ["Wordpress v4.x", "Wordpress v3.x"],
    re.compile(r"^\$\d\w\$\d+\$\S{53}$", re.IGNORECASE): ["Blowfish"]
}

# Sexy ass banner
BANNER = """\033[94m
  |                          /_/    |
- * -                       /_/   - * -           /_/    /_/
  |  /_/_/_/    /_/   /_/  /_/_/_/  |    _/_/    /_/  /_/_/_/_/    |
    /_/    _/  /_/   /_/  /_/    _/  /_/_/_/_/  /_/    /_/       - * -
   /_/    _/  /_/   /_/  /_/    _/  /_/        /_/    /_/          |
  /_/_/_/      _/_/_/   /_/_/_/_/   /_/_/_/   /_/    /_/_/
 /_/              _/
/_/     |     /_/_/    {}
      \033[94m- * -
        |\033[0m
\033[94m{}
{}\033[0m\n\n
""".format(VERSION_STRING, SAYING.strip(), CLONE_LINK)

# Path the the search results
DORK_SCAN_RESULTS_PATH = r"{}\lib\core\dork_check\scan_results".format(os.getcwd())
PROXY_SCAN_RESULTS = r"{}\lib\core\proxy_finder\proxy_results".format(PATH)

# Error message for when Google blocks your IP address
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE = "\nYou have been temporarily blocked from running Google searches."
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += " As of now there is no way around this. You will need to:\n"
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += "\tA) Change your IP address.\n"
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += "\tB) Wait about an hour for Google to lift the ban.\n"
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += "\tC) Manually check your Dorks.\n"
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += "\tD) Curse my name and this program"

# List of reserved port numbers, these are the ports that you want to check
RESERVED_PORTS = {
    1: "TCP", 5: "RDP (TCP/UDP)", 7: "Echo (TCP/UDP)", 18: "Message Protocol (MSP)",
    20: "FTP (TCP/UDP/SCTP)", 21: "FTP (TCP/UDP/SCTP)", 22: "SSH (TCP/UDP/SCTP)",
    23: "Telnet (TCP/UDP)", 25: "SMTP (TCP/UDP)", 29: "MSG-ICP (TCP/UDP)",
    37: "Time (TCP/UDP)", 42: "WINS [Nameserver] (TCP/UDP)", 43: "WHOIS (TCP/UDP)",
    49: "TACACS (TCP/UDP)", 53: "DNS (TCP/UDP)", 69: "TFT (TCP/UDP)",
    70: "Gopher (TCP/UDP)", 79: "Finger (TCP/UDP)", 80: "HTTP (TCP/UDP/SCTP)",
    103: "GPPTN (TCP/UDP)", 108: "SNAGAS (TCP/UDP)", 109: "POP2 (TCP/UDP)",
    110: "POP3 (TCP/UDP)", 115: "SFTP (TCP/UDP)", 118: "SQL Services (TCP/UDP)",
    119: "NNTP (TCP/UDP)", 135: "Windows RPC (UDP/TCP)", 137: "NETBIOS-NS (TCP/UDP)",
    138: "NETBIOS over TCP (TCP/UDP)", 139: "NETBIOS-SSN (TCP/UDP)",
    143: "IMAP (TCP/UDP)", 150: "SQL-NET (TCP/UDP)", 156: "SQL Service (TCP/UDP)",
    161: "SNMP (TCP/UDP)", 179: "BGP (TCP/UDP/SCTP)", 190: "GACP (TCP/UDP)",
    194: "IRC (TCP/UDP)", 197: "DLS (TCP/UDP)", 389: "LDAP (TCP/UDP)",
    396: "Netware-IP (TCP/UDP)", 443: "HTTPS (TCP/UDP/SCTP)", 444: "SNPP (TCP/UDP)",
    445: "Microsoft-DS (TCP/UDP)", 458: "Apple Quick Time (TCP/UDP)", 546: "DHCPv6 (TCP/UDP)",
    547: "DHCPv6 (TCP/UDP)", 563: "NNTPS (TCP/UDP)", 569: "MS-Rome (TCP/UDP)",
    1080: "Socks (TCP/UDP)", 1433: "MS SQL Server (TCP/UDP)", 1434: "MS SQL Server (TCP/UDP)",
    9001: "TOR (TCP/UDP)"
}

# Links to some wordlists I have laying around
WORDLIST_LINKS = [
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrL2FhODgyMDk5ZWQxYzNlZjAwNWYzYWY2ZjhmYmFhZTExL3Jhdy84ODQ4NjBhNjAzZWQ0MjE3MTgyN2E1MmE3M2VjNzAzMjNhOGExZWY5L2dpc3RmaWxlMS50eHQ=',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrLzAwNWU3OWQ2NmU2MzA2YWI0MzZjOGJmYTc1ZTRiODMwL3Jhdy8xNjY5YjNjMDFmMjRhM2Q2OTMwZDNmNDE1Mjk3ZTg5OGQ1YjY2NGUzL29wZW53YWxsXzMudHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrLzE4NTBmM2EwZGNjNDE0YWZlOGM3NjYyMjBlOTYxYjE4L3Jhdy9iYWQ0NTA0NjcwY2FmM2UxNDY1NWI2ZjJlZGQ0MjJmOTJjMzI2MWI5L215c3BhY2UudHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrLzBkYWU2YTI5MjgzMjcyNmE2Y2MyN2VlNmVjOTdmMTFjL3Jhdy84MWFkOWFkOWUwZjQxMmY2YjIwMTM3MDI2NDcxZGRmNDJlN2JjMjkyL2pvaG4udHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrL2Q4ZjZiYjE2MGEzYzY2YzgyNWEwYWY0NDdhMDM1MDVhL3Jhdy83MWI4NmM5MGU3NDRkZjM0YzY3ODFjM2U0MmFjMThkOGM4ZjdkYjNlL2NhaW4udHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrL2JmM2MwYjQwMTVlYzlkMzY4YzBlNTczNzQ0MTAzYmU1L3Jhdy9lNzBhMThmOTUwNGYwZmMyYjRhMWRmN2M0Mjg2YjcyOWUyMzQ5ODljL29wZW53YWxsXzIudHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrLzQ1ZTExZDBhMzNjZGE1YjM3NDM5OGYyMDgxYjEwZWZiL3Jhdy8wNzQ1ZGMzNjFlZDU5NjJiMjNkYjUxM2FkOWQyOTNlODk0YjI0YTY0L2RjLnR4dA==',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrLzNmMzcxMWUzMDdlOGM0ZTM0MDkzYzI1OGFkN2UzZWZkL3Jhdy9hMjNiYmM3YTgxNTZhOGU5NTU3NmViYTA3MmIwZDg4ZTJmYjk1MzZiL2dtYWlsXzIudHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrL2U3MzE4MGM3MGZmMzY3NDFhM2M4NzIzMDZiNTFhOTU1L3Jhdy9jODE0YjFjOTZiNGJkYzZlYTRlZDE3MmMzNDIwOTg2NTBjOTcyYWZjL2J0NC50eHQ='
]

# Program flags for the CLI console, with description and secondary call flag
TOOL_LIST = {
    "-s": ["(Run a SQLi vulnerability scan on a URL)", "sqli"],
    "-x": ["(Run a cross site scripting scan on a URL)", "xss"],
    "-p": ["(Run a Port scan on a URL or given host)", "port"],
    "-h": ["(Attempt to crack a given hash)", "crack"],
    "-v": ["(Verify the algorithm used for a given hash)", "verify"],
    "-d": ["(Do a dork check to verify if your dork is good)", "dork"],
    "-f": ["(Find usable proxies)", "proxy"],
    "-u": ["(Update the program)", "update"],
    "-hh": ["(Produce a help menu with basic descriptions)", "help"],
    "-sl": ["(Provide a file path to search for SQL injection)", "sql list"],
    "-xl": ["(Provide a file path to search for XSS vulns)", "xss file"],
    "-dl": ["(Provide a file path of dorks to scan", "dork list"],
    "-vhl": ["(Provide a file of hashes to verify the types", "v hash list"]
}


def create_random_filename():
    """ Create a random file name
    >>> print(create_random_filename())
    56558c08-ee1f-40b4-b048-be4c4066f8b6 """
    return str(uuid.uuid4())


def decode64(string):
    """ Decode a string from base64 """
    return base64.b64decode(string)


def prompt(question):
    """ Ask a question.. """
    return raw_input("[{} PROMPT] {}".format(time.strftime("%I:%M:%S"), question))


def create_wordlist(b64link):
    """ Create a word list from a base64encoded URL by decoding it and connecting to it"""
    path = "{}/lib/text_files/wordlist.txt".format(PATH)
    data = urllib2.urlopen(base64.b64decode(b64link)).read()
    open(path, "w").close()
    with open(path, 'a+') as wordlist:
        for word in data:
            wordlist.write(word)
    return


def create_dir(dir_path):
    """ Create a directory if it doesn't exist """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def hide_banner(hide=False, legal=False):
    """ Hide the banner """
    if hide is False:
        print(BANNER + "\033[91m{}\033[0m".format(LEGAL_DISC) + "\n") if legal is False else \
            BANNER + "\033[91m{}\033[0m".format(LONG_LEGAL_DISCLAIMER + "\n")
    else:
        return


def update_pybelt():
    """ Update the program """
    import subprocess
    LOGGER.info("Updating pybelt..")
    updater = subprocess.check_output(["git", "pull", "origin", "master"])
    if "Already up-to-date." in updater:
        LOGGER.warn("Pybelt is even with origin master.")
        exit(0)
    elif "error" or "Error" in updater:
        error_message = "Unable to update Pybelt, an error occurred "
        error_message += "the newest version can be found here: {}".format(CLONE_LINK)
        LOGGER.error(error_message)
        exit(1)
    else:
        LOGGER.info("Pybelt has been updated successfully to {}".format(VERSION))
        exit(0)


def integrity_check(url=MD5_CHECKSUM_URL):
    """ Check the integrity of the application """
    if open("{}/docs/checksum.md5".format(PATH)).read() == urllib2.urlopen(url).read():
        pass
    else:
        checksum_fail = "MD5 sums did not match from origin master, "
        checksum_fail += "integrity check has failed, this could be because "
        checksum_fail += "there is a new version available."
        LOGGER.fatal(checksum_fail)
        update = prompt("Would you like to update to the latest version[y/N]: ")
        if update.upper().startswith("Y"):
            update_pybelt()
        else:
            pass


def replace_http(url):
    """ Replace the http/https in a URL with www.
    >>> replace_http("http://google.com")
    www.google.com """
    data_regex = re.compile(r"^https?://")
    if data_regex.match(url) and "www." not in url:
        data = url.split("//")
        data[0] = "www."
        return ''.join(data)
    elif "www." in url:
        return url.split("//")[1]
    else:
        return url


def verify_py_version():
    version_tuple = sys.version_info
    version = "{}.{}".format(version_tuple[0], version_tuple[1])
    if version >= "2.7" <= "3.0":
        return True
    else:
        return False

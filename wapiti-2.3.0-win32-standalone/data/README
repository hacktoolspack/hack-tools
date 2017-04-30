                                WAPITI - VERSION 2.3.0
                    Wapiti is a web application security auditor.
                           http://wapiti.sourceforge.net/
                      http://www.ict-romulus.eu/web/wapiti/home


Requirements
============
In order to work correctly, Wapiti needs :
+ Python 2.x where x is >= 6 (2.6, 2.7...)
+ python-requests v1.2.3 or more ( http://docs.python-requests.org/en/latest/ )
+ BeautifulSoup ( http://www.crummy.com/software/BeautifulSoup/ )
+ python-xml


How it works
============

Wapiti works as a "black-box" vulnerability scanner,  that means it won't
study the source code of web applications but will work like a  fuzzer,
scanning the pages of the deployed web application, extracting links and
forms  and attacking  the scripts, sending payloads and looking for error
messages, special strings or abnormal behaviors.


General features
================

+ Generates vulnerability reports in various formats (HTML, XML, JSON, TXT...)
+ Can suspend and resume a scan or an attack
+ Can give you colors in the terminal to highlight vulnerabilities
+ Different levels of verbosity
+ Fast and easy way to activate/deactivate attack modules
+ Adding a payload can be as easy as adding a line to a text file


Browsing features
=================

+ Support HTTP and HTTPS proxies
+ Authentication via several methods : Basic, Digest, Kerberos or NTLM
+ Ability to restrain the scope of the scan (domain, folder, webpage)
+ Automatic removal of a parameter in URLs
+ Safeguards against scan endless-loops (max number of values for a parameter)
+ Possibility to set the first URLs to explore (even if not in scope)
+ Can exclude some URLs of the scan and attacks (eg: logout URL)
+ Import of cookies (get them with the wapiti-cookie and wapiti-getcookie tools)
+ Can activate / deactivate SSL certificates verification
+ Extract URLs from Flash SWF files
+ Try to extract URLs from javascript (very basic JS interpreter)
+ HTML5 aware (understand recent HTML tags)


Supported attacks
=================

+ Database Injection (PHP/ASP/JSP SQL Injections and XPath Injections)
+ Cross Site Scripting (XSS) reflected and permanent
+ File disclosure detection (local and remote include, require, fopen,
  readfile...)
+ Command Execution detection (eval(), system(), passtru()...)
+ XXE (Xml eXternal Entity) injection
+ CRLF Injection
+ Search for potentially dangerous files on the server (thanks to the Nikto db)
+ Bypass of weak htaccess configurations
+ Search for copies (backup) of scripts on the server

Wapiti supports both GET and POST HTTP methods for attacks.
It also supports multipart and can inject payloads in filenames (upload).
Display a warning when an anomaly is found (for example 500 errors and timeouts)
Makes the difference  beetween permanent  and reflected  XSS vulnerabilities.


How to get the best results
===========================

To find more vulnerabilities (as some attacks are error-based), you can modify
your webserver configurations.

For example, you can set the following values in your PHP configuration :
safe_mode = Off
display_errors = On (recommended)
magic_quotes_gpc = Off
allow_url_fopen = On
mysql.trace_mode = On


Where to get help
=================

In the prompt, just type the following command to get the basic usage :
python wapiti.py -h
You can also take a look at the manpage.

If you find a bug, fill a ticket on the bugtracker :
https://sourceforge.net/p/wapiti/bugs/


How to help the Wapiti project
==============================

You can :
+ Support the project by making a donation ( http://sf.net/donate/index.php?group_id=168625 )
+ Create or improve attack modules
+ Create or improve report generators
+ Work on the JS interpreter (lamejs)
+ Send bugfixes, patches...
+ Write some GUIs
+ Create some tools to convert cookies from browsers to Wapiti JSON format
+ Improve the Flash SWF parser (write a basic ABC interpreter ?)
+ Create a tool to convert PCAP files to Wapiti XML status files
+ Translate Wapiti in your language
+ Talk about Wapiti around you


What is included with Wapiti
============================

Wapiti comes with :
+ a modified version of PyNarcissus (MPL 1.1 License),
  see https://code.google.com/p/pynarcissus/
+ Kube CSS framework ( see http://imperavi.com/kube/ ) and jQuery
  for HTML report generation.


Source code structure (wapitiCore directory)
=====================================
.
|-- attack  # attack modules used for the vulnerabilities Wapiti can detect
|   |-- __init__.py
|   |-- attack.py        # Base for all attack modules
|   |-- mod_backup.py    # This module search backup of scripts on the server
|   |-- mod_blindsql.py  # Time-based blind sql scanner
|   |-- mod_crlf.py      # Search for CR/LF injection in HTTP headers
|   |-- mod_exec.py      # Module used to detect command execution vulnerabilities
|   |-- mod_file.py      # Search for include()/fread() and other file handling vulns
|   |-- mod_htaccess.py  # Try to bypass weak htaccess configurations
|   |-- mod_nikto.py     # Use a Nikto database to search for potentially dangerous files
|   |-- mod_permanentxss.py  # Look for permanent XSS
|   |-- mod_sql.py       # Standard error-based SQL injection scanner
|   `-- mod_xss.py       # Module for XSS detection
|
|-- config
|   |-- attacks   # Here are the text files where you can add payloads
|   |   |-- backupPayloads.txt
|   |   |-- blindSQLPayloads.txt
|   |   |-- execPayloads.txt
|   |   |-- fileHandlingPayloads.txt
|   |   `-- xssPayloads.txt
|   |
|   |-- language   # Compiled language files (.mo)
|   |   |-- en
|   |   |   `-- LC_MESSAGES
|   |   |       `-- wapiti.mo
|   |   |-- es
|   |   |   `-- LC_MESSAGES
|   |   |       `-- wapiti.mo
|   |   |-- de
|   |   |   `-- LC_MESSAGES
|   |   |       `-- wapiti.mo
|   |   |-- fr
|   |   |   `-- LC_MESSAGES
|   |   |       `-- wapiti.mo
|   |   `-- ms
|   |       `-- LC_MESSAGES
|   |           `-- wapiti.mo
|   |
|   |-- reports
|   |   `-- generators.xml  # Database of report engines
|   |
|   `-- vulnerabilities  # Info about vulnerability types (references etc)
|       |-- anomalies.xml
|       `-- vulnerabilities.xml
|
|-- file  # XML parsers used by Wapiti
|   |-- __init__.py
|   |-- anomalyxmlparser.py
|   |-- auxtext.py
|   |-- reportgeneratorsxmlparser.py
|   `-- vulnerabilityxmlparser.py
|
|-- language  # Manage internationalization
|   |-- __init__.py
|   |-- vulnerability.py  # Common strings used by Wapiti
|   `-- language.py
|
|-- language_sources
|   |-- de.po
|   |-- en.po
|   |-- es.po
|   |-- file_list.txt
|   |-- fr.po
|   |-- generateSources.sh  # Script to generate .po files from source code
|   |-- generateTranslations.sh  # Script to compile .po files to .mo files
|   `-- ms.po
|
|-- net
|   |-- HTTP.py    # Wrapper around python-requests, contains HTTP,
|   |              # HTTPResource and HTTPResponse classes.
|   |-- __init__.py
|   |-- crawlerpersister.py  # Class used to store and load scan status
|   |-- jsoncookie.py  # Library to load and save cookies to JSON files
|   |-- jsparser
|   |   |-- __init__.py
|   |   |-- jsparser.py  # Modified version of the PyNarcissus parser
|   |   |
|   |-- lamejs.py  # Home-made and lame JS interpreter using PyNarcissus
|   |-- lswww.py   # HTML parsing is made here
|   `-- swf_parser.py  # Home-made Flash SWF parser, not an ABC interpreter
|
|-- report   # Report generators
|   |-- __init__.py
|   |-- htmlreportgenerator.py  # The HTML generator is based on the JSON one
|   |-- jsonreportgenerator.py
|   |-- openvasreportgenerator.py  # Needs some more work
|   |-- reportgenerator.py   # Abstract class
|   |-- reportgeneratorinfo.py
|   |-- txtreportgenerator.py
|   |-- vulneranetxmlreportgenerator.py
|   `-- xmlreportgenerator.py
|
`-- report_template  # Template used for HTML reports
    |-- css
    |   |-- kube.css
    |   |-- kube.min.css
    |   `-- master.css
    |-- index.html
    |-- js
    |   |-- jquery-1.9.1.min.js
    |   |-- kube.buttons.js
    |    `-- kube.tabs.js
    `-- logo_clear.png

Licensing
=========

Wapiti is released under the GNU General Public License version 2 (the GPL).
Source code is available on SourceForge :
https://sourceforge.net/projects/wapiti/

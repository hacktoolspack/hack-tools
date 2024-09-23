#
# This file is part of fimap.
#
# Copyright(c) 2009-2010 Iman Karim(ikarim2s@smail.inf.fh-brs.de).
# http://fimap.googlecode.com
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

from tempfile import mkstemp
from ftplib import FTP
from ftplib import error_perm
from config import settings
import xml.dom.minidom
from base64 import b64encode
import pickle
import ntpath
import baseTools
import shutil
import posixpath
import os.path
import sys

DEFAULT_AGENT = "fimap.googlecode.com"

import urllib, httplib, copy, urllib2
import string,random,os,socket, os.path

__author__="Iman Karim(ikarim2s@smail.inf.fh-brs.de)"
__date__ ="$30.08.2009 20:02:04$"

import urllib2
import string,random,os,socket

new_stuff = {}

class baseClass (object):
    
    XML_Result  = None
    XML_RootItem = None
    homeDir = os.path.expanduser("~")
    
    LOG_ERROR = 99
    LOG_WARN  = 98
    LOG_DEVEL = 1
    LOG_DEBUG = 2
    LOG_INFO  = 3
    LOG_ALWAYS= 4
    
    TIMEOUT = 30
    
    tools = baseTools.baseTools()

    def __init__(self, config):
        self.tools.initLog(config)

        self.config = config
        self.logFilePath = None
        self.__init_logfile()
        self.__logfile
        self._load()
        self.xmlfile = os.path.join(self.homeDir, "fimap_result.xml")
        self.XML_Result = None

        baseClass.TIMEOUT = config["p_ttl"]

        if (self.XML_Result == None):
            self.XML_RootItem = None
            self.__init_xmlresult()

    def __init_xmlresult(self):
        xmlfile = self.xmlfile
        if (os.path.exists(xmlfile)):
            self.XML_Result = xml.dom.minidom.parse(xmlfile)
            self.XML_RootItem = self.XML_Result.firstChild
        else:
            self.XML_Result = xml.dom.minidom.Document()
            self.XML_RootItem = self.XML_Result.createElement("fimap")
            self.XML_Result.appendChild(self.XML_RootItem)

    def _createXMLElement(self, Key):
        elem = self.XML_Result.createElement(Key)
        return(elem)

    def _setAttrib(self, Node, Key, Value):
        Node.setAttribute(Key, Value)

    def _appendXMLChild(self, Parent, Child):
        Parent.appendChild(Child)

    def _getXML(self):
        return(self.XML_Result.toprettyxml(indent="  "))

    def _load(self):
        # Should be implemented
        pass

    def _log(self, txt, LVL):
        self.tools._log(txt, LVL)

    def getRandomStr(self):
        return(self.tools.getRandomStr())

    def __init_logfile(self):
        self.logFilePath = os.path.join(self.homeDir, "fimap.log")
        self.__logfile = open(self.logFilePath, "a")

    def _writeToLog(self, txt):
        self.__logfile.write("%s\n" %(txt))

    def drawBox(self, boxheader, boxarr):
        self.tools.drawBox(boxheader, boxarr)

    def addXMLLog(self, rep, t, f):
        if (not self.existsXMLEntry(rep.getDomain(), f, rep.getPath())):
            elem = self.findDomainNode(rep.getDomain())
            elem_vuln = self._createXMLElement("vuln")
            self._setAttrib(elem_vuln, "file", f)
            self._setAttrib(elem_vuln, "prefix", rep.getPrefix())
            self._setAttrib(elem_vuln, "suffix", rep.getSurfix())
            self._setAttrib(elem_vuln, "appendix", rep.getAppendix())
            self._setAttrib(elem_vuln, "mode", t)
            self._setAttrib(elem_vuln, "path", rep.getPath())
            self._setAttrib(elem_vuln, "param", rep.getVulnKey())
            self._setAttrib(elem_vuln, "paramvalue", rep.getVulnKeyVal())
            self._setAttrib(elem_vuln, "postdata", rep.getPostData())
            self._setAttrib(elem_vuln, "kernel", "")
            self._setAttrib(elem_vuln, "language", rep.getLanguage())
            
            headers_pickle = pickle.dumps(rep.getHeader())
            headers_pickle = b64encode(headers_pickle)
            self._setAttrib(elem_vuln, "header_dict", headers_pickle)
            
            self._setAttrib(elem_vuln, "header_vuln_key", rep.getVulnHeader())
            
            os_ = "unix"
            if (rep.isWindows()):
                os_ = "win"
            
            self._setAttrib(elem_vuln, "os", os_)
            
            if (rep.isRemoteInjectable()):
                self._setAttrib(elem_vuln, "remote", "1")
            else:
                self._setAttrib(elem_vuln, "remote", "0")

            if (rep.isBlindDiscovered()):
                self._setAttrib(elem_vuln, "blind", "1")
            else:
                self._setAttrib(elem_vuln, "blind", "0")

            self._setAttrib(elem_vuln, "ispost", str(rep.isPost))
                
            self._appendXMLChild(elem, elem_vuln)
            self._appendXMLChild(self.XML_RootItem, elem)

            if (t.find("x") != -1 or t.find("R") != -1):
                try:
                    new_stuff[rep.getDomain()] += 1
                except:
                    new_stuff[rep.getDomain()] = 1

    def updateKernel(self, domainnode, kernel):
        self._log("Updating kernel version in XML to '%s'"%(kernel), self.LOG_DEVEL)
        self._setAttrib(domainnode, "kernel", kernel)

    def getKernelVersion(self, domainnode):
        ret = domainnode.getAttribute("kernel")
        if (ret == ""): ret = None
        return(None)

    def findDomainNode(self, domain):
        elem = None
        for c in self.XML_RootItem.childNodes:
            if (c.nodeName != "#text"):
                c.getAttribute("hostname")
                if (c.getAttribute("hostname") == domain):
                    return(c)

        elem      = self._createXMLElement("URL")
        self._setAttrib(elem, "hostname", domain)
        return elem

    def getDomainNodes(self):
        ret = self.XML_RootItem.getElementsByTagName("URL")
        return(ret)

    def getNodesOfDomain(self, Domain):
        ret = []
        elem = self.findDomainNode(Domain)
        return(elem.getElementsByTagName("vuln"))

    def existsDomain(self, domain):
        for c in self.XML_RootItem.childNodes:
            if (c.nodeName != "#text"):
                c.getAttribute("hostname")
                if (c.getAttribute("hostname") == domain):
                    return(True)
        return(False)

    def existsXMLEntry(self, domain, file, path):
        elem = self.findDomainNode(domain)
        for c in elem.childNodes:
            if (c.nodeName != "#text"):
                f = c.getAttribute("file")
                p = c.getAttribute("path")
                if (f == file and p == path):
                    return(True)
        return(False)

    def testIfXMLIsOldSchool(self):
        already_warned = False
        for c in self.XML_RootItem.childNodes:
            if (c.nodeName != "#text"):
                if (c.nodeName == "URL"):
                    for cc in c.childNodes:
                        toss_warn = False
                        if (cc.nodeName == "vuln"):
                            if (cc.getAttribute("language") == None or cc.getAttribute("language") == ""):
                                self._setAttrib(cc, "language", "PHP")
                                toss_warn = True
                            if (cc.getAttribute("os") == None or cc.getAttribute("os") == ""):
                                self._setAttrib(cc, "os", "unix")
                                toss_warn = True
                        
                        if (toss_warn and not already_warned):
                            self._log("You have an old fimap_result.xml file!", self.LOG_WARN)
                            self._log("I am going to make it sexy for you now very quickly...", self.LOG_WARN)
                            already_warned = True
        if (already_warned):
            # XML has changed
            backupfile = os.path.join(self.homeDir, "fimap_result.backup")
            if (os.path.exists(backupfile)):
                self._log("WARNING: I wanted to backup your old fimap_result to: %s" %(backupfile), self.LOG_WARN)
                self._log("But this file already exists! Please define a backup path:", self.LOG_WARN)
                backupfile = raw_input("Backup path: ")
            print "Creating backup of your original XML to '%s'..." %(backupfile)
            shutil.copy(self.xmlfile, backupfile)
            print "Committing changes to orginal XML..."
            self.saveXML()
            print "All done."
            print "Please rerun fimap."
            sys.exit(0)
        
    def mergeXML(self, newXML):
        newVulns = newDomains = 0
        doSave = False
        XML_newPlugin = xml.dom.minidom.parse(newXML)
        XML_newRootitem = XML_newPlugin.firstChild
        for c in XML_newRootitem.childNodes:
            if (c.nodeName != "#text" and c.nodeName == "URL"):
                hostname = str(c.getAttribute("hostname"))
                for cc in c.childNodes:
                    addit = True
                    if (cc.nodeName != "#text" and cc.nodeName == "vuln"):
                        new_path = str(cc.getAttribute("path"))
                        new_file = str(cc.getAttribute("file"))

                        if (not self.existsXMLEntry(hostname, new_file, new_path)):
                            doSave = True
                            print "Adding new informations from domain '%s'..." %(hostname)
                            domainNode = self.findDomainNode(hostname)
                            self._appendXMLChild(domainNode, cc)
                            newVulns += 1
                            if (not self.existsDomain(hostname)):
                                self._appendXMLChild(self.XML_RootItem, domainNode)
                                newDomains += 1
                             
        if (doSave):
            print "Saving XML...",
            self.saveXML()
            print "All done."
        return(newVulns, newDomains)
                    

    def saveXML(self):
        self._log("Saving results to '%s'..."%self.xmlfile, self.LOG_DEBUG)
        f = open(self.xmlfile, "w")
        f.write(self.cleanUpLines(self._getXML()))
        f.close()

    def cleanUpLines(self, xml):
        ret = ""
        for ln in xml.split("\n"):
            if (ln.strip() != ""):
                ret = ret + ln + "\n"
        return(ret)

    def FTPuploadFile(self, content, suffix):
        host = settings["dynamic_rfi"]["ftp"]["ftp_host"]
        user = settings["dynamic_rfi"]["ftp"]["ftp_user"]
        pw   = settings["dynamic_rfi"]["ftp"]["ftp_pass"]
        path = os.path.dirname(settings["dynamic_rfi"]["ftp"]["ftp_path"])
        file_= os.path.basename(settings["dynamic_rfi"]["ftp"]["ftp_path"])
        http = settings["dynamic_rfi"]["ftp"]["http_map"]
        temp = mkstemp()[1]
        hasCreatedDirStruct = False
        
        # Default case return values:
        rethttp = http+ suffix
        retftp  = os.path.join(path, file_) + suffix

        directory = None
        # Check if the file needs to be in a directory.
        if (suffix.find("/") != -1):
            http = os.path.dirname(http)
            # Yep it has to be in a directory...
            tmp = self.removeEmptyObjects(suffix.split("/"))
            if suffix.startswith("/"):
                # Directory starts immediatly
                directory = os.path.join(file_, tmp[0]) # Concat the first directory to our path 
                for d in tmp[1:-1]:                     # Join all directorys excluding first and last token.
                    directory = os.path.join(directory, d)
                suffix = suffix[1:]                     # Remove the leading / from the suffix.
                file_ = tmp[-1]                         # The actual file is the last token.
                rethttp = settings["dynamic_rfi"]["ftp"]["http_map"] # Return http path
                retftp  = settings["dynamic_rfi"]["ftp"]["ftp_path"] # and ftp file path.
                hasCreatedDirStruct = True              # Say fimap that he should delete the directory after payloading.
            else:
                # File has a suffix + directory...
                subsuffix = suffix[:suffix.find("/")]   # Get the attachment of the file.
                directory = file_ + subsuffix           # Concat the attachment to the user defined filename.
                for d in tmp[1:-1]:                     # Concat all directorys excluding first and last token.
                    directory = os.path.join(directory, d)
                suffix = suffix[suffix.find("/")+1:]    # Get rest of the path excluding the file attachment.
                file_ = tmp[-1]                         # Get the actual filename.
                rethttp = settings["dynamic_rfi"]["ftp"]["http_map"]
                retftp  = settings["dynamic_rfi"]["ftp"]["ftp_path"] + subsuffix
                hasCreatedDirStruct = True
            
        else:
            file_ = file_ + suffix
        
        # Write payload to local drive
        f = open(temp, "w")
        f.write(content)
        f.close()
        f = open(temp, "r")

        # Now toss it to your ftp server
        self._log("Uploading payload (%s) to FTP server '%s'..."%(temp, host), self.LOG_DEBUG)
        ftp = FTP(host, user, pw)
        ftp.cwd(path)
        
        # If the path is in a extra directory, we will take care of it now
        if (directory != None):
            self._log("Creating directory structure '%s'..."%(directory), self.LOG_DEBUG)
            for dir_ in directory.split("/"):
                try:
                    ftp.cwd(dir_)
                except error_perm:
                    self._log("mkdir '%s'..."%(dir_), self.LOG_DEVEL)
                    ftp.mkd(dir_)
                    ftp.cwd(dir_)
                

        ftp.storlines("STOR " + file_, f)
        ftp.quit()
        ret = {}
        ret["http"] = rethttp
        ret["ftp"] =  retftp
        ret["dirstruct"] = hasCreatedDirStruct
        f.close()
        return(ret)

    def FTPdeleteFile(self, file):
        host = settings["dynamic_rfi"]["ftp"]["ftp_host"]
        user = settings["dynamic_rfi"]["ftp"]["ftp_user"]
        pw   = settings["dynamic_rfi"]["ftp"]["ftp_pass"]
        self._log("Deleting payload (%s) from FTP server '%s'..."%(file, host), self.LOG_DEBUG)
        ftp = FTP(host, user, pw)
        ftp.delete(file)
        ftp.quit()

    def FTPdeleteDirectory(self, directory, ftp = None):
        host = settings["dynamic_rfi"]["ftp"]["ftp_host"]
        user = settings["dynamic_rfi"]["ftp"]["ftp_user"]
        pw   = settings["dynamic_rfi"]["ftp"]["ftp_pass"]
        if ftp == None: 
            self._log("Deleting directory recursivly from FTP server '%s'..."%(host), self.LOG_DEBUG)
            ftp = FTP(host, user, pw)
        
        ftp.cwd(directory)
        for i in ftp.nlst(directory):
            try:
                ftp.delete(i)
            except:
                self.FTPdeleteDirectory(i, ftp)
            
        ftp.cwd(directory)
        ftp.rmd(directory)


    def putLocalPayload(self, content, append):
        fl = settings["dynamic_rfi"]["local"]["local_path"] + append
        dirname = os.path.dirname(fl)
        if (not os.path.exists(dirname)):
            os.makedirs(dirname)
        up = {}
        
        up["local"] = settings["dynamic_rfi"]["local"]["local_path"]
        if append.find("/") != -1 and (not append.startswith("/")):
            up["local"] = settings["dynamic_rfi"]["local"]["local_path"] + append[:append.find("/")]
        up["http"] = settings["dynamic_rfi"]["local"]["http_map"]
        f = open(fl, "w")
        f.write(content)
        f.close()
        
        return(up)

    def deleteLocalPayload(self, directory):
        if(os.path.exists(directory)):
            if (os.path.isdir(directory)):
                shutil.rmtree(directory)
            else:
                os.remove(directory)
                

    def removeEmptyObjects(self, array, empty = ""):
        ret = []
        for a in array:
            if a != empty:
                ret.append(a)
        return(ret)

    def relpath_unix(self, path, start="."):
        # Relpath implementation directly ripped and modified from Python 2.6 source.
        sep="/"
        
        if not path:
            raise ValueError("no path specified")
        
        start_list = posixpath.abspath(start).split(sep)
        path_list = posixpath.abspath(path).split(sep)
        # Work out how much of the filepath is shared by start and path.
        i = len(self.commonprefix([start_list, path_list]))
        rel_list = [".."] * (len(start_list)-i) + path_list[i:]
        if not rel_list:
            return "."
        return posixpath.join(*rel_list)


    def relpath_win(self, path, start="."):
        """Return a relative version of a path"""
        sep="\\"

        if not path:
            raise ValueError("no path specified")
        start_list = ntpath.abspath(start).split(sep)
        path_list = ntpath.abspath(path).split(sep)
        if start_list[0].lower() != path_list[0].lower():
            unc_path, rest = ntpath.splitunc(path)
            unc_start, rest = ntpath.splitunc(start)
            if bool(unc_path) ^ bool(unc_start):
                raise ValueError("Cannot mix UNC and non-UNC paths (%s and %s)"
                                                                    % (path, start))
            else:
                raise ValueError("path is on drive %s, start on drive %s"
                                                    % (path_list[0], start_list[0]))
        # Work out how much of the filepath is shared by start and path.
        for i in range(min(len(start_list), len(path_list))):
            if start_list[i].lower() != path_list[i].lower():
                break
        else:
            i += 1
    
        rel_list = ['..'] * (len(start_list)-i) + path_list[i:]
        if not rel_list:
            return "."
        return ntpath.join(*rel_list)

    def commonprefix(self, m):
        "Given a list of pathnames, returns the longest common leading component"
        # Ripped from Python 2.6 source.
        if not m: return ''
        s1 = min(m)
        s2 = max(m)
        for i, c in enumerate(s1):
            if c != s2[i]:
                return s1[:i]
        return s1

    def getPHPQuiz(self):
        rnd = self.getRandomStr()
        phpcode = "echo "
        for c in rnd:
            phpcode += "chr(%d)."%(ord(c))

        phpcode = phpcode[:-1] + ";"
        return(phpcode, rnd)

    def getShellQuiz(self):
        rnd1 = random.randrange(10, 99)
        rnd2 = random.randrange(10, 99)
        result = str(rnd1 * rnd2)
        shellcode = "echo $((%d*%d))"%(rnd1, rnd2)
        return(shellcode, result)

    def getUserAgent(self):
        return (self.config["p_useragent"])

    def setUserAgent(self, ua):
        if (ua != self.config["p_useragent"]):
            self._log("Useragent changed to: %s" %(ua), self.LOG_DEBUG)
            self.config["p_useragent"] = ua

    def doGetRequest(self, URL, additionalHeaders=None):
        self._log("GET: %s"%URL, self.LOG_DEVEL)
        self._log("HEADER: %s"%str(additionalHeaders), self.LOG_DEVEL)
        self._log("TTL: %d"%baseClass.TIMEOUT, self.LOG_DEVEL)
        result, headers = self.doRequest(URL, self.config["p_useragent"], additionalHeaders=additionalHeaders)
        self._log("RESULT-HEADER: %s"%headers, self.LOG_DEVEL)
        self._log("RESULT-HTML: %s"%result, self.LOG_DEVEL)
        return result

    def doPostRequest(self, URL, Post, additionalHeaders=None):
        self._log("URL   : %s"%URL, self.LOG_DEVEL)
        self._log("POST  : %s"%Post, self.LOG_DEVEL)
        self._log("HEADER: %s"%str(additionalHeaders), self.LOG_DEVEL)
        self._log("TTL: %d"%baseClass.TIMEOUT, self.LOG_DEVEL)
        result, headers = self.doRequest(URL, self.config["p_useragent"], Post, additionalHeaders=additionalHeaders)
        self._log("RESULT-HEADER: %s"%headers, self.LOG_DEVEL)
        self._log("RESULT-HTML: %s"%result, self.LOG_DEVEL)
        return result

    def doGetRequestWithHeaders(self, URL, agent = None, additionalHeaders = None):
        self._log("TTL: %d"%baseClass.TIMEOUT, self.LOG_DEVEL)
        result, headers = self.doRequest(URL, self.config["p_useragent"], additionalHeaders=additionalHeaders)
        self._log("RESULT-HEADER: %s"%headers, self.LOG_DEVEL)
        self._log("RESULT-HTML: %s"%result, self.LOG_DEVEL)
        return result


    def doRequest(self, URL, agent = None, postData = None, additionalHeaders = None, TimeOut=30):
        result = None
        headers = None

        socket.setdefaulttimeout(baseClass.TIMEOUT)


        try:
            b = Browser(agent or DEFAULT_AGENT, proxystring=self.config["p_proxy"])

            try:
                if additionalHeaders:
                    b.headers.update(additionalHeaders)

                if postData:
                    result, headers = b.get_page(URL, postData, additionalheader=additionalHeaders)
                else:
                    result, headers = b.get_page(URL, additionalheader=additionalHeaders)

            finally:
                del(b)

        except Exception, err:
            self._log(err, self.LOG_WARN)

        return result,headers

    #def doGetRequest(self, URL, TimeOut=10):
    #def doPostRequest(self, url, Post, TimeOut=10):

class BrowserError(Exception):
  def __init__(self, url, error):
    self.url = url
    self.error = error

class PoolHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        msg = "getaddrinfo returns an empty list"
        for res in socket.getaddrinfo(self.host, self.port, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                self.sock.settimeout(SOCKETTIMEOUT)
                self.sock.connect(sa)
            except socket.error, msg:
                if self.sock:
                    self.sock.close()
                self.sock = None
                continue
            break
        if not self.sock:
            raise socket.error, msg

class PoolHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, req):
        return self.do_open(PoolHTTPConnection, req)

class Browser(object):
    def __init__(self, user_agent=DEFAULT_AGENT, use_pool=False, proxystring=None):
        self.headers = {'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5'}
        self.proxy = proxystring

    def get_page(self, url, data=None, additionalheader = None):
        proxy_support = urllib2.ProxyHandler({})
        if (self.proxy != None):
            proxy_support = urllib2.ProxyHandler({'http': self.proxy, 'https': self.proxy})
        handlers = [proxy_support]

        opener = urllib2.build_opener(*handlers)

        if additionalheader != None:
            for key, head in additionalheader.items():
                opener.addheaders.append((key, head))

        ret = None
        headers = None
        response = None

        request = urllib2.Request(url, data, self.headers)
        try:
            try:
                response = opener.open(request)
                ret = response.read()

                info = response.info()
                headers = copy.deepcopy(info.items())

            finally:
                if response:
                    response.close()

        except:
            raise

        return ret, headers

    def set_random_user_agent(self):
        self.headers['User-Agent'] = DEFAULT_AGENT
        return self.headers['User-Agent']

    
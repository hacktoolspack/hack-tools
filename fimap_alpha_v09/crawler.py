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

import os.path
from xgoogle.BeautifulSoup import BeautifulSoup
import os, urllib2, urllib, socket

__author__="Iman Karim(ikarim2s@smail.inf.fh-brs.de)"
__date__ ="$09.09.2009 21:52:30$"

class crawler:

    def __init__(self, config):
        self.goodTypes = ("html", "php", "php4", "php5", "jsp", "htm", "py", "pl", "asp", "cgi", "/")
        self.config = config
        self.urlpool = []
        

    def crawl(self):
        root_url = self.config["p_url"]
        outfile = open(self.config["p_write"], "a")


        idx = 0
        print "[%d] Going to root URL: '%s'..." %(idx, root_url)
        if (self.countChar(root_url, "/") == 2):
            root_url = root_url + "/"
        self.crawl_url(root_url)

        
        while(len(self.urlpool)-idx > 0):
            url , level = self.urlpool[idx]
            url = self.__encodeURL(url)
            print "[Done: %d | Todo: %d | Depth: %d] Going for next URL: '%s'..." %(idx, len(self.urlpool) - idx, level, url)
            outfile.write(url + "\n")
            self.crawl_url(url, level)
            idx = idx +1

        print "Harvesting done."
        outfile.close()

    def countChar(self, word, c):
        cnt = 0
        for w in word:
            if w == c:
                cnt += 1
        return(cnt)

    def crawl_url(self, url, level=0):
        if (url.count("/") == 2): # If the user provides 'http://www.google.com' append an / to it.
            url += "/" 
        
        code = self.__simpleGetRequest(url)
        domain = self.getDomain(url, True)

        if (code != None):
            soup = None
            
            try:
                soup = BeautifulSoup(code)
            except:
                pass

            if soup != None:
                for tag in soup.findAll('a'):
                    isCool = False
                    new_url = None
                    try:
                        new_url = tag['href']
                    except KeyError, err:
                        pass

                    if new_url != None and not new_url.startswith("#") and not new_url.startswith("javascript:"):
                        if(new_url.startswith("http://") or new_url.startswith("https://")):
                            if (new_url.lower().startswith(domain.lower())):
                                isCool = True
                        else:
                            if (new_url.startswith("/")):
                                new_url = os.path.join(domain, new_url[1:])
                            else:
                                new_url = os.path.join(os.path.dirname(url), new_url)
                            isCool = True

                        if (isCool and self.isURLinPool(new_url)):
                            isCool = False

                        if (isCool):
                            tmpUrl = new_url
                            if (tmpUrl.find("?") != -1):
                                tmpUrl = tmpUrl[:tmpUrl.find("?")]

                            for suffix in self.goodTypes:
                                if (tmpUrl.endswith(suffix)):
                                    if (level+1 <= self.config["p_depth"]):
                                        self.urlpool.append((new_url, level+1))
                                        break


    def isURLinPool(self, url):
        for u, l in self.urlpool:
            if u.lower() == url.lower():
                return True
        return False

    def __simpleGetRequest(self, URL, TimeOut=10):
        try:
            try:
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', self.config["p_useragent"])]
                f = opener.open(URL, timeout=TimeOut) # TIMEOUT
                ret = f.read()
                f.close()
                return(ret)
            except TypeError, err:
                try:
                    # Python 2.5 compatiblity
                    socket.setdefaulttimeout(TimeOut)
                    f = opener.open(URL)
                    ret = f.read()
                    f.close()
                    return(ret)
                except Exception, err:
                    raise
            except:
                raise

        except Exception, err:
            print "Failed to to request to '%s'" %(Exception)
            print err
            return(None)

    def getDomain(self, url=None, keepPrefix=False, keepPort=False):
        if url==None:
            url = self.URL

        domain = url[url.find("//")+2:]
        prefix = url[:url.find("//")+2]
        if (not domain.endswith("/")):
            domain = domain + "/"
        domain = domain[:domain.find("/")]
        if (not keepPort and domain.find(":") != -1):
            domain = domain[:domain.find(":")]
                
        if (keepPrefix):
            domain = prefix + domain
        return(domain)

    def __encodeURL(self, url):
        ret = ""
        for c in url.encode("utf-8"):
            if c.isalnum() or c in ("=", "?", "&", ":", "/", ".", ",", "_", "-", "+", "#"):
                ret = ret + c
            else:
                ret = ret + "%" + (hex(ord(c))[2:])

        return(ret)

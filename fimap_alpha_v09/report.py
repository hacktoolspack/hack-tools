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



__author__="Iman Karim(ikarim2s@smail.inf.fh-brs.de)"
__date__ ="$01.09.2009 09:56:24$"

class report:
    def __init__(self, URL, Params, VulnKey):
        self.URL = URL
        self.Prefix = None
        self.Surfix = ""
        self.Appendix = None
        self.VulnKey = VulnKey
        self.VulnKeyVal = None
        self.Params = Params
        self.SuffixBreakable = None
        self.SuffixBreakTechName = None
        self.ServerPath = None
        self.ServerScript = None
        self.RemoteInjectable = False
        self.isLinux = True
        self.BlindDiscovered = False
        self.PostData = None
        self.isPost = 0
        self.language = None
        self.VulnHeaderKey = None
        self.HeaderDict = None
        

    def setVulnHeaderKey(self, headerkey):
        self.VulnHeaderKey = headerkey
        
    def setHeader(self, header):
        self.HeaderDict = header

    def setLanguage(self, lang):
        self.language = lang
        
    def getLanguage(self):
        return(self.language)
    
    def isLanguageSet(self):
        return(self.language != None)

    def setPostData(self, p):
        self.PostData = p

    def setPost(self, b):
        self.isPost = b
        
    def getPostData(self):
        return(self.PostData)
    
    def getVulnHeader(self):
        if (self.VulnHeaderKey == None):
            return("")
        return(self.VulnHeaderKey)
    
    def getHeader(self):
        return(self.HeaderDict)
    
    def isPost(self):
        return(self.isPost)

    def setWindows(self):
        self.isLinux = False

    def isWindows(self):
        return(not self.isLinux)

    def setLinux(self):
        self.isLinux = True

    def isLinux(self):
        return(self.isLinux)
    
    def isUnix(self):
        return(self.isLinux)

    def setVulnKeyVal(self, val):
        self.VulnKeyVal = val

    def getVulnKeyVal(self):
        return(self.VulnKeyVal)

    def setPrefix(self, path):
        self.Prefix = path

    def getPrefix(self):
        return(self.Prefix)

    def setSurfix(self, txt):
        if (self.Appendix == None):
            self.Appendix = txt
        self.Surfix = txt

    def getSurfix(self):
        return(self.Surfix)

    def isBlindDiscovered(self):
        return(self.BlindDiscovered)

    def setBlindDiscovered(self, bd):
        self.BlindDiscovered = bd

    def setServerPath(self, sP):
        self.ServerPath = sP
        
    def getServerPath(self):
        return(self.ServerPath)

    def setServerScript(self, sP):
        self.ServerScript = sP

    def getServerScript(self):
        return(self.ServerScript)

    def getAppendix(self):
        return(self.Appendix)

    def isAbsoluteInjection(self):
        return(self.getPrefix() == "")

    def isRelativeInjection(self):
        return(self.getPrefix().startswith("..") or self.getPrefix().startswith("/.."))

    def getVulnKey(self):
        return(self.VulnKey)

    def getURL(self):
        return(self.URL)

    def isRemoteInjectable(self):
        return(self.RemoteInjectable)

    def setRemoteInjectable(self, ri):
        self.RemoteInjectable = ri

    def getParams(self):
        return(self.Params)

    def setSuffixBreakable(self, isPossible):
        self.SuffixBreakable = isPossible

    def isSuffixBreakable(self):
        return(self.SuffixBreakable)

    def setSuffixBreakTechName(self, name):
        self.SuffixBreakTechName = name
        
    def getSuffixBreakTechName(self):
        return(self.SuffixBreakTechName)
    
    
    def getType(self):
        ret = ""

        if (self.isBlindDiscovered()):
            return("Blindly Identified")

        if (self.getPrefix() == None):
            return("Not checked.")
        elif (self.isAbsoluteInjection()):
            if (self.getAppendix() == ""):
                ret = "Absolute Clean"
            else:
                ret = "Absolute with appendix '%s'" %(self.getAppendix())
        elif (self.isRelativeInjection()):
            if (self.getAppendix() == ""):
                ret = "Relative Clean"
            else:
                ret = "Relative with appendix '%s'" %(self.getAppendix())
        else:
            return("Unknown (%s | %s | %s)" %(self.getPrefix(), self.isRelativeInjection(), self.isAbsoluteInjection()))

        if (self.isRemoteInjectable()):
            ret = ret + " + Remote injection"

        return(ret)

    def getDomain(self, url=None):
        if url==None:
            url = self.URL

        domain = url[url.find("//")+2:]
        domain = domain[:domain.find("/")]
        return(domain)

    def getPath(self):
        url = self.getURL()
        url = url[url.find("//")+2:]
        url = url[url.find("/"):]
        return(url)

    def autoDetectLanguageByExtention(self, languageSets):
        for Name, langClass in languageSets.items():
            exts = langClass.getExtentions()
            for ext in exts:
                if (self.URL.find(ext) != -1):
                    self.setLanguage(Name)
                    return(True)
        return(False)

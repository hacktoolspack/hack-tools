import urllib, httplib, copy, urllib2
import string,random,os,socket, os.path
import xml.dom.minidom
import shutil
from time import gmtime, strftime

class baseTools(object):
    LOG_ERROR = 99
    LOG_WARN  = 98
    LOG_DEVEL = 1
    LOG_DEBUG = 2
    LOG_INFO  = 3
    LOG_ALWAYS= 4
    
    config = None
    log_lvl = None
    
    boxsymbol = "#"
    
    # Color hack
    CONST_RST = "\033[0m"
    CONST_COL = "\033[__BOLD__;3__COLOR__m"

    BLACK   = 0
    RED     = 1
    GREEN   = 2
    YELLOW  = 3
    BLUE    = 4
    MAGENTA = 5
    CYAN    = 6
    WHITE   = 7
    
    
    BOX_HEADER_STYLE = (1, 1) 
    BOX_SPLITTER_STYLE = (3, 0)
    def getRandomStr(self):
        chars = string.letters + string.digits
        ret = ""
        for i in range(8):
            if (i==0):
                ret = ret + random.choice(string.letters)
            else:
                ret = ret + random.choice(chars)
        return ret
    
    
    def initLog(self, config):
        self.log_lvl = {}
        self.log_lvl[baseTools.LOG_ERROR]   = ("ERROR", (self.RED, 1))
        self.log_lvl[baseTools.LOG_WARN]    = ("WARN",  (self.RED, 0)) 
        self.log_lvl[baseTools.LOG_DEVEL]   = ("DEVEL", (self.YELLOW, 0))
        self.log_lvl[baseTools.LOG_DEBUG]   = ("DEBUG", (self.CYAN, 0))
        self.log_lvl[baseTools.LOG_INFO]    = ("INFO",  (self.BLUE, 0))
        self.log_lvl[baseTools.LOG_ALWAYS]  = ("OUT",   (self.MAGENTA, 0))
        self.LOG_LVL = config["p_verbose"]
        self.use_color = config["p_color"]
        self.config = config
        
        if (self.use_color):
            self.boxsymbol = self.CONST_COL + "#"
            self.boxsymbol = self.boxsymbol.replace("__BOLD__", "1")
            self.boxsymbol = self.boxsymbol.replace("__COLOR__", str(self.RED))
            self.boxsymbol += self.CONST_RST
        
    def _log(self, txt, LVL):
        if (4-self.config["p_verbose"] < LVL):
            logline = "[%s] %s" %(self.log_lvl[LVL][0], txt)
            t = strftime("%H:%M:%S", gmtime())
            if (self.use_color):
                print "[%s] %s" %(t, self.__getColorLine(logline, self.log_lvl[LVL][1]))
            else:
                print "[%s] %s" %(t, logline)
    
    def __setColor(self, txt, style):
        ret = self.CONST_COL + txt
        ret = ret.replace("__COLOR__", str(style[0]))
        ret = ret.replace("__BOLD__", str(style[1]))
        return(ret)
    
    def __getColorLine(self, txt, style):
        ret = self.__setColor(txt, style)
        ret += self.CONST_RST
        return(ret)
    
    
    def drawBox(self, header, textarray, usecolor=None):
        if (usecolor != None):
            self.use_color = usecolor
        maxLen = self.__getLongestLine(textarray, header) + 5
        headspacelen = (maxLen/2 - len(header)/2)
        print self.boxsymbol* (maxLen+1)
        if (self.use_color):
            cheader = self.__getColorLine(header, self.BOX_HEADER_STYLE)
            self.__printBoxLine(cheader, maxLen, len(header))
        else:
            self.__printBoxLine(header, maxLen)
        print self.boxsymbol* (maxLen+1)
        
        for ln in textarray:
            self.__printBoxLine(ln, maxLen)

        print self.boxsymbol* (maxLen+1)

    def __printBoxLine(self, txt, maxlen, realsize=-1):
        size = len(txt)
        if (realsize != -1): size = realsize
        suffix = " " * (maxlen - size-1)
        if (self.use_color):
            coloredtxt = txt
            if (txt.startswith("::")): # Informative Inline Message
                coloredtxt = self.__getColorLine(txt, self.BOX_SPLITTER_STYLE)
            
            print self.boxsymbol + coloredtxt + suffix + self.boxsymbol
        else:
            print self.boxsymbol + txt + suffix + self.boxsymbol

    def __getLongestLine(self, textarray, header):
        maxLen = len(header)
        for ln in textarray:
            if (len(ln) > maxLen):
                maxLen = len(ln)
        return(maxLen)
    
    def getAttributeFromFirstNode(self, xmlfile, attrib):
        if (os.path.exists(xmlfile)):
            XML_plugin = xml.dom.minidom.parse(xmlfile)
            XML_Rootitem = XML_plugin.firstChild
            value = int(XML_Rootitem.getAttribute(attrib))
            return(value)
        else:
            return False
        
    def suggest_update(self, orginal_file, replacement_file):
        #print orginal_file
        #print replacement_file
        inp = raw_input("Do you want to update? [y/N]")
        if (inp == "Y" or inp == "y"):
            print "Updating..."
            os.unlink(orginal_file)
            shutil.copy(replacement_file, orginal_file)
            

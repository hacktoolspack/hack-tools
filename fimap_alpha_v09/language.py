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
import xml.dom.minidom
import base64
import sys, os
from baseClass import baseClass
from baseTools import baseTools
import random

def getXMLNode(item, nodename):
    for child in item.childNodes:
        if (child.nodeName != "#text"):
            if (child.nodeName == nodename):
                return(child)
    return(None)

def getXMLNodes(item, nodename):
    ret = []
    for child in item.childNodes:
        if (child.nodeName != "#text"):
            if (child.nodeName == nodename):
                ret.append(child)
    return(ret)

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def convertString(txt, isBase64):
    ret = None
    if isBase64:
        ret = base64.b64decode(txt)
    else:
        ret = str(txt)
    return(ret)

class XML2Config(baseClass):

    def _load(self):
        self.langsets = {}
        self.xml_file = os.path.join(sys.path[0], "config", "generic.xml")
        self.XML_Generic = None
        self.XML_Rootitem = None

        self.version = -1

        self.relative_files = []
        self.absolute_files = []
        self.remote_files   = []
        self.log_files      = []
        self.blind_files    = []
        self.blind_min      = 0
        self.blind_max      = 0
    
        self.commandConcat_unix      = None
        self.shellquiz_code_unix     = None
        self.kernelversion_code_unix = None
        self.currentdir_code_unix    = None
        self.currentuser_code_unix   = None
        self.cd_code_unix            = None
    
        self.commandConcat_win      = None
        self.shellquiz_code_win     = None
        self.kernelversion_code_win = None
        self.currentdir_code_win    = None
        self.currentuser_code_win   = None
        self.cd_code_win            = None
        
        self.__init_xmlresult()
   
        #sys.exit(0)
    
    def __init_xmlresult(self):
        xmlfile = self.xml_file
        if (os.path.exists(xmlfile)):
            self.XML_Generic = xml.dom.minidom.parse(xmlfile)
            self.XML_Rootitem = self.XML_Generic.firstChild
            
            self.version = int(self.XML_Rootitem.getAttribute("revision"))
            
            rel_node = getXMLNode(self.XML_Rootitem, "relative_files")
            rel_files = getXMLNodes(rel_node, "file")
            for f in rel_files:
                self.relative_files.append(fiFile(f, self.config))
            
            abs_node = getXMLNode(self.XML_Rootitem, "absolute_files")
            abs_files = getXMLNodes(abs_node, "file")
            for f in abs_files:
                self.absolute_files.append(fiFile(f, self.config))
            
            rem_node = getXMLNode(self.XML_Rootitem, "remote_files")
            rem_files = getXMLNodes(rem_node, "file")
            for f in rem_files:
                self.remote_files.append(fiFile(f, self.config))
            
            log_node = getXMLNode(self.XML_Rootitem, "log_files")
            log_files = getXMLNodes(log_node, "file")
            for f in log_files:
                self.log_files.append(fiFile(f, self.config))
            
            
            blind_node = getXMLNode(self.XML_Rootitem, "blind_files")
            mindepth = blind_node.getAttribute("mindepth")
            maxdepth = blind_node.getAttribute("maxdepth")
            try:
                mindepth = int(mindepth)
                maxdepth = int(maxdepth)
            except:
                print "Mindepth and Maxdepth for blindmode have non-integer values!"
                print "Fix it in the generic.xml!"
                print "Committing suicide..."
                sys.exit(1)
                
            if (mindepth > maxdepth):
                print "Logic isn't your best friend eh?"
                print "The mindepth value is greater than the maxdepth value!"
                print "Fix that in the generic.xml!"
                print "Committing suicide..."
                sys.exit(1)
                
            self._log("Mindepth (%d) and Maxdepth (%d) loaded from generic.xml."%(mindepth, maxdepth), self.LOG_DEBUG)
            self.blind_min = mindepth
            self.blind_max = maxdepth
            
            
            blind_files = getXMLNodes(blind_node, "file")
            for f in blind_files:
                self.blind_files.append(fiFile(f, self.config))
            
            methods_node = getXMLNode(self.XML_Rootitem, "methods")
            
            unix_node = getXMLNode(methods_node, "unix")
            self.commandConcat_unix = str(unix_node.getAttribute("concatcommand"))
            
            quiz_node = getXMLNode(unix_node, "shellquiz")
            self.shellquiz_code_unix = base64.b64decode(quiz_node.getAttribute("source"))
            kernel_node = getXMLNode(unix_node, "kernelversion")
            self.kernelversion_code_unix = str(kernel_node.getAttribute("source"))
            curdir_node = getXMLNode(unix_node, "currentdir")
            self.currentdir_code_unix = str(curdir_node.getAttribute("source"))
            curusr_node = getXMLNode(unix_node, "currentuser")
            self.currentuser_code_unix = str(curusr_node.getAttribute("source"))
            
            cd_node = getXMLNode(unix_node, "cd")
            self.cd_code_unix = str(cd_node.getAttribute("source"))

            win_node = getXMLNode(methods_node, "windows")
            self.commandConcat_win = str(win_node.getAttribute("concatcommand"))
            
            quiz_node = getXMLNode(win_node, "shellquiz")
            self.shellquiz_code_win = base64.b64decode(quiz_node.getAttribute("source"))
            kernel_node = getXMLNode(win_node, "kernelversion")
            self.kernelversion_code_win = str(kernel_node.getAttribute("source"))
            curdir_node = getXMLNode(win_node, "currentdir")
            self.currentdir_code_win = str(curdir_node.getAttribute("source"))
            curusr_node = getXMLNode(win_node, "currentuser")
            self.currentuser_code_win = str(curusr_node.getAttribute("source"))
            cd_node = getXMLNode(win_node, "cd")
            self.cd_code_win = str(cd_node.getAttribute("source"))
            
            
            self.__loadLanguageSets()
        else:
            print "generic.xml file not found! This file is very important!"
            sys.exit(1)
    
    def getRealFile(self):
        return(self.xml_file)
      
    def __loadLanguageSets(self):
        langnodes = getXMLNode(self.XML_Rootitem, "languagesets")
        for c in langnodes.childNodes:
            if (c.nodeName == "language"):
                langname = str(c.getAttribute("name"))
                langfile = str(c.getAttribute("langfile"))
                langClass = baseLanguage(langname, langfile, self.config)
                self.langsets[langname] = langClass
                self._log("Loaded XML-LD for '%s' at revision %d by %s" %(langname, langClass.getRevision(), langClass.getAutor()), self.LOG_DEBUG)
    
    def getVersion(self):
        return(self.version)
    
    def generateShellQuiz(self, isUnix=True):
        ret = None
        if (isUnix):
            exec(self.shellquiz_code_unix)
        else:
            exec(self.shellquiz_code_win)
        return(ret)
    
    def getAllLangSets(self):
        return(self.langsets)
    
    def getAllReadfileRegex(self):
        ret = []
        langs = self.getAllLangSets()
        for k,v in langs.items():
            readfile_regex = v.getReadfileDetectors()
            for reg in readfile_regex:
                ret.append((k, reg))
        return(ret)
    
    def getAllSniperRegex(self):
        ret = []
        langs = self.getAllLangSets()
        for k,v in langs.items():
            readfile_regex = v.getSniper()
            ret.append((k, readfile_regex))
        return(ret)
    
    def getKernelCode(self, isUnix=True):
        if (isUnix):
            return(self.kernelversion_code_unix)
        else:
            return(self.kernelversion_code_win)
    
    def getRelativeFiles(self, lang=None):
        ret = []
        for f in self.relative_files:
            ret.append(f)
            
        if (lang != None):
            for f in self.langsets[lang].getRelativeFiles():
                ret.append(f)
        return(ret)
    
        
    def getAbsoluteFiles(self, lang=None):
        ret = []
        for f in self.absolute_files:
            ret.append(f)
            
        if (lang != None):
            for f in self.langsets[lang].getAbsoluteFiles():
                ret.append(f)
        return(ret)
    
        
    def getLogFiles(self, lang=None):
        ret = []
        for f in self.log_files:
            ret.append(f)
            
        if (lang != None):
            for f in self.langsets[lang].getLogFiles():
                ret.append(f)
        return(ret)
    
        
    def getRemoteFiles(self, lang=None):
        ret = []
        for f in self.remote_files:
            ret.append(f)
            
        if (lang != None):
            for f in self.langsets[lang].getRemoteFiles():
                ret.append(f)
        return(ret)
    
    def getBlindFiles(self):
        ret = []
        for f in self.blind_files:
            ret.append(f)
           
        return(ret)
    
    def getBlindMax(self):
        return(self.blind_max)
    
    def getBlindMin(self):
        return(self.blind_min)
    
    def getCurrentDirCode(self, isUnix=True):
        if (isUnix):
            return(self.currentdir_code_unix)
        else:
            return(self.currentdir_code_win)
        
    def getCurrentUserCode(self, isUnix=True):
        if (isUnix):
            return(self.currentuser_code_unix)
        else:
            return(self.currentuser_code_win)
    
    def getConcatSymbol(self, isUnix=True):
        if (isUnix):
            return(self.commandConcat_unix)
        else:
            return(self.commandConcat_win)
    
    def concatCommands(self, commands, isUnix=True):
        symbol = " %s " %(self.getConcatSymbol(isUnix))
        return(symbol.join(commands))
    
    def generateChangeDirectoryCommand(self, Directory, isUnix=True):
        code = self.cd_code_unix
        
        if (not isUnix):
            code = self.cd_code_win
            
        code = code.replace("__DIR__", Directory)
        return(code)
    
class baseLanguage(baseTools):
    
    def __init__(self, langname, langfile, config):
        self.initLog(config)
        langfile = os.path.join(sys.path[0], "config", langfile)
        self.RealFile     = langfile
        self.XML_Langfile = None
        self.XML_Rootitem = None

        if (os.path.exists(langfile)):
            self.XML_Langfile = xml.dom.minidom.parse(langfile)
            self.XML_Rootitem = self.XML_Langfile.firstChild
        else:
            print "%s file not found!" %(langfile)
            sys.exit(1)
        
        self.LanguageName = langname
        self.XMLRevision  = None
        self.XMLAutor     = None
        
        self.relative_files = []
        self.absolute_files = []
        self.remote_files   = []
        self.log_files      = []
        
        self.exec_methods   = []
        self.payloads       = []
        
        self.sniper_regex   = None
        
        self.quiz_function  = None
        self.print_function  = None
        self.eval_kickstarter = None
        self.write_file = None
        
        self.detector_include    = []
        self.detector_readfile   = []
        self.detector_extentions = []
        
        self.do_force_inclusion_test = False
    
        self.__populate()
    
    def getLangFile(self):
        return(self.RealFile)
    
    def getName(self):
        return(self.LanguageName)
    
    def getVersion(self):
        return(self.XMLRevision)
    
    def getRevision(self):
        return(self.XMLRevision)
    
    def getAutor(self):
        return(self.XMLAutor)
    
    def getSniper(self):
        return(self.sniper_regex)
    
    def doForceInclusionTest(self):
        return(self.do_force_inclusion_test)
    
    def getExecMethods(self):
        return(self.exec_methods)
    
    def getPayloads(self):
        return(self.payloads)
    
    def getRelativeFiles(self):
        return(self.relative_files)
    
    def getAbsoluteFiles(self):
        return(self.absolute_files)
    
    def getRemoteFiles(self):
        return(self.remote_files)
    
    def getLogFiles(self):
        return(self.log_files)
    
    def getIncludeDetectors(self):
        return(self.detector_include)
    
    def getReadfileDetectors(self):
        return(self.detector_readfile)
    
    def getExtentions(self):
        return(self.detector_extentions)
    
    def getQuizSource(self):
        return(self.quiz_function)
    
    def generateWriteFileCode(self, remotefilepath, mode, b64data):
        code = self.write_file
        code = code.replace("__FILE__", remotefilepath)
        code = code.replace("__MODE__", mode)
        code = code.replace("__B64_DATA__", b64data)
        return(code)
    
    def generateQuiz(self):
        ret = None
        try:
            exec(self.quiz_function)
        except:
            boxarr = []
            boxheader = "[!!!] BAAAAAAAAAAAAAAAANG - Welcome back to reality [!!!]"
            boxarr.append("The quiz function defined in one of the XML-Language-Definition files")
            boxarr.append("just failed! If you are coding your own XML then fix that!")
            boxarr.append("If not please report this bug at http://fimap.googlecode.com (!) Thanks!")
            self.drawBox(boxheader, boxarr)
            raise
        return(ret)
    
    def generatePrint(self, data):
        ret = self.print_function.replace("__PLACEHOLDER__", data)
        return(ret)
    
    def getEvalKickstarter(self):
        return(self.eval_kickstarter)
    
    def __populate(self):
        self.XMLRevision                = int(self.XML_Rootitem.getAttribute("revision"))
        self.XMLAutor                   = self.XML_Rootitem.getAttribute("autor")
        self.do_force_inclusion_test    = self.XML_Rootitem.getAttribute("force_inclusion_test") == "1"
        
        rel_node = getXMLNode(self.XML_Rootitem, "relative_files")
        rel_files = getXMLNodes(rel_node, "file")
        for f in rel_files:
            self.relative_files.append(fiFile(f, self.config))
        
        abs_node = getXMLNode(self.XML_Rootitem, "absolute_files")
        abs_files = getXMLNodes(abs_node, "file")
        for f in abs_files:
            self.absolute_files.append(fiFile(f, self.config))
        
        rem_node = getXMLNode(self.XML_Rootitem, "remote_files")
        rem_files = getXMLNodes(rem_node, "file")
        for f in rem_files:
            self.remote_files.append(fiFile(f, self.config))
        
        log_node = getXMLNode(self.XML_Rootitem, "log_files")
        log_files = getXMLNodes(log_node, "file")
        for f in log_files:
            self.log_files.append(fiFile(f, self.config))
        
        exec_methods = getXMLNode(self.XML_Rootitem, "exec_methods")
        exec_nodes = getXMLNodes(exec_methods, "exec")
        for f in exec_nodes:
            self.exec_methods.append(fiExecMethod(f, self.config))
        if (len(self.exec_methods) == 0):
            self._log("XML-LD has no exec-method(s) defined!", self.LOG_ERROR)
            self._log("  This XML-LD can't be used to go into exploit mode!", self.LOG_ERROR)
        
         
        payloads = getXMLNode(self.XML_Rootitem, "payloads")
        payload_nodes = getXMLNodes(payloads, "payload")
        for f in payload_nodes:
            self.payloads.append(fiPayload(f, self.config, self.getName()))
        if (len(self.payloads) == 0):
            self._log("XML-LD has no payload(s) defined!", self.LOG_DEBUG)
        
        self.sniper_regex = str(getXMLNode(self.XML_Rootitem, "snipe").getAttribute("regex"))
        if (self.sniper_regex == None or self.sniper_regex.strip() == ""):
            self._log("XML-LD has no sniper regex! So this XML-LD can only be used in blind-mode!", self.LOG_WARN)
        
        methods_node = getXMLNode(self.XML_Rootitem, "methods")
        quiz_node = getXMLNode(methods_node, "quiz")
        if (quiz_node == None):
            self._log("FATAL! XML-Language-Definition (%s) has no quiz function defined!"%(self.getName()), self.LOG_ERROR)
            self._log("Please fix that in order to run fimap without problems!", self.LOG_ERROR)
            self._log("Committing suicide :-O", self.LOG_ERROR)
            sys.exit(1)
        else:
            isbase64  = quiz_node.getAttribute("isbase64")=="1"
            quiz_code = quiz_node.getAttribute("source")
            quiz_code = convertString(quiz_code, isbase64)
                
            if (quiz_code == None or quiz_code.strip() == ""):
                self._log("FATAL! XML-Language-Definition (%s) has no quiz function defined!"%(self.getName()), self.LOG_ERROR)
                self._log("Please fix that in order to run fimap without problems!", self.LOG_ERROR)
                self._log("Committing suicide :-O", self.LOG_ERROR)
                sys.exit(1)
            self.quiz_function = str(quiz_code)
        
        print_node = getXMLNode(methods_node, "print")
        if (print_node == None):
            self._log("FATAL! XML-Language-Definition (%s) has no print function defined!"%(self.getName()), self.LOG_ERROR)
            self._log("Please fix that in order to run fimap without problems!", self.LOG_ERROR)
            self._log("Committing suicide :-O", self.LOG_ERROR)
            sys.exit(1)
        else:
            isbase64  = print_node.getAttribute("isbase64")=="1"
            print_code = print_node.getAttribute("source")
            print_code = convertString(print_code, isbase64)
            
            if (print_code == None or print_code.strip() == ""):
                self._log("FATAL! XML-Language-Definition (%s) has no print function defined!"%(self.getName()), self.LOG_ERROR)
                self._log("Please fix that in order to run fimap without problems!", self.LOG_ERROR)
                self._log("Committing suicide :-O", self.LOG_ERROR)
                sys.exit(1)
            self.print_function = str(print_code)
        
        eval_node = getXMLNode(methods_node, "eval_kickstarter")
        if (eval_node == None):
            self._log("XML-LD (%s) has no eval_kickstarter method defined."%(self.getName()), self.LOG_DEBUG)
            self._log("Language will not be able to use logfile-injection.", self.LOG_DEBUG)
        else:
            isbase64  = eval_node.getAttribute("isbase64")=="1"
            eval_code = eval_node.getAttribute("source")
            eval_code = convertString(eval_code, isbase64)
            
            if (eval_code == None or eval_code.strip() == ""):
                self._log("XML-LD (%s) has no eval_kickstarter method defined."%(self.getName()), self.LOG_DEBUG)
                self._log("Language will not be able to use logfile-injection."%(self.getName()), self.LOG_DEBUG)
            self.eval_kickstarter = str(eval_code)
        
        write_node = getXMLNode(methods_node, "write_file")
        if (write_node == None):
            self._log("XML-LD (%s) has no write_file method defined."%(self.getName()), self.LOG_DEBUG)
            self._log("Language will not be able to write files.", self.LOG_DEBUG)
        else:
            isbase64  = write_node.getAttribute("isbase64")=="1"
            write_code = write_node.getAttribute("source")
            write_code = convertString(write_code, isbase64)
            
            if (write_code == None or write_code.strip() == ""):
                self._log("XML-LD (%s) has no eval_kickstarter method defined."%(self.getName()), self.LOG_DEBUG)
                self._log("Language will not be able to use logfile-injection."%(self.getName()), self.LOG_DEBUG)
            self.write_file = str(write_code)
        
        
        detectors_node = getXMLNode(self.XML_Rootitem, "detectors")
        include_patterns = getXMLNode(detectors_node, "include_patterns")
        pattern_nodes =  getXMLNodes(include_patterns, "pattern")
        for f in pattern_nodes:
            self.detector_include.append(str(f.getAttribute("regex")))
        if (len(self.detector_include) == 0):
            self._log("XML-LD has no include patterns defined!", self.LOG_WARN)
            self._log("  Only blindmode will work because they are used to retrieve informations out of the error message!", self.LOG_DEBUG)
        
        readfile_patterns = getXMLNode(detectors_node, "readfile_patterns")
        pattern_nodes =  getXMLNodes(readfile_patterns, "pattern")
        for f in pattern_nodes:
            self.detector_readfile.append(str(f.getAttribute("regex")))
        if (len(self.detector_readfile) == 0):
            self._log("XML-LD has no readfile patterns defined!", self.LOG_DEBUG)
            self._log("  No readfile bugs can be scanned if this is not defined.", self.LOG_DEBUG)

        extentions = getXMLNode(detectors_node, "extentions")
        extention_nodes =  getXMLNodes(extentions, "extention")
        for f in extention_nodes:
            self.detector_extentions.append(str(f.getAttribute("ext")))
        if (len(self.detector_readfile) == 0):
            self._log("XML-LD has no extentions defined!", self.LOG_DEBUG)
        

class fiPayload(baseTools):
    def __init__(self, xmlPayload, config, ParentName):
        self.initLog(config)
        self.name = xmlPayload.getAttribute("name")
        self.doBase64 = (xmlPayload.getAttribute("dobase64") == "1")
        self.inshell  = (xmlPayload.getAttribute("inshell") == "1")
        self.unix     = (xmlPayload.getAttribute("unix") == "1")
        self.win      = (xmlPayload.getAttribute("win") == "1")
        self.inputlist = getXMLNodes(xmlPayload, "input")
        self.source = str(getXMLNode(xmlPayload, "code").getAttribute("source"))
        self.ParentName = ParentName
        self._log("fimap PayloadObject loaded: %s" %(self.name), self.LOG_DEVEL)

    def isForWindows(self):
        return(self.win)
    
    def isForUnix(self):
        return(self.unix)

    def getParentName(self):
        return(self.ParentName)
    
    def doInShell(self):
        return(self.inshell)
    
    def getName(self):
        return(self.name)
    
    def getSource(self):
        return(self.source)
    
    def generatePayload(self):
        ret = self.source
        for q in self.inputlist:
            type_ = q.getAttribute("type")
            if (type_ == "question"):
                question = q.getAttribute("text")
                placeholder = q.getAttribute("placeholder")
                inp = raw_input(question)
                if (self.doBase64):
                    inp = base64.b64encode(inp)
                ret = ret.replace(placeholder, inp)
            elif (type_ == "info"):
                info = q.getAttribute("text")
                print info
            elif (type_ == "wait"):
                info = q.getAttribute("text")
                raw_input(info)
        return(ret)
                    

class fiExecMethod(baseTools):
    def __init__(self, xmlExecMethod, config):
        self.initLog(config)
        self.execname   = xmlExecMethod.getAttribute("name")
        self.execsource = xmlExecMethod.getAttribute("source")
        self.dobase64   = xmlExecMethod.getAttribute("dobase64")=="1"
        self.isunix     = xmlExecMethod.getAttribute("unix")=="1"
        self.iswin      = xmlExecMethod.getAttribute("win")=="1"
        self._log("fimap ExecObject loaded: %s" %(self.execname), self.LOG_DEVEL)
        
    def getSource(self):
        return(self.execsource)
    
    def getName(self):
        return(self.execname)
    
    def generatePayload(self, command):
        if (self.dobase64):
            command = base64.b64encode(command)
        payload = self.getSource().replace("__PAYLOAD__", command)
        return(payload)
    
    def isUnix(self):
        return(self.isunix)
    
    def isWindows(self):
        return(self.iswin)
        
class fiFile(baseTools):
    def __init__(self, xmlFile, config):
        self.initLog(config)
        self.filepath = str(xmlFile.getAttribute("path"))
        self.postdata = str(xmlFile.getAttribute("post"))
        self.findstr  = str(xmlFile.getAttribute("find"))
        self.flags    = str(xmlFile.getAttribute("flags"))
        self.isunix   = str(xmlFile.getAttribute("unix")) == "1"
        self.iswin    = str(xmlFile.getAttribute("windows")) == "1"
        self._log("fimap FileObject loaded: %s" %(self.filepath), self.LOG_DEVEL)
        
    def getFilepath(self):
        return(self.filepath)
    
    def getPostData(self):
        return(self.postdata)
    
    def getFindStr(self):
        return(self.findstr)
    
    def getFlags(self):
        return(self.flags)
    
    def containsFlag(self, flag):
        return (flag in self.flags)
    
    def isInjected(self, content):
        return (content.find(self.findstr) != -1)
    
    def isUnix(self):
        return(self.isunix)
    
    def isBreakable(self):
        return(self.filepath.find("://") == -1)
    
    def isWindows(self):
        return(self.iswin)
    
    def getBackSymbols(self, SeperatorAtFront=True):
        if (SeperatorAtFront):
            if (self.isUnix()):
                return("/..")
            else:
                return("\\..")
        else:
            if (self.isUnix()):
                return("../")
            else:
                return("..\\")
    def getBackSymbol(self):
        if (self.isUnix()):
            return("/")
        else:
            return("\\")
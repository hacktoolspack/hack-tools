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

from baseClass import baseClass
from targetScanner import targetScanner
import sys, time

__author__="Iman Karim(ikarim2s@smail.inf.fh-brs.de)"
__date__ ="$03.09.2009 01:29:37$"

class singleScan(baseClass):

    def _load(self):
        self.URL = None
        self.quite = False

    def setURL(self, URL):
        self.URL = URL

    def setQuite(self, b):
        self.quite = b

    def scan(self):
        try:
            self.localLog("SingleScan is testing URL: '%s'" %self.URL)
            t = targetScanner(self.config)
            t.MonkeyTechnique = self.config["p_monkeymode"]

            idx = 0
            if (t.prepareTarget(self.URL)):
                res = t.testTargetVuln()
                if (len(res) == 0):
                    self.localLog("Target URL isn't affected by any file inclusion bug :(")
                else:
                    for i in res:
                        report = i[0]
                        files = i[1]
                        idx = idx +1
                        boxarr = []
                        header = "[%d] Possible File Inclusion"%(idx)
                        if (report.getLanguage() != None):
                            header = "[%d] Possible %s-File Inclusion"%(idx, report.getLanguage())
                        boxarr.append("::REQUEST")
                        boxarr.append("  [URL]        %s"%report.getURL())
                        if (report.getPostData() != None and report.getPostData() != ""): boxarr.append("  [POST]       %s"%report.getPostData())
                        if (report.getHeader() != None and report.getHeader().keys() > 0):
                            modkeys = ",".join(report.getHeader().keys())
                            boxarr.append("  [HEAD SENT]  %s"%(modkeys))
                        
                        boxarr.append("::VULN INFO")
                        if (report.isPost == 0):
                            boxarr.append("  [GET PARAM]  %s"%report.getVulnKey())
                        elif (report.isPost == 1):
                            boxarr.append("  [POSTPARM]   %s"%report.getVulnKey())
                        elif (report.isPost == 2):
                            boxarr.append("  [VULN HEAD]  %s"%report.getVulnHeader())
                            boxarr.append("  [VULN PARA]  %s"%report.getVulnKey())

                        if (report.isBlindDiscovered()):
                            boxarr.append("  [PATH]       Not received (Blindmode)")
                        else:
                            boxarr.append("  [PATH]       %s"%report.getServerPath())
                        if (report.isUnix()):
                            boxarr.append("  [OS]         Unix")
                        else:
                            boxarr.append("  [OS]         Windows")
                            
                        boxarr.append("  [TYPE]       %s"%report.getType())
                        if (not report.isBlindDiscovered()):
                            if (report.isSuffixBreakable() == None):
                                boxarr.append("  [TRUNCATION] No Need. It's clean.")
                            else:
                                if (report.isSuffixBreakable()):
                                    boxarr.append("  [TRUNCATION] Works with '%s'. :)" %(report.getSuffixBreakTechName()))
                                else:
                                    boxarr.append("  [TRUNCATION] Doesn't work. :(")
                        else:
                            if (report.isSuffixBreakable()):
                                boxarr.append("  [TRUNCATION] Is needed.")
                            else:
                                boxarr.append("  [TRUNCATION] Not tested.")
                        boxarr.append("  [READABLE FILES]")
                        if (len(files) == 0):
                            boxarr.append("                     No Readable files found :(")
                        else:
                            fidx = 0
                            for file in files:
                                payload = "%s%s%s"%(report.getPrefix(), file, report.getSurfix())
                                if (file != payload):
                                    if report.isWindows() and file[1]==":":
                                        file = file[3:]
                                    txt = "                   [%d] %s -> %s"%(fidx, file, payload)
                                    #if (fidx == 0): txt = txt.strip()
                                    boxarr.append(txt)
                                else:
                                    txt = "                   [%d] %s"%(fidx, file)
                                    #if (fidx == 0): txt = txt.strip()
                                    boxarr.append(txt)
                                fidx = fidx +1
                        self.drawBox(header, boxarr)
        except KeyboardInterrupt:
            if (self.quite): # We are in google mode.
                print "\nCancelled current target..."
                print "Press CTRL+C again in the next second to terminate fimap."
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    raise
            else: # We are in single mode. Simply raise the exception.
                raise
    def localLog(self, txt):
        if (not self.quite):
            print txt
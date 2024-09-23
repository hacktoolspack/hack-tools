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
import os, sys
import xml.dom.minidom

class plugininterface(baseClass):
    def _load(self):
        self.plugins = []
        self.plugin_dir = os.path.join(sys.path[0], "plugins")
        
        self.loadPlugins()
        
    def loadPlugins(self):
        x = 0
        for dir in os.listdir(self.plugin_dir):
            dirpath = os.path.join(self.plugin_dir, dir)
            if (os.path.isdir(dirpath) and dir[0] != "."):
                pluginxml = os.path.join(dirpath, "plugin.xml")
                if (os.path.exists(pluginxml)):
                    info = pluginXMLInfo(pluginxml)
                    plugin = info.getStartupClass()
                    self._log("Trying to load plugin '%s'..." %dir, self.LOG_DEBUG)
                    loadedClass = None
                    loader  = "from plugins.%s import %s\n" %(plugin, plugin)
                    loader += "loadedClass = %s.%s(self.config)"%(plugin, plugin)
                    try:
                        exec(loader)
                        loadedClass.addXMLInfo(info)
                        loadedClass.plugin_init()
                        loadedClass.printInfo()
                        self.plugins.append(loadedClass)
                        x +=1
                    except:
                        raise
                else:
                    self._log("Plugin doesn't have a plugin.xml file! -> '%s'..." %dir, self.LOG_WARN)
        for p in self.plugins:
            p.plugin_loaded()

        self._log("%d plugins loaded." %(x), self.LOG_DEBUG)
        
    def requestPluginActions(self, langClass, isSystem, isUnix):
        ret = []
        for p in self.plugins:
            modes = p.plugin_exploit_modes_requested(langClass, isSystem, isUnix)
            for m in modes:
                ret.append((p.getPluginName(), m))
        return(ret)
    
    def broadcast_callback(self, attack, haxhelper):
        for p in self.plugins:
            try:
                p.plugin_callback_handler(attack, haxhelper)
            except KeyboardInterrupt:
                print "\nReceived unhandled KeyboardInterrupt by plugin!"
            except:
                self._log("\nPlugin '%s' just crashed!"%(p.getPluginName()), self.LOG_ERROR)
                self._log("Please send a bugreport to the Plugin Developer: %s <%s>"%(p.getPluginAutor(), p.getPluginEmail()), self.LOG_ERROR)
                self._log("Push enter to see the stacktrace.", self.LOG_WARN)
                raw_input()
                print "%<--------------------------------------------"
                raise
            
    def getPluginVersion(self, StartUpClass):
        for p in self.plugins:
            if (p.getPluginStartUpClass() == StartUpClass):
                Version = p.getPluginVersion()
                return(Version)
        return(None)

    def getAllPluginObjects(self):
        return(self.plugins)

class pluginXMLInfo:
    def __init__(self, xmlfile):
        self.xmlFile = xmlfile
      
        if (os.path.exists(xmlfile)):
            XML_plugin = xml.dom.minidom.parse(xmlfile)
            XML_Rootitem = XML_plugin.firstChild
            self.name         = str(XML_Rootitem.getAttribute("name"))
            self.startupclass = str(XML_Rootitem.getAttribute("startup"))
            self.autor        = str(XML_Rootitem.getAttribute("autor"))
            self.email        = str(XML_Rootitem.getAttribute("email"))
            self.version      = int(XML_Rootitem.getAttribute("version"))
            self.url          = str(XML_Rootitem.getAttribute("url"))

    def getVersion(self):
        return(self.version)
    
    def getStartupClass(self):
        return(self.startupclass)
    
    def getAutor(self):
        return(self.autor)
    
    def getEmail(self):
        return(self.email)
    
    def getURL(self):
        return(self.url)
    
    def getName(self):
        return(self.name)
    
class basePlugin(baseClass):
    
    def addXMLInfo(self, xmlinfo):
        self.xmlInfo = xmlinfo
    
    def _load(self):
        pass
    
    def getPluginEmail(self):
        return(self.xmlInfo.getEmail())
    
    def getPluginName(self):
        return(self.xmlInfo.getName())
    
    def getPluginAutor(self):
        return(self.xmlInfo.getAutor())
    
    def getPluginURL(self):
        return(self.xmlInfo.getURL())

    def getPluginVersion(self):
        return(self.xmlInfo.getVersion())
    
    def getPluginStartUpClass(self):
        return(self.xmlInfo.getStartupClass())

    def printInfo(self):
        self._log("[%s version %d]"%(self.getPluginName(), self.getPluginVersion()), self.LOG_DEBUG)
        self._log("    Autor: %s"%(self.getPluginAutor()), self.LOG_DEBUG)
        self._log("    Email: %s"%(self.getPluginEmail()), self.LOG_DEBUG)
        self._log("    URL  : %s"%(self.getPluginURL()), self.LOG_DEBUG)

    # EVENTS
    
    def plugin_init(self):
        print "IMPLEMENT plugin_init !"
        
    def plugin_loaded(self):
        print "IMPLEMENT plugin_loaded !"
        
    def plugin_exploit_modes_requested(self, langClass, isSystem, isUnix):
        # Returns a tuple which will represent a userchoice for the exploit menu.
        # (Label, Callbackstring)
        print "IMPLEMENT plugin_exploit_modes_requested"
        
    def plugin_callback_handler(self, callbackstring, haxhelper):
        # This function will be launched if the user selected one of your attacks.
        print "IMPLEMENT plugin_callback_handler"
        
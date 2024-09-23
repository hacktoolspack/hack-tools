#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
This file is part of the cintruder project, http://cintruder.03c8.net

Copyright (c) 2012/2016 psy <epsylon@riseup.net>

cintruder is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation version 3 of the License.

cintruder is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along
with cintruder; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import optparse

class CIntruderOptions(optparse.OptionParser):
    def __init__(self, *args):
        optparse.OptionParser.__init__(self, 
                           description='Captcha Intruder - OCR Bruteforcing Toolkit - by psy',
                           prog='cintruder.py',
			   version='\nCIntruder v0.3 - 2016 - (GPLv3.0) -> by psy\n',
                           usage= '\n\ncintruder [OPTIONS]')
        self.add_option("-v", "--verbose", action="store_true", dest="verbose", help="active verbose mode output results")
        self.add_option("--proxy", action="store", dest="proxy", help="use proxy server (tor: http://localhost:8118)")
        self.add_option("--gui", action="store_true", dest="web", help="run GUI (CIntruder Web Interface)")
        self.add_option("--update", action="store_true", dest="update", help="check for latest stable version")
        group1 = optparse.OptionGroup(self, "->Tracking")
        group1.add_option("--track", action="store", dest="track", help="download captchas from url (to: 'inputs/')")
        group1.add_option("--track-num", action="store", dest="s_num", help="set number of captchas to download (default: 5)")
        self.add_option_group(group1)
        group2 = optparse.OptionGroup(self, "->Training")
        group2.add_option("--train", action="store", dest="train", help="train using common OCR techniques")
        group2.add_option("--set-id", action="store", dest="setids", help="set colour's ID manually (use -v for details)")
        self.add_option_group(group2)
        group3 = optparse.OptionGroup(self, "->Cracking")
        group3.add_option("--crack", action="store", dest="crack", help="brute force using local dictionary")
        self.add_option_group(group3)
        group4 = optparse.OptionGroup(self, "->Modules (training/cracking)")
        group4.add_option("--list", action="store_true", dest="listmods", help="list available modules (from: 'mods/')")
        group4.add_option("--mod", action="store", dest="name", help="set a specific OCR exploiting module")
        self.add_option_group(group4)
        group5 = optparse.OptionGroup(self, "->Post-Exploitation (cracking)")
        group5.add_option("--xml", action="store", dest="xml", help="export result to xml format")
        group5.add_option("--tool", action="store", dest="command", help="replace suggested word on commands of another tool. use 'CINT' marker like flag (ex: 'txtCaptcha=CINT')")
        self.add_option_group(group5)

    def get_options(self, user_args=None):
        (options, args) = self.parse_args(user_args)
        options.args = args
        if (not options.train and not options.crack and not options.track and not options.listmods and not options.web and not options.update):
            print '='*75
            print ""
            print "        o8%8888,    "
            print "       o88%8888888. " 
            print "      8'-    -:8888b   "
            print "     8'         8888  "
            print "    d8.-=. ,==-.:888b  "
            print "    >8 `~` :`~' d8888   "
            print "    88         ,88888   "
            print "    88b. `-~  ':88888  "
            print "    888b \033[1;31m~==~\033[1;m .:88888 "
            print "    88888o--:':::8888      "
            print "    `88888| :::' 8888b  "
            print "    8888^^'       8888b  "
            print "   d888           ,%888b.   "
            print "  d88%            %%%8--'-.  "
            print " /88:.__ ,       _%-' ---  -  "
            print "     '''::===..-'   =  --.  `\n"
            print  self.description, "\n"
            print '='*75, "\n"
            print " * Project site: http://cintruder.03c8.net", "\n"
            print " * IRC: irc.freenode.net -> #cintruder", "\n"
            print " * Mailing list: cintruder-users@lists.sf.net", "\n"
            print '='*75
            print "\n -> For HELP use: -h or --help"
            print "\n -> For WEB interface use: --gui\n"
            print '='*55, "\n"
            return False
        return options

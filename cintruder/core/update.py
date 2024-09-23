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
import os
from subprocess import PIPE
from subprocess import Popen as execute
        
class Updater(object):
    """     
    Update CIntruder automatically from a .git repository
    """     
    def __init__(self):
        GIT_REPOSITORY = "https://github.com/epsylon/cintruder"
        rootDir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', ''))
        if not os.path.exists(os.path.join(rootDir, ".git")):
            print "Not any .git repository found!\n"
            print "="*30
            print "\nTo have working this feature, you should clone CIntruder with:\n"
            print "$ git clone %s" % GIT_REPOSITORY +"\n"
        else:
            checkout = execute("git checkout .", shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]
            if "fast-forwarded" in checkout:
                pull = execute("git pull %s HEAD" % GIT_REPOSITORY, shell=True, stdout=PIPE, stderr=PIPE).communicate()
                print "Congratulations!! CIntruder has been updated to latest version ;-)\n"
            else:
                print "You are updated! ;-)\n"

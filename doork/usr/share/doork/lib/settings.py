#!/usr/bin/env python

"""
Copyright (c) 2016 tilt (https://github.com/AeonDave/doork)
See the file 'LICENSE' for copying permission
"""

import os ,sys

VERSION = "0.2 alpha"
AUTHOR = "AeonDave"
DESCRIPTION = "Passive WebSite Scanner that achieve his result using dorks"
SITE = "https://github.com/AeonDave/doork.git"
ISSUES_PAGE = ""
GIT_REPOSITORY = "git://github.com/AeonDave/doork.git"

PLATFORM = os.name
ROOTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
WORDLISTDIR = os.path.abspath(os.path.join(ROOTDIR, 'db'))
WORDLISTFILE = os.path.abspath(os.path.join(WORDLISTDIR, 'exploit_db.txt'))
LIBDIR = os.path.abspath(os.path.dirname(__file__))
PYVERSION = sys.version.split()[0]
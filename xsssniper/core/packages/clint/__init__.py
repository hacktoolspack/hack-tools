# -*- coding: utf-8 -*-

"""
clint
~~~~~

This module sets up the main interface for all of clint.

"""


from __future__ import absolute_import

from . import arguments
from . import textui
from . import utils
from .pipes import piped_in



__title__ = 'clint'
__version__ = '0.3.0'
__build__ = 0x000300
__author__ = 'Kenneth Reitz'
__license__ = 'ISC'
__copyright__ = 'Copyright 2012 Kenneth Reitz'
__docformat__ = 'restructuredtext'


args = arguments.Args()

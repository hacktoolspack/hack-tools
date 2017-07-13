# -*- coding: utf-8 -*-

"""
clint.colored
~~~~~~~~~~~~~

This module provides a simple and elegant wrapper for colorama.

"""


from __future__ import absolute_import

import re
import sys

PY3 = sys.version_info[0] >= 3

from ..packages import colorama

__all__ = (
    'red', 'green', 'yellow', 'blue',
    'black', 'magenta', 'cyan', 'white',
    'clean', 'disable'
)

COLORS = __all__[:-2]

if 'get_ipython' in dir():
    """
       when ipython is fired lot of variables like _oh, etc are used.
       There are so many ways to find current python interpreter is ipython.
       get_ipython is easiest is most appealing for readers to understand.
    """
    DISABLE_COLOR = True
else:
    DISABLE_COLOR = False



class ColoredString(object):
    """Enhanced string for __len__ operations on Colored output."""
    def __init__(self, color, s):
        super(ColoredString, self).__init__()
        self.s = s
        self.color = color

    @property
    def color_str(self):
        if sys.stdout.isatty() and not DISABLE_COLOR:
            return '%s%s%s' % (
                getattr(colorama.Fore, self.color), self.s, colorama.Fore.RESET)
        else:
            return self.s


    def __len__(self):
        return len(self.s)

    def __repr__(self):
        return "<%s-string: '%s'>" % (self.color, self.s)

    def __unicode__(self):
        value = self.color_str
        if isinstance(value, bytes):
            return value.decode('utf8')
        return value

    if PY3:
        __str__ = __unicode__
    else:
        def __str__(self):
            return unicode(self).encode('utf8')

    def __iter__(self):
        return iter(self.color_str)

    def __add__(self, other):
        return str(self.color_str) + str(other)

    def __radd__(self, other):
        return str(other) + str(self.color_str)

    def __mul__(self, other):
        return (self.color_str * other)

    def split(self, sep=None):
        return [self._new(s) for s in self.s.split(sep)]

    def _new(self, s):
        return ColoredString(self.color, s)


def clean(s):
    strip = re.compile("([^-_a-zA-Z0-9!@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\.\{\}\|\?\<\>\\]+|[^\s]+)")
    txt = strip.sub('', str(s))

    strip = re.compile(r'\[\d+m')
    txt = strip.sub('', txt)

    return txt


def black(string):
    return ColoredString('BLACK', string)

def red(string):
    return ColoredString('RED', string)

def green(string):
    return ColoredString('GREEN', string)

def yellow(string):
    return ColoredString('YELLOW', string)

def blue(string):
    return ColoredString('BLUE', string)

def magenta(string):
    return ColoredString('MAGENTA', string)

def cyan(string):
    return ColoredString('CYAN', string)

def white(string):
    return ColoredString('WHITE', string)

def disable():
    """Disables colors."""
    global DISABLE_COLOR

    DISABLE_COLOR = True

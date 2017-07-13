# -*- coding: utf-8 -*-

"""
clint.textui.core
~~~~~~~~~~~~~~~~~

Core TextUI functionality for Puts/Indent/Writer.

"""


from __future__ import absolute_import

import sys

from .formatters import max_width, min_width
from .cols import columns
from ..utils import tsplit


__all__ = ('puts', 'puts_err', 'indent', 'columns', 'max_width', 'min_width')


STDOUT = sys.stdout.write
STDERR = sys.stderr.write

NEWLINES = ('\n', '\r', '\r\n')



class Writer(object):
    """WriterUtilized by context managers."""

    shared = dict(indent_level=0, indent_strings=[])


    def __init__(self, indent=0, quote='', indent_char=' '):
        self.indent = indent
        self.indent_char = indent_char
        self.indent_quote = quote
        if self.indent > 0:
            self.indent_string = ''.join((
                str(quote),
                (self.indent_char * (indent - len(self.indent_quote)))
            ))
        else:
            self.indent_string = ''.join((
                ('\x08' * (-1 * (indent - len(self.indent_quote)))),
                str(quote))
            )

        if len(self.indent_string):
            self.shared['indent_strings'].append(self.indent_string)


    def __enter__(self):
        return self


    def __exit__(self, type, value, traceback):
        self.shared['indent_strings'].pop()


    def __call__(self, s, newline=True, stream=STDOUT):

        if newline:
            s = tsplit(s, NEWLINES)
            s = map(str, s)
            indent = ''.join(self.shared['indent_strings'])

            s = (str('\n' + indent)).join(s)

        _str = ''.join((
            ''.join(self.shared['indent_strings']),
            str(s),
            '\n' if newline else ''
        ))
        stream(_str)


def puts(s='', newline=True, stream=STDOUT):
    """Prints given string to stdout via Writer interface."""
    Writer()(s, newline, stream=stream)


def puts_err(s='', newline=True, stream=STDERR):
    """Prints given string to stderr via Writer interface."""
    Writer()(s, newline, stream=stream)


def indent(indent=4, quote=''):
    """Indentation context manager."""
    return Writer(indent=indent, quote=quote)

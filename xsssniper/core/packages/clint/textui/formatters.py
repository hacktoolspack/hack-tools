# -*- coding: utf-8 -*-

"""
clint.textui.formatters
~~~~~~~~~~~~~~~~~~~~~~~

Core TextUI functionality for text formatting.

"""

from __future__ import absolute_import

from .colored import ColoredString, clean
from ..utils import tsplit, schunk


NEWLINES = ('\n', '\r', '\r\n')


def min_width(string, cols, padding=' '):
    """Returns given string with right padding."""

    is_color = isinstance(string, ColoredString)

    stack = tsplit(str(string), NEWLINES)

    for i, substring in enumerate(stack):
        _sub = clean(substring).ljust((cols + 0), padding)
        if is_color:
            _sub = (_sub.replace(clean(substring), substring))
        stack[i] = _sub
        
    return '\n'.join(stack)


def max_width(string, cols, separator='\n'):
    """Returns a freshly formatted """

    is_color = isinstance(string, ColoredString)

    if is_color:
        offset = 10
        string_copy = string._new('')
    else:
        offset = 0
        
    stack = tsplit(string, NEWLINES)

    for i, substring in enumerate(stack):
        stack[i] = substring.split()

    _stack = []
    
    for row in stack:
        _row = ['',]
        _row_i = 0

        for word in row:
            if (len(_row[_row_i]) + len(word)) < (cols + offset):
                _row[_row_i] += word
                _row[_row_i] += ' '
                
            elif len(word) > (cols - offset):

                # ensure empty row
                if len(_row[_row_i]):
                    _row.append('')
                    _row_i += 1

                chunks = schunk(word, (cols + offset))
                for i, chunk in enumerate(chunks):
                    if not (i + 1) == len(chunks):
                        _row[_row_i] += chunk
                        _row.append('')
                        _row_i += 1
                    else:
                        _row[_row_i] += chunk
                        _row[_row_i] += ' '
            else:
                _row.append('')
                _row_i += 1
                _row[_row_i] += word
                _row[_row_i] += ' '

        _row = map(str, _row)
        _stack.append(separator.join(_row))

    _s = '\n'.join(_stack)
    if is_color:
        _s = string_copy._new(_s)
    return _s

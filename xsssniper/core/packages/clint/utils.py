# -*- coding: utf-8 -*-

"""
clint.utils
~~~~~~~~~~~~

Various Python helpers used within clint.

"""

from __future__ import absolute_import
from __future__ import with_statement

import errno
import os.path
from os import makedirs
from glob import glob

try:
    basestring
except NameError:
    basestring = str

def expand_path(path):
    """Expands directories and globs in given path."""

    paths = []
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)

    if os.path.isdir(path):

        for (dir, dirs, files) in os.walk(path):
            for file in files:
                paths.append(os.path.join(dir, file))
    else:
        paths.extend(glob(path))

    return paths



def is_collection(obj):
    """Tests if an object is a collection. Strings don't count."""

    if isinstance(obj, basestring):
        return False

    return hasattr(obj, '__getitem__')


def mkdir_p(path):
    """Emulates `mkdir -p` behavior."""
    try:
        makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise

def tsplit(string, delimiters):
    """Behaves str.split but supports tuples of delimiters."""

    delimiters = tuple(delimiters)
    stack = [string,]

    for delimiter in delimiters:
        for i, substring in enumerate(stack):
            substack = substring.split(delimiter)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i+j, _substring)

    return stack

def schunk(string, size):
    """Splits string into n sized chunks."""

    stack = []

    substack = []
    current_count = 0

    for char in string:
        if not current_count < size:
            stack.append(''.join(substack))
            substack = []
            current_count = 0

        substack.append(char)
        current_count += 1

    if len(substack):
        stack.append(''.join(substack))

    return stack

#/usr/bin/env python

from packages.clint.textui import colored

def info(message, prefix, label=''):
    print prefix + label + message

def success(message, prefix, label='SUCCESS: '):
    print prefix + colored.green(label) + message

def warning(message, prefix, label='WARNING: '):
    print prefix + colored.yellow(label) + message

def error(message, prefix, label='ERROR: '):
    print prefix + colored.red(label) + message

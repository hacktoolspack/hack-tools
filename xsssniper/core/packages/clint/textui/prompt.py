# -*- coding: utf8 -*-

"""
clint.textui.prompt
~~~~~~~~~~~~~~~~~~~

Module for simple interactive prompts handling

"""

from __future__ import absolute_import

from re import match, I

def yn(prompt, default='y', batch=False):
    # A sanity check against default value
    # If not y/n then y is assumed 
    if default not in ['y', 'n']:
        default = 'y'
    
    # Let's build the prompt
    choicebox = '[Y/n]' if default == 'y' else '[y/N]' 
    prompt = prompt + ' ' + choicebox + ' ' 

    # If input is not a yes/no variant or empty
    # keep asking
    while True:
        # If batch option is True then auto reply 
        # with default input
        if not batch:
            input = raw_input(prompt).strip()
        else:
            print prompt
            input = ''

        # If input is empty default choice is assumed
        # so we return True
        if input == '':
            return True

        # Given 'yes' as input if default choice is y
        # then return True, False otherwise 
        if match('y(?:es)?', input, I):
            return True if default == 'y' else False

        # Given 'no' as input if default choice is n
        # then return True, False otherwise
        elif match('n(?:o)?', input, I):
            return True if default == 'n' else False

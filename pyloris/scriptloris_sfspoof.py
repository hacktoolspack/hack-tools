#! /usr/bin/env python

"""
scriptloris_sfspoof.py
A quick script to demonstrate how ScriptLoris could be used to spoof valid
downloads on SourceForge.net, in order to improve a project's ranking. Bonus
points for using TOR Switcher in conjunction with this script.

This script requires TOR to be setup and running on localhost:9050.
"""

projectname = 'pyloris'
downloadrefer = 'http://sourceforge.net/projects/pyloris/files/pyloris/pyloris-3.0.zip/download'
downloadmirror = 'superb-east'
downloadhost1 = 'downloads.sourceforge.net'
downloadhost2 = 'voxel.dl.sourceforge.net'
downloadfile = '/sourceforge/%s/pyloris-3.0.zip' % (projectname)
downloadevery = 600
headevery = 60
pagehitevery = 120
logohitevery = 180
useragent = 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.2.15 Version/10.00'
sockshost = 'localhost'
socksport = 9050

from libloris import *

def main(projectname, downloadrefer, downloadmirror, downloadhost1, downloadhost2, downloadfile,
        downloadevery, headevery, pagehitevery, logohitevery, useragent, sockshost, socksport):
    options = DefaultOptions()
    options['referer'] = '%s.sourceforge.net/projects/%s/files/%s/download' % (projectname, projectname, downloadfile)
    options['host'] = downloadhost1
    options['port'] = 80
    options['connectionspeed'] = 0
    options['timebetweenconnections'] = downloadevery
    options['threadlimit'] = 1
    options['connectionlimit'] = 1
    options['socksversion'] = 'SOCKS5'
    options['sockshost'] = sockshost
    options['socksport'] = socksport
    options['request'] = 'GET %s?use_mirror=%s HTTP/1.1\r\n' %(downloadfile, downloadmirror)
    options['request'] += 'Host: %s\r\n' % (downloadhost1)
    options['request'] += 'Referer: %s\r\n' % (downloadrefer)
    options['request'] += 'User-Agent: %s\r\n\r\n' %(useragent)

    loris1 = ScriptLoris()
    loris1.LoadOptions(options)
    loris1.start()

    options['host'] = downloadhost2
    options['request'] = 'GET %s HTTP/1.1\r\n' % (downloadfile)
    options['request'] += 'Host: %s\r\n' % (downloadhost2)
    options['request'] += 'Referer: %s\r\n' % (downloadrefer)
    options['request'] += 'User-Agent: %s\r\n\r\n' % (useragent)

    loris2 = ScriptLoris()
    loris2.LoadOptions(options)
    loris2.start()

    options['host'] = '%s.sourceforge.net' % (projectname)
    options['request'] = 'HEAD / HTTP/1.1\r\n'
    options['request'] += 'Host: %s.sourceforge.net\r\n' % (projectname)
    options['request'] += 'User-Agent: %s\r\n\r\n' % (useragent)
    options['timebetweenconnections'] = headevery

    loris3 = ScriptLoris()
    loris3.LoadOptions(options)
    loris3.start()

    options['request'] = 'GET / HTTP/1.1\r\n'
    options['request'] += 'Host: %s.sourceforge.net\r\n' % (projectname)
    options['request'] += 'User-Agent: %s\r\n\r\n' % (useragent)
    options['timebetweenconnections'] = pagehitevery

    loris4 = ScriptLoris()
    loris4.LoadOptions(options)
    loris4.start()

    options['host'] = 'sflogo.sourceforge.net'
    options['request'] = 'GET /sflogo.php?group_id=266347&type=12 HTTP/1.1\r\n'
    options['request'] += 'Host: %sflogo.sourceforge.net\r\n'
    options['request'] += 'User-Agent: %s\r\n\r\n' % (useragent)
    options['timebetweenconnections'] = logohitevery

    loris5 = ScriptLoris()
    loris5.LoadOptions(options)
    loris5.start()

    try:
        while True:
            print('File Downloads: %i' % loris1.status()[0])
            print('Download Refers: %i' % loris2.status()[0])
            print('HEAD Requests: %i' % loris3.status()[0])
            print('Page Requests: %i' % loris4.status()[0])
            print('Logo Requests: %i' % loris5.status()[0])
            time.sleep(60)
    except:
        print('Quitting...')

if __name__ == "__main__":
    main(projectname, downloadrefer, downloadmirror, downloadhost1, downloadhost2, downloadfile,
        downloadevery, headevery, pagehitevery, logohitevery, useragent, sockshost, socksport)


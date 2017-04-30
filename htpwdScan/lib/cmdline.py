#!/usr/bin/env python
#
#  Parse command line arguments and decode string
#

import argparse
import sys
from lib.encodings import system_decode
import os
import pprint


def parse_args(self):
    parser = argparse.ArgumentParser(prog='htpwdScan',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description='* An HTTP weak pass scanner. By LiJieJie *',
                                     usage='htpwdScan.py [options]')

    target = parser.add_argument_group('Target')
    target.add_argument('-u', metavar='REQUESTURL', type=str,
                        help='Explicitly set request URL, e.g.\n-u="https://www.test.com/login.php"')
    target.add_argument('-f', metavar='REQUESTFILE', type=str,
                        help='Load HTTP request from file')
    target.add_argument('-https', default=False, action='store_true',
                        help='Explicitly set -https when load request from file and \nSSL enabled')
    target.add_argument('-get', default=False,
                        action='store_true',
                        help='Force method GET when -u was set. default: POST')
    target.add_argument('-basic', metavar='',type=str, nargs='+',
                        help='HTTP Basic Auth brute, \ne.g. -basic users.dic pass.dic')

    dictionary = parser.add_argument_group('Dictionary')
    dictionary.add_argument('-d', metavar='Param=DictFile', type=str, nargs='+',
                        help='Set dict file for parameters, \n' + \
                        'support hash functions like md5, md5_16, sha1. \n' + \
                        'e.g. -d user=users.dic pass=md5(pass.dic)')

    detect = parser.add_argument_group('Detect')
    detect.add_argument('-no302', default=False, action='store_true',
                        help='302 redirect insensitive, default: sensitive')
    detect.add_argument('-err', metavar='ERR', default='', type=str, nargs='+',
                        help='String indicates fail in response text, \ne.g. -err "user not exist" "password wrong"')
    detect.add_argument('-suc', metavar='SUC', default='', type=str, nargs='+',
                        help='String indicates success in response text, \ne.g. -suc "welcome," "admin"')
    detect.add_argument('-herr', metavar='HERR', default='', type=str,
                        help='String indicates fail in response headers')
    detect.add_argument('-hsuc', metavar='HSUC', default='', type=str,
                        help='String indicates success in response headers')
    detect.add_argument('-rtxt', metavar='RetryText', type=str, default='',
                        help='Retry when it appears in response text, \ne.g. -rtxt="IP blocked"')
    detect.add_argument('-rntxt', metavar='RetryNoText', type=str, default='',
                        help='Retry when it does not appear in response text, \ne.g. -rntxt="<body>"')
    detect.add_argument('-rheader', metavar='RetryHeader', type=str, default='',
                        help='Retry when it appears in response headers, \ne.g. -rheader="Set-Cookie:"')
    detect.add_argument('-rnheader', metavar='RetryNoHeader', type=str, default='',
                        help='Retry when it didn\'t appear in response headers, \ne.g. -rheader="HTTP/1.1 200 OK"')

    proxy_spoof = parser.add_argument_group('Proxy and spoof')
    proxy_spoof.add_argument('-proxy', metavar='Server:Port', default='', type=str,
                        help='Set several HTTP proxies \ne.g. -proxy=127.0.0.1:8000,8.8.8.8:8000')
    proxy_spoof.add_argument('-proxylist', metavar='ProxyListFile', default='', type=str,
                        help='Load HTTP proxies from file, one proxy per line, \ne.g. -proxylist=proxys.txt')
    proxy_spoof.add_argument('-checkproxy', default=False, action='store_true',
                        help='Check the usability of loaded proxy servers.\nOutput file is 001.proxy.servers.txt')
    proxy_spoof.add_argument('-fip', default=False, action='store_true',
                        help='Spoof source IP by random X-Forwarded-For')
    proxy_spoof.add_argument('-fsid', type=str,
                        help='Use a random session ID. e.g. -fsid PHPSESSID')
    proxy_spoof.add_argument('-sleep', metavar='SECONDS', type=str, default='',
                        help='Sleep some time after each request,\navoid IP blocked by web server')

    database = parser.add_argument_group('Database attack')
    database.add_argument('-database', type=str,
                          help='Load leaked passwords to attack. \ne.g. -database user,pass=csdn.txt')
    database.add_argument('-regex', type=str,
                          help='Regex used to extract values. \ne.g. -regex="(\S+)\s+(\S+)"')

    general = parser.add_argument_group('General')
    general.add_argument('-t', metavar='THREADS', type=int, default=50,
                        help='50 threads by default')
    general.add_argument('-o', metavar='OUTPUT', type=str, default='000.Cracked.Passwords.txt',
                        help='Output file. default: 000.Cracked.Passwords.txt')
    general.add_argument('-debug', default=False, action='store_true',
                        help='Enter debug mode to test request and response')
    general.add_argument('-nov', default=False, action='store_true',
                        help='Do not print verbose info, only print cracked ones')
    general.add_argument('-v', action='version', version='%(prog)s 0.0.3')


    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()

    if args.err:
        for i in range(len(args.err)):
            args.err[i] = system_decode(args.err[i])
    if args.suc:
        for i in range(len(args.suc)):
            args.suc[i] = system_decode(args.suc[i])
    if args.rtxt:
        args.rtxt = system_decode(args.rtxt)
    if args.rntxt:
        args.rntxt = system_decode(args.rntxt)

    check_args(args)
    self.args = args

    if self.args.debug:
        self.args.t = 1    # thread set to 1 in debug mode
        self.lock.acquire()
        print '*' * self.console_width
        print '[Parsed Arguments]\n'
        pprint.pprint(self.args.__dict__)
        print '\n' + '*' * self.console_width
        self.lock.release()

    self.request_thread_count = self.args.t


def check_args(args):
    if not args.f and not args.u:
        msg = 'Both RequestFILE and RequestURL were not set!\n' + \
              ' ' * 11 + 'Use -f or -u to set one'
        raise Exception(msg)

    if args.basic:
        if len(args.basic) != 2:
            msg = 'Two dict files are required. e.g. -basic users.dic pass.dic'
            raise Exception(msg)

        for df in args.basic:
            if not os.path.exists(df):
                raise Exception('Dict file not found: %s' % df)

    if not args.basic and not args.checkproxy and not args.database and not args.d:
        raise Exception('Please feed dict files. e.g. -d user=users.dic pass=md5(pass.dic)')

    if args.checkproxy and os.path.exists('001.proxy.servers.txt'):
        os.remove('001.proxy.servers.txt')

    if args.database:
        data_file = args.database.split('=')[1]
        if not os.path.exists(data_file):
            raise Exception('File not found: %s' % data_file)
        if not args.regex:
            raise Exception('Please set -regex to extract data. \ne.g. -regex="(\S+)\s+(\S+)"')


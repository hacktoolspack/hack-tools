#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''

htpwdScan v 0.0.3
A simple and fast HTTP(s) weak pass scanner
By LiJieJie (my[at]lijiejie.com)

TODO:
    Consider to save all HTTP requests and responses to temp file.

'''


import threading
import time

from lib.cmdline import parse_args
from lib.consle_width import getTerminalSize
from lib.proxy import load_proxy
from lib.queue import gen_queue
from lib.request_file import parse_request
from lib.request import do_request
from lib.colorama import init, Fore, Back, Style

class Scanner():
    def __init__(self):
        init()
        self.console_width = getTerminalSize()[0] - 2
        self.lock = threading.Lock()
        self.STOP_ME = False
        parse_args(self)
        load_proxy(self)
        self.gen_params_queue()
        parse_request(self)

    def gen_params_queue(self):
        self.queue_thread = threading.Thread(target=gen_queue, args=(self,))
        self.queue_thread.start()

    def print_s(self, s, color_red=False):
        self.lock.acquire()
        print Fore.MAGENTA + s if color_red else Fore.RESET + s
        self.lock.release()

    def now_time(self):
        return time.strftime('%H:%M:%S', time.localtime())

    def run(self):
        self.start_time = time.time()
        self.cracked_count = 0
        self.print_s('Job started at %s' % self.now_time() + '\n' + '*' * s.console_width)
        for i in range(self.args.t):
            t = threading.Thread(target=do_request, args=(s,))
            t.setDaemon(True)
            t.start()
        try:
            while s.request_thread_count > 0:
                time.sleep(0.1)
            s.print_s('_' * s.console_width + '\nTask finished at %s. Cost %.2f seconds' %
                      (self.now_time(), time.time() - s.start_time) )
        except KeyboardInterrupt, e:
            s.STOP_ME = True
            time.sleep(1.0)
            s.print_s('_' * s.console_width + '\n[KeyboardInterrupt] \nTask aborted at %s, cost %.2f seconds' %
                      (self.now_time(), time.time() - s.start_time) )

        if s.args.checkproxy:
            s.print_s('Found %s proxy server(s) in total.' % s.cracked_count if s.cracked_count else 'No proxy servers found.')
        else:
            s.print_s('Cracked %s item(s) in total.' % s.cracked_count if s.cracked_count else 'No one was cracked.')


s = Scanner()
s.run()



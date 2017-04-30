# -*- coding: utf-8 -*-

import os
import sys
from time import strftime

def logfile(to_file=True, filename="bot_debug.log"):			  # redirects all stdout and stderr to specified logfile
	if to_file:
		### Remove/comment this block to disable logging stdout/err to a file
		so = se = open(filename, 'w', 0)
		# re-open stdout without buffering
		sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
		# redirect stdout and stderr to the log file
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
		### Endblock
	else:
		pass # log statements simply get printed to stdout


def log(prefix, content=''):                                      # function used to log things to stdout with a timestamp
    try:
        for line in content.split('\n'):
            print('[%s] %s%s' % (strftime("%Y-%m-%d %H:%M:%S"), prefix, line))
    except:
        print('[%s] %s%s' % (strftime("%Y-%m-%d %H:%M:%S"), prefix, content))
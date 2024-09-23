#!/usr/bin/env python

"""
Copyright (c) 2016 tilt (https://github.com/AeonDave/doork)
See the file 'LICENSE' for copying permission
"""

import logging, sys

logger = logging.getLogger('doorkLogger')
stream = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
stream.setFormatter(formatter)
logger.addHandler(stream)
logger.setLevel(logging.INFO)

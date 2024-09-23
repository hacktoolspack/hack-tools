#!/usr/bin/env python

"""
Copyright (c) 2014 tilt (https://github.com/AeonDave/tilt)
See the file 'LICENSE' for copying permission
"""
from lib.logger import logger

def sort(value):
    return sorted(value)

def remove_duplicates(value):
    return set(value)

def list_to_string(value):
    for host in value:
        if host:
            if type(host) is list:
                for element in host:
                    logger.info(element)
            if type(host) is str:
                logger.info(host)

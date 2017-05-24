#!/usr/bin/env python
#-*- encoding: utf-8 -*-

"""
    Setup for Panthera buildZip application
"""
 
from distutils.core import setup 

setup(
    name='UDoS for GNU/Linux - Universal DoS and DDoS testing tool',
    author='Damian Kęska',
    license = "GPL",
    package_dir={'': 'src/udos/lib'},      
    packages=['udos'],
    author_email='webnull.www@gmail.com',
    scripts=['src/udos/udos']
)

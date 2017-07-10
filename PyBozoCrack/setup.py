#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='pybozocrack',
    version='1.2.2.3',
    description='PyBozoCrack is a depressingly effective MD5 password hash cracker with almost zero CPU/GPU load.',
    long_description=readme + '\n\n' + history,
    author='Henrique Pereira',
    author_email='ikkibr@gmail.com',
    url='https://github.com/ikkebr/pybozocrack',
    py_modules = ['pybozocrack'],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='pybozocrack',
    classifiers=[
		'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    entry_points={'console_scripts': ['pybozocrack = pybozocrack:main']},)

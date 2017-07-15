#!/usr/bin/python
# -*- coding: utf-8 -*-

from scapy.all import *


def pktPrint(pkt):
    if pkt.haslayer(Dot11Beacon):
        print '[+] Detected 802.11 Beacon Frame'
    elif pkt.haslayer(Dot11ProbeReq):
        print '[+] Detected 802.11 Probe Request Frame'
    elif pkt.haslayer(TCP):
        print '[+] Detected a TCP Packet'
    elif pkt.haslayer(DNS):
        print '[+] Detected a DNS Packet'


conf.iface = 'mon0'
sniff(prn=pktPrint)

#!/usr/bin/python
# -*- coding: utf-8 -*-
from scapy.all import *

interface = 'mon0'
probeReqs = []


def sniffProbe(p):
    if p.haslayer(Dot11ProbeReq):
        netName = p.getlayer(Dot11ProbeReq).info
        if netName not in probeReqs:
            probeReqs.append(netName)
            print '[+] Detected New Probe Request: ' + netName


sniff(iface=interface, prn=sniffProbe)


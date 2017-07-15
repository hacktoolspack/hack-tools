#!/usr/bin/python
# -*- coding: utf-8 -*-
from scapy.all import *

dnsRecords = {}

def handlePkt(pkt):
    if pkt.haslayer(DNSRR):
        rrname = pkt.getlayer(DNSRR).rrname
        rdata = pkt.getlayer(DNSRR).rdata
        if dnsRecords.has_key(rrname):
            if rdata not in dnsRecords[rrname]:
                dnsRecords[rrname].append(rdata)
        else:
            dnsRecords[rrname] = []
            dnsRecords[rrname].append(rdata)


def main():
    pkts = rdpcap('fastFlux.pcap')
    for pkt in pkts:  
        handlePkt(pkt)
    
    for item in dnsRecords:
        print '[+] '+item+' has '+str(len(dnsRecords[item])) \
            + ' unique IPs.'


if __name__ == '__main__':
    main()

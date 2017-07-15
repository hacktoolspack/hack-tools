#!/usr/bin/python
# -*- coding: utf-8 -*-
import dpkt
import socket
import pygeoip
import optparse
gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')


def retKML(ip):
    rec = gi.record_by_name(ip)
    try:
        longitude = rec['longitude']
        latitude = rec['latitude']
        kml = (
               '<Placemark>\n'
               '<name>%s</name>\n'
               '<Point>\n'
               '<coordinates>%6f,%6f</coordinates>\n'
               '</Point>\n'
               '</Placemark>\n'
               ) %(ip,longitude, latitude)
        return kml
    except:
        return ''


def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            srcKML = retKML(src)
            dst = socket.inet_ntoa(ip.dst)
            dstKML = retKML(dst)
            kmlPts = kmlPts + srcKML + dstKML
        except:
            pass
    return kmlPts


def main():
    parser = optparse.OptionParser('usage %prog -p <pcap file>')
    parser.add_option('-p', dest='pcapFile', type='string',\
      help='specify pcap filename')
    (options, args) = parser.parse_args()
    if options.pcapFile == None:
        print parser.usage
        exit(0)
    pcapFile = options.pcapFile
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)

    kmlheader = '<?xml version="1.0" encoding="UTF-8"?>\
    \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
    print kmldoc


if __name__ == '__main__':
    main()


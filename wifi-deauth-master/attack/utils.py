import os
import struct

from scapy.all import RadioTap

from exceptions import AttackException
from sniffer import WiFiSniffer


class ChannelFinder(object):
    
    '''Find channel used by an access point whose MAC address is given.'''
    
    DEFAULT_TIMEOUT = 60
    
    TIMESTAMP_FLAG = 0x1
    FLAGS_FLAG = 0x2
    RATE_FLAG = 0x3
    CHANNEL_FLAG = 0x8
    
    TIMESTAMP_BYTES = 8
    FLAGS_BYTES = 1
    RATE_BYTES = 1
    
    CHANNEL_1_FREQ = 2412
    
    def __init__(self, interface, bssid):
        self.interface = interface
        self.bssid = bssid
        
    def find(self):
        sniffer = WiFiSniffer(self.interface)
        packets = sniffer.sniff(timeout=self.DEFAULT_TIMEOUT,
                                lfilter=lambda pkt: pkt.haslayer(RadioTap) and\
                                                    pkt.addr3 == self.bssid)
        channel_packet = None
        
        # Find a packet containing channel information.
        for packet in packets:
            if self._packet_has_channel_info(packet[RadioTap]):
                channel_packet = packet[RadioTap]
                break
            
        sniffer.stop()
                
        if channel_packet is None:
            raise AttackException('Failed to find AP channel!')
                
        # Extract channel from radiotap header.
        return self._extract_channel_from(channel_packet)
    
    def _packet_has_channel_info(self, radiotap_header):
        return radiotap_header.present & self.CHANNEL_FLAG != 0
    
    def _extract_channel_from(self, radiotap_header):
        offset = 0
        if radiotap_header.present & self.TIMESTAMP_FLAG != 0:
            offset += self.TIMESTAMP_BYTES
        if radiotap_header.present & self.FLAGS_FLAG != 0:
            offset += self.FLAGS_BYTES
        if radiotap_header.present & self.RATE_FLAG != 0:
            offset += self.RATE_BYTES
        
        # Decode frequency and then map it to the channel number.    
        freq_bytes = radiotap_header.notdecoded[offset:offset+2]    
        freq = struct.unpack('h', freq_bytes)[0]
        
        # Only valid for 2.4 GHz frequency ranges!
        if freq == 2484:
            channel = 14
        else:
            channel = 1 + (freq - self.CHANNEL_1_FREQ) / 5
            
        return channel
    
    
class WiFiInterface(object):
    
    def __init__(self, interface):
        if isinstance(interface, self.__class__):
            self.interface_name = interface.get_name()
        else:
            self.interface_name = interface
        
    def get_name(self):
        return self.interface_name
        
    def set_channel(self, channel):
        command = 'iw %s set channel %d > /dev/null 2>&1'\
                   % (self.interface_name, channel)
        exit_code = os.system(command)
        if exit_code != 0:
            msg = 'Failed to set channel %d on interface %s!' %\
                   (channel, self.interface_name)
            raise AttackException(msg)
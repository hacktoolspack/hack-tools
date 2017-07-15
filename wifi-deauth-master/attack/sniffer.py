import threading
import Queue

from scapy.all import sniff, Dot11


class WiFiSniffer(object):
    
    '''A non-blocking 802.11 sniffer that works on top of Scapy's sniff
    function. Every relevant packet sniffed is then yielded to the
    client, which makes this object a Python generator.'''
    
    def __init__(self, interface):
        self.interface = interface.get_name()
        
    def _do_sniff(self, timeout=None, lfilter=None):
        lfilter = lfilter or (lambda packet: True)
        sniff(iface=self.interface,
              prn=lambda packet: self.packet_queue.put(packet),
              store=0,
              lfilter=lambda packet: lfilter(packet) and packet.haslayer(Dot11),
              stop_filter=lambda packet: self.stopped,
              timeout=timeout)
        
    def stop(self):
        self.stopped = True
        
    def sniff(self, timeout=None, lfilter=None):
        # Initialize a (synced) queue to retrieve packets from the sniffer. 
        self.packet_queue = Queue.Queue()

        # Flag set by clients through the stop method whenever they want to
        # stop the capture.
        self.stopped = False

        # Start an internal thread that will handle the call to Scapy's sniff
        # function, which is blocking.
        sniffer_thread = threading.Thread(target=self._do_sniff,
                                          args=(timeout,lfilter))
        sniffer_thread.setDaemon(True)
        sniffer_thread.start()
        
        while sniffer_thread.is_alive() and not self.stopped:
            # Yield sniffed packets while the timeout supplied does not
            # expire. The sniffer thread will automatically die once
            # this time elapses.
            try:
                packet = self.packet_queue.get(timeout=1)
            except Queue.Empty:
                continue
            else:
                yield packet
    
        while not self.packet_queue.empty() and not self.stopped:
            # Finally, yield remaining packets, if any.
            yield self.packet_queue.get()
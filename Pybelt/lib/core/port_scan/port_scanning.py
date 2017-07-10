import socket
import time
import Queue
import threading
from lib.core.settings import LOGGER
from lib.core.settings import RESERVED_PORTS


class PortScanner(object):

    connection_made = ""  # Connection made in list form

    def __init__(self, host):
        self.host = host
        self.ports = RESERVED_PORTS

    def connect_to_host(self):

        try:
            # Calling the thread class
            rst = RunScanThread(self.host)
            t2 = threading.Thread(target=rst.run_scan)
            t2.start()
        except Exception, e:
            LOGGER.error(e)


# Thread Class
class RunScanThread(PortScanner):

    def run_scan(self):
        start_time = time.time()

        def scn(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                res = sock.connect_ex((self.host, port))
                sock.settimeout(3)
                if res == 0:
                    LOGGER.info("[*] Open: {}  {}".format(port, RESERVED_PORTS[port]))
                    self.connection_made += "{}, ".format(port)
                sock.close()
            except Exception, e:
                print e

        q = Queue.Queue()

        def threader():
            worker = q.get()
            scn(worker)
            q.task_done()

        for x in range(200):
            t = threading.Thread(target=threader)
            t.daemon = True
            t.start()

        for worker in RESERVED_PORTS.keys():
            q.put(worker)
            pass

        q.join()

        stop_time = time.time()
        no_ports = "\033[91mNo ports available or open\033[0m"
        LOGGER.info("Completed in {} seconds".format(str(stop_time - start_time)))
        LOGGER.info("Ports readily available: {}".format(''.join(str(self.connection_made if self.connection_made is not "" else no_ports))))

# -*- coding: utf-8 -*-
 
import time, socket

def portscan(host, max_port=1000):
    yield 'Starting Singlethreaded Portscan of %s.' % host
    benchmark = time.time()
    try:
        remoteServerIP  = socket.gethostbyname(host)
    except Exception as e:
        yield e

    ports = []
    for port in range(1,max_port):  
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if s.connect_ex((remoteServerIP, port)) == 0:
            ports.append(port)
            yield port
        s.close()

    yield ports
    yield 'Finished Scan in %ss.' % str(round(time.time() - benchmark,2))

if __name__ == "__main__":
    for line in portscan("localhost", 1000):
        print line
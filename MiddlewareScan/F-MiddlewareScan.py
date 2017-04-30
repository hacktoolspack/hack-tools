#coding:utf-8
#author:wolf@future-sec

import getopt
import sys
import Queue
import threading
import socket
import urllib2
import time
import ssl
import os

queue = Queue.Queue()
sys.path.append("plugins")
mutex = threading.Lock()
timeout = 10
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
class ThreadNum(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            try:
                if queue.empty():break
                queue_task = self.queue.get()
            except:
                break
            try:
                task_type,task_host,task_port = queue_task.split(":")
                if task_type == 'portscan':
                    port_status = scan_port(task_type,task_host,task_port)
                    if port_status == True:
                        queue.put(":".join(['discern',task_host,task_port]))
                elif task_type == 'discern':
                    discern_type = scan_discern(task_type,task_host,task_port)
                    if discern_type:
                        queue.put(":".join([discern_type,task_host,task_port]))
                else:
                    scan_vul(task_type,task_host,task_port)
            except:
                continue
def scan_port(task_type,host,port):
    try:
        socket.setdefaulttimeout(timeout/2)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((str(host),int(port)))
        log(task_type,host,port)
        sock.close()
        return True
    except:
        return False
def log(scan_type,host,port,info=''):
    mutex.acquire()
    time_str = time.strftime('%X', time.localtime( time.time()))
    if scan_type == 'portscan':
        print "[%s] %s:%d open"%(time_str,host,int(port))
    elif scan_type == 'discern':
        print "[%s] http://%s:%d is %s"%(time_str,host,int(port),info)
    else:
        if info:
            print "[*%s] %s"%(time_str,info)
            log_file = open('result.log','a')
            log_file.write("[*%s] %s\r\n"%(time_str,info))
            log_file.close()
        else:
            print "[%s] http://%s:%s call plugin %s"%(time_str,host,port,scan_type)
    mutex.release()
def read_config(config_type):
    if config_type == 'discern':
        mark_list=[]
        config_file = open('discern_config.ini','r')
        for mark in config_file:
            name,location,key,value = mark.strip().split("|")
            mark_list.append([name,location,key,value])
        config_file.close()
        return mark_list
    elif config_type == 'plugin':
        plugin_list = {}
        config_file = open('plugin_config.ini','r')
        for plugin in config_file:
            name,plugin_file_list = plugin.strip().split("|")
            plugin_list[name]=[]
            plugin_list[name] = plugin_file_list.split(",")
        config_file.close()
        return plugin_list
        
def scan_discern(scan_type,host,port):
    mark_list = read_config('discern')
    for mark_info in mark_list:
        if mark_info[1] == 'header':
            try:
                header = urllib2.urlopen("http://%s:%d"%(host,int(port)),timeout=timeout).headers
            except urllib2.HTTPError,e:
                header = e.headers
            except Exception,e:
                return False
            try:
                if mark_info[3].lower() in header[mark_info[2]].lower():
                    log(scan_type,host,port,mark_info[0])
                    return mark_info[0]
            except Exception,e:
                continue
        elif mark_info[1] == 'file':
            try:
                re_html = urllib2.urlopen("http://%s:%d/%s"%(host,int(port),mark_info[2]),timeout=timeout).read()
            except urllib2.HTTPError,e:
                re_html = e.read()
            except Exception,e:
                return False
            if mark_info[3].lower() in re_html.lower():
                log(scan_type,host,port,mark_info[0])
                return mark_info[0]
def scan_vul(scan_type,host,port):
    vul_plugin = read_config("plugin")
    for plugin_name in vul_plugin[scan_type]:
        try:
            req = __import__(plugin_name)
            log(plugin_name,host,port)
            vul_data = req.check(host,port,timeout)
            if vul_data.split("|")[0].upper()=="YES":
                log(scan_type,host,port,vul_data.split("|")[1])
        except:
            continue
def get_ip_list(ip):
    ip_list = []
    iptonum = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])
    numtoip = lambda x: '.'.join([str(x/(256**i)%256) for i in range(3,-1,-1)])
    if '-' in ip:
        ip_range = ip.split('-')
        ip_start = long(iptonum(ip_range[0]))
        ip_end = long(iptonum(ip_range[1]))
        ip_count = ip_end - ip_start
        if ip_count >= 0 and ip_count <= 65536:
            for ip_num in range(ip_start,ip_end+1):
                ip_list.append(numtoip(ip_num))
        else:
            print '-h wrong format'
    elif '.ini' in ip:
        ip_config = open(ip,'r')
        for ip in ip_config:
            ip_list.extend(get_ip_list(ip.strip()))
        ip_config.close()
    else:
        ip_split=ip.split('.')
        net = len(ip_split)
        if net == 2:
            for b in range(1,255):
                for c in range(1,255):
                    ip = "%s.%s.%d.%d"%(ip_split[0],ip_split[1],b,c)
                    ip_list.append(ip)
        elif net == 3:
            for c in range(1,255):
                ip = "%s.%s.%s.%d"%(ip_split[0],ip_split[1],ip_split[2],c)
                ip_list.append(ip)
        elif net ==4:
            ip_list.append(ip)
        else:
            print "-h wrong format"
    return ip_list
def t_join(m_count):
    tmp_count = 0
    i = 0
    while True:
        time.sleep(1)
        ac_count = threading.activeCount()
        if ac_count < m_count and ac_count == tmp_count:
            i+=1
        else:
            i = 0
        tmp_count = ac_count
        #print ac_count,queue.qsize()
        if (queue.empty() and threading.activeCount() <= 1) or i > 5:
            break
def put_queue(ip_list,port_list):
    for ip in ip_list:
        for port in port_list:
            queue.put(":".join(['portscan',ip,port]))
if __name__=="__main__":
    msg = '''
A vulnerability detection scripts for middleware services author:wolf@future-sec
Usage: python F-MiddlewareScan.py -h 192.168.1 [-p 7001,8080] [-m 50] [-t 10]
    '''
    if len(sys.argv) < 2:
        print msg
    try:
        options,args = getopt.getopt(sys.argv[1:],"h:p:m:t:")
        ip = ''
        port = '80,4848,7001,7002,8000,8001,8080,8081,8888,9999,9043,9080'
        m_count = 100
        for opt,arg in options:
            if opt == '-h':
                ip = arg
            elif opt == '-p':
                port = arg
            elif opt == '-m':
                m_count = int(arg)
            elif opt == '-t':
                timeout = int(arg)
        if ip:
            ip_list = get_ip_list(ip)
            port_list = []
            if '.ini' in port:
                port_config = open(port,'r')
                for port in port_config:
                    port_list.append(port.strip())
                port_config.close()
            else:
                port_list = port.split(',')
            put_queue(ip_list,port_list)
            for i in range(m_count):
                t = ThreadNum(queue)
                t.setDaemon(True)
                t.start()
            t_join(m_count)
    except Exception,e:
        print msg


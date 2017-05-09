#!/usr/bin/env python
# -*- coding: utf_8 -*-
# Date: 2015/9/17
# Created by 独自等待
# 博客 http://www.waitalone.cn/
import sys
import threading
from optparse import OptionParser
from multiprocessing.dummy import Pool as ThreadPool
try:
    from Queue import Queue
except ImportError:
    from queue import Queue
try:
    from lxml import html
except ImportError:
    raise SystemExit('\n[X] lxml模块导入错误,请执行pip install lxml安装!')

logo = '''
 _   _        _  _      __        __            _      _
| | | |  ___ | || |  ___\ \      / /___   _ __ | |  __| |
| |_| | / _ \| || | / _ \\ \ /\ / // _ \ | '__|| | / _` |
|  _  ||  __/| || || (_) |\ V  V /| (_) || |   | || (_| | |_| |_| \___||_||_| \___/  \_/\_/  \___/ |_|   |_| \__,_|


改版于 http://www.waitalone.cn/ 增加了多线程和从文件读取功能
'''

dic = {}
lock = threading.Lock()
class SubMain():
    '''
    渗透测试域名收集
    '''
    def __init__(self):
        self.ips = {}

    @staticmethod
    def get_360(domain):
        url_360 = 'http://webscan.360.cn/sub/index/?url=%s'%domain
        scan_data = requests.get(url_360).text
        html_data = html.fromstring(scan_data)
        sub_domains = html_data.xpath("//dd/strong/text()")
        return sub_domains

    def get_links(self):
        url_link = 'http://i.links.cn/subdomain/'
        link_post = 'domain=%s&b2=1&b3=1&b4=1' % self.submain
        link_data = urllib2.Request(self.url_link, data=self.link_post)
        link_res = urllib2.urlopen(link_data).read()
        html_data = html.fromstring(link_res)
        sub_domains = html_data.xpath("//div[@class='domain']/a/text()")
        sub_domains = [i.replace('http://', '') for i in sub_domains]
        return self.sublist.extend(sub_domains)

    @staticmethod
    def check_valid(domain):
        import socket
        try:
            ip = socket.gethostbyname(domain)
            if dic.has_key(ip):
                if dic['ip']<5:
                    lock.acquire()
                    dic['ip']+=1
                    lock.release()
                    return domain
                else:
                    print '使用ip策略过滤掉一个域名%s'%domain
                    return None
            else:
                lock.acquire()
                dic['ip'] = 1
                lock.release()
                return domain
        except Exception as e:
            print e
            print(domain,'can not open!')
            pass

    def run(self):
        self.get_360()
        try:
            self.get_links()
        except Exception as e:
            pass
        return list(set(self.sublist))


def run_method(domains,thread_num,need_check=False):
    pool = ThreadPool(processes=thread_num)
    things = pool.map(SubMain.get_360,domains)
    things = [j for i in things for j in i]
    pool.close()
    pool.join()
    if need_check:
        pool = ThreadPool(processes=thread_num)
        things = pool.map(SubMain.check_valid,things)
        #print things
        #things = [i[0] for i in things]
    return things


def write_file(domains,file_name): # write list to file
    try:
        with open(file_name,'w+') as f:
            for i in domains:
                if i:
                    f.write(i+'\n')
    except Exception:
        print('写入文件失败')
if __name__ == '__main__':
    parser = OptionParser()
    print(logo)
    parser.add_option('-u',dest='url',help='scan a single host')
    parser.add_option('-f',dest='file',help='scan multi host from file')
    parser.add_option('-t',dest='thread_num',type='int',default=10,
                      help='numbers of thread, valid when -f is used, default is 10')
    parser.add_option('-w',action='store_true',dest='write_file',help='write to {url/filename}_subDomains.txt')
    parser.add_option('-c',action='store_true',dest='need_check',help='check  before print')
    (options, args) = parser.parse_args()
    #print(options)
    if not options.url and not options.file:
        parser.print_help()
        sys.exit(0)
    if options.url:
        SubMain.get_360(options.url)
        result = run_method([options.url],1,options.need_check)
    if options.file:
        try:
            urls = []
            for i in open(options.file).readlines():
                urls.append(i.strip())
            print '一共加载%s个url'%len(urls)
            result = run_method(list(set(urls)),options.thread_num,options.need_check) # 先开十个线程
        except Exception as e:
            print('cannot open file, please check-->%s'%e)
            sys.exit(1)
    if options.write_file:
        filename = options.url if options.url else options.file
        write_file(result,filename+'_subDomains.txt')
    else:
        for i in result:
            if i:
                print(i)


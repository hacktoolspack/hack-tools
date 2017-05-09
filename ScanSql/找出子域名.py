#!/usr/bin/env python
# -*- coding: utf_8 -*-
# Date: 2015/9/17
# Created by 独自等待
# 博客 http://www.waitalone.cn/
import sys, os
import urllib2

try:
    from lxml import html
except ImportError:
    raise SystemExit('\n[X] lxml模块导入错误,请执行pip install lxml安装!')


class SubMain():
    '''
    渗透测试域名收集
    '''

    def __init__(self, submain):
        self.submain = submain
        self.url_360 = 'http://webscan.360.cn/sub/index/?url=%s' % self.submain
        self.url_link = 'http://i.links.cn/subdomain/'
        self.link_post = 'domain=%s&b2=1&b3=1&b4=1' % self.submain
        self.sublist = []

    def get_360(self):
        scan_data = urllib2.urlopen(self.url_360).read()
        html_data = html.fromstring(scan_data)
        submains = html_data.xpath("//dd/strong/text()")
        return self.sublist.extend(submains)

    def get_links(self):
        link_data = urllib2.Request(self.url_link, data=self.link_post)
        link_res = urllib2.urlopen(link_data).read()
        html_data = html.fromstring(link_res)
        submains = html_data.xpath("//div[@class='domain']/a/text()")
        submains = [i.replace('http://', '') for i in submains]
        return self.sublist.extend(submains)

    def scan_domain(self):
        self.get_360()
        self.get_links()
        return list(set(self.sublist))


if __name__ == '__main__':
    print '+' + '-' * 50 + '+'
    print '\t    Python 二级域名信息收集工具'
    print '\t   Blog：http://www.waitalone.cn/'
    print '\t\t Code BY： 独自等待'
    print '\t\t Time：2015-09-17'
    print '+' + '-' * 50 + '+'
    if len(sys.argv) != 2:
        print '用法: ' + os.path.basename(sys.argv[0]) + ' 主域名地址'
        print '实例: ' + os.path.basename(sys.argv[0]) + ' waitalone.cn'
        sys.exit()
    domain = sys.argv[1]
    print u'报告爷,正在收集域名信息,请稍候!\n'
    submain = SubMain(domain).scan_domain()
    print u'报告爷,共发现域名信息 [ %d ] 条!\n' % len(submain)
    with open(domain + '.txt', 'wb+') as domain_file:
        for item in submain:
            domain_file.write(item + '\n')
            print item
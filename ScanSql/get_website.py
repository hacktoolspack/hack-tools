#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Fiht --<[url=mailto:fiht@qq.com]fiht@qq.com[/url]>
  Purpose: 用来获取攻击目标
  Created: 2016年04月20日
"""
import re
import threading
from optparse import OptionParser
try:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
except Exception: #出错的肯定是python3 2333
    pass
count = 0
#----------------------------------------------------------------------
def fuck_href(url):
    """"""
    i = re.findall('_(.*?)\.html',url)
    if i:
        return i[0]
#----------------------------------------------------------------------
def fuck_weight(text):
    """"""
    i = re.findall('themes/default/images/baidu/(.)\.gif',text)
    if i:
        return i[0]
#----------------------------------------------------------------------
def shit(shitDemo,num_want,weight=0,file=None):
    """return -1 if got a 404"""
    global count
    shit_list=[]
    #print('shitDemo-->',shitDemo)
    req = requests.get(shitDemo)
    soup = BeautifulSoup(req.text,'lxml')
    tag = soup.find(class_='listCentent')
    if tag :
        for i in tag.contents:
            fuck_we = fuck_weight(i.__str__())
            if fuck_we:
                if int(fuck_we) > weight:
                    count = count+1
                    shit_list.append(fuck_href(i.__str__()))
    return shit_list
#----------------------------------------------------------------------
def myTest():
    """"""
    for i in range(6):
        req = requests.get('http://top.chinaz.com/tag/211_%d.html'%i)
        soup = BeautifulSoup(req.text,'lxml')
        for i in soup.findAll(class_='col-gray'):
            if 'www' in i.string:
                print(i.string.strip('www.'))
def run_get(url,page,num_want,file=None,weight=0):
    """"""
    global count
    count = num_want
    if file:
        fil = open(file,'w+')
    else:
        fil=sys.stdout
    fil.write('模板url %s \n 权重大于%d的网站\n'%(url,weight))
    for i in range(2,page+1):
        try:
            lis = shit(url.replace('{page}',str(i)),num_want=num_want,file=fil,weight=weight)
            for a in lis:
                fil.write(a+'\n')
        except KeyboardInterrupt:
            print('接收到中断')
            fil.close()
            sys.exit(0)
#run_get('http://search.top.chinaz.com/Search.aspx?p={page}&url=%E4%B8%AD%E5%9B%BD',10,100)
if __name__=="__main__":
    parser = OptionParser(' %prog args')
    parser.add_option('-u','--url',dest='url',help='模板url,如=http://top.chinaz.com/diqu/index_ZhongQing_2.html -> http://top.chinaz.com/diqu/index_ZhongQing_{page}.html 其中{page}即为每次翻页的变量0->n')
    parser.add_option('-p','--page',dest='page',type='int',default=10,help='一共有多少页')
    parser.add_option('-n','--number',dest='num_want',default=9999999,type='int',help='想要获得多少个url')
    parser.add_option('-w','--weight',dest='weight',default=0,type='int',help='过滤权重,只列出权重>w的网站,默认为0')
    parser.add_option('-f','--file',dest='file',default=None,help='写入到文件而不是打印')    
    parser.add_option('-s','--search',dest='keyword',default=None,help='使用关键词获取网站')    
    (options,args) = parser.parse_args()
    if options.url:#利用url抓取
        if '{page}' in options.url:
            run_get(options.url,options.page,options.num_want,file=options.file,weight=options.weight)
        else:
            print('模板url中没有发现{page}字段,请检查')
 
    elif(options.keyword):#利用关键词抓取
        run_get('http://search.top.chinaz.com/Search.aspx?p={page}&url=%s'%options.keyword,options.page,num_want=options.num_want,file=options.file,weight=options.weight)
        sys.exit(0)
        print('-->>>--')
    else:
        parser.print_help()
 

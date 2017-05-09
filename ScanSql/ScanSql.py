# -*- coding: utf-8 -*-
import re
import sqlite3
import sys
dic = {}
http_dic = {}
count = 0
class http_url():
    #----------------------------------------------------------------------
    def init(self,url):
        """"""
        self.url = url
        self.hasScaned = 0
# 需要用到多线程的地方-->挨个请求网页的时候.用多线程能够显著提升效率        
class attack_url():
    def __init__(self,www_path,param):
        self.www_path = www_path.lower()
        self.param = param #参数
    def __hash__(self):
        return hash(self.www_path)
def get_things(url):
    first = 1
    global count
    count = count+1
    try:
        print(url)
        req = requests.get(url,timeout=3)
        print(req.text)
        pattern = re.compile('href="(.*?)"')
        for i in re.findall(pattern,req.text):
            has_http = i.find('http')!=-1
            has_flag = i.find('=')!=-1
            if has_flag and first: #有参数的链接
                first = 1
                if(has_http):
                    my_format(i)
                else:
                    my_format(url+i)
            if has_http:#有http->友情链接
                http_format(i)
            else:
                #print('没用的url',i) #不带参数，无http关键词的链接
                pass
    except Exception as e:
        #print(e)
        pass

def http_format(url):
    #print(url,'---->')
    """用来格式化http链接的util类"""
    www_path = url[0:url.rfind('/')]
    if www_path not in http_dic:
        http_dic[www_path] = url+'/'
    else:
        pass
     #   print('找到一个重复的url',url)

def my_format(url):
    #print('正在检测',url)
    url_seq = parse.urlparse(url)
    str = [tuple(sorted(i.split('=')[0] for i in url_seq[4].split('&')))] #排好序的参数
    Attack_url = attack_url(url_seq[1]+url_seq[2],str)
    if Attack_url in dic:
        for i in str:
            if i not in dic[Attack_url.www_path]:#应该取参数最多的那个
                if len(str) > len(dic[Attack_url.www_path].params):
                    dic[Attack_url.www_path].update = url+'/'
    else:
        dic[Attack_url.www_path] = url

get_things('http://www.sdu.edu.cn')
count_1 = 0
for i in http_dic.copy():
    count_1 = count_1+1
    if count_1 < count:
        continue
    get_things(http_dic[i])
print('需要扫描',len(http_dic)-count,'个IP')
for i in http_dic.copy():
    count_1 = count_1+1
    if not count_1%10:
        print(count_1)
    if count_1 < count:
        continue
    get_things(http_dic[i])
# for i in http_dic.copy():
    # get_things(http_dic[i])
for i in dic:
    if(dic[i].find('youku')==-1&dic[i].find('filename')==-1&dic[i].find('jsession')==-1):
        print(dic[i])
def write_database():
    conn = sqlite3.connect('hello.db')
    conn.execute('create table  if not exists test(url text primary key, Scaned int,Payload int)')
    for i in dic:
        if(dic[i].find('youku')==-1&dic[i].find('filename')==-1):
            try:
                conn.execute('insert into test values(?,?,?)',(dic[i],0,0,))
            except sqlite3.IntegrityError: # 已经存在 列
                continue
            #print(dic[i])
    conn.commit()
    


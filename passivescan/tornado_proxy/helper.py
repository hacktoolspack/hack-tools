# coding: utf8
import datetime
from pprint import pprint
from urlparse import urlparse

from config import CONST_WHITE_DOMAINS


class HttpInfo(object):
    def __init__(self, info, request_info, response_info):
        self.info = info
        self.request = request_info
        self.response = response_info
        self.result = None

    def get_info(self):
        # get url info
        urlparsed = urlparse(self.info.get('url'))
        domain = urlparsed.hostname
        url_info = dict(
            domain=domain,
            method=self.info.get('method'),
            url=self.info.get('url')
        )

        # get request info
        request_info = dict(
            request_url=self.request.uri,
            method=self.request.method,
            headers=self.request.headers,
            request_data=self.request.body
        )

        response_info = dict(
            request_url=self.response.effective_url,
            code=self.response.code,
            headers=self.response.headers,
            request_time=self.response.request_time,
            time_info=self.response.time_info
        )

        self.result = dict(
            domain=url_info.get('domain'),
            method=url_info.get('method'),
            url=url_info.get('url'),
            request=request_info,
            response=response_info,
            time=datetime.datetime.now(),
            status=0
        )
        pprint(self.result)
        return self.result


# Url filter class
class UrlFilter(object):
    def __init__(self, url):
        self.url = url
        self.url_info = urlparse(self.url)

    def is_static(self):
        static = ['js', 'css', 'jpg', 'gif', 'png', 'exe', 'zip', 'rar', 'ico',
                  'gz', '7z', 'tgz', 'bmp', 'pdf', 'avi', 'mp3', 'mp4', 'htm', 'html', 'shtml']

        path = self.url_info.path.strip()
        ext = path.split('.')[-1]
        # print "url_info : ,", url_info
        # print "path: %s, ext : %s" % (path, ext)
        if ext in static:
            return True
        return False

    def in_white(self):
        domain = self.url_info.netloc
        if 'com.cn' in domain:
            t = domain.split('.')
            d = ".".join(t[-3:])
        else:
            t = domain.split('.')
            d = '.'.join(t[-2:])

        if d in CONST_WHITE_DOMAINS:
            return True
        return False

    def filter(self):
        if self.is_static() or self.in_white():
            return False
        return True

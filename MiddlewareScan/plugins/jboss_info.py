#coding:utf-8
#author:wolf@future-sec
import urllib2
def check(host,port,timeout):
    url = "http://%s:%d"%(host,int(port))
    vul_url = url + '/status?full=true'
    try:
        res_html = urllib2.urlopen(vul_url,timeout=timeout).read()
    except:
        return 'NO'
    if "Max processing time" in res_html:
        info = vul_url + " Jboss Information Disclosure"
        return 'YES|'+info
    return 'NO'
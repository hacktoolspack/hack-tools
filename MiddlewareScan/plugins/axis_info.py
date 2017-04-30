#coding:utf-8
#author:wolf@future-sec
import urllib2
def check(host,port,timeout):
    url = "http://%s:%d"%(host,int(port))
    vul_url = url + "/axis2/axis2-web/HappyAxis.jsp"
    try:
        res_html = urllib2.urlopen(vul_url,timeout=timeout).read()
    except:
        return 'NO'
    if "Axis2 Happiness Page" in res_html:
        info = vul_url + " Axis Information Disclosure"
        return 'YES|'+info
    return 'NO'
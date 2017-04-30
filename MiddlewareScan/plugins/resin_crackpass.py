#coding=utf-8
#author:wolf@future-sec
import urllib2
def check(host,port,timeout):
    url = "http://%s:%d"%(host,int(port))
    error_i = 0
    flag_list=['<th>Resin home:</th>','The Resin version','Resin Summary']
    user_list=['admin']
    pass_list=['admin','123456','12345678','123456789','admin123','admin888','admin1','administrator','8888888','123123','admin','manager','root']
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    for user in user_list:
        for password in pass_list:
            try:
                PostStr='j_username=%s&j_password=%s'%(user,password)
                res = opener.open(url+'/resin-admin/j_security_check?j_uri=index.php',PostStr)
                res_html = res.read()
                res_code = res.code
            except urllib2.HTTPError,e:
                return 'NO'
            except urllib2.URLError,e:
                error_i+=1
                if error_i >= 3:
                    return 'NO'
                continue
            for flag in flag_list:
                if flag in res_html or int(res_code) == 408:
                    info = '%s/resin-admin Resin Weak password %s:%s'%(url,user,password)
                    return 'YES|'+info
    return 'NO'
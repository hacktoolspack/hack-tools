#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
This file is part of the cintruder project, http://cintruder.03c8.net

Copyright (c) 2012/2016 psy <epsylon@riseup.net>

cintruder is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation version 3 of the License.

cintruder is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along
with cintruder; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import socket, threading, re, base64, os, time
import webbrowser, subprocess, urllib, json, sys
from options import CIntruderOptions
from pprint import pprint
from shutil import copyfile

host = "0.0.0.0"
port = 9999

class ClientThread(threading.Thread):
    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.pages = Pages()

    def run(self):
        req = self.socket.recv(2048)
        res = self.pages.get(req)
        out = "HTTP/1.0 %s\r\n" % res["code"]
        out += "Pragma: no-cache\n"
        out += "Expires: Fri, 30 Oct 1998 00:00:01 GMT\n"
        out += "Cache-Control: no-cache, must-revalidate\n"
        out += "Content-Type: %s\r\n\r\n" % res["ctype"]
        out += "%s" % res["html"]
        self.socket.send(out)
        self.socket.close()
        if "run" in res and len(res["run"]):
            subprocess.Popen(res["run"], shell=True)

class Pages():
    def __init__(self):
        self.options = CIntruderOptions()
        self.pages = {}
        if not os.path.exists("outputs/words/"): 
            os.mkdir("outputs/words/")

        self.pages["/header"] = """
<!DOCTYPE html><html>
<head>
<meta name="author" content="psy">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="content-type" content="text/xml; charset=utf-8" /> 
<title>CINTRUDER: OCR Bruteforcing Toolkit</title>
<script type="text/javascript" src="/lib.js"></script>
<script src="js/web.js" type="text/javascript"></script>
<style>
a:link {
    color: cyan;
}
a:visited {
    color: black;
}
</style>
<style>
input.button {
    width: 20em;  height: 2em;
}
</style>
"""
        self.pages["/footer"] = """</body>
</html>
"""
        self.pages["/"] = self.pages["/header"] + """
<script>loadXMLDoc()</script></head><body bgcolor="blue" text="white" style="monospace;font-size:14px;" >
<center>
<table border="1" cellpadding="10" cellspacing="5" width="90%">
 <tr>
 <td bgcolor="white"><center><a href="http://cintruder.03c8.net" target="_blank"><img src="images/cintruder.png"></a></center></td>
 <td>
<center><h3><a href="https://github.com/epsylon/cintruder" target="_blank">CINTRUDER</a> is an automatic pentesting tool to bypass <a href="https://en.wikipedia.org/wiki/CAPTCHA" target="_blank">captchas</a><br/><br/>
Contact: psy (<a href="mailto:epsylon@riseup.net">epsylon@riseup.net</a>) - [<a href="https://03c8.net" target="_blank">03c8.net</a>]<br><br>
License: <a href="http://www.gnu.org/licenses/quick-guide-gplv3.pdf" target="_blank">GPLv3</a> | Donate: <a href="https://blockchain.info/address/19aXfJtoYJUoXEZtjNwsah2JKN9CK5Pcjw" target="_blank">BTC</a></h3></center>
</td>
 </tr></table><br/>
<table cellpadding="10" cellspacing="5" width="90%">
  <tr>
   <td width="315px">
<center>
<table border="1" cellpadding="10" cellspacing="5">
<tr>
 <td>
Track: <input type="radio" onclick="javascript:OptionsCheck();" name="options" id="track"/ CHECKED>
Train: <input type="radio" onclick="javascript:OptionsCheck();" name="options" id="train"/>
Crack: <input type="radio" onclick="javascript:OptionsCheck();" name="options" id="crack"/>
 </td>
</tr></table>
</center>
</td>
   <td><center>

<div id="ifTrack" style="display:none">
<table border="1" cellpadding="10" cellspacing="5">
<tr>
 <td><center><input type="text" name="track_url" id="track_url" size="43" placeholder="Download captchas from url (to: 'inputs/')"></center></td>
 <td><center>Num: <input type="text" name="track_num" id="track_num" size="2" value="5"></center></td>
 <td><center>TOR: <input type="checkbox" id="tor" name="tor"></center></td>
 <td align="right">Debug: <input type="checkbox" name="verbose" id="verbose"></td>
 <td><center><input type="submit" value="Download!" onclick="TrackCaptchas()"></center></td>
</tr></table>
</div>

<div id="ifTrain" style="display:none">
<table border="1" cellpadding="5" cellspacing="5">
<tr>
 <td><center>
LOCAL: <input type="radio" onclick="javascript:TrainSourcesCheck();" name="training_sources" id="training_local"/ CHECKED>
URL: <input type="radio" onclick="javascript:TrainSourcesCheck();" name="training_sources" id="training_url"/>
</center></td>
<td>
<div id="ifLocal" style="display:none">
<center>
<table cellpadding="5" cellspacing="5">
<tr>
 <td><center><form action='' method='POST' enctype='multipart/form-data'>
    <input type='text' size="43" name='SourceFile' id='SourceFile' placeholder="Ex: inputs/test1.gif"></form></center></td>
</tr></table>
</center>
</div>
<div id="ifUrl" style="display:none">
<table cellpadding="2" cellspacing="2">
<tr>
 <td><center><input type="text" name="train_url" id="train_url" size="43" placeholder="Apply common OCR techniques to a remote captcha"></center></td>
 <td><center>TOR: <input type="checkbox" name="tor2" id="tor2"></center></td>
</tr></table>
</div>
</td>
</tr>
<tr>
  <td align="right">Use Module: <input type="checkbox" onclick="javascript:SetTrainModule();" name="set_module" id="set_module"></td>
 <td>
<table>
 <tr>
  <td align="center">
<div id="ifMod_set" style="display:none">
<table cellpadding="5" cellspacing="5">
 <tr>
 <td>Name: <input type="text" name="use_mod" id="use_mod" size="12" placeholder="Ex: 'easy'"></td>
 <td><a href='javascript:runCommandX("cmd_list");javascript:showResults()'>List Modules</a></td>
</tr></table>
</div>
 </td>
</tr></table>
 </td>
</tr>
<tr>
<td align="right">Advanced OCR: <input type="checkbox" onclick="javascript:SetColourID();" name="set_colour_id" id="set_colour_id"></td>
 <td align="center">
<div id="ifMod_colour" style="display:none">
<table cellpadding="5" cellspacing="5">
<tr>
 <td>Set Colour ID: <input type="text" name="set_id" id="set_id" size="2" placeholder="Ex: 1"></td>
</tr></table>
</div>
</td>
</tr>
<tr>
 <td align="right">Debug: <input type="checkbox" name="verbose2" id="verbose2"></td>
 <td><center><input type="submit" class="button" value="Train!" onclick="TrainCaptchas()"></center></td>
</tr>
</table>
</div>

<div id="ifCrack" style="display:none">
<table border="1" cellpadding="5" cellspacing="5">
<tr>
 <td><center>
LOCAL: <input type="radio" onclick="javascript:CrackingCheck();" name="cracking_sources" id="cracking_local"/ CHECKED>
URL: <input type="radio" onclick="javascript:CrackingCheck();" name="cracking_sources" id="cracking_url"/>
</center></td>
<td>
<div id="ifCrackLocal" style="display:none">
<center>
<table cellpadding="5" cellspacing="5">
<tr>
 <td><center><form action='' method='POST' enctype='multipart/form-data'>
    <input type='text' size="43" name='SourceFile2' id='SourceFile2' placeholder="Ex: inputs/test1.gif"></form></center></td>
</tr>
</table>
</center>
</div>
<div id="ifCrackUrl" style="display:none">
<table cellpadding="5" cellspacing="5">
<tr>
 <td><center><input type="text" name="crack_url" id="crack_url" size="43" placeholder="Brute force using local dictionary (from: 'dictionary/')"></center></td>
 <td><center>TOR: <input type="checkbox" name="tor3" id="tor3"></center></td>
</tr>
</table>
</div>
</td>
</tr>
<tr>
  <td align="right">Use Module: <input type="checkbox" onclick="javascript:SetCrackModule();" name="set_module_crack" id="set_module_crack"></td>
 <td>

<table>
 <tr>
  <td align="center">
<div id="ifMod_set_crack" style="display:none">

<table cellpadding="5" cellspacing="5">
 <tr>
 <td>Name: <input type="text" name="use_mod_crack" id="use_mod_crack" size="12" placeholder="Ex: 'easy'"></td>
 <td><a href='javascript:runCommandX("cmd_list");javascript:showResults()'>List Modules</a></td>
</tr></table>
</div>
 </td>
</tr></table>
 </td>
</tr>
<tr>
<td align="right">Export to XML: <input type="checkbox" onclick="javascript:SetXML();" name="set_xml" id="set_xml"></td>
 <td align="center">
<div id="ifMod_xml" style="display:none">
<table cellpadding="5" cellspacing="5">
<tr>
 <td>Filename: <input type="text" name="set_xml_file" id="set_xml_file" size="16" placeholder="Ex: php-captcha.xml"></td>
</tr></table>
</div>
</td>
</tr>
<tr>
 <td align="right">Debug: <input type="checkbox" name="verbose3" id="verbose3"></td>
 <td><center><input type="submit" class="button" value="Crack it!" onclick="CrackCaptchas()"></center></td>
</tr>
</table>
</div>
</center></td>
 </tr>
</table>

<table cellpadding="5" cellspacing="5">
  <tr>
   <td>
      <div id="Results" style="display:none"><table width="100%" border="1" cellpadding="5" cellspacing="5"><th>Shell Info:<tr><td><div id="cmdOut"></div></td></tr></table></div>
   </td>
   </tr>
 <tr>
   <td align="center">
      <div id="Captcha-IN" style="display:none"><table border="1" width="100%" cellpadding="5" cellspacing="5"><th>Captcha Preview:<tr><td><center><img id="target_captcha_img_path" name="target_captcha_img_path" src=''></center></td></tr></table></div>
   </td>
 </tr>
  <tr>
   <td>
     <div id="OCR-out" style="display:none">
     <table width="100%" height="100%" border="1"><th>OCR Output:<tr>
    <td><iframe frameborder="0" id="directory-words" name="directory-words" width="800px" height="300px" src="directory-words"></iframe></td>
       </tr></table>
     </div>
  </td>
  </tr>
</table>
</center>
<br /><br/>
""" + self.pages["/footer"]

        self.pages["/directory-words"] ="""<!DOCTYPE html><html><head><meta http-equiv="Content-type" content="text/html;charset=UTF-8"><script type="text/javascript" src="/lib.js"></script>
<script language="javascript">
function Reload(word){
var w = word.substring(word.lastIndexOf('/')+1);
document.getElementById(w).style.display = "none";
document.getElementById("discarding").style.display = "none";
}
function Reload_Added(word){
var w = word.substring(word.lastIndexOf('/')+1);
document.getElementById(w).style.display = "none";
document.getElementById("adding").style.display = "none";
}
function MoveOCR(word) {
var w = word.substring(word.lastIndexOf('/')+1);
symbol = "letter_" + w
letter = document.getElementById(symbol).value;
if(letter == ""){
 window.alert("You need to enter a valid dictionary symbol (Ex: p)");
 return
}
if(word == ""){
 word = "off";
}else{
params="symbol="+escape(word)+"&letter="+escape(letter);
}
runCommandX("cmd_move_ocr",params);
setTimeout(function() { Reload_Added(word) }, 2000); // delay 2
}
function RemoveOCR(word) {
if(word == ""){
 word = "off";
}else{
params="symbol="+escape(word);
}
runCommandX("cmd_remove_ocr",params);
setTimeout(function() { Reload(word) }, 2000); // delay 2
}
</script>
<script language="javascript">function ViewWord(word) {window.open(word,"_blank","fulscreen=no, titlebar=yes, top=180, left=320, width=720, height=460, resizable=yes", false);}</script></head><body><table width='100%'><tr><td align='center'><font color='white'><div id="cmdOut"></div></font></td></tr><tr><td><br><center><a href='javascript:runCommandX("cmd_dict");'><font color="cyan"><u>View Dictionary Info</u></font></a></center></td></tr><tr><td>"""+str("".join(self.list_words()))+"""</td></tr></table></body></html>"""

        self.pages["/lib.js"] = """function loadXMLDoc() {
        var xmlhttp;
        if (window.XMLHttpRequest) {
                // code for IE7+, Firefox, Chrome, Opera, Safari
                xmlhttp = new XMLHttpRequest();
        } else {
                // code for IE6, IE5
                xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange = function() {
                if (xmlhttp.readyState == 4 ) {
                   if(xmlhttp.status == 200){
                           document.getElementById("cmdOut").innerHTML = xmlhttp.responseText;
                           setTimeout("loadXMLDoc()", 3000); 
                   }
                }
        }
        xmlhttp.send();
}

function runCommandX(cmd,params) {
        var xmlhttp;
        if (window.XMLHttpRequest) {
                // code for IE7+, Firefox, Chrome, Opera, Safari
                xmlhttp = new XMLHttpRequest();
        } else {
                // code for IE6, IE5
                xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange = function() {
                if (xmlhttp.readyState == 4 ) {
                   if(xmlhttp.status == 200){
								if(cmd.indexOf("?")!=-1){
									s=cmd.split("?")
									cmd=s[0]
									params=s[1]
								}
                                document.getElementById("cmdOut").innerHTML = xmlhttp.responseText;
                                //document.getElementById("cmdOut").scrollIntoView();
                                newcmd=cmd
                                if(newcmd=="cmd_remove_ocr" || newcmd=="cmd_move_ocr" || newcmd=="cmd_dict"){ //do not refresh
                                    return;
                                } else {
                                if(newcmd=="cmd_list" || newcmd=="cmd_track" || newcmd=="cmd_crack" || newcmd=="cmd_train") newcmd=newcmd+"_update"
								//do not refresh if certain text on response is found
								if(newcmd.match(/update/) && 
			 					(
                                                                  xmlhttp.responseText.match(/Number of tracked captchas/) ||
                                                                  xmlhttp.responseText.match(/to the correct folder/) ||
                                                                  xmlhttp.responseText.match(/by the moment/) ||
                                                                  xmlhttp.responseText.match(/Is that captcha supported?/) ||
                                                                  xmlhttp.responseText.match(/module not found/) ||
                                                                  xmlhttp.responseText.match(/No idea/) ||
                                                                  xmlhttp.responseText.match(/Possible Solution/) ||
                                                                  xmlhttp.responseText.match(/Internal problems/) ||
								  xmlhttp.responseText.match(/List end/)
										) 
											) return;
                                setTimeout(function(){runCommandX(newcmd,params)}, 3000);
								return;}
                   }
                }
        }
		if(typeof params != "undefined") cmd=cmd+"?"+params
        xmlhttp.open("GET", cmd, true);
        xmlhttp.send();
}
"""
    def list_words(self):
        m = []
        t = os.listdir("outputs/words")
        for f in t:
            ocr_preview = "<br><table style='display:block;' id='"+f+"' name='"+f+"' border='1' width='100%' cellpadding='5' cellspacing='5'><tr><td align='left' width='100%'><font color='cyan'><u><a onclick=javascript:ViewWord('images/previews/ocr/"+f+"');return false;>"+f+"</a></u></td><td align='center'><a onclick=javascript:ViewWord('images/previews/ocr/"+f+"');return false;><img border='1' style='border-color:red;' src='images/previews/ocr/"+f+"'></a></font></td><td align='center'><input type='text' name='letter_"+f+"' id='letter_"+f+"' size='2'></td><td align='center'><input type='submit' class='button' value='ADD!' onclick=javascript:MoveOCR('images/previews/ocr/"+f+"');return false;></td><td align='center'><input type='submit' class='button' value='Discard...' onclick=javascript:RemoveOCR('images/previews/ocr/"+f+"');return false;></td></tr></table>"
            m.append(ocr_preview)
        return m

    def convert_size(self, size):
        import math
        if (size == 0):
            return '0B'
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size,1024)))
        p = math.pow(1024,i)
        s = round(size/p,2)
        return '%s %s' % (s,size_name[i])

    def buildGetParams(self, request):
        params = {}
        path = re.findall("^GET ([^\s]+)", request)
        if path:
            path = path[0]
            start = path.find("?")
            if start != -1:
                for param in path[start+1:].split("&"):
                    f = param.split("=")
                    if len(f) == 2:
                        var = f[0]
                        value = f[1]
                        value = value.replace("+", " ")
                        value = urllib.unquote(value)
                        params[var] = value
        return params

    def get(self, request):
        cmd_options = ""
        runcmd = ""
        res = re.findall("^GET ([^\s]+)", request)
        if res is None:
            return
        pGet = {}
        page = res[0]
        paramStart = page.find("?")
        if paramStart != -1:
            page = page[:paramStart]
            pGet = self.buildGetParams(request)
        if page.startswith("/images/") or page.startswith("/js/") or page.startswith("/inputs/"):
            if os.path.exists("core/"+page[1:]):
                f=open("core/"+page[1:])
                self.pages[page]=f.read()
        if page == "/cmd_dict": # view dictionary info
            path, dirs, files = os.walk("dictionary/").next()
            total_dirs = len(dirs)
            total_files = len(files)
            size = 0
            for d in dirs:
                path, dirs, files = os.walk("dictionary/"+d).next()
                total_files = total_files + len(files)
                for f in files:
                    size += os.path.getsize("dictionary/"+d+"/"+f)
            size = self.convert_size(size)
            last_update = time.ctime(os.path.getctime("dictionary/"))
            self.pages["/cmd_dict"] = "<table align='center' border='1' cellspacing='5' cellpadding='5'><tr><td><u>Creation Date:</u></td><td><u>Size:</u></td><td><u>Total Words:</u></td><td><u>Total Symbols:</u></td></tr><tr><td align='center'>"+str(last_update)+"</td><td align='center'>"+str(size)+"</td><td align='center'>"+str(total_dirs)+"</td><td align='center'>"+str(total_files)+"</td></tr></table>"
        if page == "/cmd_remove_ocr": # remove ocr image from previews
            if not pGet["symbol"]=="off":
                self.pages["/cmd_remove_ocr"] = "<div style='display:block' id='discarding' name='discarding'><pre>[Info] Discarding image from previews...</pre></div>"
                symbol = pGet["symbol"]
                try:
                    os.remove("core/" + symbol)
                except:
                    pass
        if page == "/cmd_move_ocr": # move ocr image from previews to dictionary
            if not pGet["symbol"]=="off":
                self.pages["/cmd_move_ocr"] = "<div style='display:block' id='adding' name='adding'><pre>[Info] Adding image from previews to dictionary...</pre></div>"
                symbol = pGet["symbol"]
                letter = pGet["letter"]
                o = "core/" + symbol
                d = "dictionary/" + letter
                try:
                    if not os.path.exists(d):
                        os.makedirs(d)
                    head, tail = os.path.split(symbol)
                    final = d + "/" + tail
                    copyfile(o, final) # copy file to letter on dictionary
                    os.remove(o) # purge from previews
                except:
                    pass
        if page == "/cmd_list": # list mods
            self.pages["/cmd_list"] = "<pre>Waiting for a list of available modules...</pre>"
            runcmd = "(python -i cintruder --list "+ "|tee /tmp/out) &"
        if page == "/cmd_list_update":
            if not os.path.exists('/tmp/out'):
                open('/tmp/out', 'w').close()
            with open('/tmp/out', 'r') as f:
                self.pages["/cmd_list_update"] = "<pre>"+f.read()+"<pre>"
        if page == "/cmd_track": # tracking
            self.pages["/cmd_track"] = "<pre>Waiting for tracking results...</pre>"
            if pGet["tor"]=="on": 
                cmd_options = cmd_options + "--proxy 'http://localhost:8118' "
            if pGet["verbose"]=="on": 
                cmd_options = cmd_options + "--verbose "
            runcmd = "(python -i cintruder --track '"+pGet["tracking_source"]+"' --track-num '"+pGet["tracking_num"]+"' " + cmd_options + "|tee /tmp/out) &"
        if page == "/cmd_track_update":
            if not os.path.exists('/tmp/out'):
                open('/tmp/out', 'w').close()
            with open('/tmp/out', 'r') as f:
                self.pages["/cmd_track_update"] = "<pre>"+f.read()+"<pre>"
        if page == "/cmd_train": # training
            self.pages["/cmd_train"] = "<pre>Waiting for training results...</pre>"
            if pGet["tor"]=="on": 
                cmd_options = cmd_options + "--proxy 'http://localhost:8118' "
            if pGet["verbose"]=="on": 
                cmd_options = cmd_options + "--verbose "
            if not pGet["colourID"]=="off":
                cmd_options = cmd_options + "--set-id='" + pGet["colourID"] + "' "
            if not pGet["module"]=="off": 
                cmd_options = cmd_options + "--mod='" + pGet["module"] + "' "
            if pGet["source_file"]=="off": # from remote url source
                runcmd = "(python -i cintruder --train '"+pGet["train_url"]+"' " + cmd_options + "|tee /tmp/out) &"
            else: # from local source 
                source_file = pGet["source_file"]
                runcmd = "(python -i cintruder --train '"+source_file+"' " + cmd_options + "|tee /tmp/out) &"
        if page == "/cmd_train_update":
            if not os.path.exists('/tmp/out'):
                open('/tmp/out', 'w').close()
            with open('/tmp/out', 'r') as f:
                self.pages["/cmd_train_update"] = "<pre>"+f.read()+"<pre>"
        if page == "/cmd_crack": # cracking
            self.pages["/cmd_crack"] = "<pre>Waiting for cracking (bruteforcing) results...</pre>"
            if pGet["tor"]=="on":
                cmd_options = cmd_options + "--proxy 'http://localhost:8118' "
            if pGet["verbose"]=="on":
                cmd_options = cmd_options + "--verbose "
            if not pGet["module"]=="off":
                cmd_options = cmd_options + "--mod='" + pGet["module"] + "' "
            if not pGet["xml"]=="off":
                cmd_options = cmd_options + "--xml='" + pGet["xml"] + "' "
            if pGet["source_file"]=="off": # from remote url source
                runcmd = "(python -i cintruder --crack '"+pGet["crack_url"]+"' " + cmd_options + "|tee /tmp/out) &"
            else: # from local source 
                source_file = pGet["source_file"]
                runcmd = "(python -i cintruder --crack '"+source_file+"' " + cmd_options + "|tee /tmp/out) &"
        if page == "/cmd_crack_update":
            if not os.path.exists('/tmp/out'):
                open('/tmp/out', 'w').close()
            with open('/tmp/out', 'r') as f:
                self.pages["/cmd_crack_update"] = "<pre>"+f.read()+"<pre>"
        ctype = "text/html"
        if page.find(".js") != -1:
            ctype = "text/javascript"
        elif page.find(".txt") != -1:
            ctype = "text/plain"
        elif page.find(".ico") != -1:
            ctype = "image/x-icon"
        elif page.find(".png") != -1:
            ctype = "image/png"
        elif page.find(".jpeg") != -1:
            ctype = "image/jpeg"
        elif page.find(".jpg") != -1:
            ctype = "image/jpeg"
        elif page.find(".gif") != -1:
            ctype = "image/gif"
        if page in self.pages:
            return dict(run=runcmd, code="200 OK", html=self.pages[page], ctype=ctype)
        return dict(run=runcmd, code="404 Error", html="404 Error<br><br>Page not found...", ctype=ctype)

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True)
        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:9999', new=1)
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((host, port))
    while True:
        tcpsock.listen(4)
        (clientsock, (ip, c_port)) = tcpsock.accept()
        newthread = ClientThread(ip, c_port, clientsock)
        newthread.start()

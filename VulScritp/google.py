#coding=utf-8
__author__ = 'DM_'
import simplejson,random
import requests as req

page = 1
status = 200
dock = str(raw_input('请输入google关键字:')) #这里是google关键词.
while status == 200:
	headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'gb18030,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
        'Referer': 'http://www.baidu.com/'
        }

	url = "https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&rsz=8&start=%s"%(dock,page)
	try:
		HtmlContent = req.get(url, timeout=30, headers=headers).text
		result = simplejson.loads(HtmlContent)
		status = result['responseStatus']

		print "第%d页的数据:" % page
		try:
			Urls = result['responseData']['results']
			for url in Urls:
				print url['url']
		except:
			print '当前页面获取失败.'
			print result['responseDetails']
		page += 1
	except:
		print "Time Out or site is not open."
print "一共有%d页的数据" % (page-2)

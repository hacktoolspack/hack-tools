my_file = open('/home/fang/.sqlmap/output/results-05192016_1144pm.csv')
import re
def get_title(ip):
    import requests
    """给定网址返回title值"""
    try:
        req = requests.get('%s'%ip,timeout=3)
        if req.status_code !=200:
            pass
        req.encoding = req.apparent_encoding
        pattern = re.compile('<title>(.*?)</title>')
        i = re.findall(pattern,req.text)
        if i:
            return i[0]
    except Exception as e:
        print(e)
        pass
for i in my_file.readlines():
    print(i.split(',')[0],)#'页面标题:',get_title(i.split(',')[0]),'注入参数:',i.split(',')[2])
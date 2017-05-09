import requests
from bs4 import BeautifulSoup
#----------------------------------------------------------------------
def format_page(page_num):
    """"""
    req = requests.get('http://www.wooyun.org/corps/page/%d'%page_num,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'})
    soup = BeautifulSoup(req.text,'lxml')
    for i in soup.findAll(attrs={'rel':'nofollow'}):
        print(i['href'])
for i in range(1,45):
    format_page(i)
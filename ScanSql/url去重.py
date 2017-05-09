import urllib.parse
url_set = set()
for i in open('/tmp/out.json_1').readlines():
    try:
        netloc = i.split('/')[2]
        if netloc not in url_set and '360' not in netloc:
            url_set.add(netloc)
            if '.do' in i or '.action' in i:
                print(i[9:-3])
    except Exception as e:
        #print(e)
        pass
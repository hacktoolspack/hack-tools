import json
for i in open('/tmp/mmmmm'):
    try:
        print(json.loads(i.strip('\n'))['url'])
    except Exception as e:
        print(e)
        pass
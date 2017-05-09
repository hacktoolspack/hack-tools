import os
files = os.listdir('/home/fang/LifeNeedLove/自己用的脚本/一些二级域名/')
for file in files:
    if 'txt' in file:
        with open('/home/fang/LifeNeedLove/自己用的脚本/一些二级域名/%s'%file) as e:
            for i in e.readlines():
                try:
                    print(i.split(' ')[0])
                except Exception as e:
                    print(e)
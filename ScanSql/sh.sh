#!/bin/bash
count=0 
echo "请将本文件放在sqlmap目录下 并将要扫描的文件命名为all_webSite\n注意大小写哦么么哒"
echo "如果你不知道该折腾哪些网站你可以考虑使用getWebSite脚本 利用管道重定向到all_webSite中"
echo "enjoy!"
for i in $(cat all_webSite)
do
        for ii in $(python3 ./ScanSql.py 'http://'$i:)
do
        count=$((count+1))
        echo 'scaning---->'$ii
        python ./sqlmap.py -u $ii --batch --timeout=3 #$(date --iso-8601)
done
done

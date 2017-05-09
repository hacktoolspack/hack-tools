#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fiht --<fiht@qq.com>
  Purpose: 将待检测的url导入到Mongo里面
  Created: 2016年06月22日
"""

#----------------------------------------------------------------------
def main(file_name):
    """"""
    import pymongo
    db = pymongo.MongoClient('nofiht.ml')['from_tecent']['url']
    for i in open('/tmp/ss').readlines():
        db.insert({'url':i.strip()})
    db.ensure_index('url',unique=True)
if __name__=='__main__':
    main('/tmp/ss')
    

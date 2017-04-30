# coding: utf8
import pymongo


class Mongodb(object):
    def __init__(self, db_info):
        self.db_info = db_info
        self.client = pymongo.MongoClient(db_info.get('host'), db_info.get('port'))
        self.client.security_detect.authenticate(
            db_info.get('username'),
            db_info.get('password'),
            source='passive_scan'
        )
        self.db = self.client["passive_scan"]
        self.collection = self.db["url_info"]

    def insert(self, values):
        ret = self.collection.insert(values)
        # print ret
        return ret


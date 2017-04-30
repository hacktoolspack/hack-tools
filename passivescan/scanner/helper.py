# coding: utf8
__author__ = 'Hartnett'
import json

import pymongo
from bson.objectid import ObjectId

# convert dict inputs to string
def param2str(inputs):
    params = ""
    for key in inputs:
        t = "%s=%s" % (key, inputs[key])
        params = "%s&%s" % (params, t)

    return params[1:]


# get scan report value
class Reporter(object):
    def __init__(self, report):
        self.report = report
        self.result = []

    def get_value(self):
        self.report = json.loads(self.report)
        report = self.report.get('issues')
        self.result.extend(report)
        for item in self.result:
            inputs = item.get('vector').get('inputs')
            inputs1 = param2str(inputs)
            item['vector']['inputs'] = inputs1

        return self.result


class PassiveReport(object):
    def __init__(self, db_info, reports):
        self.db_info = db_info
        self.reports = reports
        self.client = pymongo.MongoClient(db_info.get('host'), db_info.get('port'))
        self.client.security_detect.authenticate(
            db_info.get('username'),
            db_info.get('password'),
            source='passive_scan'
        )
        self.db = self.client["passive_scan"]
        self.collection = self.db["reports"]

    def report(self):
        self.collection.insert(self.reports)

class TaskStatus(object):
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


    # set task checking now
    def set_checking(self, task_id):
        self.collection.update({'_id': ObjectId(task_id)}, {"$set" : {'status' : 1}})

    # set task checked
    def set_checked(self, task_id):
        self.collection.update({'_id': ObjectId(task_id)}, {"$set" : {'status' : 2}})
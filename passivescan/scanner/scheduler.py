# -*- coding: utf-8 -*-
__author__ = 'Hartnett'

import time
from pprint import pprint
import pymongo
from bson.objectid import ObjectId

from config import db_info
from scan_tasks import scan


class Scheduler(object):
    def __init__(self, interval=5):
        self.interval = interval
        self.db_info = db_info

        # connect to database
        self.client = pymongo.MongoClient(self.db_info.get('host'), self.db_info.get('port'))
        self.client.security_detect.authenticate(
            self.db_info.get('username'),
            self.db_info.get('password'),
            source='passive_scan'
        )

        self.db = self.client["passive_scan"]
        self.collection = self.db['url_info']

    def _get_task(self):
        task_id = None
        task_info = None
        tasks = self.collection.find({'status' : 0}).sort("_id", pymongo.ASCENDING).limit(1)
        for task in tasks:

            url = task.get('url')
            task_id = task.get('_id')
            domain = task.get('domain')
            method = task.get('request').get('method')
            request_data = task.get('request').get('request_data')
            user_agent = task.get('request').get('headers').get('User-Agent')
            cookies = task.get('request').get('headers').get('Cookie')
            task_info = dict(
                task_id=task_id,
                url=url,
                domain=domain,
                method=method,
                request_data=request_data,
                user_agent=user_agent,
                cookies=cookies
            )

        print("task_id : %s, \ntask_info:") % task_id
        pprint(task_info)
        return task_id, task_info

    # set task checking now
    def _set_checking(self, task_id):
        self.collection.update({'_id': ObjectId(task_id)}, {"$set" : {'status' : 1}})

    # set task checked
    def _set_checked(self, task_id):
        self.collection.update({'_id': ObjectId(task_id)}, {"$set" : {'status' : 2}})

    # distribution task
    def distribution_task(self):
        task_id, task_info = self._get_task()
        print "get scan task done, sleep %s second." % self.interval
        if task_id is not None:
            self._set_checking(ObjectId(task_id))
            url = task_info.get('url')
            domain = task_info.get('domain')
            method=task_info.get('method')
            request_data=task_info.get('request_data')
            user_agent = task_info.get('user_agent')
            cookies = task_info.get('cookies')
            scan.apply_async((task_id,url,domain,method,request_data,user_agent,cookies,))

            self._set_checked(ObjectId(task_id))

    def run(self):
        while True:
            self.distribution_task()
            time.sleep(self.interval)

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
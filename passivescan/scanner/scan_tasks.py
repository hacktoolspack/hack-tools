# -*- coding:utf8 -*-
__author__ = 'hartnett'
from celery import Celery
from arachni import arachni_console

from config import BACKEND_URL, BROKER_URL, db_info
from helper import Reporter, PassiveReport, TaskStatus

app = Celery('task', backend=BACKEND_URL, broker=BROKER_URL)

# scanning url task
# --------------------------------------------------------------------
@app.task
def scan(task_id, task_url,domain,method,request_data,user_agent,cookies):
    if task_url:
        print "start to scan %s, task_id: %s" % (task_url, task_id)
        scanner = arachni_console.Arachni_Console(task_url, method,user_agent, cookies,request_data,page_limit=1)
        report = scanner.get_report()
        if report:
            reporter = Reporter(report)
            value = reporter.get_value()
            if value:
                # 如果存在漏洞则记录到数据库中
                scan_report = PassiveReport(db_info, value)
                scan_report.report()

        task_status = TaskStatus(db_info)
        # 将状态设为已扫描
        task_status.set_checked(task_id)
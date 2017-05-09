#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
	sqlmapapi restful interface
	by zhangh (zhanghang.org#gmail.com)
'''
# api
task_new = "task/new"
task_del = "task/<taskid>/delete"
admin_task_list = "admin/<taskid>/list"
admin_task_flush = "admin/<taskid>/flush"
option_task_list = "option/<taskid>/list"
option_task_get = "option/<taskid>/get"
option_task_set = "option/<taskid>/set"
scan_task_start = "scan/<taskid>/start"
scan_task_stop = "scan/<taskid>/stop"
scan_task_kill = "scan/<taskid>/kill"
scan_task_status = "scan/<taskid>/status"
scan_task_data = "scan/<taskid>/data"
scan_task_log = "scan/<taskid>/log/<start>/<end>"
scan_task_log = "scan/<taskid>/log"
download_task = "download/<taskid>/<target>/<filename:path>"
# config
taskid = "<taskid>"
dbOld = 0
dbNew = 1
host = '172.22.1.44'
port = 2000
password = 'SEC'

joblist = 'job.set'
sqlinj = 'sqlinj'
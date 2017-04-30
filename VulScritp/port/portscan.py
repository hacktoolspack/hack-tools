#!/usr/bin/python
# encoding=utf-8
# Filename: test.py
# author = 0c0c0f
import threading,sys,socket,re
import time,Queue
import optparse

#定义扫描端口
PortList = [21,22,23,25,53,80,443,445,873,1433,1521,1723,3306,3389,4848,4899,5800,5900,7001,8080,8443,8500,9080,9200,27017]
#存放IP数组
result =[]
#定义连接超时时间
Timeout = 2
# 创建锁
mutex = threading.Lock()
#定义线程池
threads = []
#创建队列
queue = Queue.Queue()

def scan():
	global mutex,queue,Timeout
	#time.sleep(2)
	#print threading.currentThread().getName()
	while True:
		try:
			item = queue.get(timeout=0.1)
			sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sk.settimeout(Timeout)
			try:
				sk.connect((item['ip'],int(item['port'])))
				mutex.acquire()
				print('Server %s port %d OK!' % (item['ip'],item['port']))
				mutex.release()
				sk.close()
			except:
				pass
		except:
			break
	'''	
	sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sk.settimeout(Timeout)
	try:
		mutex.acquire()
		sk.connect((i,p))
		print('Server %s port %d OK!' % (i,p))
		mutex.release()
	except Exception:
		pass
	sk.close()
	'''

def main(txt,num):
	#把数组压入队列
	for j in PortList:
		queue.put({'ip': txt,'port':int(j)})
	# 先创建线程对象
	for x in xrange(0, num):
		th = threading.Thread(target=scan)
		th.start()
		threads.append(th)
	for t in threads:
		t.join()
		
if __name__ == '__main__':
	parser = optparse.OptionParser('usage: %prog [options] target')
	parser.add_option('-t','--threads', dest='threads_num',default=20, type='int',help='Number of threads. default = 20')
	(options, args) = parser.parse_args()
	m = re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', args[0])
	if len(args) < 1 and  m:
		parser.print_help()
		sys.exit(0)

	txt = str(args[0])
	time1= time.time()
	main(txt,int(options.threads_num))
	time2= time.time()
	print time2-time1

#!/usr/bin/python
# encoding=utf-8

import optparse,re,sys,os

def getip(_txt):
	result = []
	f = open(_txt,"r")
	line = f.read()
	result = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
	result = {}.fromkeys(result).keys()
	return result

def ping(hosts):
	ipss = []
	for i in hosts:
		ret = os.system("ping -c 1 -t 1 %s > nop" % i)
		#ret = os.system("ping -n 1 -w 1 %s > nop" % i)
		if not ret:
			ipss.append(i)
	return ipss


if __name__ == '__main__':
	txt = []
	parser = optparse.OptionParser('usage: %prog [options] target')
	parser.add_option('-t','--threads', dest='threads_num',default=20, type='int',help='Number of threads. default = 20')
	parser.add_option('-f', '--file', dest='names_file',default='false', type='string',help='files default = false')
	(options, args) = parser.parse_args()

	if str(options.names_file) == "false":
		if len(args) < 1 :
			parser.print_help()
			sys.exit(0)
	txt = ping(getip(str(options.names_file)))
	print txt

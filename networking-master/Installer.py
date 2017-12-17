"""
import requests as r
exec(r.get("goo.gl/xNtQB2?"))
"""

import os
import time
import requests as r

def load(msg):
	print msg,"......"
	time.sleep(0.05)

load("Making Main Directory")
try:
	os.mkdir("./RussianOtter")
except:
	pass
os.chdir("./RussianOtter")

import urllib, zipfile, sys, functools, re, os, tempfile

def extract_git_id(git):
	m = re.match((r'^http(s?)://([\w-]*\.)?github\.com/(?P<user>[\w-]+)/(?P<repo>[\w-]*)'
	'((/tree|/blob)/(?P<branch>[\w-]*))?'), git)
	return m

def dlProgress(filename, count, blockSize, totalSize):
	if count*blockSize > totalSize:
		percent=100
	else:
		percent = max(min(int(count*blockSize*100/totalSize),100),0)
		sys.stdout.write("\r" + filename + "...%d%%" % percent+" "*10)
		sys.stdout.flush()

def git_download(url):
	base='https://codeload.github.com'
	archive='zip'
	m=extract_git_id(url)
	if m:
		g=m.groupdict()
		if not g['branch']:
			g['branch']='master'
			u=   '/'.join((base,g['user'],g['repo'],archive, g['branch']))
			try:
				with tempfile.NamedTemporaryFile(mode='w+b',suffix='.zip') as f:
					urllib.urlretrieve(u,f.name,reporthook=functools.partial(dlProgress,u))
					z=zipfile.ZipFile(f)
					z.extractall()
			except:
				print('git url did not return zip file')
	else:
		print('could not determine repo url from clipboard or argv')

print "Programs are Installing"
import threading
programs = [
	"APDOS","networking","romap","RoBrutev6","Mobilesploit","iBlock","mitm"
	]
curt = int(threading.active_count())
for _ in programs:
	murl = "http://github.com/RussianOtter/"+_
	t = threading.Thread(target=git_download,args=(murl,))
	t.daemon = True
	t.start()
	time.sleep(2)

while 1:
	print "Finishing Up!"
	if (int(threading.active_count())-curt) < 1:
		break
	else:
		print (int(threading.active_count())-curt), "Programs Left!"
		time.sleep(1)
print "Installation Complete!"
print "Enjoy The Following Programs (Under LLC and MIT):"
for _ in programs:
	print "-",_

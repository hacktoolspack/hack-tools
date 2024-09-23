#!/usr/bin/python
import os,sys
if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	c1='mv darkjumperlog.txt darkjumperlog.tmp'
        c2='rm -f *.txt'
#        c3='rm -f *.log'
        c4='mv darkjumperlog.tmp darkjumperlog.txt'
	c5='rm -f *.*~'

else:
	c1='rename darkjumperlog.txt darkjumperlog.tmp'
        c2='del *.txt'
#        c3='del *.log'
        c4='rename darkjumperlog.tmp darkjumperlog.txt'
        c5='del *.*~'
os.system(c1)
os.system(c2)
#os.system(c3)
os.system(c4)
os.system(c5)


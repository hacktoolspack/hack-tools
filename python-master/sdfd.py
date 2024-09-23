#!/usr/bin/python
#Usage: sdfd.py "/folder/to/scan/for/duplicates"
#Options: -d (delete duplicate files)
# by ..:: crazyjunkie ::.. 2015
#
import sys
import os
bytes = filenames = []
x = d = delete = fd = 0
darg = 'null'
try:
    darg = str(sys.argv[2])
except IndexError:
    darg = 'null'
if darg == "-d":
    print ("OPTIONS: -d (deletion) is enabled")
    delete = 1
    print ("")
for file in os.listdir(str(sys.argv[1])):
    filesize = (os.path.getsize(("%s/%s" % (str(sys.argv[1]), file))))
    if filesize in bytes:
        print ("%s - Duplicate > Matching: %s" % (file, filenames[bytes.index(filesize)]))
        d += 1
        if delete == 1:
            os.remove(("%s/%s" % (str(sys.argv[1]), file)))
            print ("ACTION: Removed %s" % (file))
    else:
            bytes.append(filesize)
            filenames.append(file)
    x += 1
print ("")
if delete == 1:
    print ("DONE: Scanned %s file(s) and deleted %s duplicate(s)" % (x, d))
else:
    print ("DONE: Scanned %s file(s) and found %s duplicate(s)" % (x, d))

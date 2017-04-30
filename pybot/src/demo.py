#!/usr/bin/env python

import Bot
import signal
import subprocess
import sys
import time

bot1 = subprocess.Popen("python Bot.py -p 21801 -r 0.1 -o 10", shell=True)
bot2 = subprocess.Popen("python Bot.py -p 21800 -r 0.1 -o -15", shell=True)
bot3 = subprocess.Popen("python Bot.py -p 20001 -r 0.1 -o 0", shell=True)
bot4 = subprocess.Popen("python Bot.py -p 64000 -r 0.1 -o 10000", shell=True)

def shutdown(signum, frame):
   print '\nStopping demo...\n'

   bot1.terminate()
   bot2.terminate()
   bot3.terminate()
   bot4.terminate()

   print 'Demo stopped\n'
   sys.exit(0)

if __name__ == '__main__':
   signal.signal(signal.SIGINT, shutdown)

   print '\nUse Ctrl+C to stop demo at anytime\n'

   # keep the main thread running, can be stopped with ctrl+c
   while True:
      time.sleep(60)

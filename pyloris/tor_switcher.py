#! /usr/bin/env python

"""
tor_switcher.py
A light interface for issuing NEWNYM signals over TOR's control port. Usefull
for making a PyLoris DoS attack look like a DDoS attack.
"""

import random, telnetlib, thread, time
from Tkinter import *

class Switcher(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = ".o0O| TOR Switcher |O0o.")

        self.host = StringVar()
        self.port = IntVar()
        self.passwd = StringVar()
        self.time = DoubleVar()

        self.host.set('localhost')
        self.port.set('9051')
        self.passwd.set('')
        self.time.set('30')

        Label(self, text = 'Host:').grid(row = 1, column = 1)
        Label(self, text = 'Port:').grid(row = 2, column = 1)
        Label(self, text = 'Password:').grid(row = 3, column = 1)
        Label(self, text = 'Interval:').grid(row = 4, column = 1)

        Entry(self, textvariable = self.host).grid(row = 1, column = 2, columnspan = 2)
        Entry(self, textvariable = self.port).grid(row = 2, column = 2, columnspan = 2)
        Entry(self, textvariable = self.passwd, show = '*').grid(row = 3, column = 2, columnspan = 2)
        Entry(self, textvariable = self.time).grid(row = 4, column = 2, columnspan = 2)

        Button(self, text = 'Start', command = self.start).grid(row = 5, column = 2)
        Button(self, text = 'Stop', command = self.stop).grid(row = 5, column = 3)

        self.output = Text(self, foreground="white", background="black", highlightcolor="white", highlightbackground="purple", wrap=WORD, height = 8, width = 40)
        self.output.grid(row = 1, column = 4, rowspan = 5)

    def start(self):
        self.write('TOR Switcher starting.')
        self.ident = random.random()
        thread.start_new_thread(self.newnym, ())

    def stop(self):
        try:
            self.write('TOR Switcher stopping.')
        except:
            pass
        self.ident = random.random()

    def write(self, message):
        t = time.localtime()
        try:
            self.output.insert(END, '[%02i:%02i:%02i] %s\n' % (t[3], t[4], t[3], message))
        except:
            print('[%02i:%02i:%02i] %s\n' % (t[3], t[4], t[3], message))
            
    def newnym(self):
        key = self.ident
        host = self.host.get()
        port = self.port.get()
        passwd = self.passwd.get()
        interval = self.time.get()

        try:
            tn = telnetlib.Telnet(host, port)
            if passwd == '':
                tn.write("AUTHENTICATE\r\n")
            else:
                tn.write("AUTHENTICATE \"%s\"\r\n" % (passwd))
            res = tn.read_until('250 OK', 5)

            if res.find('250 OK') > -1:
                self.write('AUTHENTICATE accepted.')
            else:
                self.write('Control responded "%s".')
                key = self.ident + 1
                self.write('Quitting.')
        except Exception, ex:
            self.write('There was an error: %s.' % (ex))
            key = self.ident + 1
            self.write('Quitting.')
        
        while key == self.ident:
            try:
                tn.write("signal NEWNYM\r\n")
                res = tn.read_until('250 OK', 5)
                if res.find('250 OK') > -1:
                    self.write('New identity established.')
                else:
                    self.write('Control responded "%s".')
                    key = self.ident + 1
                    self.write('Quitting.')
                time.sleep(interval)
            except Exception, ex:
                self.write('There was an error: %s.' % (ex))
                key = self.ident + 1
                self.write('Quitting.')

        try:
            tn.write("QUIT\r\n")
            tn.close()
        except:
            pass

if __name__ == '__main__':
    mw = Switcher()
    mw.mainloop()
    mw.stop()

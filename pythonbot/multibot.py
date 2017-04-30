# -*- coding: utf-8 -*-
# MIT Liscence
version = "9"

import os, sys, socket, signal, time, random
import threading
from time import sleep
from collections import defaultdict
from queue import Queue

def timeout_handler(signum, frame):                                             # handler for timeout exceptions
    raise Exception("Timeout Alarm: %s %s" % (signum, frame))


class ircConnection(threading.Thread):
    def __init__(self, server='irc.freenode.net', port=6667, channel='##medusa'):
        threading.Thread.__init__(self)

        self.server = server
        self.port = port
        self.channel = '##medusa'
        self.keep_listening = True
        self.timeout_count = 0
        self.reconnects = 0
        self.connection_time = None
        self.threshold = 8 * 60
        self.last_ping = None
        self.last_data = ''
        self.inq = defaultdict(Queue)

    def run(self):
        # infinite runloop that checks for recieved messages
        while self.keep_listening:
            self.join_channel()

            while self.keep_listening and self.timeout_count < 50:
                content, source, return_to = self.recv()

                print content, source, return_to

    def join_channel(self):
        self.timeout_count = 0
        self.last_ping = time.time()                                             # last ping recieved
        self.last_data = ''
        data = ''
        log("[+] Connecting...")
        log("[<]    Nick:        ", nick)
        log("[<]    Server:      ", server+':'+str(port))
        log("[<]    Room:        ", channel)

        try:
            self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.irc.settimeout(60)                                              # timeout for irc.recv
            self.irc.connect((self.server, self.port))
            self.reconnects += 1
            self.connection_time = time.time()
            welcome_msg = self.irc.recv(4096)
            log("[+] Recieved:    ", welcome_msg+'\n')
            self.irc.send('NICK %s\r\n' % nick )
            self.irc.send('USER %s %s %s :%s\r\n' % (nick, nick, nick, nick))
            self.irc.send('JOIN %s\r\n' % channel)
            try:
                privmsg('Bot reloaded due to internal exception: %s' % exit_exception)
                del exit_exception
            except NameError:
                pass
        except Exception as error:
            log('[*] Connection Failed: ')
            log('[X]    ',error)
            self.timeout_count = 50
            sleep(20)

    def recv(self):
        try:
            data = self.irc.recv(4096)
            log('[+] Recieved:')
            log('[>]    ', data.strip())
            if self.last_data == data:                                     # IRC servers  will occasionally send lots of blank messages instead of disconnecting
                self.timeout_count += 1
            else:
                self.timeout_count = 0
            self.last_data = data

        except socket.timeout:
            if time.time() - self.last_ping > self.threshold:                     # if reciving data times out and ping threshold is exceeded
                self.keep_listening = True
                self.timeout_count = 50
                return (None, None, None)
            else:
                data = str(time.time())
                self.timeout_count = 0

        except Exception as exit_exception:
            log('[X] irc.recv exception: ', exit_exception)
            if not self.still_connected(irc)[0]:
                privmsg("Reloading due to irc.recv error: %s" % exit_exception)
                reload_bot()

        # check connection when instability is detected or a blank message is recieved from the server
        if len(data) < 1 or timeout_count > 5:
            if self.still_connected(irc)[0]:
                timeout_count = 0
            else:
                quit_status = False
                timeout_count = 50
                break

        if 'ickname is already in use' in data:
            nick += str(random.randint(1,200))
            if len(nick) > 15: nick = '[%s]%s' % (main_user[:11], random.randint(1,99))
            timeout_count = 50
            quit_status = False
            break

        content, source, return_to = self.parse(data)

        if content != False:
            timeout_count = 0
            if content == 'PING' and (len(source) > 0):
                irc.send('PONG ' + source + '\r')
                last_ping = time.time()
                log('[+] Sent Data:')
                log('[<]    PONG ',source)
                timeout_count = 0
            else:
                return (content, source, return_to)
        else:
            return (None, None, None)

    def parse(self, data):
        if data.find("PRIVMSG") != -1:
            from_nick = data.split("PRIVMSG ",1)[0].split("!")[0][1:]               # who sent the PRIVMSG
            to_nick = data.split("PRIVMSG ",1)[1].split(" :",1)[0]                  # where did they send it
            text = data.split("PRIVMSG ",1)[1].split(" :",1)[1].strip()             # what did it contain
            if source_checking_enabled and (from_nick not in allowed_sources and from_nick != admin):
                log("[>]     Not from an allowed source. (source checking enabled)")
                return (False,"","")                     # break and return nothing if message is invalid
            if to_nick == channel:
                source = "public"
                return_to = channel
            elif to_nick != channel:
                source = "private"
                return_to = from_nick
            log("[>]     Content: %s, Source: %s, Return To: %s" % (text, source, return_to))
            return (text, source, return_to)
        elif data.find("PING :",0,6) != -1:                                         # was it just a ping?
            from_srv = data.split("PING :")[1].strip()                              # the source of the PING
            return ("PING", from_srv, from_srv)
        return (False,"","")

    def still_connected(self):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(3)
        try:
            log('[#] Testing Connection.')
            log('[>] Sent:')
            log('[>]    PING TEST')
            sent_time = time.time()
            self.irc.send('PING TEST\r\n')
            found = False
            while not found:
                data = self.irc.recv(4096)
                if data.find("PONG") != -1:
                    latency = str(round((time.time() - sent_time)*1000, 2))+"ms"
                    signal.alarm(0)
                    found = True
            log('[#] Latency: %s' % latency)
            return (True, latency)
        except Exception as pong_exception:
            signal.alarm(0)
            log("[X] PING/PONG Failed: %s" % pong_exception)
            return (False, "X: %s" % pong_exception)

    def privmsg(msg=None, to=admin):                                                # function to send a private message to a user, defaults to master of bots!
        if type(msg) is unicode:
            msg = unicodedata.normalize('NFKD', msg).encode('ascii','ignore')
        elif type(msg) is not str or unicode:
            msg = str(msg).strip()
        if len(msg) < 1:
            pass
        elif (len(msg) > 480) or (msg.find('\n') != -1):
            log('[+] Sent Data:')
            log('[#] Starting multiline output.')
            msgs = line_split(msg, 480)                                             # use line_split to split output into multiple lines based on max message length (480)
            total = len(msgs)
            for num, line in enumerate(msgs):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(1)                                                     # doubles as flood prevention wait and input checking
                try:
                    data = irc.recv(4096)
                except:
                    data = ""
                    pass
                signal.alarm(0)
                if data.find('!stop') != -1:
                    log('[+] Recieved:')
                    log('[>]    ', data.strip())
                    retcode = "Stopped buffered multiline output."
                    privmsg("[X]: %s" % retcode, to)
                    break
                log('[<]    PRIVMSG %s :[%s/%s] %s\r' % (to, num+1, total, line))
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(2)
                try:
                    irc.send ('PRIVMSG %s :[%s/%s] %s\r\n' % (to, num+1, total, line))  # [1/10] = Output line 1 out of 10 total
                except Exception as send_error:
                    log('[X] irc.send exception: ', send_error)
                    timeout_count = 50
                signal.alarm(0)

            log('[#] Finished multiline output.')
        else:
            log('[+] Sent Data:')
            log('[<]    PRIVMSG %s :%s\r' % (to, msg))
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(2)
            try:
                irc.send('PRIVMSG %s :%s\r\n' % (to, msg))
            except Exception as send_error:
                log('[X] irc.send exception: ', send_error)
                timeout_count = 50
            signal.alarm(0)

    def broadcast(msg):                                                             # function to send a message to the main channel
        self.privmsg(msg, channel)


if __name__ == '__main__':
    connection = ircConnection()
    connection.start()

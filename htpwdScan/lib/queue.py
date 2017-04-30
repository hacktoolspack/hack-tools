#!/usr/bin/env python
# encoding=utf-8
#
# Generate parameters queue asynchronously
#

import time
import Queue
import os
import re


def gen_queue_basic_auth(self):
    f_user = open(self.args.basic[0], 'r')
    f_pass = open(self.args.basic[1], 'r')

    for str_user in f_user.xreadlines():
        f_pass.seek(0)    # Very important
        for str_pass in f_pass.xreadlines():
            auth_key = '%s:%s' % (str_user.strip(), str_pass.strip())
            while self.queue.qsize() >= self.args.t * 2 and not self.STOP_ME:
                time.sleep(0.001)
            self.queue.put(auth_key)
            if self.args.debug or self.STOP_ME: break
        if self.args.debug or self.STOP_ME: break

    f_user.close()
    f_pass.close()

    for i in range(self.args.t):
        self.queue.put(None)


def gen_queue_database(self):
    _, database_file = self.args.database.split('=')
    params = _.split(',')
    for param in params:
        self.selected_params[param] = ''
        self.selected_params_keys.append(param)

    len_params = len(params)

    obj_re = re.compile(self.args.regex)
    f_database = open(database_file, 'r')
    for str_line in f_database.xreadlines():
        if self.STOP_ME:
            break

        str_line = str_line.strip()
        m = obj_re.search(str_line)

        if not m or len(m.groups()) != len_params:
            continue
        while self.queue.qsize() >= self.args.t * 2 and not self.STOP_ME:
            time.sleep(0.001)
        self.queue.put('^^^'.join(m.groups()))

        if self.args.debug:
            break
    f_database.close()

def gen_python_code(self):
    str_code = str_code_prefix = str_code_postfix = ''
    indent = 0
    for param in self.args.d:
        pname, fname = param.split('=')

        if fname.startswith('md5(') and fname.endswith(')'):         # MD5 32-bit hashing
            self.args.md5.append(pname)
            fname = fname[4: -1]

        elif fname.startswith('md5_16(') and fname.endswith(')'):    # MD5 16-bit hashing
            self.args.md5_16.append(pname)
            fname = fname[7: -1]

        elif fname.startswith('sha1(') and fname.endswith(')'):       # SHA1 40-bit hashing
            self.args.sha1.append(pname)
            fname = fname[5: -1]

        self.selected_params[pname] =  fname    # e.g {'user': 'user.dic'}
        self.selected_params_keys.append(pname)
        if not os.path.exists(fname):
            raise Exception('File not found: %s' % fname)

        str_code += ' ' * 4 * indent
        indent += 1
        str_code_prefix += "file" + str(indent) + " = open(r'" + fname + "', 'r')\n"    # prefix
        str_code += "file" + str(indent) + ".seek(0)\n"
        str_code += ' ' * 4 * (indent - 1)
        str_code += "for line" + str(indent) + " in file" + str(indent) + ":\n"
        str_code_postfix += 'file' + str(indent) + '.close()\n'    # postfix

    str_code += ' ' * 4 * indent + 'while not self.STOP_ME:\n'
    indent += 1
    str_code += ' ' * 4 * indent + 'if self.queue.qsize() < self.args.t * 2:\n'
    indent += 1
    str_code += ' ' * 4 * indent
    index = 1
    str_line = ''
    for _ in self.args.d[:-1]:
        str_line += 'line' + str(index) + ".strip() + '^^^' + "    # values separated by '^^^'
        index += 1
    str_line += 'line' + str(index) + '.strip()'
    str_code += "self.queue.put(" + str_line + ")\n"
    str_code += ' ' * 4 * indent + 'break\n'
    str_code += ' ' * 4 * (indent - 1) + 'time.sleep(0.001)\n'
    if self.args.debug:
        for i in range(len(self.args.d)):
            str_code += ' ' * 4 * (indent - 2 - i) + 'break\n'
    str_code += 'for i in range(self.args.t):\n    self.queue.put(None)\n'
    str_code = str_code_prefix + str_code + str_code_postfix.strip()
    return str_code


def gen_queue(self):

    self.queue = Queue.Queue()
    self.args.md5 = self.args.md5_16 = self.args.sha1 = []
    self.selected_params = {}
    self.selected_params_keys = []

    if self.args.basic:
        gen_queue_basic_auth(self)
        return

    elif self.args.checkproxy:
        d = [1] if self.args.debug else self.proxy_list
        for _ in d:
            self.queue.put('')
        for _ in d:
            self.queue.put(None)
        return

    elif self.args.database:
        gen_queue_database(self)
        return

    else:
        str_code = gen_python_code(self)
        self.lock.acquire()
        if self.args.debug:
            print '[Python code generated]\n'
            print str_code
            print '\n' + '*' * self.console_width
        self.lock.release()
        exec(str_code)

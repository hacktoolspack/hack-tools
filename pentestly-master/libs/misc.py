from collections import defaultdict
from pprint import pprint

class Colors(object):
    none = '\033[m' # native
    red = '\033[31m' # red
    green = '\033[32m' # green
    orange = '\033[33m' # orange
    blue = '\033[34m' # blue

def message(msg, symbol, color):
    return '{color}[{symbol}]{endcolor} {msg}'.format(color=color,
                                                    symbol=symbol,
                                                    endcolor=Colors.none,
                                                    msg=msg)
def error(msg):
    print message(msg, '!', Colors.red)

def warn(msg):
    print message(msg, '*', Colors.orange)

def success(msg):
    print message(msg, '+', Colors.green)

def info(msg):
    print message(msg, '+', Colors.blue)

def parse_mimikatz(data):
    '''Parse mimikatz output into a dictionary'''
    curr_user = ''
    curr_category = ''

    results = {}

    data = data.split('\n')
    data = [line.strip() for line in data]
    for line in data:
        if 'user name' in line.lower():
            curr_user = line.split()[3]
            if curr_user not in results:
                results[curr_user] = defaultdict(dict)
        elif 'sid' in line.lower():
            results[curr_user]['sid'] = get_index_or_none(line.split(), 2)
        elif 'domain' in line.lower() and '*' not in line.lower():
            results[curr_user]['domain'] = get_index_or_none(line.split(), 2)
        for category in ['wdigest', 'tspkg', 'kerberos', 'ssp', 'credman']:
            if category in line.lower() and category not in results[curr_user]:
                curr_category = category
                results[curr_user][curr_category] = defaultdict(dict)
                break
        for cred_data in ['username', 'password', 'domain']:
            if cred_data in line.lower() and '*' in line.lower():
                cred = get_index_or_none(line.split(), 3) 
                results[curr_user][curr_category][cred_data] = cred


    creds = []

    # Mimikatz gives us a high level username and a username in wdigest
    for user in results:
        for category in results[user]:
            if category in ['wdigest', 'msv', 'tspkg', 'kerberos', 'ssp', 'credman']:
                if results[user][category].get('password', '(null)') == '(null)':
                    continue
                curr_creds = [user]
                for elem in ['username', 'password', 'domain']:
                    curr_creds.append(results[user][category].get(elem, None)) 
                creds.append(curr_creds)

    return creds

def get_index_or_none(line, index):
    return line[index] if len(line) > index else None

def tableify(data, headers=None):
    from itertools import izip_longest
    '''ASCII table for a list of strings'''
    if not isinstance(data, list):
        return ''

    table = []

    columns = izip_longest(*data, fillvalue='')
    widths = []
    for column in columns:
        new_row = []
        max_len = len(max(column, key=len))
        max_len = max(max_len, Colors.red*2)
        widths.append(max_len)
        for item in column:
            new_row.append(item.ljust(max_len, ' '))
        table.append(new_row)

    table = izip_longest(*table)

    result = []
    result.append('+' + '+'.join(['-' * (width+2) for width in widths]) + '+')
    result.append('| ' + ' | '.join(table.next()) + ' |')
    result.append('+' + '+'.join(['-' * (width+2) for width in widths]) + '+')

    for row in table:
        result.append('| ' + ' | '.join(row) + ' |')

    result.append('+' + '+'.join(['-' * (width+2) for width in widths]) + '+')

    return result

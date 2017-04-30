import sqlite3
import re
from time import sleep

def cardLuhnChecksumIsValid(card_number):
    """ checks to make sure that a number passes a luhn mod-10 credit card checksum """
    card_number = ''.join(card_number.split())  # remove all whitespace
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    for count in range(0, num_digits):
        digit = int(card_number[count])
        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        sum = sum + digit
    return ( (sum % 10) == 0 )

def skypeMessages(skypeDBs):
    for DB in skypeDBs:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT datetime(timestamp,'unixepoch'), dialog_partner, author, body_xml FROM Messages;")
        messages = [];
        for row in c:
            try:
                if row[2] == row[1]:
                    tofrom = '[%s] From[%s] To[%s]: ' % (row[0], row[2], 'user')
                else:
                    tofrom = '[%s] From[%s] To[%s]: ' % (row[0], 'user', row[1])
                messages.append(tofrom.ljust(70)+row[3])
            except:
                pass
    return messages

def ccnSniffer(messages):
        numbers = []
        for index, line in enumerate(messages):
            line = line.replace("-", "").replace(" ", "")
            while re.search(r'\d+', line) != None: 
                number = re.search(r'\d+', line).group()
                numbers.append((number, index))
                line = line[line.find(number)+len(number):] # removes the first matched number from the line and searches for another match

        interesting_numbers = []
        last_number = 0
        for number in numbers:
            if 17 > len(number[0]) > 12 and number[0] != last_number:
                interesting_numbers.append((number[0], number[1]))
                last_number = number[0]

        for number in interesting_numbers:
            if cardLuhnChecksumIsValid(number[0]) and int(number[0]) > 10:
                yield("[+] CC: %s" % number[0])
                yield("[>] Context:")
                yield("[-2]    %s" % messages[number[1]-2].replace('\n',''))
                yield("[-1]    %s" % messages[number[1]-1].replace('\n',''))
                yield("[ 0]    %s" % messages[number[1]].replace('\n',''))
                try:
                    yield("[+1]    %s" % messages[number[1]+1].replace('\n',''))
                    yield("[+2]    %s\n" % messages[number[1]+2].replace('\n',''))
                except:
                    yield("[+X] Most recent message\n")

if __name__ == "__main__":
    sample_cc_numbers = [   "378282246310005",
                            "4111 1111 1111 1111",
                            "5500 0000 0000 0004", 
                            "3400 0000 0000 009", 
                            "3000 0000 0000 04", 
                            "3000 0000 0000 04",
                            "6011 0000 0000 0004", 
                            "2014 0000 0000 009", 
                            "3088 0000 0000 0009",
                            "4222222222222",
                            "4012888888881881",]

    for line in ccnSniffer(skypeMessages(['/var/root/Library/Application Support/Skype/nikisweeting/main.db'])):
        print line
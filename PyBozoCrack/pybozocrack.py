#!/usr/bin/env python
import hashlib
import re
from urllib import FancyURLopener
import sys
from optparse import OptionParser

HASH_REGEX = re.compile("([a-fA-F0-9]{32})")


class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'


def dictionary_attack(h, wordlist):
    for word in wordlist:
        if hashlib.md5(word).hexdigest() == h:
            return word

    return None


def format_it(hash, plaintext):
    return "{hash}:{plaintext}".format(hash=hash, plaintext=plaintext)


def crack_single_hash(h):
    myopener = MyOpener()
    response = myopener.open(
        "http://www.google.com/search?q={hash}".format(hash=h))

    wordlist = response.read().replace('.', ' ').replace(
        ':', ' ').replace('?', '').replace("('", ' ').replace("'", ' ').split(' ')
    plaintext = dictionary_attack(h, set(wordlist))

    return plaintext


class BozoCrack(object):

    def __init__(self, filename, *args, **kwargs):
        self.hashes = []

        with open(filename, 'r') as f:
            hashes = [h.lower() for line in f if HASH_REGEX.match(line)
                      for h in HASH_REGEX.findall(line.replace('\n', ''))]

        self.hashes = sorted(set(hashes))

        print "Loaded {count} unique hashes".format(count=len(self.hashes))

        self.cache = self.load_cache()

    def crack(self):
        cracked_hashes = []
        for h in self.hashes:
            if h in self.cache:
                print format_it(h, self.cache[h])
                cracked_hashes.append( (h, self.cache[h]) )
                continue

            plaintext = crack_single_hash(h)

            if plaintext:
                print format_it(h, plaintext)
                self.cache[h] = plaintext
                self.append_to_cache(h, plaintext)
                cracked_hashes.append( (h, plaintext) )

        return cracked_hashes

    def load_cache(self, filename='cache'):
        cache = {}
        with open(filename, 'a+') as c:
            for line in c:
                hash, plaintext = line.replace('\n', '').split(':', 1)
                cache[hash] = plaintext
        return cache

    def append_to_cache(self, h, plaintext, filename='cache'):
        with open(filename, 'a+') as c:
            c.write(format_it(hash=h, plaintext=plaintext)+"\n")


def main(): # pragma: no cover
    parser = OptionParser()
    parser.add_option('-s', '--single', metavar='MD5HASH',
                      help='cracks a single hash', dest='single', default=False)
    parser.add_option('-f', '--file', metavar='HASHFILE',
                      help='cracks multiple hashes on a file', dest='target',)

    options, args = parser.parse_args()

    if not options.single and not options.target:
        parser.error("please select -s or -f")
    elif options.single:
        plaintext = crack_single_hash(options.single)

        if plaintext:
            print format_it(hash=options.single, plaintext=plaintext)
    else:
        cracked = BozoCrack(options.target).crack()
        if not cracked:
            print "No hashes were cracked."

if __name__ == '__main__': # pragma: no cover
    main()

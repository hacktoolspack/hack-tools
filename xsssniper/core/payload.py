#!/usr/bin/env python

import random
import string

class Payload:
    def __init__(self, taint=False, seed_len=None, payload=None):
        if taint:
            self.taint = True
            if seed_len is not None:
                self.seed_len = seed_len
            else:
                self.seed_len = 4
            self.seed = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(self.seed_len)).lower()
            self.payload = "{0}:{0} {0}=-->{0}\"{0}>{0}'{0}>{0}+{0}<{0}>".format(self.seed)
        elif payload is not None:
            self.taint = False
            self.seed = None
            self.seed_len = None
            self.payload = payload


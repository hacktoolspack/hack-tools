#!/usr/bin/python
#
# Peteris Krumins (peter@catonmat.net)
# http://www.catonmat.net  --  good coders code, great reuse
#
# http://www.catonmat.net/blog/python-library-for-google-sets/
#
# Code is licensed under MIT license.
#

import re
import urllib
import random
from htmlentitydefs import name2codepoint
from BeautifulSoup import BeautifulSoup

from browser import Browser, BrowserError

class GSError(Exception):
    """ Google Sets Error """
    pass

class GSParseError(Exception):
    """
    Parse error in Google Sets results.
    self.msg attribute contains explanation why parsing failed
    self.tag attribute contains BeautifulSoup object with the most relevant tag that failed to parse
    Thrown only in debug mode
    """
     
    def __init__(self, msg, tag):
        self.msg = msg
        self.tag = tag

    def __str__(self):
        return self.msg

    def html(self):
        return self.tag.prettify()

LARGE_SET = 1
SMALL_SET = 2

class GoogleSets(object):
    URL_LARGE = "http://labs.google.com/sets?hl=en&q1=%s&q2=%s&q3=%s&q4=%s&q5=%s&btn=Large+Set"
    URL_SMALL = "http://labs.google.com/sets?hl=en&q1=%s&q2=%s&q3=%s&q4=%s&q5=%s&btn=Small+Set+(15+items+or+fewer)"

    def __init__(self, items, random_agent=False, debug=False):
        self.items = items
        self.debug = debug
        self.browser = Browser(debug=debug)

        if random_agent:
            self.browser.set_random_user_agent()

    def get_results(self, set_type=SMALL_SET):
        page = self._get_results_page(set_type)
        results = self._extract_results(page)
        return results

    def _maybe_raise(self, cls, *arg):
        if self.debug:
            raise cls(*arg)

    def _get_results_page(self, set_type):
        if set_type == LARGE_SET:
            url = GoogleSets.URL_LARGE
        else:
            url = GoogleSets.URL_SMALL

        safe_items = [urllib.quote_plus(i) for i in self.items]
        blank_items = 5 - len(safe_items)
        if blank_items > 0:
            safe_items += ['']*blank_items

        safe_url = url % tuple(safe_items)

        try:
            page = self.browser.get_page(safe_url)
        except BrowserError, e:
            raise GSError, "Failed getting %s: %s" % (e.url, e.error)

        return BeautifulSoup(page)

    def _extract_results(self, soup):
        a_links = soup.findAll('a', href=re.compile('/search'))
        ret_res = [a.string for a in a_links]
        return ret_res


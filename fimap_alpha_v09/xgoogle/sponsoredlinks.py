#!/usr/bin/python
#
# Peteris Krumins (peter@catonmat.net)
# http://www.catonmat.net  --  good coders code, great reuse
#
# http://www.catonmat.net/blog/python-library-for-google-sponsored-links-search/
#
# Code is licensed under MIT license.
#

import re
import urllib
import random
from htmlentitydefs import name2codepoint
from BeautifulSoup import BeautifulSoup

from browser import Browser, BrowserError

#
# TODO: join GoogleSearch and SponsoredLinks classes under a single base class
#

class SLError(Exception):
    """ Sponsored Links Error """
    pass

class SLParseError(Exception):
    """
    Parse error in Google results.
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

GET_ALL_SLEEP_FUNCTION = object()

class SponsoredLink(object):
    """ a single sponsored link """
    def __init__(self, title, url, display_url, desc):
        self.title = title
        self.url = url
        self.display_url = display_url
        self.desc = desc

class SponsoredLinks(object):
    SEARCH_URL_0 = "http://www.google.com/sponsoredlinks?q=%(query)s&btnG=Search+Sponsored+Links&hl=en"
    NEXT_PAGE_0 = "http://www.google.com/sponsoredlinks?q=%(query)s&sa=N&start=%(start)d&hl=en"
    SEARCH_URL_1 = "http://www.google.com/sponsoredlinks?q=%(query)s&num=%(num)d&btnG=Search+Sponsored+Links&hl=en"
    NEXT_PAGE_1 = "http://www.google.com/sponsoredlinks?q=%(query)s&num=%(num)d&sa=N&start=%(start)d&hl=en"

    def __init__(self, query, random_agent=False, debug=False):
        self.query = query
        self.debug = debug
        self.browser = Browser(debug=debug)
        self._page = 0
        self.eor = False
        self.results_info = None
        self._results_per_page = 10

        if random_agent:
            self.browser.set_random_user_agent()

    @property
    def num_results(self):
        if not self.results_info:
            page = self._get_results_page()
            self.results_info = self._extract_info(page)
            if self.results_info['total'] == 0:
                self.eor = True
        return self.results_info['total']

    def _get_results_per_page(self):
        return self._results_per_page

    def _set_results_par_page(self, rpp):
        self._results_per_page = rpp

    results_per_page = property(_get_results_per_page, _set_results_par_page)

    def get_results(self):
        if self.eor:
            return []
        page = self._get_results_page()
        info = self._extract_info(page)
        if self.results_info is None:
            self.results_info = info
        if info['to'] == info['total']:
            self.eor = True
        results = self._extract_results(page)
        if not results:
            self.eor = True
            return []
        self._page += 1
        return results

    def _get_all_results_sleep_fn(self):
        return random.random()*5 + 1 # sleep from 1 - 6 seconds

    def get_all_results(self, sleep_function=None):
        if sleep_function is GET_ALL_SLEEP_FUNCTION:
            sleep_function = self._get_all_results_sleep_fn
        if sleep_function is None:
            sleep_function = lambda: None 
        ret_results = []
        while True:
            res = self.get_results()
            if not res:
                return ret_results
            ret_results.extend(res)
        return ret_results

    def _maybe_raise(self, cls, *arg):
        if self.debug:
            raise cls(*arg)

    def _extract_info(self, soup):
        empty_info = { 'from': 0, 'to': 0, 'total': 0 }
        stats_span = soup.find('span', id='stats')
        if not stats_span:
            return empty_info
        txt = ''.join(stats_span.findAll(text=True))
        txt = txt.replace(',', '').replace("&nbsp;", ' ')
        matches = re.search(r'Results (\d+) - (\d+) of (?:about )?(\d+)', txt)
        if not matches:
            return empty_info
        return {'from': int(matches.group(1)), 'to': int(matches.group(2)), 'total': int(matches.group(3))}

    def _get_results_page(self):
        if self._page == 0:
            if self._results_per_page == 10:
                url = SponsoredLinks.SEARCH_URL_0
            else:
                url = SponsoredLinks.SEARCH_URL_1
        else:
            if self._results_per_page == 10:
                url = SponsoredLinks.NEXT_PAGE_0
            else:
                url = SponsoredLinks.NEXT_PAGE_1

        safe_url = url % { 'query': urllib.quote_plus(self.query),
                           'start': self._page * self._results_per_page,
                           'num': self._results_per_page }

        try:
            page = self.browser.get_page(safe_url)
        except BrowserError, e:
            raise SLError, "Failed getting %s: %s" % (e.url, e.error)

        return BeautifulSoup(page)

    def _extract_results(self, soup):
        results = soup.findAll('div', {'class': 'g'})
        ret_res = []
        for result in results:
            eres = self._extract_result(result)
            if eres:
                ret_res.append(eres)
        return ret_res

    def _extract_result(self, result):
        title, url = self._extract_title_url(result)
        display_url = self._extract_display_url(result) # Warning: removes 'cite' from the result
        desc = self._extract_description(result)
        if not title or not url or not display_url or not desc:
            return None
        return SponsoredLink(title, url, display_url, desc)

    def _extract_title_url(self, result):
        title_a = result.find('a')
        if not title_a:
            self._maybe_raise(SLParseError, "Title tag in sponsored link was not found", result)
            return None, None
        title = ''.join(title_a.findAll(text=True))
        title = self._html_unescape(title)
        url = title_a['href']
        match = re.search(r'q=(http[^&]+)&', url)
        if not match:
            self._maybe_raise(SLParseError, "URL inside a sponsored link was not found", result)
            return None, None
        url = urllib.unquote(match.group(1))
        return title, url

    def _extract_display_url(self, result):
        cite = result.find('cite')
        if not cite:
            self._maybe_raise(SLParseError, "<cite> not found inside result", result)
            return None

        return ''.join(cite.findAll(text=True))

    def _extract_description(self, result):
        cite = result.find('cite')
        if not cite:
            return None
        cite.extract()

        desc_div = result.find('div', {'class': 'line23'})
        if not desc_div:
            self._maybe_raise(ParseError, "Description tag not found in sponsored link", result)
            return None

        desc_strs = desc_div.findAll(text=True)[0:-1]
        desc = ''.join(desc_strs)
        desc = desc.replace("\n", " ")
        desc = desc.replace("  ", " ")
        return self._html_unescape(desc)

    def _html_unescape(self, str):
        def entity_replacer(m):
            entity = m.group(1)
            if entity in name2codepoint:
                return unichr(name2codepoint[entity])
            else:
                return m.group(0)

        def ascii_replacer(m):
            cp = int(m.group(1))
            if cp <= 255:
                return unichr(cp)
            else:
                return m.group(0)

        s =    re.sub(r'&#(\d+);',  ascii_replacer, str, re.U)
        return re.sub(r'&([^;]+);', entity_replacer, s, re.U)


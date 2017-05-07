#!/usr/bin/python3
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#
# Developed by: Nasel(http://www.nasel.com.ar)
#
# Authors:
# Matías Fontanini
# Santiago Alessandri
# Gastón Traberg

import re, sre_constants
from moleexceptions import FilterCreationError
from responsefilters.base import ResponseFilter
from responsefilters import register_response_filter

class BaseRegexHTMLFilter(ResponseFilter):
    def __init__(self, name, filter_str, replacement):
        ResponseFilter.__init__(self, name, [filter_str, replacement])
        self.replacement = replacement
        try:
            self.regex = re.compile(filter_str, flags=re.DOTALL | re.MULTILINE)
        except sre_constants.error as ex:
            raise FilterCreationError(str(ex))

    def filter_(self, response):
        response.content = self.regex.sub(self.replacement, response.content)


class RemoverRegexHTMLFilter(BaseRegexHTMLFilter):
    def __init__(self, name, params):
        if len(params) != 1:
            raise FilterCreationError('Expected regex as argument.')
        BaseRegexHTMLFilter.__init__(self, name, params[0], '')

    def __str__(self):
        return '{name} \'{pat}\''.format(name=self.name, pat=self.regex.pattern)

class ReplacerRegexHTMLFilter(BaseRegexHTMLFilter):
    def __init__(self, name, params):
        if len(params) != 2:
            raise FilterCreationError('Expected regex and replacement string as arguments.')
        BaseRegexHTMLFilter.__init__(self, name, params[0], params[1])

    def __str__(self):
        return '{name} \'{pat}\' -> \'{rep}\''.format(name=self.name, pat=self.regex.pattern, rep=self.replacement)

class HTMLPretifierFilter(BaseRegexHTMLFilter):
    def __init__(self, name, params):
        BaseRegexHTMLFilter.__init__(self, name, '\(<html>|<body>|</html>|</body>\)', '')

class ScriptErrorFilter(ResponseFilter):
    def __init__(self, name, params):
        ResponseFilter.__init__(self, name, params)
        self.error_filters = [
            # PHP verbose errors.
            re.compile("<br />\n<b>Warning</b>:  [\w_\d]+\(\)(:\s|\s\[.*\]:)[\w :<>\\\\_\'\.\(\)/-]+ on line <b>(\d+)</b><br />"),
        ]

    def filter_(self, response):
        for i in self.error_filters:
            response.content = i.sub('', response.content)
        return response

class HTMLValidationFilter(ResponseFilter):
    def __init__(self, name, params):
        ResponseFilter.__init__(self, name, params)
        self.regex = re.compile('<html', flags=re.DOTALL | re.MULTILINE)
    
    def filter_(self, response):
        if not self.regex.match(response.content):
            response.content = '<html><body>{0}</body></html>'.format(response.content)
        return response

register_response_filter('regex_rem', RemoverRegexHTMLFilter)
register_response_filter('regex_rep', ReplacerRegexHTMLFilter)
register_response_filter('html_pretifier', HTMLPretifierFilter)
register_response_filter('script_error_filter', ScriptErrorFilter)
register_response_filter('html_validator', HTMLValidationFilter)

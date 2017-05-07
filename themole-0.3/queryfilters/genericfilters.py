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

import random, re
from moleexceptions import FilterConfigException, FilterCreationError
from queryfilters.base import BaseQueryFilter
from queryfilters import register_query_filter
from parameters import Parameter

class CaseFilter(BaseQueryFilter):
    word_delimiters = {' ', '/', '(', ')'}

    def filter_(self, query):
        query_list = list(query)
        so_far = ''
        skip_next = False
        for i in range(len(query_list)):
            if query_list[i] in self.word_delimiters:
                if not skip_next:
                    word = query_list[i - len(so_far):i]
                    if ''.join(word).isupper() or ''.join(word).islower():
                        word = [word[i].swapcase() if i % 2 == 1 and not word[i] == 'x' else word[i] for i in range(len(word))]
                        query_list[i - len(so_far):i] = word
                skip_next = (so_far == 'from')
                so_far = ''
            else:
                so_far += query_list[i].lower()
            if not skip_next:
                # Fix for mysql 0xFFFF syntax. These filters should be
                # applied before converting quoted strings to dbms specific
                # string representation.
                if query_list[i] != 'x' and random.randrange(0, 2) == 0:
                    if query_list[i].isupper():
                        query_list[i] = query_list[i].lower()
                    else:
                        query_list[i] = query_list[i].upper()

        return ''.join(query_list)


class Spaces2CommentsFilter(BaseQueryFilter):
    def filter_(self, query):
        return query.replace(' ', '/**/')

class Spaces2NewLineFilter(BaseQueryFilter):
    def filter_(self, query):
        return query.replace(' ', '\n')

class SQLServerCollationFilter(BaseQueryFilter):
    def __init__(self, name, params):
        BaseQueryFilter.__init__(self, name, params)
        self.cast_match = re.compile('cast\([\w\d_\-@]+ as varchar\([\d]+\)\)')
        self.field_match = re.compile('cast\(([\w\d_\-@]+) as varchar\([\d]+\)\)')
        self.blacklist = []
        self.collation = params[0] if len(params) == 1 else 'DATABASE_DEFAULT'
        self.blist_param = Parameter(lambda _, __: self.print_blacklist())
        add_blist = Parameter(lambda _, params: self.blacklist_add(params))
        del_blist = Parameter(no_args_str='Expected argument after "del"')
        self.blist_param.add_parameter('add', add_blist)
        del_blist.set_param_generator(lambda _, __: self.del_generator())
        self.blist_param.add_parameter('del', del_blist)
        self.collation_param = Parameter(lambda _, params: self.exec_collation(params))
        self.params = { 'blacklist' : self.blist_param, 'collation' : self.collation_param }

    def configuration_parameters(self):
        return self.params

    def exec_collation(self, params):
        if len(params) < 1:
            output_manager.normal(self.collation).line_break()
        else:
            self.collation = params[0]

    def blacklist_add(self, params):
        if len(params) == 0:
            output_manager.error('Expected argument after "add"').line_break()
        else:
            for i in params:
                self.blacklist.append(i)

    def del_generator(self):
        ret = {}
        for i in self.blacklist:
            ret[i] = Parameter(lambda _, __, i=i: self.blacklist.remove(i))
        return ret

    def print_blacklist(self):
        if len(self.blacklist) == 0:
            output_manager.info('No fields in blacklist.').line_break()
        else:
            for i in self.blacklist:
                output_manager.normal(i).line_break()

    def filter_(self, query):
        try:
            matches = self.cast_match.findall(query)
            for i in matches:
                field = self.field_match.findall(i)[0]
                if not field in self.blacklist:
                    replaced = i.replace(field, '(' + field + ' COLLATE ' + self.collation + ')')
                    query = query.replace(i, replaced)
        except Exception as ex:
            output_manager.error('{0}'.format(ex)).line_break()
        return query

    def export_config(self):
        import copy
        blacklist_config = ['blacklist', 'add'] + copy.copy(self.blacklist)
        collation_config = ['collation', self.collation]
        return [blacklist_config, collation_config]

    def __str__(self):
        return self.name + ' ' + self.collation

class BetweenComparerFilter(BaseQueryFilter):
    def __init__(self, name, params):
        BaseQueryFilter.__init__(self, name, params)
        self.regex = re.compile('([\d]+)[ ]+([<>])[ ]+(\(select [\w\d\(\) _\-\+,\*@\.=]+\))')

    def filter_(self, query):
        match = self.regex.search(query)
        if match:
            num, op, select = match.groups()
            preffix = 'not ' if op == '>' else ''
            return query.replace(match.string[match.start():match.end()], preffix + num + ' between 0 and ' + select + '-1 ')
        return query

class ParenthesisFilter(BaseQueryFilter):

    def __init__(self, name, params):
        BaseQueryFilter.__init__(self, name, params)
        self.regex = re.compile('(where|and)[ ]+([\'"\d\w_]+)[ ]*(between|like|[<>=])[ ]*(\(.+\)|[\'"\d\w]+)', re.IGNORECASE)

    def filter_(self, query):
        match = self.regex.search(query)
        while match:
            keyword, op1, oper, op2 = match.groups()
            if len(list(filter(lambda x: x == '"' or x == "'", op2))) & 1 == 0:
                op2 = '(' + op2 + ')'
            query = query.replace(match.string[match.start():match.end()], keyword + '(' + op1 + ')' + oper + op2)
            match = self.regex.search(query)
        return query

class NoAsteriskFilter(BaseQueryFilter):
    def filter_(self, query):
        return query.replace('*', '1')

class RegexFilter(BaseQueryFilter):
    def __init__(self, name, params):
        BaseQueryFilter.__init__(self, name, params)
        if len(params) != 2:
            raise FilterCreationError('Expected 2 arguments')
        try:
            self.regex = re.compile(params[0], re.IGNORECASE)
            self.replacement = params[1]
        except Exception as ex:
            raise FilterCreationError(str(ex))

    def filter_(self, query):
        return self.regex.sub(self.replacement, query)

    def __str__(self):
        return 'regex ' + self.regex.pattern + ' ' + self.replacement


register_query_filter('case', CaseFilter)
register_query_filter('space2comment', Spaces2CommentsFilter)
register_query_filter('space2newline', Spaces2NewLineFilter)
register_query_filter('mssqlcollation', SQLServerCollationFilter)
register_query_filter('between', BetweenComparerFilter)
register_query_filter('parenthesis', ParenthesisFilter)
register_query_filter('noasterisk', NoAsteriskFilter)
register_query_filter('regex', RegexFilter)

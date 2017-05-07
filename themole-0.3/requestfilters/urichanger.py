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

from urllib.parse import parse_qs, quote

from requestfilters import register_request_filter
from requestfilters.base import RequestFilter

from moleexceptions import FilterCreationError, FilterRuntimeException

class URIChangerFilter(RequestFilter):
    """
    
    Filter to change the URI where the request is to be sent.
    This applies to the path and the GET parameters. 
    
    """

    def __init__(self, name, params):
        RequestFilter.__init__(self, name, params)
        if len(params) == 0:
            raise FilterCreationError("URI format string is needed")
        self.__format_string = params[0]

    def filter_(self, request):
        """Apply the changes to the path and GET params by using
        the URI format string given.
        
        @param request: Request object to filter.
        
        """
        try:
            quoted_params = dict(map(lambda k: (k, quote(request.get_parameters[k])), request.get_parameters))
            new_uri = self.__format_string.format(**quoted_params)
        except KeyError as e:
            raise FilterRuntimeException('{0} was used in the string format but it is not a GET parameter'.format(e))

        splitted_uri = new_uri.split('?')
        request.path = splitted_uri[0]
        new_get_parameters = {}
        if len(splitted_uri) > 1:
            new_get_parameters = parse_qs(splitted_uri[1])
            for param in new_get_parameters:
                new_get_parameters[param] = new_get_parameters[param][0]

        request.get_parameters = new_get_parameters


register_request_filter('uri_changer', URIChangerFilter)

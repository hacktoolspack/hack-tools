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

import copy

class ResponseFilter:
    def __init__(self, name, params):
        """Initialize a Response filter identified by the name. 
        
        @param name: String used to identify the plugin.
        
        """
        self.init_params = copy.copy(params)
        self.name = name

    def filter_(self, response):
        """Apply the filter to the response.
        
        @param query: Response object to filter.
        
        """
        pass

    def configuration_parameters(self):
        return {}

    def export_config(self):
        return []

    def __str__(self):
        return self.name

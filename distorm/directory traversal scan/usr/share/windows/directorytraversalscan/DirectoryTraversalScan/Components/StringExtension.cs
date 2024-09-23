//This file is part of HTTP Directory Traversal Scanner.
//
//HTTP Directory Traversal Scanner is free software: you can redistribute it and/or modify
//it under the terms of the GNU General Public License as published by
//the Free Software Foundation, either version 3 of the License, or
//(at your option) any later version.
//
//HTTP Directory Traversal Scanner is distributed in the hope that it will be useful,
//but WITHOUT ANY WARRANTY; without even the implied warranty of
//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//GNU General Public License for more details.
//
//You should have received a copy of the GNU General Public License
//along with HTTP Directory Traversal Scanner.  If not, see <http://www.gnu.org/licenses/>.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace DirectoryTraversalScan.Components
{
    public static class StringExtension
    {
        public static string Repeat(this string s, int Count)
        {
            return new StringBuilder().Insert(0, s, Count).ToString();
        }

        public static string Aggregate(this IEnumerable<string> s)
        {
            return s.Aggregate((x, y) => x + y);
        }

        public static string Aggregate(this IEnumerable<string> s, string Delimiter)
        {
            return s.Aggregate((x, y) => x + Delimiter + y);
        }
    }
}

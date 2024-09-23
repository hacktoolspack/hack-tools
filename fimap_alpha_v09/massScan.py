#
# This file is part of fimap.
#
# Copyright(c) 2009-2010 Iman Karim(ikarim2s@smail.inf.fh-brs.de).
# http://fimap.googlecode.com
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#



__author__="Iman Karim(ikarim2s@smail.inf.fh-brs.de)"
__date__ ="$01.09.2009 04:28:51$"

from targetScanner import targetScanner
from singleScan import singleScan


class massScan:

    def __init__(self, config):
        self.config = config
        self.list = config["p_list"]

    def startMassScan(self):
        print "MassScan reading file: '%s'..."%self.list

        f = open(self.list, "r")
        idx = 0
        for l in f:
            if idx >= 0:
                l = l.strip()
                if (l.startswith("http://"), l.startswith("https://")):
                    print "[%d][MASS_SCAN] Scanning: '%s'..." %(idx,l)
                    single = singleScan(self.config)
                    single.setURL(l)
                    single.setQuite(True)
                    single.scan()

                    idx = idx +1

        print "MassScan completed."
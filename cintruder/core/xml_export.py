#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
This file is part of the cintruder project, http://cintruder.03c8.net

Copyright (c) 2012/2016 psy <epsylon@riseup.net>

cintruder is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation version 3 of the License.

cintruder is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along
with cintruder; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import xml.etree.ElementTree as xml
import datetime, os

class CIntruderXML(object):
    """
    Print results from an attack in an XML fashion
    """
    def __init__(self, cintruder):
        # initialize main CIntruder
        self.instance = cintruder

    def print_xml_results(self, captchas, filename, word_sug):
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.mkdir(dirname)
        root = xml.Element("report")
        hdr = xml.SubElement(root, "header")
        title = xml.SubElement(hdr, "title")
        title.text = "Captcha Intruder [http://cintruder.03c8.net] Report: " + str(datetime.datetime.now())
        target = xml.SubElement(root, "target")
        captcha = xml.SubElement(target, "captcha")
        words = xml.SubElement(captcha, "word")
        captcha.text = str(captchas)
        words.text = str(word_sug)
        tree = xml.ElementTree(root)
        tree.write(filename)

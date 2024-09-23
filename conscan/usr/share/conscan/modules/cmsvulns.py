#!/usr/bin/python

import xml.etree.ElementTree as ET

tree = ET.parse('data/cmsvulns.xml')
root = tree.getroot()

bold = '\033[1m'
normal = '\033[0m'

## Module to list vulnerabilites against the version detected
def vulncheck(version):

	try:
		for ver in root:
			vers = ver.get('version')
			if vers >= version:
				for vulnerability in ver.iter('vulnerability'):
					for title in vulnerability:
						print bold + '\n [+] ' + title.text + normal
						break

					for references in vulnerability.iter('references'):
						for url in references.iter('url'):
			     				print url.text
	except Exception, error:
	    pass


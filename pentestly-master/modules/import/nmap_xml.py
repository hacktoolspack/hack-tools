from recon.core.module import BaseModule

import os
from xml.etree import ElementTree

class Module(BaseModule):

    meta = {
        'name': 'Import Nmap XML',
        'author': 'Cory Duplantis (@ctfhacker)',
        'description': 'Imports port scan from nmap XML',
        'options': (
            ('filename', None, True, 'Path and filename for nmap XML input'),
        ),
    }
    
    def module_run(self):
        cnt = 0
        filename = self.options['filename']
        if not os.path.exists(filename):
            raise RuntimeError("File does not exist {}".format(filename))
        with open(filename) as fh:
            data = fh.read()

        xml = ElementTree.parse(filename)
        for host in xml.findall('host'):
            addr = host.find('address').get('addr')
            try:
                for curr_port in host.find('ports').findall('port'):
                    if curr_port.find('state').get('state') != 'open':
                        continue
                    port = curr_port.get('portid')
                    protocol = curr_port.get('protocol')
                    cnt += self.add_ports(ip_address=addr, port=port, protocol=protocol)
            except AttributeError:
                pass
        self.output('{} new records added.'.format(cnt))

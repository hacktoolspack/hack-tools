#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created using Metafidv2 by Matthew Bryant (mandatory)
# Unauthorized use is stricly prohibited, please contact mandatory@gmail.com with questions/comments.
import requests
import json
import time
import csv
import sys
import os
from bs4 import BeautifulSoup

class cloudflare_enum:
    def __init__( self ):
        # Master list of headers to be used in each connection
        self.global_headers = {
        }
        self.verbose = True

        self.s = requests.Session()
        self.s.headers.update( self.global_headers )
        self.atok = ''

    def log_in( self, username, password ):
        parse_dict = {}

        r = self.s.get('https://www.cloudflare.com/', )

        new_headers = {
            'Referer': 'https://www.cloudflare.com/',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/a/login', )
        parse_dict[ 'security_token_0' ] = self.find_between_r( r.text, '"security_token":"', '"}};</script>' ) # http://xkcd.com/292/

        post_data = {
            'email': username,
            'password': password,
            'security_token': parse_dict[ 'security_token_0' ],
        }
        new_headers = {
            'Referer': 'https://www.cloudflare.com/a/login',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.post('https://www.cloudflare.com/a/login', data=post_data)
        self.atok = self.find_between_r( r.text, 'window.bootstrap = {"atok":"', '","locale":"' ) # http://xkcd.com/292/

    def get_domain_dns( self, domain ):
        parse_dict = {}
        post_data = {
            "betas": [],
            "created_on": "2015-08-24T00:27:16.048Z",
            "development_mode": False,
            "jump_start": True,
            "meta": {},
            "modified_on": 'null',
            "name": domain,
            "owner": {},
            "paused": False,
            "status": "initializing",
            "type": "full"
        }

        new_headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.cloudflare.com/a/add-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'X-ATOK': self.atok,
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.post('https://www.cloudflare.com/api/v4/zones', data=json.dumps( post_data ))
        data = json.loads( r.text )
        success = data['success']
        if not success:
            print r.text
            return False

        request_id = data['result']['id']
        time.sleep( 60 )

        get_data = {
            'per_page': '100',
            'direction': 'asc',
            'page': '1',
            'order': 'type',
        }
        new_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.cloudflare.com/a/setup/' + domain + '/step/2',
            'X-ATOK': self.atok,
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/api/v4/zones/' + request_id + '/dns_records', params=get_data)
        return_data = json.loads( r.text )

        new_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.cloudflare.com/a/setup/' + domain + '/step/2',
            'X-ATOK': self.atok,
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.delete('https://www.cloudflare.com/api/v4/zones/' + request_id, )

        get_data = {
            'status': 'initializing,pending',
            'per_page': '50',
            'page': '1',
        }
        new_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.cloudflare.com/a/add-site',
            'X-ATOK': self.atok,
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/api/v4/zones', params=get_data)

        return return_data['result']

    def get_spreadsheet( self, domain ):
        dns_data = self.get_domain_dns( domain )
        if dns_data:
            filename = domain.replace( ".", "_" ) + ".csv"

            with open( filename, 'wb' ) as csvfile:
                dns_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                dns_writer.writerow( [ "name", "type", "content" ] )
                for record in dns_data:
                    dns_writer.writerow( [ record["name"], record["type"], record["content"] ] )
                
            self.statusmsg( "Spreadsheet created at " + os.getcwd() + "/" + filename )

    def print_banner( self ):
        if self.verbose:
            print """
            
                                                     `..--------..`                               
                                                 .-:///::------::///:.`                           
                                              `-//:-.`````````````.-://:.`    `   `               
                                            .://-.```````````````````.-://-`  :  `-   .           
                                          `-//:.........................-://. /. -: `:`  ``       
                                         `://--------:::://////:::--------://-::.::`:- .:.        
                              ``.---..` `///::::::///////////////////:::::::///::::::--:.`.-.     
                            .://::::///::///::///////////////////////////:::///:-----::--:-`  `    
                          `:/:-...--:://////////////////////////////////////////----------.--.`    
                         `:/:..-:://////////////////////////////////////////////-----------.````    
                         .//-::////////////////////////////////////:::::////////-...--------...`    
                         -/////////////////////////////////////////////::::----:. `.-::::::-..``    
                    ``.--:////////////////////////////////////////////////::-..```-///::::///:-`    
                 `.:///::::://////////////////////////////////////:::::::::::::::-----......-:/:.    
               `-//:-----::::://///////////////////////////////:///////////////////:-::::---..-//:`    
              `:/:---://+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//+++//::--//:    
             `//:-/+oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo+++oooo+//://.    
             :///ossssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssosssssso+//:    
            `//+sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss+/-    
            `//+ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo+++++/.    
             ``````````````````````````````````````````````````````````````````````````````````````     
                                                             Cloudflare DNS Enumeration Tool v1.2
                                                                                    By mandatory
        """


    def pprint( self, input_dict ):
        print json.dumps(input_dict, sort_keys=True, indent=4, separators=(',', ': '))

    def statusmsg( self, msg ):
        if self.verbose:
            print "[ STATUS ] " + msg

    def errormsg( self, msg ):
        if self.verbose:
            print "[ ERROR ] " + msg

    def successmsg( self, msg ):
        if self.verbose:
            print "[ SUCCESS ] " + msg

    def find_between_r( self, s, first, last ):
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def find_between( s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def get_cookie_from_file( self, cookie_file ):
        return_dict = {}
        with open( cookie_file ) as tmp:
            data = tmp.readlines()
            tmp_data = []
            for i, item in enumerate(data):
                if "	" in data[i]:
                    pew = data[i].split( "	" )
                    return_dict[ pew[5] ] = pew[6] 

        return return_dict

if __name__ == "__main__":
    if len( sys.argv ) < 3:
        print "Usage: " + sys.argv[0] + " username@email.com password domain.com"
    else:
        cloud = cloudflare_enum()
        cloud.print_banner()
        cloud.log_in( sys.argv[1], sys.argv[2] )
        cloud.get_spreadsheet( sys.argv[3] )

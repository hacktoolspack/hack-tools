#Author:D4Vinci

def ip2long(ip):
      ip = ip.split("/")[0].split(":")[0]
      p = ip.split(".")
      return str( ( ( ( ( int(p[0]) * 256 + int(p[1]) ) * 256 ) + int(p[2]) ) * 256 ) + int(p[3]))
              #p[0] + "." + str( ( ( ( int( p[1] ) * 256 + int( p[2] ) ) * 256 ) + int( p[3] ) ) * 256 ),
              #p[0] + "." + p[1] +  str( ( int( p[2] ) *256 ) + int( p[3] ) )

def ip2hex(ip):
      ip = ip.split("/")[0].split(":")[0]
      p = ip.split(".")
      return [str( hex( int(p[0]) ) ) +"."+ str( hex( int(p[1]) ) ) +"."+ str( hex( int(p[2]) ) ) +"."+ str( hex( int(p[3]) ) ),
              str( hex( int(p[0]) ) ) +"."+ str( hex( int(p[1]) ) ) +"."+ str( hex( int(p[2]) ) ) +"."+ str( int(p[3]) ),
              str( hex( int(p[0]) ) ) +"."+ str( hex( int(p[1]) ) ) +"."+ str( int(p[2]) ) +"."+ str( int(p[3]) ),
              str( hex( int(p[0]) ) ) +"."+ str( int(p[1]) ) +"."+ str( int(p[2]) ) +"."+ str( int(p[3]) ),
              "0x"+"0"*8+str( hex( int(p[0]) ) ).replace("0x","") +"."+ "0x"+"0"*6+str( hex( int(p[1]) ) ).replace("0x","") +"."+ "0x"+"0"*4+str( hex( int(p[2]) ) ).replace("0x","")+"."+ "0x"+"0"*2+str( hex( int(p[3]) ) ).replace("0x",""),
              str( hex( int( ip2long( ip ) ) ) ).replace( "L" , "" )]

def ip2Octal(ip):
      return '.'.join(format(int(x), '04o') for x in ip.split('.'))

def ip_as_urlencoded(ip):
      ip = ip.split("/")[0]
      en=""
      for i in ip :
            if i.isdigit() :
                  en += "%3{}".format(i)
            elif i == "." :
                  en += "%2E"
            elif i == ":" :
                  en += "%3A"
      return en

def ip_as_url(ip):
      return [ "http://howsecureismypassword.net@"+str(ip),
               "http://google.com@"+str( ip2long( ip ) ),
               "http://facebook.com@"+str( ip2hex( ip )[-1] ),
               "http://"+str( ip_as_urlencoded(ip) ),
               "https://www.google.com@search@"+str( ip_as_urlencoded(ip) ),
               "http://anywebsite@"+str( ip2Octal(ip) )]

print "\n Cuteit - Make a malicious ip a bit cuter :D"
print " Note:don't type a long url because it's encode the ip only.!"
ip = raw_input("  ip > ")
ip=ip.replace("http://","")
print "\n"
for n,i in enumerate( ip2hex(ip) + ip_as_url(ip) ):
      if "http" not in i:
            print " ["+str(n)+"] "+"http://"+i
      else:
            print " ["+str(n)+"] "+i
print " [12] http://" + ip2Octal(ip)
print " [13] http://" + ip2long(ip)

#!/usr/bin/python
"""
#     __                                           _             __   _    
#    / /_  __  __   ______________ _____  __  __  (_)_  ______  / /__(_)__ 
#   / __ \/ / / /  / ___/ ___/ __ `/_  / / / / / / / / / / __ \/ //_/ / _ \
#  / /_/ / /_/ /  / /__/ /  / /_/ / / /_/ /_/ / / / /_/ / / / / ,< / /  __/
# /_.___/\__, /   \___/_/   \__,_/ /___/\__, /_/ /\__,_/_/ /_/_/|_/_/\___/ 
#       /____/                         /____/___/                          
#
###############################################################################
 Download huge collections of wordlist:#
http://ul.to/folder/j7gmyz#
##########################################################################

####################################################################
 Need daylie updated proxies?#
http://j.mp/Y7ZZq9#
################################################################

######################################################
#### HashTag ######
###################################################

Description:    HashTag.py is a python script written to parse and identify password hashes.  It has three main arguments
                which consist of identifying a single hash type (-sh), parsing and identifying multiple hashes from a 
                file (-f), and traversing subdirectories to locate files which contain hashes  and parse/identify them (-d).
                Many common hash types are supported by the CPU and GPU cracking tool Hashcat.  Using an additional 
                argument (-hc) hashcat modes will be included in the output file(s).
#  
#				This program is free software; you can redistribute it and/or modify
#  				it under the terms of the GNU General Public License as published by
#  				the Free Software Foundation; either version 2 of the License, or
#  				(at your option) any later version.
#  
#  				This program is distributed in the hope that it will be useful,
#  				but WITHOUT ANY WARRANTY; without even the implied warranty of
#  				MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  				GNU General Public License for more details.
#  
#  				You should have received a copy of the GNU General Public License
#  				along with this program; if not, write to the Free Software
#  				Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  				MA 02110-1301, USA.
#  
#				18.02.2014
"""
import argparse
import mimetypes
import os
import shutil
import string

parser = argparse.ArgumentParser(prog='HashTag.py', usage='%(prog)s {-sh hash |-f file |-d directory} [-o output_filename] [-hc] [-n]')
argGroup = parser.add_mutually_exclusive_group(required=True)
argGroup.add_argument("-sh", "--singleHash", type=str, help="Identify a single hash")
argGroup.add_argument("-f", "--file", type=str, help="Parse a single file for hashes and identify them")
argGroup.add_argument("-d", "--directory", type=str, help="Parse, identify, and categorize hashes within a directory and all subdirectories")
parser.add_argument("-o", "--output", type=str, help="Filename to output full list of all identified hashes. Default is ./HashTag/HashTag_Output_File.txt")
parser.add_argument("-hc", "--hashcatOutput", action='store_true', default=False, help="Output a separate file for each hash type based on hashcat modes")
parser.add_argument("-n", "--notFound", action='store_true', default=False, help="--file:Include unidentifiable hashes in the output file.")
args = parser.parse_args()

hashDict = dict()

hashcatDict = { \
'MD5': '0', 'md5($pass.$salt)': '10', 'Joomla': '11', 'md5($salt.$pass)': '20', 'osCommerce, xt:Commerce': '21', 'm\
d5(unicode($pass).$salt)': '30', 'md5($salt.unicode($pass))': '40', 'HMAC-MD5 (key = $pass)': '50', 'HMAC-MD5 (key\
= $salt)': '60', 'SHA1': '100', 'nsldap, SHA-1(Base64), Netscape LDAP SHA': '101', 'sha1($pass.$salt)': '110', 'nsl\
daps, SSHA-1(Base64), Netscape LDAP SSHA': '111', 'Oracle 11g': '112', 'Oracle 11g, SHA-1(Oracle)': '112', 'sha1($s\
alt.$pass)': '120', 'sha1(strtolower($username).$pass),  SMF >= v1.1': '121', 'OSX v10.4, v10.5, v10.6': '122', 's\
ha1(unicode($pass).$salt)': '130', 'MSSQL(2000)': '131', 'MSSQL(2005)': '132', 'sha1($salt.unicode($pass))': '140',\
 'EPiServer 6.x < v4': '141', 'HMAC-SHA1 (key = $pass)': '150', 'HMAC-SHA1 (key = $salt)': '160', 'sha1(LinkedIn)':\
 '190', 'MySQL': '200', 'MySQL4.1/MySQL5': '300', 'phpass, MD5(Wordpress), MD5(phpBB3)': '400', 'md5crypt, MD5(Unix\
), FreeBSD MD5, Cisco-IOS MD5': '500', 'SHA-1(Django)': '800', 'MD4': '900', 'md4($pass.$salt)': '910', 'NTLM': '10\
00', 'Domain Cached Credentials, mscash': '1100', 'SHA256': '1400', 'sha256($pass.$salt)': '1410', 'sha256($salt.$p\
ass)': '1420', 'sha256(unicode($pass).$salt)': '1430', 'sha256($salt.unicode($pass))': '1440', 'EPiServer 6.x > v4'\
: '1441', 'HMAC-SHA256 (key = $pass)': '1450', 'HMAC-SHA256 (key = $salt)': '1460', 'descrypt, DES(Unix), Tradition\
al DES': '1500', 'md5apr1, MD5(APR), Apache MD5': '1600', 'SHA512': '1700', 'sha512($pass.$salt)': '1710', 'SSHA-51\
2(Base64), LDAP {SSHA512}': '1711', 'sha512($salt.$pass)': '1720', 'OSX v10.7': '1722', 'sha512(unicode($pass).$sal\
t)': '1730', 'MSSQL(2012)': '1731', 'sha512($salt.unicode($pass))': '1740', 'HMAC-SHA512 (key = $pass)': '1750', 'H\
MAC-SHA512 (key = $salt)': '1760', 'sha512crypt, SHA512(Unix)': '1800', 'Domain Cached Credentials2, mscash2': '210\
0', 'Cisco-PIX MD5': '2400', 'WPA/WPA2': '2500', 'Double MD5': '2600', 'md5(md5($pass))': '2600', 'vBulletin < v3.8\
.5': '2611', 'vBulletin > v3.8.5': '2711', 'IPB2+, MyBB1.2+': '2811', 'LM': '3000', 'Oracle 7-10g, DES(Oracle)': '3\
100', 'bcrypt, Blowfish(OpenBSD)': '3200', 'MD5(Sun)': '3300', 'md5(md5(md5($pass)))': '3500', 'md5(md5($salt).$pas\
s)': '3610', 'md5($salt.md5($pass))': '3710', 'md5($pass.md5($salt))': '3720', 'WebEdition CMS': '3721', 'md5($salt\
.$pass.$salt)': '3810', 'md5(md5($pass).md5($salt))': '3910', 'md5($salt.md5($salt.$pass))': '4010', 'md5($salt.md5\
($pass.$salt))': '4110', 'md5($username.0.$pass)': '4210', 'md5(strtoupper(md5($pass)))': '4300', 'md5(sha1($pass))\
': '4400', 'sha1(sha1($pass))': '4500', 'sha1(sha1(sha1($pass)))': '4600', 'sha1(md5($pass))': '4700', 'MD5(Chap)':\
 '4800', 'SHA-3(Keccak)': '5000', 'Half MD5': '5100', 'Password Safe SHA-256': '5200', 'IKE-PSK MD5': '5300', 'IKE-\
PSK SHA1': '5400', 'NetNTLMv1-VANILLA / NetNTLMv1+ESS': '5500', 'NetNTLMv2': '5600', 'Cisco-IOS SHA256': '5700', 'S\
amsung Android Password/PIN': '5800', 'RipeMD160': '6000', 'Whirlpool': '6100', 'TrueCrypt 5.0+ PBKDF2-HMAC-RipeMD1\
60': '621Y', 'TrueCrypt 5.0+ PBKDF2-HMAC-SHA512': '622Y', 'TrueCrypt 5.0+ PBKDF2-HMAC-Whirlpool': '623Y', 'TrueCryp\
t 5.0+ PBKDF2-HMAC-RipeMD160 boot-mode': '624Y', 'TrueCrypt 5.0+': '62XY', 'AIX {smd5}': '6300', 'AIX {ssha256}': '\
6400', 'AIX {ssha512}': '6500', '1Password': '6600', 'AIX {ssha1}': '6700', 'Lastpass': '6800', 'GOST R 34.11-94':\
'6900', 'Fortigate (FortiOS)': '7000', 'OSX v10.8': '7100', 'GRUB 2': '7200', 'IPMI2 RAKP HMAC-SHA1': '7300', 'sha2\
56crypt, SHA256(Unix)': '7400'}

#Check whether a string consists of only hexadecimal characters.
def isHex(singleString):
    for c in singleString:
        if not c in string.hexdigits: return False
    return True

#Check whether a string consists of hexadecimal characters or '.' or '/'
def isAlphaDotSlash(singleString):
    for c in singleString:
        if not c in string.ascii_letters and not c in string.digits and not c in '.' and not c in '/': return False
    return True

#Identifies a single hash string based on attributes such as character length, character type (hex, alphanum, etc.), and specific substring identifiers.
#These conditional statements are ordered specifically to address efficiency when dealing with large inputs
def identifyHash(singleHash):
    if len(singleHash) == 32 and isHex(singleHash):
        hashDict[singleHash] = ['MD5', 'NTLM', 'MD4', 'LM', 'RAdmin v2.x', 'Haval-128', 'MD2', 'RipeMD-128', 'Tiger-128', 'Snefru-128', 'MD5(HMAC)', 'MD4(HMAC)', 'Haval-128(HMAC)', 'RipeMD-128(HMAC)', 'Tiger-128(HMAC)', \
        'Snefru-128(HMAC)', 'MD2(HMAC)', 'MD5(ZipMonster)', 'MD5(HMAC(Wordpress))', 'Skein-256(128)', 'Skein-512(128)', 'md5($pass.$salt)', 'md5($pass.$salt.$pass)', 'md5($pass.md5($pass))', 'md5($salt.$pass)', 'md5($salt.$pass.$salt)', \
        'md5($salt.$pass.$username)', 'md5($salt.\'-\'.md5($pass))', 'md5($salt.md5($pass))', 'md5($salt.md5($pass).$salt)', 'md5($salt.MD5($pass).$username)', 'md5($salt.md5($pass.$salt))', 'md5($salt.md5($salt.$pass))', 'md5($salt.md5(md5($pass).$salt))', \
        'md5($username.0.$pass)', 'md5($username.LF.$pass)', 'md5($username.md5($pass).$salt)', 'md5(1.$pass.$salt)', 'md5(3 x strtoupper(md5($pass)))', 'md5(md5($pass)), Double MD5', 'md5(md5($pass).$pass)', 'md5(md5($pass).$salt), vBulletin < v3.8.5', 'md4($salt.$pass)', 'md4($pass.$salt)' \
        'md5(md5($pass).md5($pass))', 'md5(md5($pass).md5($salt))', 'md5(md5($salt).$pass)', 'md5(md5($salt).md5($pass))', 'md5(md5($username.$pass).$salt)', 'md5(md5(base64_encode($pass)))', 'md5(md5(md5($pass)))', 'md5(md5(md5(md5($pass))))', \
        'md5(md5(md5(md5(md5($pass)))))', 'md5(sha1($pass))', 'md5(sha1(base64_encode($pass)))', 'md5(sha1(md5($pass)))', 'md5(sha1(md5($pass)).sha1($pass))', 'md5(sha1(md5(sha1($pass))))', 'md5(strrev($pass))', 'md5(strrev(md5($pass)))', \
        'md5(strtoupper(md5($pass)))', 'md5(strtoupper(md5(strtoupper(md5(strtoupper(md5($pass)))))))', 'strrev(md5($pass))', 'strrev(md5(strrev(md5($pass))))', '6 x md5($pass)', '7 x md5($pass)', '8 x md5($pass)', '9 x md5($pass)', '10 x md5($pass)', '11 x md5($pass)', '12 x md5($pass)']
    elif len(singleHash) > 32 and singleHash[32] == ':' and singleHash.count(':') == 1:
        hashDict[singleHash] = ['md5($salt.$pass.$salt)', 'md5($salt.md5($pass))', 'md5($salt.md5($pass.$salt))', 'md5($salt.md5($salt.$pass))', 'md5($username.0.$pass)', 'md5(md5($pass).md5($salt))', 'md5(md5($salt).$pass)', 'HMAC-MD5 (key = $pass)', 'HMAC-MD5 (key = $salt)', 'md5($pass.md5($salt))', \
        'WebEdition CMS', 'IPB2+, MyBB1.2+', 'md5(unicode($pass).$salt)', 'Domain Cached Credentials2, mscash2', 'md5($salt.unicode($pass))', 'vBulletin > v3.8.5', 'DCC2', 'md5(md5($pass).$salt), vBulletin < v3.8.5']
    elif len(singleHash) == 40:
        hashDict[singleHash] = ['SHA1', 'Tiger-160', 'Haval-160', 'RipeMD160', 'HAS-160', 'SHA-1(HMAC)', 'Tiger-160(HMAC)', 'Haval-160(HMAC)', 'RipeMD-160(HMAC)', 'Skein-256(160)', 'Skein-512(160)', 'sha1(LinkedIn)', 'SAPG', 'SHA-1(MaNGOS)', 'SHA-1(MaNGOS2)', \
        'sha1($salt.$pass.$salt)', 'sha1(md5($pass.$salt))', 'sha1(md5($pass).$userdate.$salt)', 'sha1($pass.$username.$salt)', 'sha1(md5($pass).$pass)', 'sha1(md5(sha1($pass)))', 'xsha1(strtolower($pass))', 'sha1($pass.$salt)', 'sha1($salt.$pass)', \
        'sha1($salt.$username.$pass.$salt)', 'sha1($salt.md5($pass))', 'sha1($salt.md5($pass).$salt)', 'sha1($salt.sha1($pass))', 'sha1($salt.sha1($salt.sha1($pass)))', 'sha1($username.$pass)', 'sha1($username.$pass.$salt)', 'sha1(md5($pass))', \
        'sha1(md5($pass).$salt)', 'sha1(md5(sha1(md5($pass))))', 'sha1(sha1($pass))', 'sha1(sha1($pass).$salt)', 'sha1(sha1($pass).substr($pass,0,3))', 'sha1(sha1($salt.$pass))', 'sha1(sha1(sha1($pass)))', 'sha1(strtolower($username).$pass)']
    elif len(singleHash) > 40 and singleHash[40] == ':' and singleHash.count(':') == 1:
        hashDict[singleHash] = ['sha1($pass.$salt)', 'HMAC-SHA1 (key = $pass)', 'HMAC-SHA1 (key = $salt)', 'sha1(unicode($pass).$salt)', 'sha1($salt.$pass)', 'sha1($salt.unicode($pass))', 'Samsung Android Password/PIN', 'sha1($salt.$pass.$salt)', 'sha1(md5($pass.$salt))', 'sha1(md5($pass).$userdate.$salt)', 'sha1($pass.$username.$salt)']
    elif len(singleHash) == 64 and isHex(singleHash):
        hashDict[singleHash] = ['Keccak-256', 'sha256(md5($pass).$pass))', 'Skein-256', 'Skein-512(256)', 'Ventrilo', 'WPA-PSK PMK', 'GOST R 34.11-94', 'Haval-256', 'RipeMD-256', 'SHA256', 'sha256(md5($pass))', 'sha256(sha1($pass))', 'Snefru-256', 'HMAC-SHA256 (key = $salt)', 'SHA-3(Keccak)']
    elif len(singleHash) > 64 and singleHash[64] == ':' and singleHash.count(':') == 1:
        hashDict[singleHash] = ['sha256(md5($pass.$salt))', 'sha256(md5($salt.$pass))', 'SHA-256(RuneScape)', 'sha256(sha256($pass).$salt)', 'Haval-256(HMAC)', 'RipeMD-256(HMAC)', 'sha256($pass.$salt)', 'sha256($salt.$pass)', 'SHA-256(HMAC)', 'Snefru-256(HMAC)', 'HMAC-SHA256 (key = $pass)', 'sha256(unicode($pass).$salt)', 'sha256($salt.unicode($pass))']
    elif singleHash.startswith('sha1$'):
        hashDict[singleHash] = ['SHA-1(Django)']
    elif singleHash.startswith('$H$'):
        hashDict[singleHash] = ['phpass, MD5(Wordpress), MD5(phpBB3)']
    elif singleHash.startswith('$P$'):
        hashDict[singleHash] = ['phpass, MD5(Wordpress), MD5(phpBB3)']
    elif singleHash.startswith('$1$'):
        hashDict[singleHash] = ['md5crypt, MD5(Unix), FreeBSD MD5, Cisco-IOS MD5']
    elif singleHash.startswith('$apr1$'):
        hashDict[singleHash] = ['md5apr1, MD5(APR), Apache MD5']
    elif singleHash.startswith('sha256$'):
        hashDict[singleHash] = ['SHA-256(Django)']
    elif singleHash.startswith('$SHA$'):
        hashDict[singleHash] = ['SHA-256(AuthMe)']
    elif singleHash.startswith('sha256$'):
        hashDict[singleHash] = ['SHA-256(Django)']
    elif singleHash.startswith('sha384$'):
        hashDict[singleHash] = ['SHA-384(Django)']
    elif singleHash.startswith('$SHA$'):
        hashDict[singleHash] = ['SHA-256(AuthMe)']
    elif singleHash.startswith('$2$') or singleHash.startswith('$2a$') or singleHash.startswith('$2y'):
        hashDict[singleHash] = ['bcrypt, Blowfish(OpenBSD)']
    elif singleHash.startswith('$5$'):
        hashDict[singleHash] = ['sha256crypt, SHA256(Unix)']
    elif singleHash.startswith('$6$'):
        hashDict[singleHash] = ['sha512crypt, SHA512(Unix)']
    elif singleHash.startswith('$S$'):
        hashDict[singleHash] = ['SHA-512(Drupal)']
    elif singleHash.startswith('{SHA}'):
        hashDict[singleHash] = ['nsldap, SHA-1(Base64), Netscape LDAP SHA']
    elif singleHash.startswith('{SSHA}'):
        hashDict[singleHash] = ['nsldaps, SSHA-1(Base64), Netscape LDAP SSHA']
    elif singleHash.startswith('{smd5}'):
        hashDict[singleHash] = ['AIX {smd5}']
    elif singleHash.startswith('{ssha1}'):
        hashDict[singleHash] = ['AIX {ssha1}']
    elif singleHash.startswith('$md5$'):
        hashDict[singleHash] = ['MD5(Sun)']
    elif singleHash.startswith('$episerver$*0*'):
        hashDict[singleHash] = ['EPiServer 6.x < v4']
    elif singleHash.startswith('$episerver$*1*'):
        hashDict[singleHash] = ['EPiServer 6.x > v4']
    elif singleHash.startswith('{ssha256}'):
        hashDict[singleHash] = ['AIX {ssha256}']
    elif singleHash.startswith('{SSHA512}'):
        hashDict[singleHash] = ['SSHA-512(Base64), LDAP {SSHA512}']
    elif singleHash.startswith('{ssha512}'):
        hashDict[singleHash] = ['AIX {ssha512}']
    elif singleHash.startswith('$ml$'):
        hashDict[singleHash] = ['OSX v10.8']
    elif singleHash.startswith('grub'):
        hashDict[singleHash] = ['GRUB 2']
    elif singleHash.startswith('sha256$'):
        hashDict[singleHash] = ['SHA-256(Django)']
    elif singleHash.startswith('sha384$'):
        hashDict[singleHash] = ['SHA-384(Django)']
    elif singleHash.startswith('0x'):
        if len(singleHash) == 34:
            hashDict[singleHash] = ['Lineage II C4']
        elif len(singleHash) < 60:
            hashDict[singleHash] = ['MSSQL(2005)']
        elif len(singleHash) < 100:
            hashDict[singleHash] = ['MSSQL(2000)']
        else:
            hashDict[singleHash] = ['MSSQL(2012)']
    elif singleHash.startswith('S:'):
        hashDict[singleHash] = ['Oracle 11g']
    elif len(singleHash) > 41 and singleHash.count(':') == 1 and singleHash[-41] == ':' and isHex(singleHash[-40:]):
        hashDict[singleHash] = ['sha1(strtolower($username).$pass),  SMF >= v1.1']
    elif singleHash.count(':') > 1:
        if singleHash.count(':') == 5:
            hashDict[singleHash] = ['NetNTLMv2', 'NetNTLMv1-VANILLA / NetNTLMv1+ESS']
        elif singleHash.count(':') == 2 and '@' not in singleHash:
            hashDict[singleHash] = ['MD5(Chap)']
        elif singleHash.count(':') == 3 or singleHash.count(':') == 6:
            hashDict[singleHash] = ['Domain Cached Credentials, mscash']
            try:
                hashDict[singleHash.split(':')[3]] = 'NTLM'
                if not singleHash.split(':')[2] == 'aad3b435b51404eeaad3b435b51404ee' and not singleHash.split(':')[2] == 'aad3b435b51404eeaad3b435b51404ee'.upper():
                    hashDict[singleHash.split(':')[2]] = 'LM'
            except Exception as e:
                pass
        elif singleHash.count(':') == 2 and '@' in singleHash:
            hashDict[singleHash] = ['Lastpass']
    elif len(singleHash) == 4:
        hashDict[singleHash] = ['CRC-16', 'CRC-16-CCITT', 'FCS-16']
    elif len(singleHash) == 8:
        hashDict[singleHash] = ['CRC-32', 'CRC-32B', 'FCS-32', 'ELF-32', 'Fletcher-32', 'FNV-32', 'Adler-32', 'GHash-32-3', 'GHash-32-5']
    elif len(singleHash) == 13:
        if singleHash.startswith('+'):
            hashDict[singleHash] = ['Blowfish(Eggdrop)']
        else:
            hashDict[singleHash] = ['descrypt, DES(Unix), Traditional DES']
    elif len(singleHash) == 16:
        if isHex(singleHash):
            hashDict[singleHash] = ['MySQL, MySQL323', 'Oracle 7-10g, DES(Oracle)', 'CRC-64', 'SAPB', 'substr(md5($pass),0,16)', 'substr(md5($pass),16,16)', 'substr(md5($pass),8,16)']
        else:
            hashDict[singleHash] = ['Cisco-PIX MD5']
    elif len(singleHash) > 16 and singleHash[-17] == ':' and singleHash.count(':') == 1:
        hashDict[singleHash] = ['DES(Oracle)', 'Oracle 10g']
    elif len(singleHash) == 20:
        hashDict[singleHash] = ['substr(md5($pass),12,20)']
    elif len(singleHash) == 24 and isHex(singleHash):
        hashDict[singleHash] = ['CRC-96(ZIP)']
    elif len(singleHash) == 35:
        hashDict[singleHash] = ['osCommerce, xt:Commerce']
    elif len(singleHash) > 40 and singleHash[40] == ':' and singleHash.count(':') == 1:
        hashDict[singleHash] = ['sha1($salt.$pass.$salt)', 'sha1(md5($pass.$salt))']
    elif len(singleHash) > 40 and singleHash.count('-') == 2 and singleHash.count(':') == 2:
        hashDict[singleHash] = ['sha1(md5($pass).$userdate.$salt)']
    elif len(singleHash) > 40 and singleHash.count(':') == 2 and len(singleHash.split(':')[1]) == 40 :
        hashDict[singleHash] = ['sha1($pass.$username.$salt)']
    elif len(singleHash) == 41 and singleHash.startswith('*') and isHex(singleHash[1:40]):
        hashDict[singleHash] = ['MySQL4.1/MySQL5']
    elif len(singleHash) == 43:
        hashDict[singleHash] = ['Cisco-IOS SHA256']
    elif len(singleHash) == 47:
        hashDict[singleHash] = ['Fortigate (FortiOS)']
    elif len(singleHash) == 48 and isHex(singleHash):
        hashDict[singleHash] = ['Oracle 11g, SHA-1(Oracle)', 'Haval-192', 'Haval-192(HMAC)' 'Tiger-192', 'Tiger-192(HMAC)', 'OSX v10.4, v10.5, v10.6']
    elif len(singleHash) == 51 and isHex(singleHash):
        hashDict[singleHash] = ['MD5(Palshop)', 'Palshop']
    elif len(singleHash) == 56 and isHex(singleHash):
        hashDict[singleHash] = ['SHA-224', 'Haval-224', 'SHA-224(HMAC)', 'Haval-224(HMAC)', 'Keccak-224', 'Skein-256(224)', 'Skein-512(224)']
    elif len(singleHash) == 65:
        hashDict[singleHash] = ['Joomla']
    elif len(singleHash) > 64 and singleHash[64] == ':':
        hashDict[singleHash] = ['SHA-256(PasswordSafe)', 'sha256(md5($salt.$pass))', 'sha256(md5($pass.$salt))', 'SHA-256(HMAC)', 'SHA-256(RuneScape)', 'sha256($salt.$pass)', 'sha256($pass.$salt)', 'Haval-256(HMAC)', 'RipeMD-256(HMAC)', 'Snefru-256(HMAC)', 'sha256(sha256($pass).$salt)']
    elif len(singleHash) == 80 and isHex(singleHash):
        hashDict[singleHash] = ['RipeMD-320', 'RipeMD-320(HMAC)']
    elif len(singleHash) == 96 and isHex(singleHash):
        hashDict[singleHash] = ['SHA-384', 'Keccak-384', 'SHA-384(HMAC)', 'sha384($salt.$pass)', 'sha384($pass.$salt)', 'Skein-512(384)', 'Skein-1024(384)']
    elif len(singleHash) == 128 and isHex(singleHash):
        hashDict[singleHash] = ['Keccak-512', 'Skein-1024(512)',  'Skein-512', 'SHA512', 'sha512($pass.$salt)', 'sha512($salt.$pass)', 'SHA-512(HMAC)', 'Whirlpool', 'Whirlpool(HMAC)', 'sha512(unicode($pass).$salt)', 'sha512($salt.unicode($pass))', 'HMAC-SHA512 (key = $pass)']
    elif len(singleHash) > 128 and singleHash[128] == ':':
        hashDict[singleHash] = ['HMAC-SHA512 (key = $salt)']
    elif len(singleHash) == 130 and isHex(singleHash):
        hashDict[singleHash] = ['IPMI2 RAKP HMAC-SHA1']
    elif len(singleHash) == 136 and isHex(singleHash):
        hashDict[singleHash] = ['OSX v10.7']
    elif len(singleHash) == 177:
        hashDict[singleHash] = ['Whirlpool(Double)']
    elif len(singleHash) == 256 and isHex(singleHash):
        hashDict[singleHash] = ['Skein-1024']
    else:
        hashDict[singleHash] = []

if args.singleHash:
    """
    Single Hash Identification: HashTag.py -sh hash
    Prints to screen all possible hash types and their corresponding hashcat mode if one exists.
    Note: When identifying a single hash on *nix operating systems remember to use single quotes to prevent interpolation. (e.g. python HashTag.py -sh '$1$abc$12345')
    """
    identifyHash(args.singleHash)
    if len(hashDict[args.singleHash]):
        print '\nHash: {0}\n'.format(args.singleHash)
        for value in hashDict[args.singleHash]:
            hcFound = False
            for k, v in hashcatDict.iteritems():
                if value == k:
                    print '[*] {0} - Hashcat Mode {1}'.format(value, v)
                    hcFound = True
                    break
            if hcFound == False:
                print '[*] {0}'.format(value)       
    else:
        print '\nHash not found: {0}'.format(args.singleHash)
elif args.file:
    """
    File Parsing and Hash Identification: HashTag.py -f file.txt [-o output_filename] [-hc] [-n]
    Parses a single file for possible password hashes and attempts to identify each one.  Outputs to one or multiple files depending on -hc argument.
    """
    inputFile = args.file
    hashCount = 0
    foundModes = list()

    while not os.path.isfile(inputFile):
        inputFile = raw_input("\nFile \'{0}\' not Found!\n\nHash File Path: ".format(str(inputFile)))
    openInputFile = open(inputFile, 'r')
    
    if not os.path.exists('HashTag'):
        os.mkdir('HashTag')
    if args.output: 
        while os.path.isfile(args.output) or os.path.isfile(args.output + '.txt'):
            args.output = raw_input("\nOutput file already exists!\n\nOutput Filename: ")
        outputFile = open(args.output, 'w')
    else:
        outputFile = open(os.path.join('HashTag', 'HashTag_Output_File.txt'), 'w')

    for line in openInputFile.readlines():
        identifyHash(line.strip())
    
    if hashDict:
        for k, v in hashDict.iteritems():
            for mode, num in hashcatDict.iteritems():
                if mode in v:
                    hashcatMode = num
                    foundModes.append(num)
                else:
                    hashcatMode = ''
                    
            if v:
                hashCount += 1
                foundModes.sort(key=int)
                outputFile.write('Hash: {0}\nChar Length: {1}\nHashcat Modes: {2}\nHash Types: {3}\n\n'.format(k, len(k), foundModes, v))

                if args.hashcatOutput and foundModes:
                    for mode in foundModes:
                        with open(os.path.join('HashTag', mode), "a") as outputTypeFile:
                            outputTypeFile.write(k + '\n')
                            outputTypeFile.close()
                foundModes = []
            elif k and args.notFound:
                outputFile.write('Hash: {0}\nChar Length: {1}\nHashcat Modes: {2}\nHash Types: {3}\n\n'.format(k, len(k), hashcatMode, 'NONE FOUND'))

        print '\nFile Mimetype: {0}\nHashes Found: {1}\nFile successfully written: {2}'.format(mimetypes.guess_type(inputFile)[0], hashCount, outputFile.name)

        openInputFile.close()
        outputFile.close()
    else:
        print '\nNo hashes parsed from file {0}'.format(inputFile)
elif args.directory:
    """
    File Parsing and Hash Identification while traversing directories and subdirectories: HashTag.py -d test_dir/hash_files/ [-o output_filename] [-hc]
    Traverses user specified directory and all subdirectories.  Identifies each file based on type or extension and attempts to parse each file for possible password hashes.
    Potential password protected files are separated by filetype and copied using the shutil module to new folders. Outputs to one or multiple files depending on -hc argument.
    """
    inputDir = args.directory
    while not os.path.isdir(inputDir):
        inputDir = raw_input("\nDirectory \'{0}\' not Found!\n\nHash Files Directory: ".format(str(inputDir)))

    if not os.path.exists('HashTag'):
        os.mkdir('HashTag')
    if args.output:
        while os.path.isfile(args.output) or os.path.isfile(args.output + '.txt'):
            args.output = raw_input("\nOutput file already exists!\n\nOutput Filename: ")
        outputFile = open(args.output, 'w')
    else:
        outputFile = open(os.path.join('HashTag', 'HashTag_Hash_File.txt'), 'w')

    validFiles = list()
    validHashes = list()
    invalidFiles = list()
    nonTextFiles = ['.1password', '.7z', '.bdb', '.dd', '.hccap', '.ikemd5', '.ikesha1', '.kdbx', '.odt', '.pdf', '.plist', '.psafe', '.sig', '.sign', '.tc', '.torrent', '.zip', '.xz']
    nonTextFileCount = 0

    for root, dirnames, filenames in os.walk(inputDir):
        for filename in filenames:
            if mimetypes.guess_type(filename)[0] == 'text/plain' or '.hash' in filename:
                foundHashFile = (os.path.join(root, filename))
                validFiles.append(foundHashFile)
            elif any(nonTextFile in filename for nonTextFile in nonTextFiles):
                for nonTextFile in nonTextFiles:
                    if nonTextFile in filename:
                        newDir = os.path.join('HashTag', nonTextFile.replace('.', ''))
                        if not os.path.exists(newDir):
                            os.makedirs(newDir)
                        shutil.copy2(os.path.join(root, filename), os.path.join(newDir, filename))
            else:
                invalidFiles.append((os.path.join(root, filename)))

    if validFiles:
        for hashFile in validFiles:
            openHashFile = open(hashFile)
            hashLines = [line.strip() for line in openHashFile]
            for singleHash in hashLines:
                if len(line) > 3 and len(line) <= 300:
                    validHashes.append(singleHash)
            openHashFile.close()
    else:
        print 'No valid file formats found.'

    if validHashes:
        for singleHash in validHashes:
            identifyHash(singleHash)
            #Write all parsed hashes to output file. Comment out for less overhead.
            outputFile.write(singleHash + '\n')
        outputFile.close()

    validHashCount = len(validHashes)
    validFileCount = len(validFiles) + nonTextFileCount
    invalidFileCount = len(invalidFiles)

    print '\nTotal Hashes Found: {0}'.format(validHashCount)
    print 'Valid file types: {0}'.format(validFileCount)
    print 'Invalid file types: {0}'.format(invalidFileCount)

    openInvalidFiles = open(os.path.join('HashTag','HashTag_Invalid_Files' + '.txt'), 'w')
    for invalidFile in invalidFiles:
        openInvalidFiles.write(invalidFile + '\n')

    print '\nNow identifying {0} hashes from {1} files...'.format(validHashCount, validFileCount)

    notifyCount = 0
    tenPercentCount = (validHashCount / 10)

    if args.hashcatOutput:
        for key, valueList in hashDict.iteritems():
            if valueList:
                for value in valueList:
                    if value in hashcatDict.iterkeys():
                        with open(os.path.join('HashTag',value) + '_{0}.txt'.format(hashcatDict[value]), "a") as f:
                            f.write(key + '\n')
                    else:
                        with open(os.path.join('HashTag',value) + '.txt', "a") as f:
                            f.write(key + '\n')
            else:
                with open(os.path.join('HashTag','HashTag_Invalid_Hashes') + '.txt', "a") as g:
                        g.write(key + '\n')
            notifyCount += 1
            if (notifyCount % tenPercentCount) == 0:
                print '{0}/{1} hashes have been identified and written.'.format(notifyCount,validHashCount)
    else:
        for key, valueList in hashDict.iteritems():
            if valueList:
                for value in valueList:
                    with open(os.path.join('HashTag',value) + '.txt', "a") as f:
                        f.write(key + '\n')
            else:
                with open(os.path.join('HashTag','HashTag_Invalid_Hashes') + '.txt', "a") as g:
                    g.write(key + '\n')
            notifyCount += 1
            if (notifyCount % tenPercentCount) == 0:
                print '{0}/{1} hashes have been identified and written.'.format(notifyCount,validHashCount)

    print '\n{0} hashes have been identified and written to separate files based on hash type.\nA full list has been written to file {1}'.format(notifyCount, outputFile.name)

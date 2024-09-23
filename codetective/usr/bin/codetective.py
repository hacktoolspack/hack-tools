#!/usr/bin/env python2
# encoding: utf-8
__description__ = 'a tool to determine the crypto/encoding algorithm used according to traces of its representation'
__author__ = 'Francisco da Gama Tabanez Ribeiro'
__version__ = '0.8.1'
__date__ = '2014/09/07'
__license__ = 'GPL'

MIN_ENTROPY=3.3
MAX_FILE_WINDOW_SIZE=1000000 #recommended: 1000000
MAX_OVERLAP_WINDOW_SIZE=5000
MIN_AV=5
MAX_PREPROCESS_ERRORS=20
BAD_CHARS="\n\r-" # chars to be ignored by validators

# data types: bytes, numbers, text, hex, bytecodes
import re,sys,argparse,base64
from urlparse import urlparse
from encodings import aliases
import string, math
from collections import Counter
from datetime import datetime
import io, struct, os

########################################################################
class Finding:
	"""
	represents a potential finding
	"""

	#----------------------------------------------------------------------
	def __init__(self, findingType, payload, location=None, certainty=None, details=None):
		"""define a finding"""
		self.type = findingType
		self.payload = payload
		self.location=location[0]+location[1][0]
		self.size = location[1][1]-location[1][0]
		self.certainty = certainty
		self.details = details
		self.created_on = datetime.now()
	
	def getConfidence(self):		
		if self.certainty >= 80:
			return 'confident'
		elif self.certainty >= 60 and self.certainty < 80:
			return 'likely'
		else:
			return 'possible'	
		
	def setConfidence(self):
		pass
	
	
	confidence = property(getConfidence, setConfidence)	
	
	def __str__(self):
		return "%s  [%s]" % (self.details , self.getConfidence)
	
	def display(self):
		return "%s\t(%s:%s:%s[%d]:%s)" % (self.details, self.type , self.location, self.confidence, self.certainty, self.created_on)

# from http://rosettacode.org/wiki/Entropy#Python
def entropy(s):
	p, lns = Counter(s), float(len(s))
	return -sum( count/lns * math.log(count/lns, 2) for count in p.values())

#@TODO: avoid \b's in regexps
regFinder={}
regFinder['web-cookie']=re.compile(r";?([\w_:|\-\$\&\%\#\@]+?)=([^;\s\n]+)")
regFinder['mssql2000']=re.compile(r"\b(?:0x0100)?[a-fA-F\d]{88}")
regFinder['md5']=re.compile(r"[a-fA-F\d]{32}")
regFinder['URL']=re.compile(r"(?<![a-zA-Z0-9])[a-zA-Z0-9]+://[a-zA-Z0-9./]+\b") #[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{22}(?![a-zA-Z0-9./])
regFinder['md4']=re.compile(r"[a-fA-F\d]{32}")
regFinder['phone']=re.compile(r"[^\d]\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}[^\d]")
regFinder['credit']=re.compile(r"\b(?:\d[ -]*?){13,16}\b")
regFinder['mssql2005']=re.compile(r"\b(?:0x0100)?[a-fA-F\d]{48}\b")
regFinder['lm']=re.compile(r"(?<![a-fA-F0-9])[a-fA-F\d]{32}(?![a-fA-F0-9])")
regFinder['ntlm']=regFinder['lm']
regFinder['MySQL4+']=re.compile(r"\b(?:\*)?[a-fA-F\d]{40}\b")
regFinder['MySQL323']=re.compile(r"\b[a-fA-F\d]{16}\b")
regFinder['base64']=re.compile(r"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})$")
regFinder['SAM(*:ntlm)']=re.compile(r"^(\w+:\d+:)?:([a-fA-F\d]{32})(?![a-fA-F0-9])")
regFinder['SAM(lm:*)']=re.compile(r"^(\w+:\d+:)?[a-fA-F\d]{32}:\*")
regFinder['SAM(lm:ntlm)']=re.compile(r"^(\w+:\d+:)?[a-fA-F\d]{32}:[a-fA-F\d]{32}\b")
regFinder['RipeMD320']=re.compile(r"\b[a-fA-F\d]{80}\b")
regFinder['sha1']=re.compile(r"\b[a-fA-F\d]{40}\b")
regFinder['sha224']=re.compile(r"\b[a-fA-F\d]{56}\b")
regFinder['sha256']=re.compile(r"\b[a-fA-F\d]{64}\b")
regFinder['sha384']=re.compile(r"\b[a-fA-F\d]{96}\b")
regFinder['sha512']=re.compile(r"\b[a-fA-F\d]{128}\b")
regFinder['whirpool']=regFinder['sha512']
regFinder['CRC']=re.compile(r"0x[a-fA-F\d]{1,16}\b")
regFinder['des-salt-unix']=re.compile(r"(?<![a-zA-Z0-9./$])[a-zA-Z0-9./]{13}(?![a-zA-Z0-9./])")
regFinder['sha256-salt-django']=re.compile(r"^(?:sha256|sha1)\$[a-zA-Z\d./]+\$[a-zA-Z0-9./]{64}$")
regFinder['sha256-django']=re.compile(r"^(?:sha256|sha1)\$\$[a-zA-Z0-9./]{64}$")
regFinder['sha384-salt-django']=re.compile(r"^sha384\$[a-zA-Z\d.]+\$[a-zA-Z0-9./]{96}$")
regFinder['sha384-django']=re.compile(r"^sha384\$\$[a-zA-Z0-9./]{96}$")
regFinder['sha256-salt-unix']=re.compile(r"\$5\$[a-zA-Z0-9./]{8,16}\$[a-zA-Z0-9./]{43}(?![a-zA-Z0-9./])")
regFinder['sha512-salt-unix']=re.compile(r"\$6\$[a-zA-Z0-9./]{8,16}\$[a-zA-Z0-9./]{86}(?![a-zA-Z0-9./])")
regFinder['apr1-salt-unix']=re.compile(r"\$apr1\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{22}(?![a-zA-Z0-9./])")
regFinder['md5-salt-unix']=re.compile(r"(?<![a-zA-Z0-9.])[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{22}(?![a-zA-Z0-9./])")
regFinder['md5-wordpress']=re.compile(r"(?<![a-zA-Z0-9.])[a-zA-Z0-9./]{31}(?![a-zA-Z0-9.=/])")
regFinder['md5-phpBB3']=re.compile(r"(?<![a-zA-Z0-9.])[a-zA-Z0-9./]{31}(?![a-zA-Z0-9.=/])")
regFinder['md5-joomla2']=re.compile(r"(?<![a-zA-Z0-9.])([a-zA-Z0-9./]{32})(?::[a-zA-Z0-9./]{32})?(?![a-zA-Z0-9./])")
regFinder['md5-salt-joomla2']=regFinder['md5-joomla2']
regFinder['md5-joomla1']=re.compile(r"(?<![a-zA-Z0-9.])([a-zA-Z0-9./]{32})(?::[a-zA-Z0-9./]{16})?(?![a-zA-Z0-9./])")
regFinder['md5-salt-joomla1']=regFinder['md5-joomla1']
regFinder['blowfish-salt-unix']=re.compile(r"[a-zA-Z0-9./]{2}\$[a-zA-Z0-9./]{53}(?![a-zA-Z0-9./])")
regFinder['uuid']=re.compile(r"(?<![a-fA-F0-9])[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}(?![a-fA-F0-9])")

def regFind(regType, data):
	return regFinder[regType].finditer(data)

def get_type_of(subText, filters, baseLocation=0, analyze=False):
	results2=[]
					
	#@TODO: poorly tested... test against burp files, add 'set-cookie'...
	if ('web' in filters or 'crypto' in filters):
		known_cookies=['_Utm','APSESSION', 'sessionID','Web_session']
		for finding in regFind('web-cookie', subText): # cookie
			data, location = finding.group(), (baseLocation,finding.span())	
			if len(data) > 2:
				cookie_find=Finding('web-cookie', finding.groups(), location, 45, 'Web cookie name: %s\n\t\tvalue: %s' % finding.groups())
				if ( any(cookie for cookie in known_cookies if string.lower(cookie) in string.lower(finding.groups()[0])) and entropy(finding.groups()[1])>MIN_ENTROPY):
					cookie_find.certainty+=40
				
				results2.append(cookie_find)
			
	if(any(x for x in filters if x in ['web','unix','crypto','other'])):
		for finding in regFind('md5', subText):  # md4 or md5
			data,location = finding.group(), (baseLocation,finding.span())
			potential_hash=re.findall(r"[a-fA-F\d]{32}", data)[0]
#		if re.findall(r"(?<![a-fA-F0-9])[a-fA-F\d]{32}(?![a-fA-F0-9])", data): # md4 or md5
#			potential_hash=re.findall(r"(?<![a-fA-F0-9])([a-fA-F\d]{32})(?![a-fA-F0-9])", data)[0]

			md5_find=Finding('md5', potential_hash, location, 40, 'MD5 hash: %s' % potential_hash)
			md4_find=Finding('md4', potential_hash, location, 20, 'MD4 hash: %s' % potential_hash)
			if (entropy(potential_hash) > MIN_ENTROPY):
				md5_find.certainty+=40
				md4_find.certainty+=10
			else:
				md5_find.certainty-=30
				md4_find.certainty-=10				
			results2+=[md4_find,md5_find]
			
	if(any(x for x in filters if x in ['web','personal','other'])):
		for finding in regFind('URL', subText):  # URL
			data,location = finding.group(), (baseLocation,finding.span())			
			o = urlparse(data)
			if(o.scheme != '' and o.netloc != ''):
				url_find = Finding('URL', data, location, 70, "URL: %s\n\t%s" % (data,str(o)))
				if(urlparse(data).path != ''):
					url_find.certainty+=20
	
				results2.append(url_find)
			del(o)
	
			
	# from http://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script
	if(any(x for x in filters if x in ['web','personal','other'])):
	
		for finding in regFind('phone', subText): # phone numbers
			data, location = finding.group(), (baseLocation,finding.span())
	#		if re.findall(r"[^\d]\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}[^\d]", data) and 'personal' in filters: 
			potential_phone=re.findall(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", data)[0]
			phone_find=Finding('phone', potential_phone, location, 40, 'Phone number: %s' % potential_phone)		
			if('personal' in filters):
				if re.match(r"\+\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}[^\d]", data):
					phone_find.certainty+=15 
			results2.append(phone_find)
	
	# from http://www.regular-expressions.info/creditcard.html
	# http://www.paypalobjects.com/en_US/vhelp/paypalmanager_help/paypalmanager.htm#credit_card_numbers.htm
	if('personal' in filters):
		for finding in regFind('credit', subText):	
			data, location = finding.group(), (baseLocation,finding.span())
			credit_find=Finding('credit', None, location, 45, None)
			
			if(re.findall(r"4[0-9]{12}(?:[0-9]{3})?",data)): # Visa
				credit_find.payload = re.findall(r"(?:4[0-9]{12})(?:[0-9]{3})?", data)[0]
				credit_find.details='Credit card number: %s\n\tCredit card type: Visa' % credit_find.payload
			elif (re.findall(r"5[1-5][0-9]{14}",data)): # Mastercard
				credit_find.payload = re.findall(r"5[1-5][0-9]{14}", data)[0]
				credit_find.details='Credit card number: %s\n\tCredit card type: Mastercard' % credit_find.payload
			elif (re.findall(r"3[47][0-9]{13}",data)): # American Express
				credit_find.payload = re.findall(r"3[47][0-9]{13}", data)[0]
				credit_find.details='Credit card number: %s\n\tCredit card type: American Express' % credit_find.payload
			elif (re.findall(r"3(?:0[0-5]|[68][0-9])[0-9]{11}",data)): # Diners Club
				credit_find.payload = re.findall(r"3(?:0[0-5]|[68][0-9])[0-9]{11}", data)[0]			
				credit_find.details='Credit card number: %s\n\tCredit card type: Diners Club' % credit_find.payload
			elif (re.findall(r"6(?:011|5[0-9]{2})[0-9]{12}",data)): # Discover
				credit_find.payload = re.findall(r"6(?:011|5[0-9]{2})[0-9]{12}", data)[0] 
				credit_find.details='Credit card number: %s\n\tCredit card type: Discover' % credit_find.payload
			elif (re.findall(r"(?:2131|1800|35\d{3})\d{11}",data)): # JCB
				credit_find.payload = re.findall(r"(?:2131|1800|35\d{3})\d{11}", data)[0]
				credit_find.details='Credit card number: %s\n\tCredit card type: JCB' % credit_find.payload
			else:
				credit_find.payload = re.findall(r"\b(?:\d[ -]*?){13,16}\b", data)[0]
				credit_find.details='Credit card number: %s' % credit_find.payload 
				credit_find.certainty-=30
			results2.append(credit_find)
		
		
	if ('db' in filters or 'crypto' in filters):
		for finding in regFind('mssql2005', subText): # mssql 2005 hash
			data, location = finding.group(), (baseLocation,finding.span())	
			potential_hash = re.findall(r"(?:0x0100)?([a-fA-F\d]{8})([a-fA-F\d]{40})", data)[0]
			mssql2005_find=Finding('mssql2005', potential_hash, location, 55, 'Microsoft SQL Server 2005\n\t\theader: 0x0100\n\t\tsalt: %s\n\t\tmixed case hash (SHA1): %s' % potential_hash)
			if(re.match(r"\b0x0100[a-fA-F\d]{48}\b", data)):
				mssql2005_find.certainty+=40
			elif (re.match(r"\b[a-fA-F\d]{48}\b", data) and entropy(re.findall(r"\b[a-fA-F\d]{48}\b", data)[0])>MIN_ENTROPY):
				mssql2005_find.certainty+=20
			results2.append(mssql2005_find)
	
	if ('db' in filters or 'crypto' in filters):
		for finding in regFind('mssql2000', subText):		#mssql 2000 hash
			data, location = finding.group(), (baseLocation,finding.span())
			potential_hash = re.findall(r"(?:0x0100)?([a-fA-F\d]{8})([a-fA-F\d]{40})([a-fA-F\d]{40})", data)[0]
			mssql2000_find=Finding('mssql2000', potential_hash, location, 55, 'Microsoft SQL Server 2000\n\t\theader: 0x0100\n\t\tsalt: %s\n\t\tmixed case hash (SHA1): %s\n\t\tupper case hash (SHA1): %s' % potential_hash)

			if re.match(r"\b0x0100[a-fA-F\d]{88}\b", data):
				mssql2000_find.certainty+=40
			elif (re.match(r"\b[a-fA-F\d]{48}\b", data) and entropy(re.findall(r"\b[a-fA-F\d]{48}\b", data)[0])>MIN_ENTROPY):
				mssql2000_find.certainty+=20			
			results2.append(mssql2000_find)				

	if ('win' in filters or 'crypto' in filters):
			
		for finding in regFind('lm', subText): # lm or ntlm
			data, location = finding.group(), (baseLocation,finding.span())
			potential_hash=re.findall(r"(?<![a-fA-F0-9])([a-fA-F\d]{32})(?![a-fA-F0-9])", data)[0]
			lm_find=Finding('lm', potential_hash, location, 50, 'LM hash: %s' % potential_hash)
			ntlm_find=Finding('ntlm', potential_hash, location, 50, 'NTLM hash: %s' % potential_hash)					
			if(all(chr.isupper() or chr.isdigit() for chr in data)):
				if entropy(potential_hash)> MIN_ENTROPY:
					lm_find.certainty+=30
					ntlm_find.certainty+=30
				else:
					lm_find.certainty+=10
					ntlm_find.certainty+=10
			results2+=[lm_find,ntlm_find]	

	if ('db' in filters or 'crypto' in filters): # MySQL4+
		for finding in regFind('MySQL4+', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			potential_hash=re.findall(r"\b(?:\*)?([a-fA-F\d]{40})\b", data)[0]
			mysql4_find=Finding('MySQL4+', potential_hash,location, 50, 'MySQL v4 or later hash: %s' % potential_hash)		
			if(all(chr.isupper() or chr.isdigit() for chr in potential_hash) and data[0]=='*' and entropy(potential_hash)>MIN_ENTROPY):
				mysql4_find.certainty+=30
			results2.append(mysql4_find)
				
		
	if ('db' in filters or 'crypto' in filters): # MySQL323
		for finding in regFind('MySQL323', subText):
			data, location = finding.group(), (baseLocation,finding.span())			
			potential_hash=re.findall(r"\b([a-fA-F\d]{16})\b", data)[0]
			mysql3_find=Finding('MySQL323', potential_hash, location, 40, 'MySQL v3.23 or previous hash: %s' % potential_hash)				
			if(filters==['db'] and all(chr.isupper() or chr.isdigit() for chr in data) and entropy(potential_hash)>MIN_ENTROPY):
				mysql4_find.certainty+=30
			results2.append(mysql3_find)

	if 'other' in filters: # base64
		for finding in regFind('base64', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			base64_find=Finding('base64', data, location, 40, 'base64 decoded string: %s' % base64.b64decode(data))				
			if(data.endswith('=')):
				base64_find.certainty+=40
			results2.append(base64_find)
	
	if ('win' in filters or 'crypto' in filters): # SAM(*:NTLM)
		for finding in regFind('SAM(*:ntlm)', subText):
			potential_hash=re.findall(r"\*:([a-fA-F\d]{32})\b",data)[0]
			sam_ntlm_find=Finding('SAM(*:ntlm)', potential_hash, None, 40, 'hashes in SAM file - LM: not defined\tNTLM: %s' % potential_hash)				
			if(all(chr.isupper() or chr.isdigit() for chr in potential_hash) and entropy(potential_hash)>MIN_ENTROPY):
				sam_ntlm_find.certainty+=30
				if re.findall(r"^(\w+:\d+:)\*:([a-fA-F\d]{32})(?![a-fA-F0-9])", data): #@TODO: untested
					sam_ntlm_find.certainty+=15
			results2.append(sam_ntlm_find)
			
	if ('win' in filters or 'crypto' in filters): # SAM(LM:*)
		for finding in regFind('SAM(lm:*)', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			potential_hash=re.findall(r"([a-fA-F\d]{32}):\*",data)[0]
			sam_lm_find=Finding('SAM(lm:*)', potential_hash, location, 40, 'hashes in SAM file - LM: %s\tNTLM: not defined' % potential_hash)				
			
			if(all(chr.isupper() or chr.isdigit() for chr in potential_hash) and entropy(potential_hash)>MIN_ENTROPY):
				sam_lm_find.certainty+=30
			elif(re.match(r"^[\w+:]{4,6}", data) and entropy(potential_hash)>MIN_ENTROPY): #@TODO: untested
				sam_lm_find.certainty+=45
			results2.append(sam_lm_find)
				
	if ('win' in filters or 'crypto' in filters): # SAM(LM:NTLM)
		for finding in regFind('SAM(lm:ntlm)', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			lm,ntlm=re.findall(r"^(?:\w+:\d+:)?([a-fA-F\d]{32}):([a-fA-F\d]{32})\b",data)[0]
			sam_lm_ntlm_find=Finding('SAM(lm:ntlm)', (lm,ntlm), location, 50, 'hashes in SAM file - LM: %s\tNTLM: %s' % (lm,ntlm))				
		
			if(re.findall(r"^(\w+:\d+:)", data) and entropy(lm)>MIN_ENTROPY and entropy(ntlm)>MIN_ENTROPY):
				sam_lm_ntlm_find.certainty+=30
				if all(chr.isupper() or chr.isdigit() for chr in lm+ntlm):
					sam_lm_ntlm_find.certainty+=10
			results2.append(sam_lm_ntlm_find)
			
	if ('crypto' in filters or 'other' in filters): # RipeMD320
		for finding in regFind('RipeMD320', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			potential_hash=re.findall(r"\b([a-fA-F\d]{80})\b",data)[0]			
			results2.append(Finding('RipeMD320', potential_hash, location, 10, 'RipeMD320: %s' % potential_hash))
		
				
	if ('crypto' in filters or 'other' in filters): # SHA1
		for finding in regFind('sha1', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			potential_hash=re.findall(r"\b([a-fA-F\d]{40})\b",data)[0]
			sha1_find=Finding('sha1', potential_hash, location, 15, 'SHA1: %s' % potential_hash)
			
			if (entropy(potential_hash)>MIN_ENTROPY):
				sha1_find.certainty+=50
			
			results2.append(sha1_find)

	if ('crypto' in filters or 'other' in filters): # SHA224
		for finding in regFind('sha224', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			potential_hash=re.findall(r"\b([a-fA-F\d]{56})\b",data)[0]
			sha224_find=Finding('sha224', potential_hash, location, 15, 'SHA224: %s' % potential_hash)
			
			if (entropy(potential_hash)>MIN_ENTROPY):
				sha224_find.certainty+=50
				
			results2.append(sha224_find)
		
	if ('crypto' in filters or 'other' in filters): # SHA224
		for finding in regFind('sha256', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			potential_hash=re.findall(r"\b([a-fA-F\d]{64})\b",data)[0]
			sha256_find=Finding('sha256', potential_hash, location, 15, 'SHA256: %s' % potential_hash)
			
			if (entropy(potential_hash)>MIN_ENTROPY):
				sha256_find.certainty+=50
				
			results2.append(sha256_find)
			#		results['possible'].append('AES key [256 bit]')

	if ('crypto' in filters or 'other' in filters): # SHA384
		for finding in regFind('sha384', subText):
			data, location = finding.group(), (baseLocation,finding.span())		
			potential_hash=re.findall(r"\b([a-fA-F\d]{96})\b",data)[0]
			sha384_find=Finding('sha384', potential_hash, location, 15, 'SHA384: %s' % potential_hash)
		
			if (entropy(potential_hash)>MIN_ENTROPY):
				sha384_find.certainty+=50
			
			results2.append(sha384_find)


	if ('crypto' in filters or 'other' in filters): # SHA512 or Whirlpool
		for finding in regFind('sha512', subText):
			data, location = finding.group(), (baseLocation,finding.span())			
			potential_hash=re.findall(r"\b([a-fA-F\d]{128})\b",data)[0]
			sha512_find=Finding('sha512', potential_hash, location, 15, 'SHA512: %s' % potential_hash)
			whirlpool_find=Finding('whirlpool', potential_hash, location, 5, 'Whirlpool: %s' % potential_hash)	
			
			if (entropy(potential_hash)>MIN_ENTROPY):
				sha512_find.certainty+=50
				whirlpool_find.certainty+=15
				
			results2+=[sha512_find,whirlpool_find]
	

	if 'other' in filters: # CRC
		for finding in regFind('CRC', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			potential_crc=re.findall(r"0x([a-fA-F\d]{1,16})\b", data)[0]
			crc_find=Finding('CRC', potential_crc, location, 25, None)
			
			if len(data[2:]) == 1:
				crc_find.details='Cyclic redundancy check - CRC1 or CRC-4-ITU: %s' % potential_crc
			elif len(data[2:]) == 2:
				crc_find.details='Cyclic redundancy check - CRC-4-ITUCRC-5-ITU, CRC-5-EPC, CRC-5-USB, CRC-6-ITU, CRC-7, CRC-8-CCITT, CRC-8-Dallas/Maxim, CRC-8, CRC-8-SAE J1850, CRC-8-WCDMA: %s' % potential_crc
			elif len(data[2:]) == 3:
				crc_find.details='Cyclic redundancy check - CRC-10, CRC-11, CRC-12: %s' % potential_crc
			elif len(data[2:]) == 4:
				crc_find.details='Cyclic redundancy check - CRC-15-CAN, CRC-16-IBM, CRC-16-CCITT, CRC-16-T10-DIF, CRC-16-DNP, CRC-16-DECT: %s' % potential_crc
			elif len(data[2:]) == 6:
				crc_find.details='Cyclic redundancy check - CRC-24, CRC-24-Radix-64: %s' % potential_crc
			elif len(data[2:]) == 8:
				crc_find.details='Cyclic redundancy check - CRC-30, CRC-32, CRC-32C, CRC-32K, CRC-32Q: %s' % potential_crc
			elif len(data[2:]) == 10:
				crc_find.details='Cyclic redundancy check - CRC-40-GSM: %s' % potential_crc
			elif len(data[2:]) == 16:
				crc_find.details='Cycle redundancy check - CRC-64-ISO, CRC-64-ECMA-182: %s' % potential_crc
			else: 
				crc_find.details='invalid CRC? truncated data? %s' % potential_crc
				crc_find.certainty-=15
			crc_find.certainty-=10
			results2.append(crc_find)

	if ('crypto' in filters or 'unix' in filters): # DES-salt(UNIX)
		for finding in regFind('des-salt-unix', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			des_find = re.findall(r"(?:\w+:)?([a-zA-Z0-9./]{2})([a-zA-Z0-9./]{11})",data)[0]
			des_salt_find=Finding('des-salt-unix', des_find, location, 55, 'UNIX shadow file using salted DES - salt: %s\thash: %s' % des_find)
			if(filters == ['unix'] or re.match(r'(?:\w+:)[a-zA-Z0-9./]{13}(?::\d*){2}(?::.*?){2}:.*$', data)  and (entropy(re.findall(r"(?:\w+:)([a-zA-Z0-9./]{13})(?::\d*){2}(?::.*?){2}:.*$",data[0]))>MIN_ENTROPY)):
				des_salt_find.certainty+=25
			results2.append(des_salt_find)

	if ('crypto' in filters or 'web' in filters): # SHA256-salt(Django)
		for finding in regFind('sha256-salt-django', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			sha256_find = re.findall(r"^(?:sha256|sha1)\$([a-zA-Z\d.]+)\$([a-zA-Z0-9./]{64})$", data)[0]
			sha256_salt_django=Finding('sha256-salt-django', sha256_find, location, 65, 'Django shadow file using salted SHA256 - salt:%s\thash:%s' % sha256_find)
			if(all(chr.islower() or chr.isdigit() or chr == '$' for chr in data) and (entropy(re.findall(r"^(?:sha256|sha1)\$([a-zA-Z\d./]+\$[a-zA-Z0-9./]{64})$",data[0]))>MIN_ENTROPY)):
				sha256_salt_django.certainty+=20
			results2.append(sha256_salt_django)

	if ('crypto' in filters or 'web' in filters): # SHA256(Django)
		for finding in regFind('sha256-django', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			sha256_find = re.findall(r"^(?:sha256|sha1)\$\$([a-zA-Z0-9./]{64})$", data)[0]
			sha256_django=Finding('sha256-django', sha256_find, location, 65, 'Django shadow file using SHA256 - hash: %s' % sha256_find)
			if(all(chr.islower() or chr.isdigit() or chr == '$' for chr in data) and (entropy(re.findall(r"^(?:sha256|sha1)\$\$([a-zA-Z0-9./]{64})$",data[0]))>MIN_ENTROPY)):
				sha256_django.certainty+=20
			results2.append(sha256_django)

	if ('crypto' in filters or 'web' in filters): # SHA384-salt(Django)
		for finding in regFind('sha384-salt-django', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			sha384_find = re.findall(r"^sha384\$([a-zA-Z\d.]+)\$([a-zA-Z0-9./]{96})$", data)[0]
			sha384_salt_django=Finding('sha384-salt-django', sha384_find, location, 65, 'Django shadow file using salted SHA384 - salt: %s\thash: %s' % sha384_find)
			if(all(chr.islower() or chr.isdigit() or chr == '$' for chr in data) and (entropy(re.findall(r"^sha384\$([a-zA-Z\d.]+)\$([a-zA-Z0-9./]{96})$",data[0]))>MIN_ENTROPY)):
				sha384_salt_django.certainty+=20
			results2.append(sha384_salt_django)
			

	if ('crypto' in filters or 'web' in filters): # SHA384(Django)
		for finding in regFind('sha384-django', subText):
			data, location = finding.group(), (baseLocation,finding.span())	
			sha384_find = re.findall(r"^sha384\$\$([a-zA-Z0-9./]{96})$", data)[0]
			sha384_django=Finding('sha384-django', sha384_find, location, 65, 'Django shadow file using SHA384 - hash: %s' % sha384_find)
			if(all(chr.islower() or chr.isdigit() or chr == '$' for chr in data) and (entropy(re.findall(r"^sha384\$\$([a-zA-Z0-9./]{96})$",data[0]))>MIN_ENTROPY)):
				sha384_django.certainty+=20
			results2.append(sha384_django)

	if ('crypto' in filters or 'unix' in filters): # SHA256-salt(UNIX)
		for finding in regFind('sha256-salt-unix', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			sha256_find = re.findall(r"\$5\$([a-zA-Z0-9./]{8,16})\$([a-zA-Z0-9./]{43})", data)[0]
			sha256_salt_unix=Finding('sha256-salt-unix', sha256_find, location, 55, 'UNIX shadow file using salted SHA256 - salt: %s\thash: %s' % sha256_find)
			if (entropy(re.findall(r"\$5\$[a-zA-Z0-9./]{8,16}\$([a-zA-Z0-9./]{43})",data[0]))>MIN_ENTROPY):
				sha256_salt_unix.certainty+=25
			results2.append(sha256_salt_unix)
		
	if ('crypto' in filters or 'unix' in filters): # SHA512-salt(UNIX)
		for finding in regFind('sha512-salt-unix', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			sha512_find = re.findall(r"\$6\$([a-zA-Z0-9./]{8,16})\$([a-zA-Z0-9./]{86})", data)[0]
			sha512_salt_unix=Finding('sha512-salt-unix', sha512_find, location, 55, 'UNIX shadow file using salted SHA512 - salt: %s\thash: %s' % sha512_find)
			if (entropy(re.findall(r"\$6\$[a-zA-Z0-9./]{8,16}\$([a-zA-Z0-9./]{86})(?![a-zA-Z0-9./])",data[0]))>MIN_ENTROPY):
				sha512_salt_unix.certainty+=25
			results2.append(sha512_salt_unix)			
		
	if ('crypto' in filters or 'web' in filters): # APR1-salt(Apache)
		for finding in regFind('apr1-salt-unix', subText):
			apr1_find = re.findall(r"\$apr1\$([a-zA-Z0-9./]{8})\$([a-zA-Z0-9./]{22})", data)[0]
			data, location = finding.group(), (baseLocation,finding.span())		
			apr1_salt_unix=Finding('apr1-salt-unix', apr1_find, location, 45, 'Apache htpasswd file (MD5x2000)- salt: %s\thash: %s' % apr1_find)
			if (entropy(re.findall(r"\$apr1\$([a-zA-Z0-9./]{8})\$([a-zA-Z0-9./]{22})",data[0]))>MIN_ENTROPY):
				apr1_salt_unix.certainty+=35
			results2.append(apr1_salt_unix)

	if ('crypto' in filters or 'unix' in filters): # MD5-salt(UNIX)
		for finding in regFind('md5-salt-unix', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			md5_find = re.findall(r"([a-zA-Z0-9./]{8})\$([a-zA-Z0-9./]{22})", data)[0]
			md5_salt_unix=Finding('md5-salt-unix', md5_find, location, 45, 'UNIX shadow file using salted MD5 - salt: %s\thash: %s' % md5_find)
			if (entropy(re.findall(r"[a-zA-Z0-9./]{8}\$([a-zA-Z0-9./]{22})", data)[0])>MIN_ENTROPY):
				md5_salt_unix.certainty+=35
			results2.append(md5_salt_unix)

	if ('crypto' in filters or 'web' in filters):  # MD5(Wordpress)
		for finding in regFind('md5-wordpress', subText):
			data, location = finding.group(), (baseLocation,finding.span())		
			md5_find = re.findall("([a-zA-Z0-9./]{31})", data)[0]
			md5_wordpress=Finding('md5-wordpress', md5_find, location, 45, 'Wordpress MD5 - hash: %s' % md5_find)
			if re.match(r"\$P\$[a-zA-Z0-9./]{31}$", data) and entropy(re.findall(r"\$P\$([a-zA-Z0-9./]{31})$", data)[0])>MIN_ENTROPY:
				md5_wordpress.certainty+=40
			elif filters == ['web'] and data.startswith('$'):
				md5_wordpress.certainty+=20
			results2.append(md5_wordpress)


	if ('crypto' in filters or 'web' in filters):  # MD5(phpBB3)
		for finding in regFind('md5-phpBB3', subText):
			data, location = finding.group(), (baseLocation,finding.span())	
			md5_find = re.findall("[a-zA-Z0-9./]{31}", data)[0]
			md5_phpbb3=Finding('md5-phpBB3', md5_find, location, 45, 'phpBB3 MD5 - hash: %s' % md5_find)
			if re.match(r"\$H\$[a-zA-Z0-9./]{31}$", data) and entropy(re.findall(r"\$H\$([a-zA-Z0-9./]{31})$", data)[0]) > MIN_ENTROPY:
				md5_phpbb3.certainty+=40
			elif filters == ['web'] and data.startswith('$'):
				md5_phpbb3.certainty+=20
			results2.append(md5_phpbb3)
			
	
	#@TODO:untested	
	if ('crypto' in filters or 'web' in filters):  # MD5-salt(joomla2)
		for finding in regFind('md5-phpBB3', subText):
			data, location = finding.group(), (baseLocation,finding.span())	
			if(re.findall(r"(?<![a-zA-Z0-9.])([a-z0-9./]{32}):([a-zA-Z0-9./]{32})\b", data) and entropy(re.findall(r"(?<![a-zA-Z0-9.])([a-z0-9./]{32}):([a-zA-Z0-9./]{32})\b", data)[0])>MIN_ENTROPY):
				md5_find = re.findall(r"([a-z0-9./]{32}):([a-zA-Z0-9./]{32})", data)[0]	
				results2.append(Finding('md5-salt-joomla2', md5_find, location, 85, 'Joomla v2 salted MD5 - hash: %s\tsalt:%s' % md5_find))			
			elif(re.findall(r"(?<![a-zA-Z0-9.])([a-z0-9./]{32})\b", data)):
				md5_find = re.findall(r"([a-z0-9./]{32})", data)[0]
				results2.append(Finding('md5-joomla2', md5_find, location, 50, 'Joomla v2 MD5 - hash: %s' % md5_find))
#		else:
#			results['possible'].append('md5-salt-joomla2')

	if ('crypto' in filters or 'web' in filters):  # MD5-salt(joomla1)
		for finding in regFind('md5-joomla1', subText):
			data, location = finding.group(), (baseLocation,finding.span())		
			if(re.findall(r"(?<![a-zA-Z0-9.])([a-z0-9./]{32}):([a-zA-Z0-9./]{16}(?![a-zA-Z0-9./]))", data) and entropy(re.findall(r"(?<![a-zA-Z0-9.])([a-z0-9./]{32}):([a-zA-Z0-9./]{16}(?![a-zA-Z0-9./]))", data)[0])>MIN_ENTROPY):
				md5_find = re.findall(r"([a-z0-9./]{32}):([a-zA-Z0-9./]{16})", data)[0]
				results2.append(Finding('md5-salt-joomla1', md5_find, location, 85,'Joomla v1 salted MD5 - hash: %s\tsalt:%s' % md5_find))
			elif(re.findall(r"(?<![a-zA-Z0-9.])([a-z0-9./]{32})(?![a-zA-Z0-9./])", data)):
				md5_find = re.findall(r"([a-z0-9./]{32})", data)[0]
				results2.append(Finding('md5-joomla1', md5_find, location, 45,'Joomla v1 MD5 - hash:%s' % md5_find))
	#		else:
#			results['possible'].append('md5-salt-joomla1')	

	if ('crypto' in filters or 'unix' in filters):  # Blowfish(UNIX)
		for finding in regFind('blowfish-salt-unix', subText):
			data, location = finding.group(), (baseLocation,finding.span())	
			blow_find = re.findall(r"\$(?:2a|2)\$([a-zA-Z0-9./]{2})\$([a-zA-Z0-9./]{53})", data)[0]
			blowfish_salt_unix=Finding('blowfish-salt-unix', blow_find, location, 55, 'UNIX shadow file using salted Blowfish - salt: %s\thash: %s' % blow_find)
			if re.findall(r"\$(?:2a|2)\$[a-zA-Z0-9./]{2}\$([a-zA-Z0-9./]{53})\$?", data)  and entropy(re.findall(r"\$(?:2a|2)\$[a-zA-Z0-9./]{2}\$([a-zA-Z0-9./]{53})\$?", data)[0])>MIN_ENTROPY:
				blowfish_salt_unix.certainty+=30
			results2.append(blowfish_salt_unix)
		
	#@TODO: review - solution for \b?
	if ('other' in filters):	# UUIDs
		for finding in regFind('uuid', subText):
			data, location = finding.group(), (baseLocation,finding.span())
			number=re.findall(r"(?<![a-fA-F0-9])([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})(?![a-fA-F0-9])", data)[0]
			version, subversion = re.findall(r"(?<![a-fA-F0-9])[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-([a-fA-F0-9])[a-fA-F0-9]{3}-([a-fA-F0-9])[a-fA-F0-9]{3}-[a-fA-F0-9]{12}(?![a-fA-F0-9])", data)[0]
			uuid=Finding('uuid', number, location, 75, None)
			
			if version == '3':
				uuid.details='Universally Unique identifier (UUID) - Version 3 (MD5 hash): %s' % number
			elif version == '4' and subversion.upper() in ['8','9','A','B']:
				uuid.details='Universally Unique identifier (UUID) - Version 4 (random): %s' % number
			elif version == '5':    # not sure about this one
				uuid.details='Universally Unique identifier (UUID) - Version 5 (SHA-1 hash): %s' % number
			elif version == '1':
				uuid.details='Universally Unique identifier (UUID) - Version 1 (MAC address): %s' % number
			elif version == '2':
				uuid.details='Universally Unique identifier (UUID) - Version 2 (DCE Security): %s' % number
			else:
				uuid.details='Universally Unique identifier (UUID) - Unknown version %s: %s' % (version,number)
				uuid.certainty=5
			results2.append(uuid)
			
	return results2 #,result_details

def generator(data, mode):
	gen_results={}

	# courtesy of monkeynut
	for a in set( aliases.aliases.values() ):
		try:
			if mode == 'both' or mode == 'decode':			
				gen_results['decoding '+a]=data.decode(a)
			if mode == 'both' or mode == 'encode':
				gen_results['encoding '+a]=data.encode(a)
		except: pass
	return gen_results

def run_validators(results, validators):
	final_results = []
	for validator in validators:		
		validator_func = None
		validator_type = None
		mode = validator.split(':')[0].lower()
		
		if mode == 'all':
			validator_func=all
		elif mode == 'has':
			validator_func=any
		elif mode == 'search':			
			validator_func=re.compile(validator.split(':')[1])			
		else:
			print 'invalid validator provided.'
			exit()
			
		validator_type = validator.split(':')[1].upper()
		

		for result in results:
			payload=None

			if type(result.payload) is tuple:
				payload = "".join([item for item in result.payload])
			else: payload = result.payload
			payload = re.sub('['+BAD_CHARS+']', '', payload)
			
			if validator_type == 'NUMERIC':
				if validator_func(char.isdigit() for char in payload):
					final_results.append(result) 
			elif validator_type == 'ALPHA':
				if validator_func(char.isalpha() for char in payload):
					final_results.append(result)
			elif validator_type == 'LOWER':
				if validator_func(char.islower() for char in payload):
					final_results.append(result)	
			elif validator_type == 'UPPER':
				if validator_func(char.isupper() for char in payload):
					final_results.append(result)	
			elif validator_type == 'ALPHANUMERIC':
				if validator_func(char.isalnum() for char in payload):
					final_results.append(result)
			elif validator_type == 'SYMBOL':
				if validator_func(not char.isalnum() for char in payload):
					final_results.append(result)	
			else:
				if(validator_func.search(payload)):
					final_results.append(result)
					
	return final_results
	
#@TODO: improve
def show2(results, showDetails, validators, min_certainty):

	if min_certainty > 0:
		results = [finding for finding in results if finding.certainty >= min_certainty] 
	
	if len(validators) > 0:
		results = run_validators(results, validators)
	
	for finding in results:
		print finding.display() if showDetails else finding.details

def unpack(stream, fmt):
    size = struct.calcsize(fmt)
    buf = stream.read(size)
    unpacked_struct=None
    try:
	unpacked_struct= struct.unpack(fmt, buf)
    except (struct.error) as e:
	print buf
    return unpacked_struct

def ensure_finished(stream, struct_fmt_string):
    unpacked_data = unpack(stream, struct_fmt_string)
    return str(unpacked_data[0])

#@TODO: test properly
def pre_process(data, struct_fmt_string):
	import binascii, struct
	stream = io.BytesIO(data)
	processed_content=''
	while True:
		try:	
			processed_content += ensure_finished(stream, struct_fmt_string)
		
		except (TypeError) as e: #@TODO: handle IndexError
			break
		except (ValueError):
			break
#@TODO: invalid hit mgmt?

	return processed_content

def testenc(data, filters, analyze, validators, verbose, mode, min_certainty):
	print repr(generator(data, mode).iteritems())
	for element in generator(data, mode).iteritems():
		results = get_type_of(element[1], filters)
		if len(validators) >0:
			results = run_validators(results, validators)
		
		if verbose:
			print 'after %s:' % element[0]
		show2(results, analyze, validators, min_certainty)

def enumerate_files(rootPath, pattern, recursive=True):
	import fnmatch
	fileList = []
	
	if recursive:
		print "enumerating files..."
		for root, dirs, files in os.walk(rootPath):
			for filename in fnmatch.filter(files, pattern):
				fileList.append(os.path.join(root, filename))
	else:
		fileList = [f for f in fnmatch.filter(os.listdir(rootPath), pattern) if os.path.isfile(f)]
	
	return fileList

def process_file(filename, args):
	fl = open(filename,'rb')

	content=None
	overlap_window_size=0
	file_size=os.path.getsize(filename)
	results=[]

	if (args.verbose):
		print 'progress: 0'+'%\t' + 'location: [0/%d]' %(file_size)		

	if  MAX_OVERLAP_WINDOW_SIZE > file_size:
		file_window_size=file_size
	else:
		file_window_size=MAX_FILE_WINDOW_SIZE
		overlap_window_size=MAX_OVERLAP_WINDOW_SIZE
		
	while(fl.tell() != file_size):
		
		content=fl.read(file_window_size)

		file_location=fl.tell()
		if file_location != file_size:
			next_file_position=file_location-overlap_window_size
			fl.seek(next_file_position if next_file_position > 0 else 0)
	
		if args.preprocessor is not None and len(args.preprocessor) == 1 :
			content=pre_process(content, args.preprocessor[0])
			#for artifact in pre_process(content, args.preprocessor[0], struct_format_string):
				#if(args.generator):
					#testenc(data, args.filters, args.analyze, validators, args.verbose, args.generator)						
				#else:			
					#results += get_type_of(artifact, args.filters)
	
	#	else:					
		if(args.generator):
			testenc(content, args.filters, args.analyze, validators, args.verbose, args.generator[0], min_certainty)
		else:
			results = get_type_of(content, args.filters)
			show2(results, args.analyze, validators, min_certainty)

		if (args.verbose):
			print 'progress: '+ str(file_location*100/file_size) + '%' + '\tlocation: [%d/%d]' %(file_location,file_size)

	fl.close()
	
def show_version():
	print 'Codetective v' + __version__ + ' ' + __date__
	print __author__


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=__description__,
	                                 epilog='use filters for more accurate results. Report bugs, ideas, feedback to: blackthorne@ironik.org')	           
	parser.add_argument('string',type=str,nargs='?',
	                    help='determine algorithm used for <string> according to its data representation')
	parser.add_argument('-t', metavar='filters', default=['win','web','unix','db','personal','crypto','other'], type=str, nargs=1,
                   dest='filters', help='filter by source of your string. can be: win, web, db, unix or other')
	parser.add_argument('-a', '-analyze', dest='analyze', help='show more details whenever possible (expands shadow files fields,...)', required=False, action='store_true')
	parser.add_argument('-v', '-verbose', dest='verbose', help='verbose mode shows progress status (useful for large files) and time taken', required=False, action='store_true')
	parser.add_argument('-m','-minimum-certainty', dest='min_certainty', nargs=1, help='specify the minimum acceptable certainty level for displayed results (0 - 100)', type=int)	
	parser.add_argument('-p', '--preprocessor', dest='preprocessor', type=str, help='<struct format string> interpret bytes as packed binary data. Unpacks contents from different data and endianess types according to format strings patterns as specified on: https://docs.python.org/2/library/struct.html', required=False, nargs=1)
	parser.add_argument('-g', '-generator', dest='generator', type=str, nargs=1, help='find encoding/decoding algorithm that exposes interesting artifacts (choose: \'encode\', \'decode\', \'both\')')
	parser.add_argument('-v1','-validator1', dest='validator1', nargs=1, required=False, type=str, help='applies validator 1')
	parser.add_argument('-v2','-validator2', dest='validator2', nargs=1, required=False, type=str, help='applies validator 2')
	parser.add_argument('-v3','-validator3', dest='validator3', nargs=1, required=False, type=str, help='applies validator 3')
	parser.add_argument('-r', '-recursive', dest='recursive', help='sets recursive mode upon specified directory (current workdir by default). Consider using it with min_certainty option', required=False, action='store_true')
	parser.add_argument('-f','-file', dest='filename', nargs=1, help='load a specified file')
	parser.add_argument('-d','-directory', dest='directory', nargs=1, help='load a specified directory')
	parser.add_argument('-fp','-file-pattern', dest='file_pattern', nargs=1, help='specified which file pattern to be used with directory (default: \'*\')')			
	parser.add_argument('-l','-list', dest='list', help='lists supported algorithms', required=False, action='store_true')
        parser.add_argument('-s', '-stdin', dest='stdin', help='read data from standard input', action='store_true')
	parser.add_argument('-ver', '-version', dest='version', help='displays software version', action='store_true')
	args=parser.parse_args()
	
	# set defaults	
	min_certainty=0 if not args.min_certainty else args.min_certainty[0]
	validators = [args.__dict__[val][0] for val in ['validator1','validator2', 'validator3'] if args.__dict__[val] is not None]
	file_pattern='*' if not args.file_pattern else args.file_pattern[0]
	recursive_mode=True if args.recursive else False
	target_directory=args.directory[0] if args.directory else os.getcwd()
		
	
	if(args.list): 
		print "shadow and SAM files, URLs, phpBB3, Wordpress, Joomla, CRC, LM, NTLM, MD4, MD5, Apr, SHA1, SHA256, base64, MySQL323, MYSQL4+, MSSQL2000, MSSQL2005, DES, RipeMD320, Whirlpool, SHA1, SHA224, SHA256, SHA384, SHA512, Blowfish, UUID, phone numbers, credit cards, web cookies"
	
	# string mode
	elif(args.string is not None):
		
		data = args.string

		if args.preprocessor is not None and len(args.preprocessor) == 1 :
			data=pre_process(data, args.preprocessor[0])
			
		if(args.generator):
			testenc(data, args.filters, args.analyze, validators, args.verbose, args.generator[0])
		else:	
			results = get_type_of(data, args.filters)
			show2(results, args.analyze, validators, min_certainty) 
	
	# file mode		
	elif(args.filename is not None):
		process_file(args.filename[0], args)
		
	# directory mode
	elif (args.directory or recursive_mode):	
		fileList = enumerate_files(target_directory, file_pattern, recursive_mode)
		for file in fileList:
			print "== file: " + file
			process_file(file, args)

	# stdin mode
	elif args.stdin:
		
		for data in sys.stdin:
			if args.preprocessor is not None and len(args.preprocessor) == 1 :
				data=pre_process(data, args.preprocessor[0])
				
			if(args.generator):
				testenc(data, args.filters, args.analyze, validators, args.verbose, args.generator[0])
			else:	
				results = get_type_of(data, args.filters)
				show2(results, args.analyze, validators, min_certainty) 		
		
	elif args.version:
		show_version()

	else:
		parser.print_help()
		

#@TODO: add OS fingerprinting from shadow/SAM file parsing
#@TODO: proper logging rather than print's
#@TODO: handle content as binary, octal, hexadecimal or another numeric base of your choice, int() base must be >= 2 and <= 36

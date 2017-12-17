"""

	R --------- R
	O  O ------ O
	N  C  A --- A
	D  C  L
	O	 U  G  +Copyright SavSec (c) 2017
	M	 r  O  
		 E  R  +Algorithms are intellectual
		 N  I  so no Copyright except
		 C  T  directly to ownership of the
		 E  H  base algorithm.
	      M                  -MIT License-

"""

import time, random, sys, string, itertools, os
import base64, hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher (object):

	def __init__(self, key): 
		self.bs = 32
		self.key = key

	def encrypt(self, raw):
		raw = self._pad(raw)
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return base64.b64encode(iv + cipher.encrypt(raw))

	def decrypt(self, enc):
		enc = base64.b64decode(enc)
		iv = enc[:AES.block_size]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode("utf-8")

	def _pad(self, s):
		return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

	@staticmethod
	def _unpad(s):
		return s[:-ord(s[len(s)-1:])]

class RoA (object):
	"""
	RoA / Random Occurence Algorithm is an algorithm developed by Russian Otter! This basic algorithm generates random data based on the exponential outputs given from the algorithm!
	Requirements To Decrypt:
		1.) AES Key
		2.) RoA Key
		3.) Salt
		4.) Encrypted Dictionary
	
	""" 
	def __init__(self,verbose=False):
		"""
		Setting this option to True makes RoA display all active activities!
		"""
		self.verbose = verbose
	
	def algorithm(self,tm,base_length):
		"""
		RoA.algorithm(3 Digits, Key Length) -> Numeric Algorithm Output
		
		This is how RoA generates it's data! The output to RoA is simular to Pi in the fact that it doesnt end and doesnt repeat!
		"""
		
		base = ""
		d = ".".join("`"*i+" "[i : i+i] for i in range(0,125,random.randint(1,4)))+ ".".join("`"*i+" "[i : i] for i in range(0,125,random.randint(1,10)))
		
		b = "".join(d[a : i] for i in range(0,10+tm,2) for a in range(i+~-i*i))
		
		for _ in "".join(b[i:i+i] for i in range(0,tm+base_length,2)):
			base += _
			time.sleep(0.000005)
		
		base = base[:base_length]
		n = ""
		for _ in range(tm):
			n += str("".join(random.sample(base,random.choice(range(len(base))))).count("."))
			time.sleep(0.0005)
		try:
			n = hex(int(n))[2:].replace("L","")[:base_length]
		except:
			return n
		while 1:
			if len(n) == base_length:
				break
			n += random.choice(string.hexdigits.lower())
		return n[:base_length]
	
	def generate_key(self,AESkey):
		"""
		RoA.generate_key(32bit AES Key)
		
		This is used to general the basic RoA Encryption Key
		"""
		if len(AESkey) != 32:
			raise "AESkey length is %s. 32 bit key is required!"
		tm = random.choice(range(0,100))
		if len(str(tm)) == 2 and tm < 77:
			tm = int("0"+str(tm))
		if len(str(tm)) == 1:
			tm = int("00"+str(tm))
		key = self.algorithm(tm,16)
		key = key + AESkey
		return key
		
	def encrypt(self,msg,key):
		"""
		RoA.Encrypt(message, RoAKey)
		
		This is the main encryption process of RoA which makes it secure
		"""
		if self.verbose:
			print "Master Key:",key
			print "\nAES Key:",key[16:]
			print "\nRoA Key:",key[:16]
			print "\nEncrypting Message in AES..."
		AESKey = key[16:]
		rokey = key[:16] *2
		aes = AESCipher(key[16:])
		en_msg = aes.encrypt(msg)
		if self.verbose:
			print "\nEncrypted AES:",en_msg
			print "\nApplying Salt Mix..."
		
		msg = en_msg
		frag = None
		while 1:
			for _ in range(4,9):
				l = len(msg)/float(_)
				if l.is_integer():
					frag = _
				msg += b"\x01"
			if frag != None:
				break
			
		sp = len(msg)/frag
		fragged = []
		
		salt = []
		while 1:
			pun = True
			for _ in msg:
				if _ in string.punctuation:
					t = "".join(random.sample(string.ascii_letters + string.digits + string.punctuation.strip("}").strip("'").strip("\"") +b"\x01",7))
					pun = False
					break
			if pun:
				t = "".join(random.sample(string.ascii_letters + string.digits+b"\x01",7))
			
			if t not in "".join(msg):
				salt.append(t)
			if len(salt) > 15:
				break
		
		prev = 0
		while True:
			f = random.randint(1,sp)
			fragged.append(msg[prev:prev+f])
			prev = prev + f
			if prev >= len(msg)-1:
				break
		
		if self.verbose:
			print "Fragmented Text:"
			print fragged
			print "\nSalt & Pepper:"
			print salt
		
		refrag = {}
		
		def shuffled(x):
			y = x[:]
			random.shuffle(y)
			return y
		x = shuffled(fragged)
		
		for _ in fragged:
			for i in x:
				if i == _:
					refrag.update(
					{str(x[x.index(_)]
					):fragged.index(i)})
		
		if self.verbose:
			print "\nMixed Fragments:"
			print x
			print "\nDictionary:"
			print refrag
		
		comp_refrag = str(refrag).replace(", '",",'")
		comp_salt = str(salt).replace(", '",",'")
		comp_dict = comp_refrag+b"\x02"+comp_salt.strip("\n")
		if self.verbose:
			print "\nCompressed Dictionary:"
			print comp_dict
		
		salt_mix = ""
		sl = 0
		for _ in x:
			if sl > len(salt)-1:
				sl = 0
			salt_mix += _+salt[sl]
			sl = sl + 1
		
		if self.verbose:
			print "\nSalted Text:"
			print salt_mix
			
		aessalt = AESCipher(rokey)
		en_comp_dict = aessalt.encrypt(comp_dict)
		en_salt = aessalt.encrypt(salt_mix)
		
		if self.verbose:
			print "\nEncrypted Dictionary:"
			print en_comp_dict
			print "\nEncrypted Salt:"
			print en_salt
		
		return en_salt+b"\x03"+en_comp_dict,rokey,AESKey
	
	def decrypt(self,en_saltdict,key,AESKey):
			"""
			RoA.decrypt(encrypted salt dictionary, RoA Key, AES Key)
			
			This fuction process reverses all the past actions based on the information it decrypts
			"""
			en_comp_dict = en_saltdict.split(b"\x03")[1]
			en_salt = en_saltdict.split(b"\x03")[0]
			
			aessalt = AESCipher(key)
			comp_dict = aessalt.decrypt(en_comp_dict)
			aessalt = AESCipher(key)
			salt_mix = aessalt.decrypt(en_salt)
			
			if self.verbose:
				print "\n - Starting Decryption Process -"
				print "\nCollecting Dictionary Data..."
			de_dict = eval(comp_dict.split(b"\x02")[0])
			water = eval(comp_dict.split(b"\x02")[1])
			de_salt = salt_mix
			remain = []
			if self.verbose:
				print "Diluting Salt..."
			for _ in water:
				de_salt = de_salt.replace(_,"")
			
			if self.verbose:
				print "Re-arranging Text..."
			c = 0
			en_txt = ""
			for _ in de_dict:
				for _ in de_dict:
					if de_dict[_] == c:
						en_txt += _
						c = c + 1
			aes = AESCipher(AESKey)
			de_txt = aes.decrypt(en_txt)
			if self.verbose:
				print "\nEncrypted Text:"
				print en_txt
				print "\nDecrypting..."
				print "\nDecrypted Text:"
				print de_txt
			return de_txt

Ro = RoA(True)

def example():
	Ro = RoA(True)
	saltdic = Ro.encrypt("Follow @Russian_Otter on Instagram!",Ro.generate_key("PythonRo"*4))
	time.sleep(5)
	decrypted = Ro.decrypt(saltdic[0],saltdic[1],saltdic[2])

def pattern_test():
	import matplotlib.pyplot as plt
	import numpy as np
	amount = "\r\r\ra: %s b: %s c: %s d: %s e: %s f: %s 1: %s 2: %s 3: %s 4: %s 5: %s 6: %s 7: %s 8: %s 9: %s 0: %s "
	for _ in range(100):
		key = Ro.algorithm(10,16)
		f = open("tmp.bit","a")
		f.write(key)
		f.close()
		total = open("tmp.bit").read()
		a = amount.replace(" "," | ")
		t = total
		data = a % (t.count("a"),t.count("b"),t.count("c"
		),t.count("d"),t.count("e"),t.count("f"),t.count("1"),t.count("2"
		),t.count("3"),t.count("4"),t.count("5"),t.count("6"),t.count("7"),t.count("8"),t.count("9"),
		t.count("0"))
		sys.stdout.write(data)
		time.sleep(0.00005)
	
	t = data.split(" | ")
	alphab = list("abcdef1234567890")
	frequencies = []
	for _ in range(1,32,2):
		frequencies.append(int(t[_].replace(" ","")))
	pos = np.arange(len(alphab))
	width = 1.0
	ax = plt.axes()
	ax.set_xticks(pos + (width / 1))
	ax.set_xticklabels(alphab)
	plt.bar(pos, frequencies, width, color="lime")
	plt.show()
	os.remove("./tmp.bit")

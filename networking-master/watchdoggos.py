import console, time, sys, string, random

def crypt(word):
	id = list(word)
	for _ in range(len(word)):
		rd = "".join(random.sample(string.printable[:75]*5,len(word)))
		for __ in word:
			rd = "".join(random.sample(string.printable[:75]*5,len(word)))
			cr = rd[_+1:]+word[_]
			sys.stdout.write("\r"+cr)
			time.sleep(random.choice([0.05,0.005,0.03,0.009]))
	for _ in range(len(word)):
		sys.stdout.write("\r"+word[:_+1])
		time.sleep(0.05)
	print

print 

import console
from os import listdir
console.set_font("Menlo",30)
crypt("\t Watch_Doggos")
console.set_font()
print "\nWhat Program Would You Like To Run?"
for _ in listdir("./"):
	if _.endswith(".py"):
		sys.stdout.write(_+"  ")
		time.sleep(0.2)
print "\n"
while 1:
	try:
		cmd = "import "+raw_input("> ")
		if cmd == "import exit":
			break
		try:
			exec(cmd)
		except: pass
	except: sys.exit()

# Move file to 'site-packages'
def func_bytes(fl):
	import console, dis
	"""
	This function reads a script and
	prints it's memory address.
	"""
	f = open(fl).readlines()
	for line in f:
		try:
			co = compile(line,"<none>","exec")
			t = str(str(co).split("at ")[1]).split(",")[0]
			print t, co.consts
		except:
			pass
	console.set_font("Menlo",10)
	f = open(fl).readlines()
	for line in f:
		try:
			dis.dis(line)
		except:
			pass
	console.set_font()

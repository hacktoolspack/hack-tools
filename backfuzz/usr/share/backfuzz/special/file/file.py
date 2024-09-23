from functions import *
"""File Fuzzer"""
PROPERTY={}
PROPERTY['PROTOCOL']="FILE"
PROPERTY['NAME']=": File Fuzzer"
PROPERTY['DESC']="Generate multiple files with payload"
PROPERTY['AUTHOR']='localh0t'

class FuzzerClass:
	def fuzzer(self):
		try:
			directory = raw_input("\n[!] Path to dir where save the files (must exist, Ex: ./fuzzfiles) > ")
			ext = raw_input("[!] File extension (Ex: .m3u) > ")
			header = fileInput("[!] Insert a file header (for each file) (Crtl-C when you're done, or hit now Crtl-C for no header) >")
			eof = fileInput("[!] Insert a EOF (for each file) (Crtl-C when you're done, or hit now Crtl-C for no EOF) > ")
		except KeyboardInterrupt:
			exitProgram(6)
		for length in range(globalvars.minim, globalvars.maxm+1, globalvars.salt):
			pattern = createPattern(length)
			pattern = header + pattern + "\n" + eof
			fileWrite(directory + "/" + "fuzz" + str(length) + ext,pattern)
			print "[!] Generating " + directory + "/" + "fuzz" + str(length) + ext
		exitProgram(2)
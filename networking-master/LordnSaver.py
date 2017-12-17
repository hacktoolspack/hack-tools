import gzip, shutil, tempfile, os, time

class LnS (object):
	"""
	LordnSaver is a program built to save recent backups of scripts you have run! 
	Saves are compressed to save data!
	
	Usage:
		import LordnSaver, os
		L = LordnSaver.LnS(os.path.basename(__file__))
		L.save()
	
	SavSec LordnSaver (c) 2017
	
	"""
	
	def __init__(self,cfile):
		"""
		LordnSaver must have the name of the file being saved included. Make sure you get the file correct or else the program will not save your work!
		Recommeneded method for getting file name:
			
		import os
		nfile = os.path.basename(__file__)
		
		"""
		self.cfile = cfile
		self.add = "LNS_%s/lns_" %self.cfile
		if self.add.split("/")[0] not in os.listdir("./"):
			os.mkdir(self.add.split("/")[0])

	def noise(self):
		"""
		Noise will return the current time for the save file
		"""
		return "_".join(str(time.ctime()).split(" ")[:4])

	def make_file(self):
		"""
		make_file automatically creates all the needed files inorder for your script to save
		"""
		self.sfile = self.add.split("lns_")[0]+self.noise()
		self.tfile, self.filename = tempfile.mkstemp()
		os.write(self.tfile, open(self.cfile).read())

	def compress2(self,file):
		"""
		compress2 is a simple gzip file compresser used to decrease the size of your saved file
		(miniumizing storage usage)
		compress2 requires the name of your file to run (but will be put in automatically)
		"""
		self.f_in = open(file, 'rb')
		self.f_out = gzip.open(self.sfile+'.lns', 'wb')
		self.f_out.writelines(self.f_in)
		self.f_out.close()
		self.f_in.close()

	def readgzip(self,file):
		"readgzip will read and return the code from your select file"
		file = self.add.split("lns_")[0]+file
		file += ".lns"
		f = gzip.open(file, 'rb')
		file_content = f.read()
		print file_content
		f.close()
		return file_content

	def wipe_dir(self):
		"""
		Deletes save files
		"""
		if raw_input("Are You Sure? [Y/N] ").lower() == "y":
			loc = self.sfile.split("/")[0]
			try:
				for _ in os.listdir(loc):
					os.remove(loc+"/"+_)
				os.rmdir(loc)
			except Exception as e:
				print e
	
	def save(self):
		"""
		Saves the running file code to a folder: LNS_<filename>
		"""
		self.make_file()
		self.compress2(self.filename)
		os.close(self.tfile)


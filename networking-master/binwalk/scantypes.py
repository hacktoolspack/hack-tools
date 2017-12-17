import sys, console
try:
  import binwalk
except:
  print "Download binwalk with GitHubGet!"
  print "After that look for the folder 'binwalk' and move it to 'site-packages'"
  print "Then move this script into 'site-packages'"
  print "Once that is done all you need to do is run:"
  print ">>> import scantypes"
  print ">>> scantypes.sigscan(file,size)"
  print "binwalk link: https://github.com/devttys0/binwalk"
  sys.exit()
  
def sigscan(fl,font=8):
	console.set_font("Menlo",font)
	try:
		for module in binwalk.scan(fl, signature=True, quiet=True):
			print ("%s Results:" % module.name)
			for result in module.results:
				print ("\t%s	0x%.8X	%s [%s]" % (
					result.file.name, result.offset, result.description, str(result.valid)))
	except binwalk.ModuleException as e:
		pass
	console.set_font()

def extract(fl):
	for module in binwalk.scan(fl, signature=True, quiet=True, extract=True):
		for result in module.results:
			if module.extractor.output.has_key(result.file.path):
				if module.extractor.output[result.file.path].extracted.has_key(result.offset):
					print (
						"Extracted '%s' at offset 0x%X from '%s' to '%s'" % (result.description.split(',')[0],
						result.offset,
						result.file.path,
						str(module.extractor.output[result.file.path].extracted[result.offset])))

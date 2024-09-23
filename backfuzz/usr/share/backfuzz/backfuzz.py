import dircache
from functions import *

# Back to the FUZZ'er - protocol fuzzing toolkit
# Contact: mattdch0@gmail.com (suggerences, ideas, reviews)
# Follow: @mattdch
# Blog: www.localh0t.com.ar

# Version
VERSION = "0.3.2"

# Plugin read class
class Plugins:
	def __init__(self):
		self.plugins = []
    	def loadPlugins(self, directory):
        	filelist = dircache.listdir(directory)
        	for filename in filelist:
        		if not '.' in filename:
				sys.path.insert(0, directory + filename)
                		self.plugins += [__import__(filename)]
                		sys.path.remove(directory + filename)

listadoPlugins = Plugins()
listadoPlugins.loadPlugins("./plugins/")
listadoSpecial = Plugins()
listadoSpecial.loadPlugins("./special/")

# Start Fuzzer function
def startFuzzer(object):
	for plugin in object:
		if plugin.PROPERTY['PROTOCOL'] == globalvars.plugin_use:
			fuzzmaster = plugin.FuzzerClass()
			fuzzmaster.fuzzer()

# Show Help function
def showHelp():
	print "\n##################################################"
	print "# Back to the FUZZ'er - " + "protocol fuzzing toolkit #"
	print "##################################################"
	print "\nVersion: " + colors.BLUE + VERSION + colors.ENDC
	print "\nArguments (Normal Plugins):\n===========================\n"
	print "-h   [IP]" + colors.RED + " [Required] " + colors.ENDC
	print "-p   [PORT]" + colors.RED + " [Required] " + colors.ENDC
	print "-min [START LENGTH]" + colors.RED + " [Required] " + colors.ENDC
	print "-max [END LENGTH]" + colors.RED + " [Required] " + colors.ENDC
	print "-s   [SALT BETWEEN FUZZ STRINGS]" + colors.RED + " [Required] " + colors.ENDC
	print "-pl  [PLUGIN TO USE]" + colors.RED + " [Required] " + colors.ENDC
	print "-pf  [PATTERN-FLAVOUR TO USE (default: Cyclic)]" + colors.GREEN + " [Optional] " + colors.ENDC
	print "-t   [TIMEOUT (Seconds) (default: 0.8)]" + colors.GREEN + " [Optional] " + colors.ENDC
	print "-S   [SHOW PATTERN ON CRASH (default: False)]" + colors.GREEN + " [Optional] " + colors.ENDC 
	print "\nArguments (Special Plugins):\n============================\n"
	print "-SPECIAL" + colors.RED + " [Required] " + colors.ENDC
	print "-pl [SPECIAL PLUGIN TO USE]" + colors.RED + " [Required] " + colors.ENDC
	print "-min [START LENGTH]" + colors.RED + " [Required] " + colors.ENDC
	print "-max [END LENGTH]" + colors.RED + " [Required] " + colors.ENDC
	print "-s [SALT BETWEEN FUZZ STRINGS]" + colors.RED + " [Required] " + colors.ENDC
	print "-pf [PATTERN-FLAVOUR TO USE (default: Cyclic)]" + colors.GREEN + " [Optional] " + colors.ENDC
	print "\nPattern Flavours are:\n=====================\n"
	print "Cyclic :          Aa0Aa1Aa2Aa3Aa4Aa [...]"
	print "Cyclic Extended : Aa.Aa;Aa+Aa=Aa-Aa [...]"
	print "Single :          AAAAAAAAAAAAAAAAA [...]"
	print "FormatString :    %n%x%n%x%s%x%s%n  [...]"
	print "\nAvailable plugins:"
	print "==================\n"
	for plugin in listadoPlugins.plugins:
		print plugin.PROPERTY['PROTOCOL'], plugin.PROPERTY['NAME'], "|", plugin.PROPERTY['DESC'], "|", "Author:", plugin.PROPERTY['AUTHOR']
	print "\nSpecial plugins:"
	print "================\n"
	for special in listadoSpecial.plugins:
		print special.PROPERTY['PROTOCOL'], special.PROPERTY['NAME'], "|", special.PROPERTY['DESC'], "|", "Author:", special.PROPERTY['AUTHOR']

# Read Args function
def readArgs(arguments):
	count = 0
	globalvars.timeout = 0.8
	globalvars.pattern_flavour = "Cyclic"
	globalvars.show_pattern    = False 
	for arg in arguments:
		try:
			if arg == "-h":
				globalvars.host = arguments[count + 1]
			elif arg == "-p":
				globalvars.port = strToInt(arguments[count + 1], "-p")
			elif arg == "-min":
				globalvars.minim = strToInt(arguments[count + 1], "-min")
			elif arg == "-max":
				globalvars.maxm = strToInt(arguments[count + 1], "-max")
			elif arg == "-s":
				globalvars.salt = strToInt(arguments[count + 1], "-s")
			elif arg == "-pl":
				globalvars.plugin_use = arguments[count + 1]
			elif arg == "-pf":
				globalvars.pattern_flavour = arguments[count + 1]
			elif arg == "-t":
				globalvars.timeout = strToFloat(arguments[count + 1], "-t")
			elif arg == '-S':
				globalvars.show_pattern = True 
			count += 1
		except:
			exitProgram(3)
	# Args check
	try:
		arglist = [globalvars.host, globalvars.port, globalvars.minim, globalvars.maxm, globalvars.salt, globalvars.plugin_use]
		checkMinMax(globalvars.minim, globalvars.maxm)
		checkFlavour(globalvars.pattern_flavour)
	except:
		exitProgram(3)

# Special Read Args function
def readArgsSpecial(arguments):
	count = 0
	globalvars.pattern_flavour = "Cyclic"
	for arg in arguments:
		try:
			if arg == "-min":
				globalvars.minim = strToInt(arguments[count + 1], "-min")
			elif arg == "-max":
				globalvars.maxm = strToInt(arguments[count + 1], "-max")
			elif arg == "-s":
				globalvars.salt = strToInt(arguments[count + 1], "-s")
			elif arg == "-pl":
				globalvars.plugin_use = arguments[count + 1]
			elif arg == "-pf":
				globalvars.pattern_flavour = arguments[count + 1]
			count += 1
		except:
			exitProgram(3)
	# Args check
	try:
		arglist = [globalvars.minim, globalvars.maxm, globalvars.salt, globalvars.plugin_use]
		checkMinMax(globalvars.minim, globalvars.maxm)
		checkFlavour(globalvars.pattern_flavour)
	except:
		exitProgram(3)

# Show Help
if len(sys.argv) <= 12 and "-SPECIAL" not in sys.argv:
	showHelp()
	exitProgram(1)

# Read Args & Start
if "-SPECIAL" in sys.argv:
	readArgsSpecial(sys.argv)
	startFuzzer(listadoSpecial.plugins)
else:
	readArgs(sys.argv)
	startFuzzer(listadoPlugins.plugins)

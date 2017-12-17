# Version 9.5.3 Omega
# Made for Pythonista 3
# By: SavSec
# - I Don't Give A Fuck License -
# Debugging: SavSec, PotatoGod
# API Script: SavSec

import clipboard, random, sys, os, time, console, traceback

verbose = False
try:
	if sys.argv[1] == "-v":
		verbose = True
		print "Verbose: ON\n"
except:
	pass

purplefade = ["#5700ff",'#5300f3','#4f00e7','#4b00db','#4600cd','#4100bf','#3d00b3','#3900a7','#35009b','#30008e','#35009b','#3900a7','#3d00b3','#4100bf','#4600ce','#4a00da','#4f00e7','#5300f3']
rainbowfade = "#ff0000","#ff4909","#ff7100","#ffac00","#eeff00","#b1ff00",'#27ff00','#09ff00','#00ff21','#00ff9b','#00ffd8','#00deff','#009bff','#0059ff','#0016ff','#5700ff','#b100ff','#f400ff','#ff00c8','#ff0085','#ff0043'
bloodfade = "#cc0000","#bb0000","#aa0000","#990000","#880000","#770000","#880000","#990000","#aa0000","#bb0000"
bluefade = "#0000cc","#0000bb","#0000aa","#000099","#000088","#000077","#000088","#000099","#0000aa","#0000bb"
rainbow = "#ff0000","#ff8500","#f2ff00","#00ff00","#00ffff","#0000ff","#ff00ff"

global colors

def execute_api():
	print "   - Color Execution API - "
	time.sleep(0.3)
	print "To run a loaded api color"
	print "type \"e:<name>|<file>\" and"
	print "the api color will run!"
	print "\nExample:"
	print " e:rainfade|colors.api"
	time.sleep(0.3)

def write_api():
	print "   - Color Writing API - "
	time.sleep(0.3)
	print "To write your own color and"
	print "have it stored om your local"
	print "device for later usage, type"
	print " \"w:<file>!<name>|#hex,#hex\""
	print "\nExample:"
	print " w:colors.api!dark:d1|#484848,#585858,#686868"
	time.sleep(0.3)
	
def loading_api():
	print "   - Loading Colors API - "
	time.sleep(0.3)
	print "Once you have a collection of"
	print "api colors stored, you can call"
	print "them back into the program by"
	print "typing \"l:<file>\""
	time.sleep(0.3)
	print "\nExample:"
	print " l:colors.api"

def parse_color(line):
	try:
		if line.startswith("e:"):
			ec = line[2:].split("|")
			f = open(ec[1]).readlines()
			for _ in f:
				if ec[0] in _:
					lin = _.replace("\n","")
					break
			ec = lin.split("|")
			ec[1] = '"'+ec[1].replace(",",'","')
			ex = ec[0] + "=" +ec[1]
			try:
				exec ex
				exec "AutoLength(%s)" %(ec[0])
			except:
				print "Failed 1"
				pass
		
		if line.startswith("w:"):
			f = open(line[2:].split("!")[0],"a")
			f.write(line[2:].split("!")[1]+'"'+"\n")
			f.close()
		
		if line.startswith("l:"):
			f = open(line[2:]).readlines()
			for _ in f:
				par = _.split("|")
				par[1] = '"'+par[1].replace(",",'","')
				name = par[0]
				ex = name + "=" +par[1]
				try:
					exec "global "+name
					exec ex
					print "Loaded:",name
				except Exception as e:
					traceback.print_exc(e)
					print "Failed 1"
					pass
	except Exception as e:
		if verbose: traceback.print_exc(e)
		pass
	
	if ":" not in line and "!" not in line:
		print
		loading_api()
		print "\n"
		write_api()
		print "\n"
		execute_api()
		print

def bloodforum():
	# BloodForum is used on Hacker's Forum Page To Make Blood Text
	try:
		colors = ["#e00000","#c70000","#af0000","#a10000","#8e0000","#7d0000","#a00000","#ad0000","#ca0000","#e00000"]
		new = ""
		s = 0
		a = 0
		n = 2
		while 1:
			msg = unicode(raw_input("Message: "))
			if msg == "!quit":
				if verbose: print "Stopped"
				break
			msg = [msg[i:i+n] for i in range(0, len(msg), n)]
			for _ in msg:
				if s == 10:
					s = a
					a = 1
					if a == 10:
						a = 0
				if _ == " ":
					new = new + _
					s = s - 1
				else:
					new = new + "[color=" + colors[s] + "]" + _ + "[/color]"
				s = s + 1
			clipboard.set(new)
			new = ""
	except Exception as e:
		if verbose: print traceback.print_exc(file=sys.stdout)
		pass

def updown():
	# UpDown Makes Your Text Go Up And Down
	colors = ["#sup","#/sup","#sub","#/sub"]
	s = 0
	new = ""
	msgb = ""
	try:
		while 1:
			sys.stderr = msg = unicode(raw_input("Message: "))
			if msg == "!quit":
				if verbose: print "Stopped"
				break
			if len(msg) >= 100:
				msgb = msg[100:]
				msg = msg[:100]
			msg = msg.split(" ")
			for _ in msg:
				if s == len(colors):
					s = 0
				if _ == " ":
					new = new + " "
					s = s - 1
				else:
					new = new + colors[s].replace("#","[") + "]" + _ + " "
				s = s + 1
			clipboard.set("[c][b][efffff]" + new + msgb)
			if verbose: print "Copied"
			new = ""
			msgb = ""
	except Exception as e:
		if verbose: print traceback.print_exc(file=sys.stdout)
		pass

def captcha():
	# Makes text almost impossible to read
	colors = ["#i","#/i","#i","#/i"]
	s = 0
	new = ""
	msgb = ""
	try:
		while 1:
			sys.stderr = msg = unicode(raw_input("Message: ").replace("a","4").replace("e","3").replace("t","7").replace("i","1").replace("o","0").replace("B","8").replace("s","5"))
			if msg == "!quit":
				if verbose: print "Stopped"
				break
			if len(msg) >= 100:
				msgb = msg[100:]
				msg = msg[:100]
			msg = list(msg)
			for _ in msg:
				if s == len(colors):
					s = 0
				if _ == " ":
					new = new + " "
					s = s - 1
				else:
					new = new + colors[s].replace("#","[") + "]" + _
				s = s + 1
			clipboard.set("[c][b][efffff]" + new + msgb)
			if verbose: print "Copied"
			new = ""
			msgb = ""
	except Exception as e:
		if verbose: print traceback.print_exc(file=sys.stdout)
		pass

def italics():
	# italics or not italics, which one?
	colors = ["#i","#/i","#i","#/i"]
	s = 0
	new = ""
	msgb = ""
	try:
		while 1:
			sys.stderr = msg = unicode(raw_input("Message: "))
			if msg == "!quit":
				if verbose: print "Stopped"
				break
			if len(msg) >= 100:
				msgb = msg[100:]
				msg = msg[:100]
			msg = list(msg)
			for _ in msg:
				if s == len(colors):
					s = 0
				if _ == " ":
					new = new + " "
					s = s - 1
				else:
					new = new + colors[s].replace("#","[") + "]" + _
				s = s + 1
			clipboard.set("[c][b][efffff]" + new + msgb)
			if verbose: print "Copied"
			new = ""
			msgb = ""
	except Exception as e:
		if verbose: print traceback.print_exc(file=sys.stdout)
		pass

def liner():
	# so many lines!
	colors = ["#u","#/u","#u","#/u"]
	s = 0
	new = ""
	msgb = ""
	try:
		while 1:
			sys.stderr = msg = unicode(raw_input("Message: "))
			if msg == "!quit":
				if verbose: print "Stopped"
				break
			if len(msg) >= 100:
				msgb = msg[100:]
				msg = msg[:100]
			msg = list(msg)
			for _ in msg:
				if s == len(colors):
					s = 0
				if _ == " ":
					new = new + " "
					s = s - 1
				else:
					new = new + colors[s].replace("#","[") + "]" + _
				s = s + 1
			clipboard.set("[c][b][efffff]" + new + msgb)
			if verbose: print "Copied"
			new = ""
			msgb = ""
	except Exception as e:
		if verbose: print traceback.print_exc(file=sys.stdout)
		pass

def undercolor():
	# Undercolor Provides a Under Beam of Colour
	colors = ["#ff0000"]
	colors = rainbowfade
	s = 0
	new = ""
	msgb = ""
	try:
		while 1:
			sys.stderr = msg = unicode(raw_input("Message: "))
			if msg == "!quit":
				if verbose: print "Stopped"
				break
			if len(msg) <= 11:
				n = 1
			elif 11 < len(msg) <= 18:
				n = 2
			elif 18 < len(msg) <= 32:
				n = 3
			elif 32 < len(msg) <= 50:
				n = 4
			msg = [msg[i:i+n] for i in range(0, len(msg), n)]
			if len(msg) >= 25:
				msgb = msg[25:]
				msg = msg[:35]
			msg = list(msg)
			for _ in msg:
				if s == len(colors):
					s = 0
				new = new + colors[s].replace("#","[") + "]" + u"\u0332" + "[efffff]" + _
				s = s + 1
			clipboard.set("[c][b]" + new + msgb)
			if verbose: print "Copied"
			new = ""
			msgb = ""
			s = s
	except Exception as e:
		if verbose: print traceback.print_exc(file=sys.stdout)
		pass

def l33t():
	try:
		while 1:
			sys.stderr = msg = unicode(raw_input("Message: "))
			if msg == "!quit":
				if verbose: print "Stopped"
				break
			clipboard.set("[c][b][00ff00]"+unicode(msg.replace("a","4").replace("e","3").replace("t","7").replace("i","1").replace("o","0").replace("B","8").replace("s","5")))
			if verbose: print "Copied"
	except Exception as e:
		if verbose: print traceback.print_exc(file=sys.stdout)
		pass

def fancy(cl="ord"):
	# Font Types
	# ord - Ordered cycle through all font options
	# ran - Random choice of font options
	# rancycle - Randomly choose 1 font to cycle with
	# 1 - font 1, Candy-Cain-Like font structure
	# 2 - font 2, blue and yellow lightning-like font structure
	# 3 - font 3, black and yellow storm font structure
	# 4 - font 4, light prism font structure
	fa1 = "[c][b][efffff]-[ff0000]=[efffff]-[ff0000]=[efffff]- %s [efffff]-[ff0000]=[efffff]-[ff0000]=[efffff]-" 
	fa2 = "[c][b][0000ff]>[ffff00]> [0000ff]>[ffff00]>[efffff] %s [ffff00]<[0000ff]< [ffff00]<[0000ff]<"
	fa3 = "[c][b][ffff00]+[585858]-[484848]=[585858]-[ffff00]+[efffff] %s [ffff00]+[585858]-[484848]=[585858]-[ffff00]+"
	fa4 = "[c][b][9f9f9f]|[ffff00]: : :[9f9f9f]| [ffff00]-[efffff] %s [ffff00]- [9f9f9f]|[ffff00]: : :[9f9f9f]|"
	ord = [fa1,fa2,fa3,fa4]
	if cl == "ord":
		try:
			while 1:
				for _ in ord:
					sys.stderr = msg = unicode(raw_input("Message: "))
					if msg == "!quit":
						if verbose: print "Stopped"
						break
					clipboard.set(_ %(msg))
					if verbose: print "Copied"
		except Exception as e:
			if verbose: print traceback.print_exc(file=sys.stdout)
			pass
	if cl == "ran":
		try:
			while 1:
				_ = random.choice(ord)
				sys.stderr = msg = unicode(raw_input("Message: "))
				if msg == "!quit":
					if verbose: print "Stopped"
					break
				clipboard.set(_ % (msg))
				if verbose: print "Copied"
		except Exception as e:
			if verbose: print traceback.print_exc(file=sys.stdout)
			pass

def RegularMulticolor(colors):
	s = 0
	new = ""
	msgb = ""
	try:
		while 1:
			sys.stderr = msg = unicode(raw_input("Message: "))
			if msg == "!quit":
				if verbose: print "Stopped"
				break
			msg = unicode(msg)
			if len(msg) >= 22:
				msgb = msg[22:]
				msg = msg[:22]
			msg = list(msg)
			for _ in msg:
				if s == len(colors):
					s = 0
				if _ == " ":
					new = new + " "
					s = s - 1
				else:
					new = new + colors[s].replace("#","[") + "]" + _
				s = s + 1
			clipboard.set("[c][b]" + new + msgb)
			if verbose: print "Copied"
			new = ""
			msgb = ""
			s = 0
	except Exception as e:
		if verbose: print traceback.print_exc(file=sys.stdout)
		pass

def AutoLength(colors):
	s = 0
	new = ""
	msgb = ""
	try:
		while 1:
			sys.stderr = msg = unicode(raw_input("Message: "))
			if msg == "!quit":
				if verbose: print "Stopped"
				break
			if len(msg) >= 1 and len(msg) <= 22:
				n = 1
			if len(msg) > 22 and len(msg) <= 38:
				n = 2
			if len(msg) > 38 and len(msg) <= 54:
				n = 3
			if len(msg) > 54 and len(msg) <= 68:
				n = 4
			if len(msg) > 68 and len(msg) <= 75:
				n = 5
			if len(msg) > 75 and len(msg) <= 84:
				n = 6
			if len(msg) > 84 and len(msg) <= 91:
				n = 7
			if len(msg) > 91 and len(msg) <= 99:
				n = 8
			if len(msg) > 99 and len(msg) <= 108:
				n = 9
			if len(msg) > 108 and len(msg) <= 110:
				n = 10
			if len(msg) > 110 and len(msg) <= 126:
				n = 11
			elif len(msg) >= 127:
				n = 15
			msg = [msg[i:i + n] for i in xrange(0, len(msg), n)]
			for _ in msg:
				if s >= len(colors):
					s = 0
				if _ == " ":
					new = new + _
					s = s - 1
				else:
					new = new + colors[s].replace("#","[") + "]" + _
				s = s + 1
			clipboard.set("[c][b]"+new)
			if verbose: print "Copied"
			new = ""
			msgb = ""
			s = 0
	except Exception as e:
		if verbose: print traceback.print_exc(file=sys.stdout)
		pass

def colorhelp():
	print ""
	console.set_font("Arial-BoldMT",16)
	print "Commands: "
	console.set_font()
	time.sleep(0.3)
	print "Rainbow  - rainbow | r1"
	time.sleep(0.3)
	print "Rainfade - rainfade | r1"
	time.sleep(0.3)
	print "Blood    - blood | b1"
	time.sleep(0.3)
	print "BlueFade - bluefade | r1"
	time.sleep(0.3)
	print "L33T     - leet | l3"
	time.sleep(0.3)
	print "Italics  - italic | i"
	time.sleep(0.3)
	print "Captcha  - captcha | cap"
	time.sleep(0.3)
	print "Underline - underline | u2"
	time.sleep(0.3)
	print "UnderColor - undercolor | u1"
	time.sleep(0.3)
	print "Updown   - updown | ud"
	time.sleep(0.3)
	print "L33T      - leet | l3"
	time.sleep(0.3)
	print "PurpleFade - purplefade | p1"
	print "Exit      - q | exit"
	time.sleep(0.3)
	print "Back      - cd | back"
	time.sleep(0.3)
	print "Clear     - cls | clear"
	time.sleep(0.3)
	print "\nTip: Typing \"!quit\" while using a color will return you to the command line!"

while 1:
	location = "Menu"
	act = "\n~/" + str(location) + "$: "
	console.set_color(1,1,1)
	try:
		data = raw_input(act)
	except:
		pass
	console.set_color()
	if data == "r" or data == "reg" or data == "regular":
		while 1:
			location = "Regular"
			act = "\n~/" + str(location) + "$: "
			console.set_color(1,1,1)
			try:
				data = raw_input(act)
			except:
				sys.exit()
			console.set_color()
			if data == "rainbow" or data == "r1":
				RegularMulticolor(rainbow)
			if data == "rainfade" or data == "r2":
				RegularMulticolor(rainbowfade)
			if data == "blood" or data == "b1":
				RegularMulticolor(bloodfade)
			if data == "bluefade" or data == "b2":
				RegularMulticolor(bluefade)
			if data == "purplefade" or data == "p1":
				RegularMulticolor(purplefade)
			if data == "captcha" or data == "cap":
				captcha()
			if data == "italics" or data == "i":
				italics()
			if data == "leet" or data == "l":
				l33t()
			if data == "updown" or data == "ud":
				updown()
			if data == "underline" or data == "u2":
				liner()
			if data == "undercolor" or data == "u1":
				undercolor()
			if data == "quit" or data == "q" or data == "exit":
				sys.exit()
			if data == "clear" or data == "cls" or data == "clr":
				console.clear()
			if data == "back" or data == "cd":
				break
			if data == "?" or data == "help":
				colorhelp()
	if data == "a" or data == "auto" or data == "stable":
		while 1:
			location = "AutoStablized"
			act = "\n~/" + str(location) + "$: "
			console.set_color(1,1,1)
			try:
				data = raw_input(act)
			except:
				sys.exit()
			console.set_color()
			if data == "rainbow" or data == "r1":
				AutoLength(rainbow)
			if data == "rainfade" or data == "r2":
				AutoLength(rainbowfade)
			if data == "blood" or data == "b1":
				AutoLength(bloodfade)
			if data == "bluefade" or data == "b2":
				AutoLength(bluefade)
			if data == "purplefade" or data == "p1":
				AutoLength(purplefade)
			if data == "captcha" or data == "cap":
				captcha()
			if data == "italics" or data == "i":
				italics()
			if data == "leet" or data == "l":
				l33t()
			if data == "updown" or data == "ud":
				updown()
			if data == "underline" or data == "u2":
				liner()
			if data == "undercolor" or data == "u1":
				undercolor()
			if data == "quit" or data == "q" or data == "exit":
				sys.exit()
			if data == "clear" or data == "cls" or data == "clr":
				console.clear()
			if data == "?" or data == "help":
				colorhelp()
			if data == "back" or data == "cd":
				break
	if data == "exit" or data == "quit" or data == "q":
		sys.exit()
	if data == "clear" or data == "cls" or data == "clr":
		console.clear()
	if data[1] == ":" or data == "api" or data == "cc":
		parse_color(data)
	if data == "help" or data == "?":
		print ""
		console.set_font("Arial-BoldMT",16)
		print "Menu Commands: "
		console.set_font()
		time.sleep(0.3)
		print "Regular   - r | regular | reg"
		time.sleep(0.3)
		print "Stablized - a | auto | stable"
		time.sleep(0.3)
		print "Exit       - q : exit"
		time.sleep(0.3)
		print "Back       - cd : back"
		time.sleep(0.3)
		print "Clear      - cls : clear"
		time.sleep(0.3)
		print "API        - api : cc"

# Move To Site-Packages
import sys

try:
	import objc_util
	print "You are running Pythonista,\nyou dont need this!"
	print "THIS FILE WILL BE AUTOMATICALLY DELETED"
	import os
	os.remove("./console.py")
	sys.exit()
except:
	pass

def set_color(r=None,g=None,b=None):
	"""
	Console is a default module which
	allows users to change color of
	text! (Since Pythonista doesnt have
	bash) This program will work as a color
	changer for PC that still supports the
	same syntax as console on Pythonista!
	"""
	if r >= 1 > g >= b: # red
		sys.stdout.write("\e[91m")
	if g >= 1 > r >= b: # green
		sys.stdout.write("\e[92m")
	if b >= 1 > r >= g: # blue
		sys.stdout.write("\e[34m")
	if r >= g > b: # yellow
		sys.stdout.write("\e[93m")
	if b >= g > r: # aqua
		sys.stdout.write("\e[96m")
	if r >= b > g: # magenta
		sys.stdout.write("\e[95m")
	if r == b == g >= 1: # white
		sys.stdout.write("\e[97m")
	if r == b == g == 0: # black
		sys.stdout.write("\e[30m")
	if r == None or b == None or g == None:
		sys.stdout.write("\e[39m")

def set_font(font,size):
	"""
	PC's running Python don't have font
	options while running python programs,
	so this function is in place to prevent
	crashes from some of my programs that
	do use font change.
	"""
	pass

def write_link(url,text):
	"""
	Programs like Romap use this but there
	are no PC functions that can do this
	action, so this function is just in place to prevent crashes!
	"""
	sys.stdout.write(text)

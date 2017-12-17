from objc_util import *
import random, sys, os, inspect, re, time

#Base By: OMZ Admin
#Mod By: Russian Otter

load_framework('ReplayKit')
RPScreenRecorder = ObjCClass('RPScreenRecorder')

def previewControllerDidFinish_(_self, _cmd, _vc):
	ObjCInstance(_vc).dismissViewControllerAnimated_completion_(True, None)

PreviewDelegate = create_objc_class('PreviewDelegate', methods=[previewControllerDidFinish_])

def stop_callback(_cmd, _vc):
	vc = ObjCInstance(_vc)
	delegate = PreviewDelegate.new().autorelease()
	vc.setPreviewControllerDelegate_(delegate)
	rootvc = UIApplication.sharedApplication().keyWindow().rootViewController()
	rootvc.presentViewController_animated_completion_(vc, True, None)
	
stop_handler = ObjCBlock(stop_callback, restype=None, argtypes=[c_void_p, c_void_p])
recorder = RPScreenRecorder.sharedRecorder()

@on_main_thread
def start_recording():
	recorder.startRecordingWithMicrophoneEnabled_handler_(False, None)

@on_main_thread
def stop_recording():
	recorder.stopRecordingWithHandler_(stop_handler)

def begin():
	path1 = os.path.abspath(inspect.stack()[0][1])
	path1 = re.sub(r'.*ents/', '', path1)
	path1 = "pythonista3://" + path1
	path1 = path1.replace("<string>","")
	path1 = path1.replace("r3cord3r.py","r3cord3r.py?action=run&argv=b")
	path2 = path1.replace("b","s")
	#start_recording()
	import string, time, console
	time.sleep(2)
	console.clear()
	mix = string.ascii_uppercase + string.digits
	word = "R3CORD3R"
	amt = len(word)
	console.set_font("Menlo",30)
	print ""
	def mk(size=1):
		data = []
		for i in range(size):
			data.append(random.choice(mix))
		return "".join(data)
	
	for i in range(amt):
		temp = mk(amt)
		sys.stdout.write("\r\t\t "+temp)
		time.sleep(0.05)
	for i in range(amt):
		temp = mk(amt-2)
		sys.stdout.write("\r\t\t "+temp+word[6]+mk(1))
		time.sleep(0.05)
	for i in range(amt):
		temp = mk(amt-7)
		sys.stdout.write("\r\t\t "+temp+word[1]+mk(4)+word[6]+mk())
		time.sleep(0.05)
	for i in range(amt):
		temp = mk(amt-7)
		sys.stdout.write("\r\t\t "+temp+word[1]+mk()+word[3]+word[6]+mk())
		time.sleep(0.05)
	for i in range(amt):
		temp = mk(amt-7)
		sys.stdout.write("\r\t\t "+word[:2]+mk(4)+word[6]+mk())
		time.sleep(0.05)
	for i in range(amt):
		temp = mk(amt-7)
		sys.stdout.write("\r\t\t "+word[:2]+mk(4)+word[6]+"R")
		time.sleep(0.05)
	for i in range(amt):
		temp = mk(amt-7)
		sys.stdout.write("\r\t\t "+word[:3]+mk(3)+word[6]+"R")
		time.sleep(0.05)
	for i in range(amt):
		temp = mk(amt-7)
		sys.stdout.write("\r\t\t "+word[:3]+mk(2)+"D3R")
		time.sleep(0.05)
	for i in range(amt):
		temp = mk(amt-7)
		sys.stdout.write("\r\t\t "+word)
		time.sleep(0.05)
	print "\r\t\t R3CORD3R"
	console.set_font()
	print " " * 9 + "By: Russian Otter\n"
	sys.stdout.write("          \r")
	console.write_link("Start Recording",path1)
	print ""
	sys.stdout.write("           \r")
	console.write_link("End Recording",path2)

if __name__ == "__main__":
	try:
		if sys.argv[1] == "b":
			start_recording()
		if sys.argv[1] == "s":
			stop_recording()
	except:
		begin()
		pass

import urllib, sys
baseurl = "http://keepvid.com/?url="
baseurl = baseurl + raw_input("Video Link: ")
a = urllib.urlopen(baseurl)
b = a.read()
b = b.split("1080P/4K (Pro Version)</td>")[1]
b.split("""position:absolute;background-color:#fff;padding:4px 10px;box-shadow: 10px 10px 5px #888888;left:\'+parseFloat(xx+10)+\'px;top:\'+ parseFloat(yy+$(window).scrollTop()+10)+\'px">\'+$""")[0]
b = b.replace("\n","").replace("\r","").replace("\t","")
b = b.split('class="btn btn-outline btn-sm')
outs = []
for _ in b:
	if "Max 720p" in _:
		outs.append(("720p",_))
	if "128 kbps" in _:
		outs.append(("M4A",_))
	if "WEBM" in _:
		outs.append(("webm",_))
	if "3GP" in _:
		outs.append(("3GP",_))
print "1.) "+outs[0][0]
opt1 = outs[0][1].split('href="')[1].replace('"  ',"")
print "2.) "+outs[1][0]
opt2 = outs[1][1].split('href="')[1].replace('"  ',"")
print "3.) "+outs[2][0]
opt3 = outs[2][1].split('href="')[1].replace('"  ',"")
print "4.) "+outs[3][0]
opt4 = outs[3][1].split('href="')[1].replace('"  ',"")
print "5.) "+outs[4][0]
opt5 = outs[4][1].split('href="')[1].replace('"  ',"")
inp = input("Number Wanted: ")
if inp == 1:
	newurl = opt1
	name = raw_input("Video type is .")
	name = opt1.split("title=")[1].replace("+"," ").replace("%3F","."+name)
if inp == 2:
	newurl = opt2
	name = raw_input("Video type is .")
	name = opt2.split("title=")[1].replace("+"," ").split("%3F")[0]+"."+name
if inp == 3:
	newurl = opt3
	name = raw_input("Video type is .")
	name = opt3.split("title=")[1].replace("+"," ").split("%3F")[0]+"."+name
if inp == 4:
	newurl = opt4
	name = raw_input("Video type is .")
	name = opt4.split("title=")[1].replace("+"," ").split("%3F")[0]+"."+name
if inp == 5:
	newurl = opt5
	name = raw_input("Video type is .")
	name = opt5.split("title=")[1].replace("+"," ").split("%3F")[0]+"."+name
else:
	sys.exit()
get=urllib.FancyURLopener()
get.retrieve(newurl,name)

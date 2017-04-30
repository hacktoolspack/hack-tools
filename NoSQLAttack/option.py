import globalVar as GlobalVar

def option():
    '''
    global victim
    global webPort
    global uri
    global https
    https = 1
    global platform
    global httpMethod
    global postData
    global myIP
    global myPort
    global verb
    global mmSelect
    global dbPort
    global requestHeaders#
    global optionSet
    optionSet = [False]*9
#    GlobalVar.set_optionSet(0,True);
#    print GlobalVar.get_optionSet(0);

    requestHeaders = {}
    '''
    optSelect = True
#print "test"
    if GlobalVar.get_optionSet(0) == False:
#    if optionSet[0] == False:
        GlobalVar.set_victim("Not Set")
    if GlobalVar.get_optionSet(1) == False:
        GlobalVar.set_webPort(80)
        GlobalVar.set_optionSet(1,True)
    if GlobalVar.get_optionSet(2) == False: #Set App Path (Current: Not Set)
        GlobalVar.set_url("Not Set")
    if GlobalVar.get_optionSet(3) == False:
        GlobalVar.set_httpMethod("GET")
    if GlobalVar.get_optionSet(4) == False:
        GlobalVar.set_myIP("127.0.0.1")
        GlobalVar.set_optionSet(4, True)
    if GlobalVar.get_optionSet(5) == False:
        GlobalVar.set_myPort("Not Set")
    if GlobalVar.get_optionSet(6) == False:
        GlobalVar.set_verb("OFF")
    if GlobalVar.get_optionSet(8) == False:
        GlobalVar.set_https("OFF")
        GlobalVar.set_optionSet(8, True)
    while optSelect:
        print "\n\n"
        print "Options"
        print "1-Set target host/IP (Current: " + str(GlobalVar.get_victim()) + ")"
        print "2-Set web app port (Current: " + str(GlobalVar.get_webPort()) + ")"
        print "3-Set App Path (Current: " + str(GlobalVar.get_url()) + ")"
        print "4-Toggle HTTPS (Current: " + str(GlobalVar.get_https()) + ")" # set http or https
        print "5-Set " + GlobalVar.get_platform() + " Port (Current : " + str(GlobalVar.get_dbPort()) + ")"
        print "6-Set HTTP Request Method (GET/POST) (Current: " + GlobalVar.get_httpMethod() + ")"
        print "7-Set my local " + GlobalVar.get_platform() + "/Shell IP (Current: " + str(GlobalVar.get_myIP()) + ")"
        print "8-Set shell listener port (Current: " + str(GlobalVar.get_myPort()) + ")"
        print "9-Toggle Verbose Mode: (Current: " + str(GlobalVar.get_verb()) + ")" # more detail infor while attacking
        print "x-Back to main menu"
        select = raw_input("Set an option:")

        if select == '1':
#            optionSet[0] = False
            GlobalVar.set_optionSet(0,False) #if reset host ip, optionSet[0] should be false again
            while GlobalVar.get_optionSet(0) == False:
                notDNS = True
                goodDigits = True
                victim = raw_input("Enter host or IP/DNS name:")
                octets = victim.split(".")
                if len(octets) != 4:
                    GlobalVar.set_optionSet(0,False)
                    notDNS = False
                else:
                    for item in octets:
                        try:
                            if int(item)<0 or int(item)>255:
                                print "Bad octets in IP address."
                                goodDigits = False
                        except:
                            notDNS = False
                if goodDigits == True or notDNS == False:
                    print "\nTarget set to:" + victim + "\n"
                    GlobalVar.set_victim(victim)
                    GlobalVar.set_optionSet(0,True)
        elif select == '3':
            url = raw_input("Enter URL path(Press enter for no URL):")
            print "\nHTTP port set to " + str(GlobalVar.get_webPort()) + "\n"
            GlobalVar.set_optionSet(2,True)
            GlobalVar.set_url(url)


        elif select == '7':
            GlobalVar.set_optionSet(4,False)
            while GlobalVar.get_optionSet(4) == False:
                goodLen = False
                goodDigits = True
                myIP = raw_input("Enter host IP for my "+ GlobalVar.get_platform() +"/Shells:")
                octets = myIP.split(".")
                if len(octets) != 4:
                    print "Invalid IP length."
                else:
                    goodLen = True
                    for item in octets:
                        try:
                            if int(item)<0 or int(item)>255:
                                print "Bad octets in IP address."
                                goodDigits = False
                        except:
                            goodDigits = False
                if goodDigits == True and goodLen == True:
                    print "\nShell/DB listener set to "+ myIP +"\n"
                    GlobalVar.set_myIP(myIP)
                    GlobalVar.set_optionSet(4,True)

        elif select == "9":
            if GlobalVar.get_verb() == "OFF":
                print "Verbose output enabled."
                GlobalVar.set_verb("ON")
                GlobalVar.set_optionSet(6,True)

            elif GlobalVar.get_verb() == "ON":
                print "Verbose output disabled."
                GlobalVar.set_verb("OFF")
                GlobalVar.set_optionSet(6, True)
        elif select == 'x':
            return



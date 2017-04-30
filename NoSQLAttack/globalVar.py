class GlobalVar:
    optionSet = [False] * 9
    yes_tag = ['y', 'Y'] # easy for users to choose "y" or "Y"
    no_tag = ['n', 'N']
    victim = "Not Set" # target IP
    webPort = 80
    url = "Not Set"
    httpMethod= "Not Set"
    platform = "Not Set"
    https = "Not Set" # use http or https for attacking URL
    myIP = "Not Set" # local IP
    myPort = "Not Set" # local port
    verb = "Not Set" # verbose mode mean user can get more detail info while attacking
    scanNeedCreds = "Not Set"
    dbPort = 27017
    vulnAddrs = []
    possAddrs = []
def set_vulnAddrs(value):
    GlobalVar.vulnAddrs.append(value)
def get_vulnAddrs():
    return GlobalVar.vulnAddrs

def set_possAddrs(value):
    GlobalVar.possAddrs.append(value)
def get_possAddrs():
    return GlobalVar.possAddrs

def set_optionSet(i,value):
    GlobalVar.optionSet[i]=value
def get_optionSet(i):
    return GlobalVar.optionSet[i]

def get_yes_tag():
    return GlobalVar.yes_tag
def get_no_tag():
    return GlobalVar.no_tag

def set_victim(value):
    GlobalVar.victim = value
def get_victim():
    return GlobalVar.victim

def set_webPort(value):
    GlobalVar.webPort = value
def get_webPort():
    return GlobalVar.webPort

def set_url(value):
    GlobalVar.url = value
def get_url():
    return GlobalVar.url;

def set_httpMethod(value):
    GlobalVar.httpMethod = value
def get_httpMethod():
    return GlobalVar.httpMethod

def set_platform(value):
    GlobalVar.platform = value
def get_platform():
    return GlobalVar.platform

def set_myIP(value):
    GlobalVar.myIP = value
def get_myIP():
    return GlobalVar.myIP

def set_myPort(value):
    GlobalVar.myPort = value
def get_myPort():
    return GlobalVar.myPort

def set_dbPort(value):
    GlobalVar.dbPort = value
def get_dbPort():
    return GlobalVar.dbPort

def set_https(value):
    GlobalVar.https = value
def get_https():
    return GlobalVar.https;

def set_verb(value):
    GlobalVar.verb = value
def get_verb():
    return GlobalVar.verb

scanNeedCreds = "not set"
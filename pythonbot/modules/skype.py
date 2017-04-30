import sqlite3
import os

def findProfiles(user=None):
	if user != None and user != "root":
		paths = os.popen("find /Users/%s/Library/Application\ Support/Skype -name 'main.db'" % user).read().strip().split('\n')
	else:
		paths = os.popen("find /*/*/Users/*/Library/Application\ Support/Skype -name 'main.db'").read().strip().split('\n')
		root_skypes = os.popen("find /var/root/Library/Application\ Support/Skype -name 'main.db'").read().strip().split('\n')
		for path in root_skypes:
			if len(path) > 0:
				paths.append(path)
	return paths

def skypeProfile(skypeDBs):
	for DB in skypeDBs:
		conn = sqlite3.connect(DB)
		c = conn.cursor()
		c.execute("SELECT fullname, skypename, city, country, datetime(profile_timestamp,'unixepoch') FROM Accounts;") 
		for row in c:
			yield '[*] -- Found Account --'
			yield '[+] User: '+str(row[0])
			yield '[+] Skype Username: '+str(row[1])
			yield '[+] Location: '+str(row[2])+','+str(row[3])
			yield '[+] Profile Date: '+str(row[4])

def skypeContacts(skypeDBs):
	for DB in skypeDBs:	
		conn = sqlite3.connect(DB)
		c = conn.cursor()
		c.execute("SELECT displayname, skypename, city, country, phone_mobile, birthday FROM Contacts;") 
		for row in c:
			yield('\n[*] -- Found Contact --')
			yield('[+] User                : %s' % row[0])
			yield('[+] Skype Username      : %s' % row[1])

			if str(row[2]) != '' and str(row[2]) != 'None':
				yield('[+] Location            : %s,%s' % (row[2],row[3]))

			if str(row[4]) != 'None':
				yield('[+] Mobile Number       : %s' % row[4])

			if str(row[5]) != 'None':
				yield('[+] Birthday            : %s' % row[5])


def skypeCalls(skypeDBs):
	for DB in skypeDBs:
		conn = sqlite3.connect(DB)
		c = conn.cursor()
		c.execute("SELECT * FROM calls, conversations;")

		yield('\n[*] -- Found Calls --')
		for row in c:
			yield('[+] Time: %s' % row[0])
			yield('[+] Partner %s' % row[1])

def skypeMessages(skypeDBs):
    for DB in skypeDBs:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT datetime(timestamp,'unixepoch'), dialog_partner, author, body_xml FROM Messages;")
        messages = [];
        for row in c:
            try:
                if row[2] == row[1]:
                    tofrom = '[%s] From[%s] To[%s]: ' % (row[0], row[2], 'user')
                else:
                    tofrom = '[%s] From[%s] To[%s]: ' % (row[0], 'user', row[1])
                messages.append(tofrom.ljust(70)+row[3])
            except:
                pass
    return messages

def purgeMessages(skypeDBs, conversation_partner):
	for DB in skypeDBs:
		conn = sqlite3.connect(skypeDBs)
		c = conn.cursor()
		c.execute("SELECT datetime(timestamp,'unixepoch'), dialog_partner, author, body_xml FROM Messages WHERE dialog_partner = '%s'" % conversation_partner)
		c.execute("DELETE FROM messages WHERE skypename = '%s'" % conversation_partner)
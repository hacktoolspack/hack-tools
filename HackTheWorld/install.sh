#!/bin/bash


arch="$(uname -m)"
wine32=/usr/lib/wine/wine
#echo $arch
BOLD="\033[01;01m"     # Highlight
RED="\033[01;31m"      # Issues/Errors
GREEN="\033[01;32m"    # Success
YELLOW="\033[01;33m"   # Warnings/Information
RESET="\033[00m"
echo ""
if [  -e /usr/bin/msfvenom ]; then
    echo -e $GREEN "[ ✔ ] Msfvenom ................[ found ]"
else 
	echo -e $RED "[ X ] Msfvenom -> not found "
	echo -e "\n [*] ${YELLOW} Installing Metasploit-framework ${RESET}\n"
	sudo apt-get install metasploit-framework 
	echo -e $GREEN " Start the install.sh File  Again"
	exit 0
	
fi

if [  -e /usr/bin/wine ]; then
    echo -e $GREEN "[ ✔ ] Wine ....................[ found ]"
else 
	echo -e $RED "[ X ] Wine -> not found "
      	sudo apt-get -qq update
	echo -e "\n [*] ${YELLOW}Adding x86 architecture to x86_64 system for Wine${RESET}\n"
      	sudo dpkg --add-architecture i386
      	sudo apt-get -qq update
	sudo apt-get install wine
	echo -e $GREEN " Start the install.sh File  Again"
	exit 0
fi


if [  -e /usr/bin/x86_64-w64-mingw32-gcc ]; then
    echo -e $GREEN "[ ✔ ] Mingw-w64 Compiler.......[ found ]"
else 
	echo "deb http://http.kali.org/kali kali-rolling main non-free contrib
deb http://http.kali.org/kali kali-rolling main contrib non-free" >> /etc/apt/sources.list
	echo -e $RED "[ X ] Mingw-w64 -> not found "
	#sudo apt-get install mingw-w64 mingw32 -y
	sudo apt-get install mingw-w64 mingw32 --force-yes -y
	echo -e $GREEN " Start the install.sh File  Again"
	exit 0
	
fi

echo "";
    echo "[✔] Dependencies installed successfully! [✔]";
    echo "";
    echo "[✔]==========================================================================[✔]";
    echo "[✔]      All is done!! You can execute by typing \"python HackTheWorld.py\"    [✔]";
    echo "[✔]==========================================================================[✔]";
    echo "";

exit 0


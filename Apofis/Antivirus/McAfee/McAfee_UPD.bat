@echo off
del *.tar
wget.exe -N ftp://ftp.mcafee.com/pub/antivirus/datfiles/4.x/*.tar
7z.exe x -o "%cd%" -y "*.zip"
exit
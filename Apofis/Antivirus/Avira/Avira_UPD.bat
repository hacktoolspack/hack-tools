@echo off
del /f /q *.zip
wget.exe -N http://dl.antivir.de/down/vdf/ivdf_fusebundle_nt_en.zip
7z.exe x -o "%cd%" -y "*.zip"
exit
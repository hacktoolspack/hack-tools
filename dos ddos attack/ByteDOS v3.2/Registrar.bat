@echo off
cls

Rem Modificado by PiToLoKo
REM Visita Foro.ElHacker.Net
 
echo **** REGISTRAR OCX O DLL ****
echo.
For /f "tokens=*" %%a in ('dir /B "%cd%\*.dll"; "%cd%\*.ocx"') do (
	copy /y "%cd%\%%a" "%windir%\system32\" >nul
	regsvr32 "%windir%\system32\%%a" /s)
echo.
pause 
exit
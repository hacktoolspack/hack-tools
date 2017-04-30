@echo off 
setlocal ENABLEDELAYEDEXPANSION 
 @FOR /F "usebackq eol=- skip=1 delims=\" %%j IN (`net view ^| find "命令成功完成" /v ^|find
 "The command completed successfully." /v`) DO ( 
 @FOR /F "usebackq delims=" %%i IN (`@ping -n 1 -4 %%j ^| findstr "Pinging"`) DO ( 
 @FOR /F "usebackq tokens=2 delims=[]" %%k IN (`echo %%i`) DO (echo \\%%k  [%%j]) 
 ) 
 ) 

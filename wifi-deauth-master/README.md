### WiFi Deauth

This is a quick implementation of an 802.11 deauthentication attack using Python and Scapy.

#### Requirements
 
 * Python 2.7
 * A wireless device (and driver) with monitor mode capabilities
 * [Scapy](http://www.secdev.org/projects/scapy/)
 * Linux (w/ availability of `iw` command)
 
#### Description

There are three type of attacks that can be performed, given a monitor-mode interface and the MAC address of an access point reachable through that interface:

  * Standard deauth attack against a single client MAC address
    * This injects deauthentication packets coming from and sent to this client address, and repeats the injection fifty times.
  * Global deauth attack
    * Although not really effective, this attack injects broadcast disassociation as well as deauthentication packets sent from the given BSSID.
  * Deauth attack against discovered client addresses
    * This will sniff the network, gather client addresses and finally launch the first attack for every address found.
    
Optionally, the user can specify how many times the attack will be iterated, and also how long the program will wait between each iteration (actually, this time is randomly calculated after the minimum and maximum times supplied by the user).

<b>Note:</b> in order to execute the attack, the program will first find the channel used by the access point and then set this channel to the given interface. This action might occasionally fail (for example, if the interface is in use by other applications).

#### Usage

See command-line options using switch `-h`. In particular, the only mandatory options are the name of the monitor-mode interface (`-i`) and the targeted BSSID (`-b`). 
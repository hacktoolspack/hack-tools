DDosPing
--------

DDoSPing is a remote network scanner for the most common Distributed Denial
of Service programs (often called Zombies by the press). These were the programs
responsible for the recent rash of attacks on high profile web sites.

This tool will (hopefully!) detect Trinoo, Stacheldraht and Tribe Flood Network
programs running with their default settings, although configuration of each program
type is possible from the tool's configuartion screen. Scanning is performed by
sending the appropriate UDP and ICMP messages at a controlable rate to a user defined
range of addresses.

DdosPing requires Winsock 2 to run. If you are running Windows 95 without the
Winsock 2 upgrade you will need to visit Microsoft's web site to obtain their
upgrade. The quickest way to find it is to go to http://www.microsoft.com and
perform a search in their knowledge base for article number Q182108.

I am releasing this program for testing by responsible network admins and anybody
who can confirm whether it is working correctly or not. I have been unwilling
to test it myself with live subjects on the Internet for risk of being accused
of attempted malicious attacks and besides that, it would be considered rude to
probe machines that did not belong to me or that I didn't have permission to
use the program on. The same goes for anybody who uses this program.

DDoSPing 2.00
-------------

Version 2.00 does not represent any additional functionality to previous
versions of DDoSPing, it simply signifies the fact that DDoSPing has
been acquired by Foundstone (http://www.foundstone.com).

Version 1.03
------------

o  Added buttons to switch between Windows and UNIX default configurations
   for Trinoo.

Version 1.02
------------

o  Changed trinoo default ports and "ping" text to comply with what seems
   to be the correct settings for Win.trinoo agents.
o  Hopefully fixed the "Winsock 10048" error when running the program
   for a second time.


----------------------------------------------------------------------
http://www.foundstone.com
robin.keir@foundstone.com

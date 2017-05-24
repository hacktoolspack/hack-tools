# dhcp_dos

dhcp_dos is the easiest way to do a DHCP Denial Of Service attack.


The DOS attacks supported are:
- [Starvation](http://hakipedia.com/index.php/DHCP_Starvation)
- [Consumption](http://www.cisco.com/c/en/us/products/collateral/switches/catalyst-6500-series-switches/white_Paper_C11_603833.html)

## Parameter

  - -i or --interface: used to specify the interface to use for the attack. You **must** use this.
  - -f or --flood: execute a *DHCP starvation* attack instead of the default *DHCP consumption*

## Requirements

- The [Scapy](http://www.secdev.org/projects/scapy/) Python library
- tcpdump

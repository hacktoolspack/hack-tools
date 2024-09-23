XSS ChEF - Chrome Extension Exploitation Framework
======

by [Krzysztof Kotowicz](http://blog.kotowicz.net)
ver 1.0

https://github.com/koto/xsschef

![](https://github.com/koto/xsschef/raw/master/bootstrap/img/xss-chef.png "Logo by Gareth Heyes")

About
-----
This is a Chrome Extension Exploitation Framework - think [BeEF](http://beefproject.com/) for Chrome extensions.
Whenever you encounter a XSS vulnerability in Chrome extension, ChEF will ease the exploitation.

What can you actually do (when having appropriate permissions)?
    
  - Monitor open tabs of victims
  - Execute JS on every tab (global XSS)
  - Extract HTML, read/write cookies (also httpOnly), localStorage
  - Get and manipulate browser history
  - Stay persistent until whole browser is closed (or even futher if you can persist in extensions' localStorage)
  - Make screenshot of victims window
  - Further exploit e.g. via attaching BeEF hooks, keyloggers etc.
  - Explore filesystem through file:// protocol
  - Bypass Chrome extensions content script sandbox to interact directly with page JS

Demo
----
See http://youtu.be/KmIG2EKLP2M for a demonstrational video. BeEF hooking: http://youtu.be/uonVWh0QO1A

Installation & usage
------------
### Setup CHeF server (on attacker's machine)

ChEF has three spearate backends to choose from: *PHP/XHR*, *PHP/WebSockets* and *node.js/WebSockets* version.

#### PHP 
PHP backends require only a PHP and a HTTP server (Apache/nginx) for hosting attacker command & control center.

You can choose one of two flavours:

 WebSockets (recommended) - requires launching a PHP WebSocket server that will listen on a separate TCP port.
 XHR - Legacy mode. Communication with hooked browsers has certain latency as it is based on XMLHttpRequest polling.

To install PHP version just download the files somewhere within your document root.

   $ mv xsschef /var/www/

If you want to use XHR backend, you're done. If you want to use the WebSockets backend, additionally lauch a PHP WebSocket server:

   $ php server.php [port=8080] [host=127.0.0.1] 2>log.txt

#### Node.js
Node.js version requires a [node.js](http://nodejs.org/) installation and is much faster as it is based on [WebSockets](http://dev.w3.org/html5/websockets/) protocol.

Installation:

    $ npm install websocket
      // windows users: npm install websocket@1.0.3
      // see https://github.com/Worlize/WebSocket-Node/issues/28
    $ npm install node-static
    $ node server.js [chosen-tcp-port] 2>log.txt
    
### Launch CHeF console (on attacker's machine)
  - PHP/WebSockets: http://127.0.0.1/console.html
  - PHP/XHR: http://127.0.0.1/console.html?server_type=xhr
  - node.js/WebSockets: http://127.0.0.1:8080/

### Hook Chrome extension (on victim's)
First, you have to find a XSS vulnerability in a Google Chrome addon. I won't help you here.
This is similar to looking for XSS in webpages, but totally different, as there are way more DOM based XSSes than reflected ones and the debugging is different.

Once you found a vulnerable extension, inject it with CheF hook script. See 'hook' menu item in console UI for the hook code.

ChEF ships with an exemplary XSS-able chrome addon in `vulnerable_chrome_extension` directory. Install this unpackaged extension (Tools, Extensions, Developer mode, load unpacked extension) in Chrome to test.

### Exploit ###
Once code has been injected and run, a notification should be sent to console, so you can choose the hook by clicking on a 'choose hooked browser' icon on the left and start exploiting.

How does it work?
=================


                   ATTACKER                                VICTIM(S)

                                                                          +------------+
                                                                          |  tab 1     |
                                                                 command  | http://..  |
                                                               +---------->            |
                                                               |          +------------+
                                                               |
       +------------+                              +-----------+-+
       |  console   |                              | addon w/XSS |  result+------------+
       |            |   +-------------+  (XHR/WS)  |             |<------+|  tab 2     |
       |            |+->| ChEF server |<----------+|             |+------>+ https://.. |
       |            |<-+|             |+---------->|  ChEF hook  |        |            |
       |            |   +-------------+            |             |        +------------+
       +------------+                              +-----------+-+
                                                               |
                                                               |          +------------+
                                                               |          |  tab 3     |
                                                               +----------> https://.. |
                                                                          |            |
                                                                          +------------+
                                                                          
Chrome addons usually have permissions to access inidividual tabs in the browser. They can also inject JS code into those tabs. So addons are theoretically cabable of doing a global XSS on any tab. When there is a exploitable XSS vulnerability within a Chrome addon, attacker (with ChEF server) can do exactly that. 

Script injected into Chrome extension (ChEF hook served from a ChEF server) moves to extension background page and installs JS code into every tab it has access to. This JS code listens for various commands from the addon and responds to them. And ChEF-hooked addon receives commands and responds to them by connecting to CHeF server on attackers machine (using XMLHttpRequest or WebSockets connection). Attacker has also a nice web-based UI console to control this whole XSS-based botnet.

Exploitability requirements
===========================
Vulnerable extension needs to have:

  - `tabs` permissions
  - origin permission for sites you want to interact with - ideally, `<all_urls>` or `http://*/*`
  - background page for the code to persist. ChEF will try to work anyways, but it will be very limited in functionality.
  - no [CSP](http://code.google.com/chrome/extensions/trunk/contentSecurityPolicy.html) restrictions i.e. [manifest v1.0 in Chrome 18+](http://blog.chromium.org/2012/02/more-secure-extensions-by-default.html)
  
To be able to read/write cookies, `cookies` permission is needed, though you can get non httpOnly cookies with `eval()`. To manipulate history, `history` permission is needed.

More info
=========
XSS ChEF was demonstrated during Black Hat USA 2012 *Advanced Chrome Extension Exploitation: Leveraging API powers for Better Evil* workshops.
There is more info about the workshops and XSS ChEF in [the whitepaper](http://kotowicz.net/bh2012/advanced-chrome-extension-exploitation-osborn-kotowicz.pdf)

Licence
-------
XSS ChEF - Chrome Extension Exploitation framework
Copyright (C) 2012  Krzysztof Kotowicz - http://blog.kotowicz.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.

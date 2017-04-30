IRC botnet for Controlling Mac OS X Computers
========

## Install:
1. Download and run [Droplet.app](https://github.com/nikisweeting/python-medusa/raw/master/Droplet.app.zip) on a **computer you are willing to compromise (this is a botnet that exposes unlimited access to your computer!)** (or in a VM)
2. Log into the `##medusa` IRC channel on [irc.freenode.net](https://webchat.freenode.net/) and type a command (e.g. `!status`)

## Developer Install:
```bash
git clone https://github.com/pirate/python-medusa.git
cd python-medusa
nano bot.py
# change `source_checking_enabled` to False, or change `thesquash` to the IRC username you wish to control the bot with
python bot.py
# Log into the `##medusa` IRC channel on irc.freenode.net and type a command (e.g. `!status`)
```

## Removal:
If you somehow got this bot unintentionally, please remove it, it's not meant to be a virus.

1. Open Terminal.app
2. Run this command to kill the bot: 
```sh
sudo kill `ps -ax|grep -v grep|grep bot.py|head -1|awk '{print $1}'`
```
(3.) If you want to remove its runtime files and logs, run the following:

```sh
sudo launchctl unload -w /Library/LaunchDaemons/sys.daemon.connectd.plist
sudo rm -Rf /var/softupdated
sudo rm /Library/LaunchDaemons/sys.daemon.connectd.plist
sudo kill `ps -ax|grep -v grep|grep bot.py|head -1|awk '{print $1}'`
```

## Information:  
Nick Sweeting 2015 -- MIT License  

After reading a [book](http://books.google.com/books/about/Violent_Python.html?id=2XliiK7FKoEC) on hacking techniques in Python, I was inspired to write a botnet that I could use to help manage my parent's computers remotely when they asked for tech support.  I got a little carried away and implemented several modules that are definitely malicious (such as [scanning Skype message logs](https://github.com/pirate/python-medusa/blob/master/modules/skype.py) and network traffic for [credit card numbers](https://github.com/pirate/python-medusa/blob/master/modules/cardcheck.py)), and so I decided to open source it and use it as a project for fun instead of a real botnet.  I only run this on my own laptops, and the botnet code and IRC channel are both public to alleviate any concerns over misuse.  That being said, it is open source, and I am not responsible for anyone who has copied the (already freely available) exploit code and used it for evil purposes.

As of 2015 Sept. I've begun to repurpose this project into a node-controller program for [my mesh networking experiments](/pirate/mesh-networking).  The current goal is to make a botnet that communicates over all network interfaces, forming its own internally routed network by finding the minimum spanning trees between infected nodes.  I plan to integrate Apple's native MultiPeerConnectivityFramework (Bluetooth+Wifi+Bonjour), as well as raw Wifi & Ethernet sockets, audio (see [quietnet](https://github.com/Katee/quietnet)), IRC, and [WebRTC](https://github.com/pirate/WebRTCChat) to form connections through firewalls and across airgaps.  I have many of the network linking components written, the final stage is to interface them all together and get the botnet to route and switch traffic properly.

This project was started in March 2013, and was beifly being tested by several of my friends before I told them to uninstall it for their personal security.  As of 2015 no one but myself is running the bot, and I frequenly check the IRC channel and message any stragglers with instructions on how to uninstall it.

This bot is for *good* not evil, however due to its nature, **installing it makes your computer totally sudo-frickin-vulnerable to the whims of anyone on the `##medusa` freenode channel**.  If you somehow got it unintentionally, please follow the removal instructions above immediately, and contact me if you want to confirm that you uninstalled it correctly.

Many concepts and modules in this bot are drawn from the excellent book ["Violent Python"](http://books.google.com/books/about/Violent_Python.html?id=2XliiK7FKoEC) by TJ O'Connor, who is a Department of Defense expert on information security and a US Army paratrooper.  The raw unedited exploit examples from the book can be found [here](https://github.com/shadow-box/Violent-Python-Examples).

Screenshots:  
========
**1. Trojan impersonates Google Chrome and unwitting victim types in their password*:**  
![](http://i.imgur.com/200NfKl.png)  
**2. Bot installs installs itself with boot hook and connects to the C&C IRC channel:**  
![](http://i.imgur.com/FEIRtR3.png)  
**3. Victim can be controlled by sending a privmsg to the bot:**  
![](http://i.imgur.com/KJnwaGU.png)  
**4. Bots can be controlled en-masse by sending commands to the whole C&C channel:**
![](http://imgur.com/tu8y9ym.png)

\* I removed the Google Chrome trojan because I don't want script kiddies finding this and using it on people, it's trivial to modify Droplet.app into a real trojan if needed though.  
\*\* 2016 note: this infection vector no longer works due to Gatekeeper and SIP.  Gatekeeper prevents a fake Chrome from launching without a valid developer ID, and SIP prevents the installer from copying files into `/var/`.


Beginner's Contributor Guide:  
========

1. Install the [Github App](http://mac.github.com) or [GitUp](http://gitup.co/) for an easy GUI
2. Pick a folder to store your code in
3. Download the source to that folder:

  ```bash
  cd ~/Desktop/
  git clone https://github.com/pirate/python-medusa.git
  cd python-medusa
  ```
4. To run it and debug, do the following:
  ```bash
  sudo ./test.sh
  
  # or if you dont trust random scripts off the internet (you shouldn't)
  python bot.py & tail -f bot_v*.log
  ```

  
* Listen to badass music, you're a real hacker now!  
* Pick a good editor like [Sublime Text 3](http://appdl.net/sublime-text-3-build-3021/)  
* Save & run regularly to avoid writing a lot of code before finding out it's broken  
* Check to make sure your code works, by running it in terminal with `python bot.py &`   
* There is great documentation on Python all over the web: [http://www.python.org/doc/](http://www.python.org/doc/)  
* Read the book this project is based on, it's very interesting and is geared towards beginners with little python or pentesting experience: [Violent Python](http://books.google.com/books/about/Violent_Python.html?id=2XliiK7FKoEC)

## How to use Git

Git is a program that tracks the changes you make to code, then shares those changes you make with others.  A collection of code in one folder is called a "repository" (repo for short).  Groups of changes are put together to make a "commit".  You can view a history of all the commits made using `git log`.

**Editing locally**   

  1. Edit the code you want to edit, save it, test it, fix it, save it
  2. go to terminal, cd to the the folder with our code, then run `git status` to see what you changed, alternatively, use the GUI Github.app downloadable from github.com 
  3. Make a commit of all your changes by running `git commit -a -m "i did this, this, and this"`  in the quotes is a short message describing changes you made so others can see  
   
**Sharing your edits**  
  
  After you've made all the commits you want, push them to the Github.com  
  
  1. `git remote update` to make sure your local code is up to date  
  2. `git pull --rebase` to update your code if it isnt up to date  
  3. `git push origin master` to push your code  

# doork

description
----

doork is a open-source passive vulnerability auditor tool that automates the process of searching on Google information about specific website based on dorks.

doork can update his own database from ghdb and use it for find flaws without even contact the target endpoint.
You can provide your custom wordlist and save the output anywhere

installation
----

You can download doork by cloning the [Git](https://github.com/AeonDave/doork) repository:

    git clone https://github.com/AeonDave/doork doork

doork works with [Python](http://www.python.org/download/) version **2.6.x** and **2.7.x** on any platform.
You have also to install 

    pip install beautifulsoup4
    pip install requests
    pip install Django

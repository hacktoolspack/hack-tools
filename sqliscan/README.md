# sqli-scanner

This is a sql vulnerability scanner, intended for a list of urls. This is made to be multi-process, so it's much much faster than traditional single thread/process scanning. 

# Usage

```
    -------------------------------------------------------
    MASS
     _____ _____ __    _     _____
    |   __|     |  |  |_|___|   __|___ ___ ___ ___ ___ ___
    |__   |  |  |  |__| |___|__   |  _| .'|   |   | -_|  _|
    |_____|__  _|_____|_|   |_____|___|__,|_|_|_|_|___|_|
             |__|
                                                  the-c0d3r
    -------------------------------------------------------

usage: sqli-scanner.py [-h] [-f FILE] [-o OUTPUT] [-p PROCESSCOUNT] [-v]

Mass SQL vulnerability scanner

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Target file with URLs
  -o OUTPUT, --output OUTPUT
                        Output file to save vulnerable websites to
  -p PROCESSCOUNT, --processcount PROCESSCOUNT
                        Number of processes to generate
  -v, --verbose         Enable Verbose mode
```

Only 1 command argument is required to run this program. It is the `-f` arugment that provides the file where the urls are written inside. 

You can use `-p` to change the number of processes to generate. The default is the number of CPU the computer has, multiplied by 2. *If you use too much processes, it might have trouble stopping it.*

---
> If you have trouble stopping the processes with `Ctrl+C`, try `Ctrl+Z` to move it to background and then do `kill processID` to kill the process using the process ID. 



## Writing a Module

For __brut3k1t__, there are 2 types of modules.

1. core 
3. miscellaneous

---

A __core__ module is source code that instantiates a method for bruteforcing. These are found in the `core/` directory, and can be for web-based services, or network protocols. The ones that the author wrote are `web.py` and `protocols.py`. Core modules are run as so:

    python brut3k1t.py -a www.address.com -s service-name -u username -w wordlist.txt

Bear in mind that core modules are created for the main purpose of the brut3k1t framework: bruteforce. Any community written core module should follow such a standard.

---

__Miscellaneous__ modules are included as part of brut3k1t to help aide in the process of bruteforcing. Found in the `modules/` directory, these are often scripts that perform menial tasks, such as wordlist generation, proxy list checking, and XSS discovery so that the researcher is able to overcome discrepancies when conducting a bruteforce. In order to instantiate a module, these require the use of the `--module` flag:

    python brut3k1t.py --module THIS_MODULE [-otherflags 123]

---

Core and Miscellaneous modules are __community-supported__. You may help contribute by writing modules for brut3k1t. However, when doing so, please include the folowing as a block of comment. This is for structural purposes, as well as a to provide organization to the program. 

    '''
    module.py - My module for blah blah.

    Category: Core / Miscellaneous
    Description: 
        This module is really cool. It is the best ever. 
        It supports:
        - this 
        - that
        - and also this

    Dependencies: library1, library2

    Version: v.1.2.3
    Author: Me
    License: SomeLicense-x.x // https://somelicense.org

    '''
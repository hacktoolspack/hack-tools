#[中文说明](https://github.com/youngyangyang04/NoSQLAttack/blob/master/docs/README-zh.md)
#NoSQLAttack
#Introduction
NoSQLAttack is an open source Python tool to automate expose MongoDB server IP on the internet and disclose the database data by MongoDB default configuration weaknesses and injection attacks. Presently, this project focuses on MongoDB.

It is base on [NoSQLMap](http://www.nosqlmap.net/index.html), tcstool's popular NoSQL injection tool and [shodan](https://www.shodan.io/), first search engine for Internet-connected devices. 

Some attack tests are based on and extensions of follow papers
* [Diglossia: Detecting Code Injection Attacks with Precision and Efficiency](http://www.cs.cornell.edu/~shmat/shmat_ccs13.pdf)
* [No SQL, No Injection?](https://www.research.ibm.com/haifa/Workshops/security2015/present/Aviv_NoSQL-NoInjection.pdf)
* [Several thousand MongoDBs without access control on the Internet](https://cispa.saarland/wp-content/uploads/2015/02/MongoDB_documentation.pdf).

There are two systems for testing NoSQL injection in this  project-[NoSQLInjectionAttackDemo](https://github.com/youngyangyang04/NoSQLInjectionAttackDemo).
#Background
NoSQL injection attacks, for example php array injection, javascript injection and mongo shell injection, endanger  mongoDB.
There are thousands of mongoDB are exposed on the internet, and hacker can download data from exposed mongoDB.

#Requirements
On a Debian or Red Hat based system, NoSQLAttack's dependencies already be writen in setup.py.
This project is built on Pycharm COMMUNITY 2016.1 with python 2.7.10. 

Varies based on features used:
* Shodan-1.5.3
* httplib2-0.9
* Python-2.7
* pymongo-2.7.2
* requests-2.5.0
* ipcalc-1.1.3
* MongoDB


#Building
On Linux, it goes something like this:
```bash
cd NoSQLAttack
python setup.py install
```
#Tips
* If after entering "python setup.py install", terminal show error information "No module named setuptools", just install setuptools. On Ubuntu, "sudo apt-get install python-setuptools", this command is useful
* Install [MongoDB](https://docs.mongodb.com/manual/administration/install-on-linux/) for MongoDB default configuration attack.

#Usage
After building, you can run NoSQLAttack like this:
```bash
NoSQLAttack
```
Upon starting NoSQLAttack you are presented with the main menu:
```bash
================================================
        _   _       _____  _____ _                      
       | \ | |     /  ___||  _  | |                     
       |  \| | ___ \ `--. | | | | |                   
       | . ` |/ _ \ `--. \| | | | |                    
       | |\  | (_) /\__/ /\ \/' / |____          
       \_| \_/\___/\____/  \_/\_\_____/                  
                                        _          
    /\      _      _                   | |  _        
   /  \   _| |_  _| |    _____    ___  | | / /       
  / /\ \ |_   _||_   _| / __  \  / __| | |/ /        
 / /--\ \  | |_   | |_  | |_| | | |__  | |\ \       
/ / -- \ \ \___\  \___\ \______\ \___| | | \_\      
================================================    
NoSQLAttack-v0.2
sunxiuyang04@gmail.com


1-Scan attacked IP
2-Configurate parameters
3-MongoDB Access Attacks
4-Injection Attacks
x-Exit
```
#videos
NoSQLAttack Demo for MongoDB.

(1)default configuration Attacks demo  (2)injection attacks demo


<a href="https://www.youtube.com/watch?v=R6-nXCVNxEw" target="_blank"><img src="https://github.com/youngyangyang04/NoSQLAttack/blob/master/images/Screen%20Shot%202017-01-14%20at%202.33.10%20PM.png" alt="NoSQLAttack MongoDB default configuration Attacks demo" width="300" height="280" border="50" /></a> 
<a href="https://www.youtube.com/watch?v=R6-nXCVNxEw" target="_blank"><img src="https://github.com/youngyangyang04/NoSQLAttack/blob/master/images/Screen%20Shot%202017-01-14%20at%202.36.34%20PM.png" alt="NoSQLAttack MongoDB default configuration Attacks demo" width="300" height="280" border="50" /></a> 


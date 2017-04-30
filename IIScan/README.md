# IIS shortname Scanner #

Under certern circumstances, windows 8.3 short names may be bruteforce enumerated under IIS with .net enabled,

request these two urls:

* http://www.target.com/*~1****/a.aspx

* http://www.target.com/l1j1e*~1****/a.aspx

If the first one return HTTP 404 and the second one return no 404. Your server might be exploitable to this vulnerability.

## Change Log (Oct 27, 2016)
* Bug fixed: extention short than 4 letters like ```/webdeb~1.cs``` now could be enumerated
* Code reconstruction

## Usage

```
	iis_shortname_Scan.py target
```


from [http://www.lijiejie.com](http://www.lijiejie.com)    my[at]lijiejie.com

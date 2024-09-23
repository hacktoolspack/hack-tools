Codetective
=============
Sometimes we run into hashes and other artefacts and can't figure out where did they come from and how they were generated. This tool is able to recognise the output format of many different algorithms in many different possible encodings for analysis purposes. It also infers the levels of certainty for each finding based on traces of its representation .

This may be useful e.g. when you are testing systems from a security perspective and are able to grab a password file with hashed contents maybe from an exposed backup file or by dumping memory. This may also be useful as a part of a fingerprinting process or simply to verify valid implementations of different algorithms. You may also try running this tool against network traffic captures or large source code repositories to look out for interesting stuff.

You can either use a generic version or as a plugin for the Volatility framework. The usage is similar.

Changelog
--------

Version 0.8.1
--------
Finally a new version of Codetective is ready. This is close to a complete re-write with new features and many, many bug fixes. The code is still not something to look at but it’s now a lot more object oriented and easier to maintain. Now, codetective can also report the exact location of a finding and the ‘certainty’ feature is now numeric in order to include multiple factors with different weights and become more precise. The new entropy checks added to better detect cryptographic findings also take advantage of this and you can limit results being displayed only to findings with a specified minimum level of certainty (-m number).
A different approach regarding the way data is loaded into memory has been adopted so now Codetective will break data into slices and analyse them by turn. This is to prevent it from filling the memory when reading large files. To prevent losing results there is now an overlapping window which will make sure no findings are caught in the breaks (*). A verbose mode was also added, it’s now possible to see the progress status which can be useful for the longer runs.

Directory mode (-d rootPath) allows you to tell Codetective to look at folders rather than files and you can use it in recursive mode (-r) as well. if applied to large amounts of data, it might be useful to filter outputs by minimum certainty level e.g. -m 70. It also supports reading data from standard input.

A new filter was added called ‘personal’ and can be used for findings that may include personal data such as phone numbers and credit cards which are now supported as well. Other algorithms supported in the new version include web cookies, URLs and with the ‘generator’ option, Codetective will try to load all encoding/decoding supported by your Python environment (the ‘aliases’ module) and apply them in order to find something meaningful. This can be used to try multiple encoding (-g encode) or decodings (-g decode) or both (-g both). Preprocessors (-p) now allow binary structures to be first converted onto strings using the C struct packing string patterns. 
Finally, the ‘validators’ function now provides a powerful way to filter outputs. You may use up to 3 validators per run using the -v1 -v2 -v3 parameters respectively. Each validator it is a combination of a predicate ‘ALL’ or ‘HAS’ with a matching function such as UPPER for findings in upper case. Functions currently supported are :

* NUMERIC
* ALPHA
* LOWER
* UPPER
* ALPHANUMERIC
* SYMBOL

For a custom validator you can also provide your own regular expression using the predicate SEARCH followed by the desired regular expression.

(*) - you may have duplicate results because of this but will be addressed in future.

Supported filters are: win, web, unix, db, personal, crypto and other.
* web-cookie
* mssql2000
* md5
* URL
* md4
* phone number
* credit cards
* mssql2005
* lm hash
* ntlm hash
* MySQL4+
* MySQL323
* base64
* SAM(*:ntlm)
* SAM(lm:*)
* SAM(lm:ntlm)
* RipeMD320
* sha1
* sha224
* sha256
* sha384
* sha512
* whirpool
* CRC
* des-salt-unix
* sha256-salt-django
* sha256-django
* sha384-salt-django
* sha384-django
* sha256-salt-unix
* sha512-salt-unix
* apr1-salt-unix
* md5-salt-unix
* md5-wordpress
* md5-phpBB3
* md5-joomla2
* md5-salt-joomla2
* md5-joomla1
* md5-salt-joomla1
* blowfish-salt-unix
* uuid

Examples (old)
--------

	$ python codetective.py '79b61b093c3c063fd45f03d55493902f'
	confident: ['md5']
	likely: ['lm', 'ntlm', 'md5-joomla2', 'md5-joomla1']
	possible: ['md4', 'base64']

	$ python codetective.py '79B61B093C3C063FD45F03D55493902F'
	confident: ['md5', 'lm', 'ntlm']
	possible: ['md4', 'base64']

	$ python codetective.py '79B61B093C3C063FD45F03D55493902F:*'
	confident: ['md5', 'SAM(lm:*)']
	likely: ['lm', 'ntlm']
	possible: ['md4']

	$ python codetective.py -t win '79B61B093C3C063FD45F03D55493902F:*'
	confident: ['SAM(lm:*)']
	likely: ['md5', 'lm', 'ntlm']
	possible: ['md4']

	$ python codetective.py -a -t win '79B61B093C3C063FD45F03D55493902F:*'
	confident: ['SAM(lm:*)']
        	hashes in SAM file - LM:79B61B093C3C063FD45F03D55493902F        NTLM:not defined
	likely: ['md5', 'lm', 'ntlm']
	possible: ['md4']


	$ python vol.py codetective -n notepad -v -f JOHN-2CF071298B-20120318-024807.raw 
	Volatile Systems Volatility Framework 2.0

	Found 29 tasks
	kernel mapping...
	Calculating task mappings...
	Process: wuauclt.exe	PPID: 1120	Pid: 1908
	Process: vmtoolsd.exe	PPID: 688	Pid: 348
	Process: vmacthlp.exe	PPID: 688	Pid: 912
    Process: svchost.exe	PPID: 688	Pid: 976
	Process: smss.exe	PPID: 4	Pid: 384
	Process: explorer.exe	PPID: 1680	Pid: 1696
	Process: cmd.exe	PPID: 1696	Pid: 1520
	Process: svchost.exe	PPID: 688	Pid: 160
	Process: vmtoolsd.exe	PPID: 1696	Pid: 1820
	Process: lsass.exe	PPID: 644	Pid: 700
	Process: services.exe	PPID: 644	Pid: 688
	Process: alg.exe	PPID: 688	Pid: 1936
	Process: svchost.exe	PPID: 688	Pid: 924
	Process: csrss.exe	PPID: 384	Pid: 620
	Process: svchost.exe	PPID: 688	Pid: 1208
	Process: TPAutoConnSvc.e	PPID: 688	Pid: 1220
	Process: spoolsv.exe	PPID: 688	Pid: 1572
	Process: svchost.exe	PPID: 688	Pid: 1172
	Process: svchost.exe	PPID: 688	Pid: 1120
	Process: winlogon.exe	PPID: 384	Pid: 644
	Process: rundll32.exe	PPID: 1696	Pid: 1788
	Process: TPAutoConnect.e	PPID: 1220	Pid: 1256
	Process: notepad.exe	PPID: 1696	Pid: 1896
	
	=> at offset Virtual: 0x8012e000  	Physical: 0x12e000    	 Size: 0x1000        
	 Found md5 (likely) 	MD5 hash: 0A5AE0AB474FF954BA5FB5CC22691599
	 Found md4 (possible) 	MD4 hash: 0A5AE0AB474FF954BA5FB5CC22691599

	=> at offset Virtual: 0x8013d000  	Physical: 0x13d000    	 Size: 0x1000        
	 Found md5 (likely) 	MD5 hash: 4BE2C18D9154D0240B36AEF861085FEC
	 Found md4 (possible) 	MD4 hash: 4BE2C18D9154D0240B36AEF861085FEC

	=> at offset Virtual: 0x80153000  	Physical: 0x153000    	 Size: 0x1000        
	 Found md5 (likely) 	MD5 hash: 0B79C053C7D38EE4AB9A00CB3B5D2472
	 Found md4 (possible) 	MD4 hash: 0B79C053C7D38EE4AB9A00CB3B5D2472

	=> at offset Virtual: 0x80171000  	Physical: 0x171000    	 Size: 0x1000        
	 Found md5 (likely) 	MD5 hash: 10F84F9347B42F6428155C59A743D317
	 Found md4 (possible) 	MD4 hash: 10F84F9347B42F6428155C59A743D317

	=> at offset Virtual: 0x8018a000  	Physical: 0x18a000    	 Size: 0x1000        
	 Found md5 (likely) 	MD5 hash: 5046ab8cb6b1ce11920c00aa006c4972
	 Found md4 (possible) 	MD4 hash: 5046ab8cb6b1ce11920c00aa006c4972

	=> at offset Virtual: 0x801a2000  	Physical: 0x1a2000    	 Size: 0x1000        
	 Found md5 (likely) 	MD5 hash: C25F308FAE39B3A4D9E1561F679CD8AA
	 Found md4 (possible) 	MD4 hash: C25F308FAE39B3A4D9E1561F679CD8AA
	...	



	$ python codetective.py -a -f test.txt 
	Administrator:500:CC5E9ACBAD1B25C9AAD3B435B51404EE:996E6760CDDD8815A2C24A110CF040FB::: : {'confident': ['md5', 'SAM(lm:ntlm)'], 'likely': ['lm', 'ntlm'], 'possible': ['md4', 'des-salt-unix']}
   	     hashes in SAM file - LM:CC5E9ACBAD1B25C9AAD3B435B51404EE        NTLM:996E6760CDDD8815A2C24A110CF040FB
        	UNIX shadow file using salted DES - salt:Ad     hash:ministrator
	ibrahim:$1$hanhd/cF$3lzrzB14HceT7uc3oTmog1:14323:0:99999:7::: : {'confident': ['md5-salt-unix'], 'likely': [], 'possible': []}
        	UNIX shadow file using salted MD5 - salt:hanhd/cF       hash:3lzrzB14HceT7uc3oTmog1
	563DE3D2F07D0747BBE4BA2697AE33AA : {'confident': ['md5'], 'likely': ['lm', 'ntlm'], 'possible': ['md4', 'base64']}
		base64 decoded string: ??p?N?Ӿ;8
	463C8A7593A8A79078CB5C119424E62A : {'confident': ['md5'], 'likely': ['lm', 'ntlm'], 'possible': ['md4', 'base64']}
        	base64 decoded string: ?????p<?t????-u?????
	E852191079EA08B654CCF4C2F38A162E3E84EE04 : {'confident': [], 'likely': ['sha1'], 'possible': ['base64']}
        	base64 decoded string: ?v??t????z瀂??׭??O8M8
	94F94C9C97BFA92BD267F70E2ABD266B069428C282F30AD521D486A069918925 : {'confident': [], 'likely': ['sha256'], 'possible': ['base64']}
        	base64 decoded string: ??}?/B??E݁n???Cۮ?ӯx????aw???P??4??u?ݹ
	sha384$12345678$c0be393a500c7d42b1bd03a1a0a76302f7f472fc132f11ea6373659d0bd8675d04e12d8016d83001c327f0ab70843dd5 : {'confident': [], 'likely': ['sha384', 'sha384-salt-django'], 'possible': []}
        	Django shadow file using salted SHA384 - salt:12345678  hash:c0be393a500c7d42b1bd03a1a0a76302f7f472fc132f11ea6373659d0bd8675d04e12d8016d83001c327f0ab70843dd5
	5850478A34D818CE : {'confident': [], 'likely': ['mysql323'], 'possible': ['base64']}
        	base64 decoded string: ??t?߀????
        	MySQL v3.23 or previous hash: ['5850478A34D818CE']
	08EE13E9A295641BE6158366C0651B84A1AD9E47 : {'confident': [], 'likely': ['sha1'], 'possible': ['base64']}
        	base64 decoded string: ???q=oy?A?y?~?
                                             N??8P?N;
	****:7db9d24c238b77af11b99f0a67e99abe  : {'confident': ['md5'], 'likely': ['lm', 'ntlm', 'md5-joomla1'], 'possible': ['md4']}
        	Joomla v1 MD5 - hash:7db9d24c238b77af11b99f0a67e99abe
	****:d2f46e7173b1d88c9d7b2f52271cd8af:YEfafQuaj58ExG3V  : {'confident': ['md5', 'md5-salt-joomla1'], 'likely': ['lm', 'ntlm'], 'possible': ['md4']}
        	Joomla v1 salted MD5 - hash:d2f46e7173b1d88c9d7b2f52271cd8af    salt:YEfafQuaj58ExG3V
	****:4aad84c0929c72f1c72a9c884e5c0f18:tNT52oL0I8ClmMjO  : {'confident': ['md5', 'md5-salt-joomla1'], 'likely': ['lm', 'ntlm'], 'possible': ['md4']}
        	Joomla v1 salted MD5 - hash:4aad84c0929c72f1c72a9c884e5c0f18    salt:tNT52oL0I8ClmMjO
	****:1ad6692b7e3b2deb36606603ced0c8b6:LhiqX4pL3s8xy0qd  : {'confident': ['md5', 'md5-salt-joomla1'], 'likely': ['lm', 'ntlm'], 'possible': ['md4']}
        	Joomla v1 salted MD5 - hash:1ad6692b7e3b2deb36606603ced0c8b6    salt:LhiqX4pL3s8xy0qd
	dGVzdGUK : {'confident': [], 'likely': [], 'possible': ['base64']}
        	base64 decoded string: teste

Usage
-----

Generic version:
    usage: codetective.py [-h] [-t filters] [-a] [-v] [-m MIN_CERTAINTY]
			  [-p PREPROCESSOR] [-g GENERATOR] [-v1 VALIDATOR1]
			  [-v2 VALIDATOR2] [-v3 VALIDATOR3] [-r] [-f FILENAME]
			  [-d DIRECTORY] [-fp FILE_PATTERN] [-l] [-s] [-ver]
			  [string]

    a tool to determine the crypto/encoding algorithm used according to traces of
    its representation

    positional arguments:
      string                determine algorithm used for <string> according to its
			    data representation

    optional arguments:
      -h, --help            show this help message and exit
      -t filters            filter by source of your string. can be: win, web, db,
			    unix or other
      -a, -analyze          show more details whenever possible (expands shadow
			    files fields,...)
      -v, -verbose          verbose mode shows progress status (useful for large
			    files) and time taken
      -m MIN_CERTAINTY, -minimum-certainty MIN_CERTAINTY
			    specify the minimum acceptable certainty level for
			    displayed results (0 - 100)
      -p PREPROCESSOR, --preprocessor PREPROCESSOR
			    <struct format string> interpret bytes as packed
			    binary data. Unpacks contents from different data and
			    endianess types according to format strings patterns
			    as specified on:
			    https://docs.python.org/2/library/struct.html
      -g GENERATOR, -generator GENERATOR
			    find encoding/decoding algorithm that exposes
			    interesting artifacts (choose: 'encode', 'decode',
			    'both')
      -v1 VALIDATOR1, -validator1 VALIDATOR1
			    applies validator 1
      -v2 VALIDATOR2, -validator2 VALIDATOR2
			    applies validator 2
      -v3 VALIDATOR3, -validator3 VALIDATOR3
			    applies validator 3
      -r, -recursive        sets recursive mode upon specified directory (current
			    workdir by default). Consider using it with
			    min_certainty option
      -f FILENAME, -file FILENAME
			    load a specified file
      -d DIRECTORY, -directory DIRECTORY
			    load a specified directory
      -fp FILE_PATTERN, -file-pattern FILE_PATTERN
			    specified which file pattern to be used with directory
			    (default: '*')
      -l, -list             lists supported algorithms
      -s, -stdin            read data from standard input
      -ver, -version        displays software version

    use filters for more accurate results. Report bugs, ideas, feedback to:
    blackthorne@ironik.org
        
As a Volatility v2.0 plugin:

	$ python vol.py codetective -h
	Volatile Systems Volatility Framework 2.0
	Usage: Volatility - A memory forensics analysis platform.
	
	Options:
	  -h, --help            list all available options and their default values.
	                        Default values may be set in the configuration file
	                        (/etc/volatilityrc)
	  --conf-file=/your/home/.volatilityrc
	                        User based configuration file
	  -d, --debug           Debug volatility
	  --info                Print information about all registered objects
	  --plugins=PLUGINS     Additional plugin directories to use (colon separated)
	  --cache-directory=/Users/blackthorne/.cache/volatility
	                        Directory where cache files are stored
	  --no-cache            Disable caching
	  --tz=TZ               Sets the timezone for displaying timestamps
	  -f FILENAME, --filename=FILENAME
	                        Filename to use when opening an image
	  --output=text         Output in this format (format support is module
	                        specific)
	  --output-file=OUTPUT_FILE
	                        write output in this file
	  -v, --verbose         Verbose information
	  -k KPCR, --kpcr=KPCR  Specify a specific KPCR address
	  -g KDBG, --kdbg=KDBG  Specify a specific KDBG virtual address
	  --dtb=DTB             DTB Address
	  --cache-dtb           Cache virtual to physical mappings
	  --use-old-as          Use the legacy address spaces
	  -w, --write           Enable write support
	  --profile=WinXPSP2x86
	                        Name of the profile to load
	  -l LOCATION, --location=LOCATION
	                        A URN location from which to load an address space
	  -n PNAME, --pname=PNAME
	                        define target Process name
	  -p PID, --pid=PID     define target Process ID
	  -t FILTERS, --filters=FILTERS
	                        apply filters, can be: win, web, unix, db and other
	                        (default: none)
	  -u, --uuids           include UUIDS in search (default: No)
	
	---------------------------------
	Module Codetective
	---------------------------------
	determine the crypto/encoding algorithm used according to traces from its representation




Requirements
------------

python v2.4 - 2.7


Discussion
----------

This script is heavily based on regular expressions done with a mindset of rejecting the maximum possible alternatives for each possible hash/code submitted but never to reject valid choices. Also, this code requires proper testing, so you're welcome to contribute with more algorithms and bring me the feedback.
Notice that this tool also infers on the confidence level relative to each guess and it's able to give you a preliminary analyze (-a). 

Notice that results improve with filters (-f) that can be specified so if you know that the source of the file is related to the web, Codetective will have more confidence when trying to determine the source of code when considering web applications frameworks such as Joomla or Django. 
If you find this tool useful, know that there is other called [Hash Identifier] (http://code.google.com/p/hash-identifier/)  that works in a different way that may also be helpful to you.

When using Codetective as plugin for Volatility remember to use uuids search option (-u) if you need it, since it is disabled by default. Most relevant options are -u (show UUIDs), -v (verbose mode), -t (filters), -p (search for Process ID) and -n (search for process name). If neither -p or -n is defined, if will search in all processes.

Finally, when passing strings from the command-line, always wrap your input string with '' (at least, if you're using bash) so that special characters such as '!' don't mess up with the input before it gets processed by Codetective.

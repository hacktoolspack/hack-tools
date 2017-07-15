<img src="https://s30.postimg.org/t64sh7kyp/operative4.png" width="450">

![version](https://img.shields.io/badge/version-1.0b-red.svg) [![twitter](https://img.shields.io/badge/twitter-@graniet75-blue.svg)](https://twitter.com/graniet75)

Copyright (c) 2017 written in python with Love

Author: Tristan Granier (graniet)

This is a framework based on fingerprint action, this tool is used for get information on website or enterprise target

##### Dependency & launching
+ pip install -r requirements.txt
+ python operative.py

##### Youtube
+ [how use fingerprint modules ](https://www.youtube.com/watch?v=3ogNpa8s16g)

##### Campaign

+ You can start a (gathering/fingerprinting) campaign with :campaign command.
+ Update a value of YOURWEBSITE.COM / ENTERPRISE_NAME in config.json file.
+ You can add a module process for a customized campaign.

##### Core Modules

+ core/modules/cms_gathering
+ core/modules/domain_search
+ core/modules/email_to_domain
+ core/modules/https_gathering
+ core/modules/linkedin_search
+ core/modules/reverse_ipdomain
+ core/modules/search_db
+ core/modules/waf_gathering
+ core/modules/whois_domain
+ core/modules/generate_email
+ core/modules/viadeo_search
+ core/modules/file_common
+ core/modules/get_websiteurl
+ core/modules/getform_data
+ core/modules/subdomain_search
+ core/modules/vhost_IPchecker
+ core/modules/tools_suggester
+ core/modules/metatag_look
+ core/modules/header_retrieval

##### SQL File forensics
+ import database in core/dbs/
+ read table
+ read columns
+ search information with pattern

### Write module

For write module look core/modules/sample_module class

### Thanks

+ @qwartz2 : Code update - multiple shortcut ...

#### This is only for testing purposes and can only be used where strict consent has been given. Do not use this for illegal purposes, period.

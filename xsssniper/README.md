# XSSSNIPER

xsssniper is an handy xss discovery tool with mass scanning functionalities.

## Usage:

    Usage: xsssniper.py [options]

    Options:
      -h, --help            show this help message and exit
      -u URL, --url=URL     target URL
      --post                try a post request to target url
      --data=POST_DATA      post data to use
      --threads=THREADS     number of threads
      --http-proxy=HTTP_PROXY
                            scan behind given proxy (format: 127.0.0.1:80)
      --tor                 scan behind default Tor
      --crawl               crawl target url for other links to test
      --forms               crawl target url looking for forms to test
      --user-agent=USER_AGENT
                            provide an user agent
      --random-agent        perform scan with random user agents
      --cookie=COOKIE       use a cookie to perform scans
      --dom                 basic heuristic to detect dom xss


## Examples:

Scanning a single url with GET params:

    $ python xsssniper.py -u "http://target.com/index.php?page=test"

Scanning a single url with POST params:

    $ python xsssniper.py -u "http://target.com/index.php" --post --data=POST_DATA

Crawl a single url looking for forms to scan:

    $ python xsssniper.py -u "http://target.com" --forms

Mass scan an entire website:

    $ python xsssniper.py -u "http://target.com" --crawl

Mass scan an entire website forms included:

    $ python xsssniper.py -u "http://target.com" --crawl --forms

Analyze target page javascripts (embedded and linked) to search for common sinks and sources:
    
    $ python xsssniper.py -u "http://target.com" --dom

## Thanks:

* Miroslav Stamparm 
* Claudio Telmon

## License

ISC License.
 
 > Copyright (c) 2012, Gianluca Brindisi < g@brindi.si >
 >
 > Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
 >
 > THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

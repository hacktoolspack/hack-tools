import urllib2
import json
import time
import socket
import httplib
from lib.core.settings import PROXY_URL
from lib.core.settings import LOGGER
from lib.core.settings import PROXY_SCAN_RESULTS
from lib.core.settings import create_random_filename
from lib.core.settings import create_dir


def connect_and_pull_info():
    """ Connect to the proxy source and pull the proxies in JSON form """
    results = {}
    count = 0
    data = json.loads(urllib2.urlopen(PROXY_URL).read())
    for i in range(0, 60):
        count += 1
        results[count] = data[i]
    LOGGER.info("Found {} possible proxies, moving to connection attempts..".format(len(results)))
    return results


def attempt_to_connect_to_proxies():
    """ Attempted connections to the proxies pulled from the JSON data """
    results = []
    prox_info = connect_and_pull_info()
    for i, proxy in enumerate(prox_info, start=1):
        if prox_info[i]["type"] == "HTTP":
            candidate = "{}://{}:{}".format(prox_info[i]["type"],
                                            prox_info[i]["ip"],
                                            prox_info[i]["port"])
            opener = urllib2.build_opener(urllib2.ProxyHandler({"http": candidate}))
            urllib2.install_opener(opener)
            request = urllib2.Request("http://google.com")
            try:
                start_time = time.time()
                urllib2.urlopen(request, timeout=10)
                stop_time = time.time() - start_time
                LOGGER.info("Successful: {}\n\t\tLatency: {}s\n\t\tOrigin: {}\n\t\tAnonymity: {}\n\t\tType: {}".format(
                    candidate.lower(), stop_time, prox_info[i]["country"],
                    prox_info[i]["anonymity"], prox_info[i]["type"]
                ))
                results.append("http://" + prox_info[i]["ip"] + ":" + prox_info[i]["port"])
            except urllib2.HTTPError:
                pass
            except urllib2.URLError:
                pass
            except socket.timeout:
                pass
            except httplib.BadStatusLine:
                pass
            except socket.error:
                pass
    LOGGER.info("Found a total of {} proxies.".format(len(results)))
    filename = create_random_filename()
    create_dir(PROXY_SCAN_RESULTS)
    with open(PROXY_SCAN_RESULTS + "/" + filename + ".txt", "a+") as res:
        for prox in results:
            res.write(prox + "\n")
    LOGGER.info("Results saved to: {}".format(PROXY_SCAN_RESULTS + "/" + filename + ".txt"))

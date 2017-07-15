#!/usr/bin/python
# -*- coding: utf-8 -*-
import mechanize


def testProxy(url, proxy):
    browser = mechanize.Browser()
    browser.set_proxies(proxy)
    page = browser.open(url)
    source_code = page.read()
    print source_code


url = 'http://ip.nefsc.noaa.gov/'
hideMeProxy = {'http': '216.155.139.115:3128'}

testProxy(url, hideMeProxy)


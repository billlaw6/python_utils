#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: submit_get.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 19 Jan 2017 05:21:38 PM CST
# Description: 

import sys
import urllib
import urllib.request
from urllib.parse import urlencode


def add_GET_data(url, data):
    return url + '?' + urlencode(data)


zipcode = sys.argv[1]

url = add_GET_data('http://www.wunderground.com/cgi-bin/findweather/getForecast', [('query', 'zipcode')])

print("Using URL %s", url)
fd = urllib.request.urlopen(url)

while 1:
    data = fd.read(1024)
    if not len(data):
        break
    sys.stdout.write(data.decode('utf-8'))




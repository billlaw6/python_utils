#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: submit_post.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 19 Jan 2017 05:30:25 PM CST
# Description: 

import sys
import urllib
import urllib.request
from urllib.parse import urlencode


zipcode = sys.argv[1]

url = 'http://www.wunderground.com/cgi-bin/findweather/getForecast'
data = urlencode([('query', zipcode)])

print("Using URL %s", url)
try:
    fd = urllib.request.urlopen(url, data)
except urllib.request.URLError as e:
    print("Error retrieving data: %s" % e)
    sys.exit(1)

# while 1:
    # data = fd.read(1024)
    # if not len(data):
        # break
    # sys.stdout.write(data.decode('utf-8'))

print("Retrieved %" % fd.geturl())
info = fd.info()
for key, value in info:
    print("%s = %s" % (key, value))



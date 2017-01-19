#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: dump_page.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 19 Jan 2017 04:29:18 PM CST
# Description: 

import sys, urllib
import urllib.request


fd = urllib.request.urlopen(sys.argv[1])

while 1:
    data = fd.read(1024)
    if not len(data):
        break
    sys.stdout.write(data.decode('utf-8'))



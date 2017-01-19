#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: getaddrinfo-basic.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 19 Jan 2017 03:00:52 PM CST
# Description: 

import sys, socket


result = socket.getaddrinfo(sys.argv[1], None)
print(result[0][4])

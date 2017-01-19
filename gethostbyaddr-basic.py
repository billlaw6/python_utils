#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: gethostbyaddr-basic.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 19 Jan 2017 03:07:08 PM CST
# Description: 

import sys, socket


try:
    result = socket.gethostbyaddr(sys.argv[1])

    print("Primary hostname:")
    print(" " + result[0])

    print("\n Addresses: ")
    for item in result[2]:
        print(" " + item)
except socket.herror as e:
    print("Couldn't look up name: %s" % e)



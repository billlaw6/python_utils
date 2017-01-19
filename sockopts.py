#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: sockopts.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 19 Jan 2017 11:07:31 AM CST
# Description: 

import socket


solist = [x for x in dir(socket) if x.startswith('SO_')]
solist.sort()
for x in solist:
    print(x)



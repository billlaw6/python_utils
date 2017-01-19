#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: inetdserver.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 19 Jan 2017 01:51:40 PM CST
# Description: 

import sys


print("Welcome.")
print("Please enter a string:")
sys.stdout.flush()
line = sys.stdin.readline().strip()
print("You entered %d characters. " % len(line))



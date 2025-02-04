#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: udp.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 19 Jan 2017 10:44:49 AM CST
# Description: 

import socket, sys


host = sys.argv[1]
textport = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    port = int(textport)
except ValueError:
    # That didn't work. Look it up instead.
    port = socket.getservbyname(textport, 'udp')

s.connect((host, port))
print("Enter data to transmit: ")
data = sys.stdin.readline().strip()
s.sendall(data)
print("Looking for replies; press Ctrl-C or Ctrl-Break to stop.")
while 1:
    buf = s.recv(2048)
    if not len(buf):
        break
    sys.stdout.write(buf)



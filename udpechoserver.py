#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: udpechoserver.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 19 Jan 2017 11:33:42 AM CST
# Description: 

import socket, traceback


host = ''   # Bind to all interface
port = 51423

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))

while 1:
    try:
        message, address = s.recvfrom(8192)
        print("Got data from %s, %s" % address)
        print("Got data: %s" % message)
        s.sendto(message, address)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()




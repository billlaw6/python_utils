#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: server.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Wed 18 Jan 2017 04:30:56 PM CST
# Description: 

import socket, traceback


host = ''   # Bind to all interfaces
port = 51423

s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)

print("Server is running on port %d; press Ctrl-C to terminate." % port)

while 1:
    clientsock, clientaddr = s.accept()
    clientfile = clientsock.makefile('rw', 0)
    clientfile.write("Welcome, " + str(clientaddr) + "\n")
    clientfile.write("Please enter a string: ")
    line = clientfile.readline().strip()
    clientfile.write("You entered %d characters.\n" % len(line))
    clientfile.close()
    clientsock.close()

while 1:
    try:
        clientsock, clientaddr = s.accept()
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exc()
        continue

    try:
        print("Got connection from ", clientsock.getpeername())
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()

    try:
        clientsock.close()
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exc()



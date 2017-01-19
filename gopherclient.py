#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: gopherclient.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Wed 18 Jan 2017 04:00:53 PM CST
# Description: Simple Gopher Client
import socket, sys
import optparse


# port = 70   # Gopher uses port 70
# host = sys.argv[1]
# filename = sys.argv[2]
parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="port", type="int", help=("port number [default: %default]"))
parser.set_defaults(port = 70)
parser.add_option("-s", "--host", dest="host", help=("host [default: %default]"))
parser.set_defaults(host = "quux.org")
parser.add_option("-f", "--filename", dest="filename", help=("filename [default: %default]"))
parser.set_defaults(filename = "/")
opts, args = parser.parse_args()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((opts.host, opts.port))
except socket.gaierror as e:
    print("Error connecting to server: %s" % e)
    sys.exit(1)

# Option 1
# s.sendall(opts.filename + "\r\n")
# while 1:
    # buf = s.recv(2048)
    # if not len(buf):
        # break
    # sys.stdout.write(buf)

# Option 2
fd = s.makefile('rw', 0)
fd.write(opts.filename + "\r\n")

for line in fd.readlines():
    sys.stdout.write(line)


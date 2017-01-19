#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: dump_info_auth.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 19 Jan 2017 04:49:15 PM CST
# Description: 

import sys, urllib, getpass
import urllib.request


class TerminalPassword(urllib.request.HTTPPasswodMgr):
    def find_user_password(self, realm, authuri):
        retval = urllib.request.HTTPPasswodMgr.find_user_password(self, realm, authuri)

    if retval[0] == None and retval[1] == None:
        sys.stdout.write("Login required for %s at %s" % (realm, authuri))
        sys.stdout.write("Username: ")
        username = sys.stdin.readline().rstrip()
        password = getpass.getpass().rstrip()
        return (username, password)
    else:
        return retval

req = urllib.request(sys.argv[1])
opener = urllib.build_opener(urllib.request.HTTPBasicAuthHandler(TerminalPassword()))
fd = opener.open(req)


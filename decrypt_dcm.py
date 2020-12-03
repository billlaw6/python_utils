#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from Crypto.Cipher import AES


with open('/Users/liubin/Projects/python_utils/IMG-enc.dcm', 'rb') as fr:
    nonce, tag, ciphertext = [ fr.read(x) for x in (16, 16, -1) ]
    cipher = AES.new(b'12345678abcdefgh', AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

with open('/Users/liubin/Projects/python_utils/IMG-bak.dcm', 'wb') as fw:
    fw.write(data)

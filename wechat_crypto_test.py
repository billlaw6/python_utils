#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name: wechat_crypto_test.py
# Version: V1.0
# Author: LiuBin
# Created Time: 2020-12-02 08:14:54
# Description:
# https://www.pycryptodome.org/en/latest/src/examples.html

# import pdb
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP, PKCS1_v1_5

# ############### ################ ################ ################
private_key = RSA.import_key(open("apiclient_key.pem").read())
cipher = PKCS1_v1_5.new(private_key)
result = cipher.encrypt("".encode('utf-8'))
print(result)
# pdb.set_trace()


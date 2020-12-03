#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name: sha256_rsa_study.py
# Version: V1.0
# Author: LiuBin
# Created Time: 2020-12-01 17:12:18
# Description: RSA包没解决加载"-----BEGIN PRIVATE KEY"开头形私钥的问题，应该与“-----BEGIN RSA PRIVATE KEY"不是同一类，直接改内容会报：
# int() argument must be a string, a bytes-like object or a number, not 'Sequence'
# https://stackoverflow.com/questions/42668142/how-to-load-rsa-keystirng-in-python
# https://github.com/sybrenstuvel/python-rsa/issues/31
# 都提出了此问题，但没有解决，转换到pycryptodome包
# https://stuvel.eu/python-rsa-doc/usage.html#generating-keys
import rsa
import logging
import pdb


logger = logging.getLogger(__name__)

####################################################################################################################
# 常规用法，信息发送方用公钥加密，信息接收方用私钥解密
# RSA 只能解密比key小的数据
# RSA can only encrypt messages that are smaller than the key. A couple of bytes are lost on random padding, and the rest is available for the message itself. For example, a 512-bit key can encode a 53-byte message (512 bit = 64 bytes, 11 bytes are used for random padding and other stuff). See Working with big files for information on how to work with larger files.
# To encrypt or decrypt a message, use rsa.encrypt() resp. rsa.decrypt(). Let’s say that Alice wants to send a
# message that only Bob can read.
# Bob generates a keypair, and gives the public key to Alice. This is done such that Alice knows for sure that
# the key is really Bob’s (for example by handing over a USB stick that contains the key).
(pubkey, privkey) = rsa.newkeys(512)
# 学习rsa公钥和私钥有概念和用法
pubkey_pem = pubkey.save_pkcs1(format='PEM')
with open('test_pubkey.pem', 'wb') as f:
    f.write(pubkey_pem)

privkey_pem = privkey.save_pkcs1(format='PEM')
with open('test_privkey.pem', 'wb') as f:
    f.write(privkey_pem)

# Alice writes a message, and encodes it in UTF-8. The RSA module only operates on bytes, and not on strings,
# so this step is necessary.
message = 'hello Bob!'.encode('utf8')

# Alice encrypts the message using Bob’s public key, and sends the encrypted message.
crypto = rsa.encrypt(message, pubkey)

# 方式一：直接取生成的私钥解密
# Bob receives the message, and decrypts it with his private key.
message = rsa.decrypt(crypto, privkey)
print("message: {}".format(message.decode('utf8')))

# 方式二：从私钥文件中读取私钥解密
with open('test_privkey.pem', 'rb') as f:
    privkey_pem = rsa.PrivateKey.load_pkcs1(f.read(), format='PEM')
    message1 = rsa.decrypt(crypto, privkey_pem)
    print("message1: {}".format(message1.decode('utf8')))

# 修改加密结果crypto后尝试解密，会报:rsa.pkcs1.DecryptionError: Decryption failed
try:
    err_result = rsa.decrypt(crypto[:-1] + b'X', privkey)
except rsa.pkcs1.DecryptionError as e:
    logger.info(str(e))


####################################################################################################################
# 签名和验证
# 用于确认加密信息是持有privkey的用户发出来的
# 签名方式一：
signature = rsa.sign(message, privkey, 'SHA-1')
# print(signature)
# 签名方式二：
hash = rsa.compute_hash(message, 'SHA-1')
signature1 = rsa.sign_hash(hash, privkey, 'SHA-1')
try:
    # 校验正常时返回哈希加密类型；校验失败时报VerificationError
    verified = rsa.verify(message, signature, pubkey)
    print(verified)
    verified1 = rsa.verify(message, signature1, pubkey)
    print(verified1)
except rsa.pkcs1.VerificationError as e:
    logger.info(str(e))

# 另一种哈希算法
# 签名方式一：
signature = rsa.sign(message, privkey, 'SHA-256')
# print(signature)
# 签名方式二：
hash = rsa.compute_hash(message, 'SHA-256')
signature1 = rsa.sign_hash(hash, privkey, 'SHA-256')
try:
    # 校验正常时返回哈希加密类型；校验失败时报VerificationError
    verified = rsa.verify(message, signature, pubkey)
    print(verified)
    verified1 = rsa.verify(message, signature1, pubkey)
    print(verified1)
except rsa.pkcs1.VerificationError as e:
    logger.info(str(e))

####################################################################################################################
# 签名和验证
# Instead of a message you can also call rsa.sign() and rsa.verify() with a file-like object. If the message object has a read(int) method it is assumed to be a file. In that case the file is hashed in 1024-byte blocks at the time.

# pdb.set_trace()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name: pycryptodome_study.py
# Version: V1.0
# Author: LiuBin
# Created Time: 2020-12-02 08:14:54
# Description:
# https://www.pycryptodome.org/en/latest/src/examples.html

# import pdb
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# ############### ################ ################ ################
# 用密码生成加密的密钥导入导出测试
secret_code = "Unguessable"
key = RSA.generate(2048)
# 至少有pkcs#1和pkcs#8两种密码编码类型
# encrypted_key = key.export_key(passphrase=secret_code, pkcs=1,
#                                protection="scryptAndAES128-CBC")
encrypted_key = key.export_key(passphrase=secret_code, pkcs=8,
                               protection="scryptAndAES128-CBC")

file_out = open("rsa_key.bin", "wb")
file_out.write(encrypted_key)
file_out.close()

print(key.publickey().export_key())

# The following code reads the private RSA key back in, and then prints again the public key:
secret_code = "Unguessable"
encoded_key = open("rsa_key.bin", "rb").read()
key = RSA.import_key(encoded_key, passphrase=secret_code)

print(key.publickey().export_key())
# ############### ################ ################ ################
# 生成常规的公钥和私钥对测试
key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("private.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key()
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
file_out.close()

# ############### ################ ################ ################
# Encrypt data with RSA
# The following code encrypts a piece of data for a receiver we have the RSA public key of. The RSA public key is stored in a file called receiver.pem.

# Since we want to be able to encrypt an arbitrary amount of data, we use a hybrid encryption scheme. We use RSA with PKCS#1 OAEP for asymmetric encryption of an AES session key. The session key can then be used to encrypt all the actual data.

# As in the first example, we use the EAX mode to allow detection of unauthorized modifications.
data = "I am important message!".encode('utf-8')
with open("encrypted_data.bin", "wb") as file_out:
    recipient_key = RSA.import_key(open("receiver.pem").read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]


# The receiver has the private RSA key. They will use it to decrypt the session key first, and with that the rest of the file:
file_in = open("encrypted_data.bin", "rb")

private_key = RSA.import_key(open("private.pem").read())

enc_session_key, nonce, tag, ciphertext = \
    [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

# Decrypt the session key with the private RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(ciphertext, tag)
print(data.decode("utf-8"))
# pdb.set_trace()

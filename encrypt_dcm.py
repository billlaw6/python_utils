#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import getpass
import pdb


class EncryptDecryptor(object):
    """
    DICOM文件加密解密
    """
    def __init__(self, key=None):
        if not key:
            key = getpass.getpass("请输入16位的Key:").encode(encoding='utf-8')
            if len(key) != 16:
                print("您输入的Key长度不为16，请重新输入！")
                return
        self.key = key


    def encrypt(self, src=None, dest=None):
        """
        加密文件:
        src: 待加密文件路径，
        dest: 加密结果文件路径
        """
        if not src:
            print('请输入有效的待加密源文件路径')
        else:
            try:
                with open(src, 'rb') as f:
                    data = f.read()
                    cipher = AES.new(self.key, AES.MODE_EAX)
                    ciphertext, tag = cipher.encrypt_and_digest(data)
                    if not dest:
                        filepath, fullname = os.path.split(src)
                        basename, ext = os.path.splitext(fullname)
                        dest = os.path.join(filepath, basename + '-enc' + ext)
                    with open(dest, 'wb') as fw:
                        [ fw.write(x) for x in (cipher.nonce, tag, ciphertext) ]
            except Exception as e:
                print(e)


    def decrypt(self, src=None, dest=None):
        """
        解密文件:
        src: 待解密文件路径，
        dest: 解密结果文件路径
        """
        if not src:
            print('请输入有效的待解密源文件路径')
        else:
            try:
                with open(src, 'rb') as f:
                    nonce, tag, ciphertext = [ f.read(x) for x in (16, 16, -1)]
                    if not dest:
                        filepath, fullname = os.path.split(src)
                        basename, ext = os.path.splitext(fullname)
                        dest = os.path.join(filepath, basename + '-dec' + ext)
                    cipher = AES.new(self.key, AES.MODE_EAX, nonce)
                    # cipher = AES.new(b'abcdefgh12345678', AES.MODE_EAX, nonce)
                    # cipher = AES.new(b'01234567abcdefgh', AES.MODE_EAX, nonce)
                    data = cipher.decrypt_and_verify(ciphertext, tag)
                    with open(dest, 'wb') as fw:
                        fw.write(data)
            except ValueError as e:
                # print(e)
                print('Wrang password')
            except Exception as e:
                print(e)


def test():
    # pdb.set_trace()
    # key=b'01234567abcdefgh'
    key=b'01#345_7abCdefgh'
    enc_dec = EncryptDecryptor(key)
    src = "/Users/liubin/Projects/python_utils/IMG.dcm"
    enc_dec.encrypt(src)
    src1 = "/Users/liubin/Projects/python_utils/IMG-enc.dcm"
    enc_dec.decrypt(src1)


if __name__ == '__main__':
    test()

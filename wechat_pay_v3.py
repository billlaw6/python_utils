#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File Name: wechat_pay_settings.py
# Version: V1.0
# Author: LiuBin
# Created Time: 2020-11-27 13:50:13
# Description: 微信支付配置
# ========支付相关配置信息===========
import random
import time
import json
from random import Random
import requests
import string
import logging
import qrcode
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_PSS
from Crypto.Cipher import AES
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 支付途径、APP_ID和openid要匹配
# OPEN_APP_ID = "wxff0c154cf85303f8"  # 服务公众号的appid
MINI_APP_ID = "wxa88e026016fe3f9d"   # 小程序的appid
APP_SECRECT = "2d4b69d20261946afcce9f34fdafc45f"
MCH_ID = "1602017948"  # 你的商户号
# 微信商户平台(pay.weixin.qq.com) -->账户设置 -->API安全 -->密钥设置，设置完成后把密钥复制到这里
API_KEY = "20190928medicloudscnMEDIMAGE2020"
SERIAL_NO = '73E7FE5506C1461C46986C962997882812B1711F'
WECHAT_DOMAIN = "https://api.mch.weixin.qq.com"
# https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/pay/transactions/chapter3_2.shtml

# 微信支付结果回调接口，需要改为你的服务器上处理结果回调的方法路径
NOTIFY_URL = "http://mi.mediclouds.cn/public-api/pay/complete/v3/"
# NOTIFY_URL = "http://115.29.148.227:8083/public-api/pay/complete/v3/"
CREATE_IP = '115.29.148.227'  # 你服务器的IP

# 写在这里会不会只是加载时生成一次不变了？
# timestamp = str(int(time.time()))
# nonce_str = str(random.randint(100000, 10000000))


def get_random_str(length=32):
    """
    返回指定长度的随机字符串
    """
    chars = string.ascii_letters + string.digits
    s = [random.choice(chars) for i in range(length)]
    return "".join(s)


def get_sign_str(method, url_path, timestamp, nonce_str, request_body):
    """
    生成欲签名字符串
    """
    sign_list = [
        method,
        url_path,
        timestamp,
        nonce_str,
        request_body
    ]
    return '\n'.join(sign_list) + '\n'


def get_mini_pay_sign_str(app_id, timestamp, nonce_str, prepay_id):
    """
    生成小程序支付的欲签名字符串
    https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/pay/transactions/chapter3_12.shtml
    """
    sign_list = [
        app_id,
        timestamp,
        nonce_str,
        "prepay_id={}".format(prepay_id)
    ]
    return '\n'.join(sign_list) + '\n'


def get_sign_v3(private_key, sign_str):
    """
    生成签名
    """
    rsa_key = RSA.importKey(private_key)
    signer = pkcs1_15.new(rsa_key)
    digest = SHA256.new(sign_str.encode('utf8'))
    sign = base64.b64encode(signer.sign(digest)).decode('utf8')
    return sign


def authorization(mchid, serial_no, method, url_path, timestamp, nonce_str, request_body):
    """
    生成Authorization
    """
    sign_str = get_sign_str(method, url_path, timestamp,
                            nonce_str, request_body)
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname('manage.py')))
    key_path = os.path.join(base_dir, 'pay_manage', 'apiclient_key.pem')
    s = get_sign_v3(open(key_path).read(), sign_str)
    # logger.info(s)
    authorization = 'WECHATPAY2-SHA256-RSA2048  ' \
        'mchid="{mchid}",' \
        'nonce_str="{nonce_str}",' \
        'signature="{sign}",' \
        'timestamp="{timestamp}",' \
        'serial_no="{serial_no}"'.\
        format(mchid=mchid,
               nonce_str=nonce_str,
               sign=s,
               timestamp=timestamp,
               serial_no=serial_no
               )
    return authorization


def get_mini_prepay_data(detail):
    """
    微信小程序下单
    返回小程序继续支付需要提交的数据
    """
    data = {}
    data['appid'] = MINI_APP_ID
    data['mchid'] = MCH_ID
    data['description'] = detail.get('description', '')
    data['out_trade_no'] = detail.get('out_trade_no', '')
    data['notify_url'] = NOTIFY_URL
    payer = {}
    payer['openid'] = detail.get('payer', '')
    data['payer'] = payer
    amount = {
        "total": detail.get('total', 0),
        "currency": "CNY"
    }
    data['amount'] = amount
    timestamp = str(int(time.time()))
    # nonce_str = get_random_str(32)
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    # 测试签名用请求
    method = "POST"
    url = "/v3/pay/transactions/jsapi"
    body = json.dumps(data)
    auth_str = authorization(MCH_ID, SERIAL_NO, method,
                             url, timestamp, nonce_str, body)
    try:
        headers = {
            'Authorization': auth_str,
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        if method.upper() == 'POST':
            # 以POST方式向微信公众平台服务器发起请求
            response = requests.post(
                WECHAT_DOMAIN + url, headers=headers, data=body)
        elif method.upper() == 'GET':
            # 以POST方式向微信公众平台服务器发起请求
            response = requests.get(
                WECHAT_DOMAIN + url, headers=headers, data=body)
        # logger.info(response.content.decode('utf-8'))
        # logger.info(response.json())
        result = response.json()
        if "prepay_id" in result:
            prepay_id = result["prepay_id"]
            timestamp = str(int(time.time()))
            # nonce_str = get_random_str(32)
            nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
            mini_pay_sign_str = get_mini_pay_sign_str(
                MINI_APP_ID, timestamp, nonce_str, prepay_id)
            base_dir = os.path.abspath(
                os.path.dirname(os.path.dirname('manage.py')))
            key_path = os.path.join(
                base_dir, 'pay_manage', 'apiclient_key.pem')
            sign_v3 = get_sign_v3(open(key_path).read(), mini_pay_sign_str)
            return {
                "timeStamp": timestamp,
                "nonceStr": nonce_str,
                "package": prepay_id,
                "paySign": sign_v3
            }
        else:
            # logger.info(result)
            raise Exception(response.json())
    except requests.ConnectionError as e:
        logger.info(str(e))
        raise requests.ConnectionError


def decrypt(key, nonce, ciphertext, associated_data):
    """
    https://wechatpay-api.gitbook.io/wechatpay-api-v3/qian-ming-zhi-nan-1/zheng-shu-he-hui-tiao-bao-wen-jie-mi
    """
    key_bytes = str.encode(key)
    nonce_bytes = str.encode(nonce)
    ad_bytes = str.encode(associated_data)
    data = base64.b64decode(ciphertext)

    aesgcm = AESGCM(key_bytes)
    return aesgcm.decrypt(nonce_bytes, data, ad_bytes)


if __name__ == "__main__":
    # method = "POST"
    # url = "/v3/pay/transactions/jsapi"
    # timestamp = str(int(time.time()))
    # # nonce_str = get_random_str(32)
    # nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    # body = ""
    # sign = get_sign_v3(method, url, timestamp, nonce_str, body)
    ciphertext = "jz8Yi12ASS/b1gRAc0CnQaj5pM/3XkMGuy0pZoZ+dsZZvsz25GBVLDg33A+kcAb1TKq5+2ViGBcCGUDzzmjE96vKoTmVJV+quCT29KHe+2ARGWtp2pXDoPAImN2T1xRq22o8U0eZDTgh4/BC7rY1qA7G1BvsLf/+FKtHjg2SZUVqr9apgjvB7H98gVzUrq4v5Cxu3MSs9rtoVSOAqxVtBhgtp4ksoTV/Iz9mum9HND53nMGuM9f6Fm5fumF3z2muXlH9mutORfs/2EJqiRg0s94uvy+M4Qvw1e+Zl8O9SZY6aVdWrqAK1Kl884LXOe1TH/6sWtams8340m6Ciaty4b3GlFdaTeenDo8FcwTkzn9eMkIXIm6s7Z0bM3e+mg9r43U13+4bVHK+OYQ1Otym6kxZxdiWEbkJeYWo815aH6cbTQPa3U4uJ+THNzEbRfNoIJhN0jJqgJlYqAtBLL8ojh3kPWY+qHxSvTYNmobHhnvMNszmwD3jkuEhnLzG50t3UtFUxkK0nyB1cdF4avon7GTAk0Do+EKxgNSI5e17pXtC46Yy8xFi4j/sLE2eRk0Lzw=="
    associated_data = 'transaction'
    nonce = 'e5HBmJee8DFz'
    key = 'mimedicloudscn201910141111111111'
    text = decrypt(key, nonce, ciphertext, associated_data)
    result = json.loads(text)
    out_trade_no = result.get('out_trade_no', None)
    print(out_trade_no)

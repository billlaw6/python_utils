#!/usr/env python3
# -*- coding:utf-8 -*-

# import os

# with open('400011489-001844551400-0-3-0-1.txt', 'rb') as f:
#     print(f.read().decode('utf-8'))

a = 'çç¨è®°å½1'
a1 = 'lasdkfaçç¨è®°å½1lasdkfj'
print(a.encode('utf-8'))
import pdb
pdb.set_trace()
print(b'\xc3\xa7\xc2\x97\xc2\x85\xc3\xa7\xc2\xa8\xc2\x8b\xc3\xa8\xc2\xae\xc2\xb0\xc3\xa5\xc2\xbd\xc2\x951'.decode('utf-8'))
b = a1.replace(b'\xc3\xa7\xc2\x97\xc2\x85\xc3\xa7\xc2\xa8\xc2\x8b\xc3\xa8\xc2\xae\xc2\xb0\xc3\xa5\xc2\xbd\xc2\x951'.decode('utf-8'), '')
print(a1)
print(b)
pass

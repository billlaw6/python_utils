#/usr/env python
#-*- coding: utf-8 -*-
import pdb

try:
    with open("not_exists", 'rb') as f:
        pass
except Exception as e:
    pdb.set_trace()
    print(e)

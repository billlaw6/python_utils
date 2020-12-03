#!/usr/env python3
#-*- coding: utf-8 -*-

import numpy as np

a = np.arange(0, 1, 0.1)
print(a)
np.savetxt('a.txt', a, fmt='%.2e', delimiter=',')

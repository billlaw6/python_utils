#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Mon Mar  5 10:29:21 CST 2018
#
# @desc:
#
# @history
#


from random import randrange
import timeit


def main():
    """
    成员查询在list中是线性级的，在set中是常数级的；
    往集合里添加新值，并在操作前检查该值是否存在，list是平方级，而set是线性级。
    """
    L = [randrange(10000) for i in range(1000)]
    S = set(L)

    def list_func(var):
        return 42 in var

    def set_func(var):
        return 42 in var

    # timeit.timeit('list_func(L)')
    timeit.timeit('42 in L')

    # timeit.timeit('set_func(S)')
    timeit.timeit('42 in S')


if __name__ == '__main__':
    main()

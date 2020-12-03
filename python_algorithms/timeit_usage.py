#!/usr/bin/env python
# -*-coding=utf-8-*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Sun Mar  4 20:28:14 CST 2018
#
# @desc:
#
# @history
#

import timeit
import cProfile


def main():
    timeit.timeit('x = 2 + 2')
    timeit.timeit('x = sum(range(10))')

# python -m timeit -s 'import mymodule as m' 'm.myfunction()'

if __name__ == '__main__':
    main()
    cProfile.run('main()')

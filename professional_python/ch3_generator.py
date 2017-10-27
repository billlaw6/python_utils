#!/usr/bin/env python
# -*- coding=utf-8 -*-
#
# File Name: ".expand("%:t"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Fri Oct 27 13:46:46 CST 2017
#
# @desc:
#
# @history
#


# 最简生成器示例
def generator():
    yield 1
    yield 1
    yield 2
    yield 3
    yield 5
    yield 8


def fibonacci():
    numbers = []
    while True:
        if len(numbers) < 2:
            numbers.append(1)
        else:
            numbers.append(sum(numbers))
            numbers.pop(0)
        yield numbers[-1]


if __name__ == '__main__':
    for i in generator():
        print(i)
    # for i in fibonacci():
    #     print(i)
    gen = fibonacci()
    for i in range(10):
        print(next(gen))

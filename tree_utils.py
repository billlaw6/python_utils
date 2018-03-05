#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Mon Mar  5 10:08:05 CST 2018
#
# @desc:
#
# @history
#


class Tree(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

t = Tree(Tree('a', 'b'), Tree('c', 'd'))
print(t.right.left)

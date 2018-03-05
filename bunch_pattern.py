#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# File Name: '.expand('%'))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Mon Mar  5 10:18:48 CST 2018
#
# @desc:
#
# @history
#


class Bunch(dict):
    '''
    Python算法教程P34
    树型数据结构原型推荐
    '''
    def __init__(self, *args, **kwargs):
        super(Bunch, self).__init__(*args, **kwargs)
        self.__dict__ = self


def main():
    x = Bunch(name='Bill', position='Company')
    print(x.name)


if __name__ == '__main__':
    main()


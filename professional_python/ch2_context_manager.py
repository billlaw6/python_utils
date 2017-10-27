#!/usr/bin/env python
# -*-coding=utf-8-*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Fri Oct 27 10:15:29 CST 2017
#
# @desc:
#
# @history
#
import psycopg2

# 上下文管理器
# 本质上是with语句对其后代码进行求值，该表达式会返回一个对象，该对象包含两个特殊
# 方法:__enter__和__exit__。__enter__方法返回的结果会被赋给as关键字之后的变量。


# 上下文管理器最简示例
class ContextManager(object):

    def __init__(self):
        self.entered = False

    def __enter__(self):
        self.entered = True
        return self

    def __exit__(self, exc_type, exc_instance, traceback):
        self.entered = False


# 打开和关闭资源是编写上下文管理器的重要因素
# 数据库打开示例
class DBConnection(object):

    def __init__(self, dbname=None, user=None, password=None,
                 host='localhost'):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password

    def __enter__(self):
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            host=self.host,
            user=self.user,
            password=self.password,
        )
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_instance, traceback):
        self.connection.close()


# 上下文异常处理
class BubbleException(object):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_instance, traceback):
        # 上下文中抛出的异常会传给__exit__函数
        if exc_instance:
            print('Bubbing up exception: %s.' % exc_instance)
        # 返回False会继续抛出异常，返回True则终止异常
        return False


# 处理特定的异常类
class ValueErrorSubclass(ValueError):
    pass

class HandleValueError(object):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_instance, traceback):
        if not exc_type:
            return True
        if exc_type == ValueError:
            print('Handling ValueError: %s' % exc_instance)
            return True
        return False


if __name__ == '__main__':
    cm = ContextManager()
    print(cm.entered)
    with cm:
        print(cm.entered)

    # with BubbleException():
    #     5 / 0

    with HandleValueError():
        raise ValueErrorSubclass('foo bar baz')



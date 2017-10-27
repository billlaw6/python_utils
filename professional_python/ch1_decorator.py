#!/usr/bin/env python
# -*-coding=utf-8-*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Thu Oct 26 14:39:40 CST 2017
#
# @desc:
#
# @history
#

# import os
# import sys
import functools
import json
import logging
import time


# 装饰器作用一：函数注册表
class Registry(object):
    """
    《Python高级编程》第8页
    """
    def __init__(self):
        self._functions = []

    def register(self, decorated):
        self._functions.append(decorated)
        return decorated

    def run_all(self, *args, **kwargs):
        return_values = []
        for func in self._functions:
            return_values.append(func(*args, **kwargs))
        return return_values


# 装饰器作用二：类型检查
def required_ints(decorated):
    """
    确保函数接收的所有参数都是整型，否则报错
    """
    @functools.wraps(decorated)
    # @functools.wraps(decorated) 将一个函数的重要内部元素复制到另一个函数
    # 这样help(decorated)获取的信息就不是inner的信息了。
    def inner(*args, **kwargs):
        # Get any values that may have been sent as keyword arguments.
        kwarg_values = [i for i in kwargs.values()]

        # Iterate over every value sent to the decorated method, and
        # ensure that each one is an integer; raise TypeError if not.
        for arg in list(args) + kwarg_values:
            if not isinstance(arg, int):
                raise TypeError('%s only accepts integers as arguments.'
                                % decorated.__name__)
        # Run the decorated method, and return the result.
        return decorated(*args, **kwargs)
    return inner


# 装饰器作用三：保存帮助信息
class User(object):
    def __init__(self, username, email):
        self.username = username
        self.email = email


class AnonymousUser(User):
    def __init__(self):
        self.username = None
        self.email = None

    def __nonzero__(self):
        return False


def required_user(func):
    @functools.wraps(func)
    def inner(user, *args, **kwargs):
        if user and isinstance(user, User):
            return func(user, *args, **kwargs)
        else:
            raise ValueError('A valid user is required to run this.')
    return inner


# 输出格式化
def json_output(decorated):
    @functools.wrap(decorated)
    def inner(*args, **kwargs):
        result = decorated(*args, **kwargs)
        return json.dumps(result)
    return inner


# 捕获特定异常并以指定格式的JSON输出
class JSONOutputError(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


def json_output1(decorated):
    @functools.wraps(decorated)
    def inner(*args, **kwargs):
        try:
            result = decorated(*args, **kwargs)
        except JSONOutputError as e:
            result = {
                'status': 'error',
                'message': str(e)
            }
        return json.dumps(result)
    return inner


@json_output1
def error():
    raise JSONOutputError('json_output1 test')


@json_output1
def other_error():
    raise ValueError('json_output1 does not accept this kind of Exception')


# 装饰器功能四：日志管理
def logged(method):
    """
    Cause the decorated method to be run and its results logged. along
    with some other diagnostic information.
    """
    @functools.wraps(method)
    def inner(*args, **kwargs):
        # Record our start time
        start = time.time()

        # Run the decorated method.
        return_value = method(*args, **kwargs)

        # Record out completion time, and calculated the delta.
        end = time.time()
        delta = end - start

        # Log the method call and the result.
        logger = logging.getLogger('decorateor.logged')
        logger.warn('Called method %s at %.02f; execution time %.02f '
                    'seconds; result %r.' %
                    (method.__name__, start, delta, return_value))
        # Return the method's original return value.
        return return_value
    return inner


@logged
def sleep_and_return(return_value):
    time.sleep(2)
    return return_value


# 装饰类示例
def sortable_by_creation_time(cls):
    original_init = cls.__init__

    @functools.wraps(original_init)
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self._created = time.time()
    cls.__init__ = new_init

    cls.__lt__ = lambda self, other: self._created < other._created
    cls.__gt__ = lambda self, other: self._created > other._created

    return cls


@sortable_by_creation_time
class Sortable(object):
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return self.identifier


# 装饰器作用五：类型转换（函数、类）
class Task(object):
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        raise NotImplementedError('Subclases must implement `run`.')

    def identify(self):
        return 'I am a task.'


def task(decorated):
    class TaskSubclass(Task):
        def run(self, *args, **kwargs):
            def run(self, *args, **kwargs):
                return decorated(*args, **kwargs)
    return TaskSubclass()


@task
def add():
    return 2 + 2

if __name__ == '__main__':
    a = Registry()
    b = Registry()

    @a.register
    def foo(x=3):
        return x

    @b.register
    def bar(x=5):
        return x

    @a.register
    @b.register
    def baz(x=7):
        return x

    print(a.run_all())
    print(b.run_all())
    print(error())
    other_error()
    sleep_and_return(32)

    first = Sortable('first')
    second = Sortable('second')
    third = Sortable('third')

    print(add())

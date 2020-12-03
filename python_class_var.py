#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# 2018-09-29
# https://blog.csdn.net/Marvel__Dead/article/details/79368272
class A:
    x = []  # 不用创建实例就能访问
    y = 0   # 不用创建实例就能访问
    def __init__(self):
        # pass 初始化时不赋值容易出现修改了类变量，影响后续实例变量的不可控bug
        self.x = []
        self.y = 0
        self.z = 1
    def add(self):
        self.x.append('1')
        self.y+=1
    def show(self):
        print(self.x)
        print(self.y)
        print('z: %s' % self.z)

a=A()
print a.x,a.y
print A.x,A.y
a.add()
print a.x,a.y
print A.x,A.y
b=A()
print b.x,b.y
print A.x,A.y
a.show()


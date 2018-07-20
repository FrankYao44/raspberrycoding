# -*- coding:utf-8;-*-
#decorator
import functools
def date(day=None):
    def dectratorA(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            def start(func):
                print("this is %s"%(func.__name__))
                if day!=None:
                    print("today is %s "%(day) )
            def aa():
                print("game over")
            return start(func),func(*args, **kw),aa()
        
        return wrapper
    return dectratorA
@date()
def saytheword1():
    print("have a fucking day")
i="july 5th"

@date(i)
def saytheword2():
    print("have a fucking day")
i=0
saytheword1()
print()
saytheword2()

#lambda
print(list(sorted(range(-100,100),key=lambda x: x**2)))

import functools
#partial
def Aaa(x,y,z):
    return x**y+z

Bbb=functools.partial(Aaa,2,z=10)
print(Bbb(34))






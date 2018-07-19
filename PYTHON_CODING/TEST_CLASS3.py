#enum
from enum import Enum,unique
Class=Enum("Class",('1','2','3','4'))
for name,member in Class.__members__.items():
    print(name," " ,member," ",member.value)
@unique
class Class(Enum):
    ClassA=1
    ClassB=2
    ClassC=3
    ClassD=4
Aaaaa=Class.ClassA
print(Aaaaa)

def A(self):
    print(111111111111111111111)
class LMetaclass(type):
    def __new__(cls,name,bases,attrs):
        attrs["hello"]=lambda self:print(233333333333333333333333333333333333333333333333333333)
        return type.__new__(cls, name, bases, attrs)

class Hello(object,metaclass=LMetaclass):
    pass
a=Hello()
a.hello()

A=type("game",(object,),dict(a=A))
c=A()
c.a()

class Animals(object):
    __slots__=('name','age','__name__',)
    def __init__(self,a,b):
        self.name=a
        self.age=b
    def get_age(self):
        print("%s is %d"%(self.name,self.age))


class Dog (Animals):
    def running(self):
        print("%s is running"%(self.name))
    def __len__(self):
        return self.age


Bob=Dog("Bob",2)
Bob.running()
Bob.get_age()
print(isinstance(Bob,Animals))


#getattr,setattr,hasattr
print(len(Bob))
print(hasattr(Bob,"age"))
print(setattr(Bob,"speed",10))
print(getattr(Bob, 'speed'))
print(getattr(Bob,"sex","we don't  know"))

class Cat(Animals):
    #slots
    __slots__=('color','name','age')
    def miao(self):
        for i in range(100):
            print("miao")
kitty=Cat("Kitty",2)
kitty.color="white and black"
try :
    kitty.sex="boy"
except:
    print("cannot give %s this thing"%(kitty.name))

class Bird(Animals):
    @property
    def sound(self):
        return self._time

    @sound.setter
    def sound(self,time):
        if time=="spring":
            pass
        elif time=="summer":
            pass
        elif time=="fall":
            pass
        else:
            raise ValueError("it has died at that time")
        self._time=time
    #this is an read-only attr
    @property
    def wing(self):
        return 2

harvey=Bird("Harvery",10)
harvey.sound="spring"
print(harvey.sound)
try : harvey.sound="winter"
except ValueError as e :
    print(e)
print(harvey.wing)
print()
#this is MIXIN
class FlyMixIN(object):
    def fly(self):
        print("rokket in the sky")
class Supercat(Cat,FlyMixIN):
    pass
tom=Supercat("Tom",65)
tom.fly()
print()






    


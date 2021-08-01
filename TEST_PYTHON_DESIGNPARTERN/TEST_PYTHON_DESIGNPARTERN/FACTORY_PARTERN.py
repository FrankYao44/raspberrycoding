#simple factory method
class Ice_Craem_Factory(object):
    def __init__(self,kind):
        if kind=="Chocolate":
            self.name=Chocolate_Ice_Cream()
        if kind=="Strawberry":
            self.name=Strawberry_Ice_Cream()
    def sell(self):
        print("we sell %s icecream"%(self.name))
class Chocolate_Ice_Cream():
    def __repr__(self):
       return "Hello!Chocolate?"
class Strawberry_Ice_Cream():
    def __repr__(self):
       return "A Strawberry Icecream?"
if __name__=="__main__":
    Ice_Craem_Factory('Chocolate').sell()
    Ice_Craem_Factory('Strawberry').sell()

#factory method
print("\n")
import abc
class Normal_Ice_Cream_Factory(object):
    @abc.abstractmethod
    def sell(self):
        pass

class Chocolate_Ice_Cream_Factory(Normal_Ice_Cream_Factory):
    def sell():
        return Chocolate_Ice_Cream()
class Strawberry_Ice_Cream_Factory(Normal_Ice_Cream_Factory):
    def sell():
        return Strawberry_Ice_Cream()

if __name__=="__main__":
    Ice_Craem_Factory('Chocolate').sell()
    Ice_Craem_Factory('Strawberry').sell()

#similarity
class Call_Chocolate_Ice_Cream(object):
    def __repr__(self):
        return "chocolate the finest"
class Call_Strawberry_Ice_Cream(object):
    def __repr__(self):
        return "strawberry the best"
class Normal_Ice_Cream_factory(object):
    @abc.abstractmethod
    def sell(self):
        pass
    @abc.abstractmethod
    def callit(self):
        pass

class Chocolate_Ice_Cream_Factory(Normal_Ice_Cream_Factory):
    def sell(self):
        return Chocolate_Ice_Cream()
    def callit(self):
        return Call_Chocolate_Ice_Cream()  
class Strawberry_Ice_Cream_Factory(Normal_Ice_Cream_Factory):
    def sell(self):
        return Strawberry_Ice_Cream()
    def callit(self):
        return Call_Strawberry_Ice_Cream()
if __name__=="__main__":
    a=Strawberry_Ice_Cream_Factory()
    print(a.callit())
    print(a.sell())
    b=Chocolate_Ice_Cream_Factory()
    print(b.callit())
    print(b.sell())


       
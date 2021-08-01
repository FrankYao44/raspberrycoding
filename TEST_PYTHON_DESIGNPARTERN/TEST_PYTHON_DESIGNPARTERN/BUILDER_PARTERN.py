import abc
class Dog(object):
    def __init__(self):
        pass
    def run(self):
        print("a dog is running")
    @abc.abstractmethod
    def bark(self):
        pass
    eatable=True
class Big_Dog(Dog):
    def bark(self):
        print("bark loudly")
class Little_Dog(Dog):
    def bark(self):
        print("berk sharply")
class Cat(object):
    mouse=0
    def __init__(self):
        pass
    def run(self):
        print("a cet is running")
    @abc.abstractmethod
    def catch_mouse(self):
        pass
class Clever_Cat(Cat):
    def catch_mouse(self):
        self.mouse+=1
class Clumsy_Cat(Cat):
    def catch_mouse(self):
        self.mouse+=0

class Home(object):
    def __init__(self,builder):
        self.cat=builder.cat
        self.dog=builder.dog
    def show(self):
        self.cat.run()
        self.dog.run()
        self.cat.catch_mouse()
        print(self.cat.mouse)
        self.dog.bark()
class Builder(object):
    def __init__(self):
        pass
    def argsgetter(self,cat,dog):
        self.cat=cat
        self.dog=dog
        return Home(self)
#in fact, the builder should get args one by one,in different fuctions

if __name__=="__main__":
    Builder().argsgetter(Clever_Cat(),Little_Dog()).show()
    Builder().argsgetter(Clumsy_Cat(),Big_Dog()).show()



import copy
class Propotyper_Yuri(object):
    def clone(self,**kwargs):
        obj=copy.deepcopy(self)
        obj.__dict__.update(kwargs)
        print(obj.__dict__)
        return obj
    def point(self):
        print("Your mind is clear")
    def walk(self):
        print("thought recieved")
    def control(self):
        print("A new commuda joined us")
        print("%s:I belong to Yuri"%(self.con))
if __name__=="__main__":
    pro=Propotyper_Yuri()
    a=pro.clone(con="GI")
    a.walk()
    a.control()
    b=pro.clone(con="IFV")
    b.point()
    b.control()











class WebApp(object):
    def __new__(cls,*args,**kwargs):
        if not hasattr(WebApp,"_instant"):
            WebApp._instant=object.__new__(cls)
        return WebApp._instant
    def __init__(self,newone):
        print("webapp online")
        self.newone=newone
    def callmyself(self):
        print(self.newone)
if __name__=="__main__":
    a=WebApp(1)
    a.callmyself()
    b=WebApp(2)
    b.callmyself()
    print(a==b)

#additionally
print('\n')
import threading
def Fuct(fuct):
    fuct.__lock__=threading.Lock()
    def fuctlock(*args,**kwargs):
        with fuct.__lock__:
            return fuct(*args,**kwargs)
    return fuctlock
class WebApp(object):
    @Fuct
    def __new__(cls,*args,**kwargs):
        if not hasattr(WebApp,"_instant"):
            WebApp._instant=object.__new__(cls)
        return WebApp._instant
    def __init__(self,newone):
        print("webapp online")
        self.newone=newone
    def callmyself(self):
        print(self.newone)
if __name__=="__main__":
    def test():
        a=WebApp(1)
        a.callmyself
    def worker(i):
        a=WebApp(i)
        a.callmyself()
    test()
    task=[]
    for i in range(30):
        thre=threading.Thread(target=worker,args=(i,))
        task.append(thre)

    for one in task:
        one.start()
    for one in task:
        one.join()

#moreover
#print("\n")
#    def singleton(*args,**kwargs):
#        instance=cls(*args,**kwargs)
#        if not hasattr(cls,"_instance"):
#            cls._instance=True
#            cls.__new__=lambda:object.__new__(*args,**kwargs)
#        return instance
#    return singleton
#@Singleton
#class WebApp(object):
#    def __init__(self,newone):
#        print("webapp online")
#        self.newone=newone
#    def callmyself(self):
#        print(self.newone)
#    a=WebApp(1)
#    a.callmyself()
#    b=WebApp(2)
#    b.callmyself()
#    print(a==b)





            
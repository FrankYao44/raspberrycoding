class Student(object):
    __havenotiter=True
    def __init__(self,name,score,det):
        self.name=name
        self.score=score
        self.det=det
        
    #str and repr
    def __str__(self):
        return "%s\'s score is %d"%(self.name,self.score)
    
    __repr__=__str__
    # iter
    def __iter__(self):
        return self
    def __next__(self):
        if self.__havenotiter==True:
            self.finalscore=self.score
            self.__havenotiter=False
        self.finalscore=self.finalscore+self.det
        if self.finalscore>150:
            self.__havenotiter=True
            raise StopIteration
        return self.finalscore
    def __getitem__(self,n):
        self.finalscore=self.score
        if isinstance(n,int):
            return self.score+n*self.det
        if isinstance(n,slice):
            start=n.start
            stop=n.stop
            if start is None:
                start=0
            L=[]
            for x in range(stop):
                if x>=start:
                    L.append(self.finalscore)
                self.finalscore+=self.det

            return L

    def __getattr__(self,attr):
        if attr=="class_":
            return 6
        else:
            raise ValueError
    def __call__(self):
        print("this is a score")
                 

                    
            










xiaoming=Student("xiaoming",65,3)
print(xiaoming)
for n in xiaoming:
    print(n)
print(xiaoming[10])
print(xiaoming[5:10])
print(xiaoming.class_)
xiaoming()

import json
d = [1,2,4,'a',"wo",(1,"23")]
n=json.dumps(d)
print(n)
print(json.loads(n))
class Student(object):
    def __init__(self,name,score):
        self.name=name
        self.score=score

bob=Student('Bob',96)
d=json.dumps(bob,default=lambda obj:obj.__dict__)
print(d)
def returnload(obj):
    return Student(obj['name'], obj['score'])
n=json.loads(d,object_hook=returnload)
print(n)
print(n.name)

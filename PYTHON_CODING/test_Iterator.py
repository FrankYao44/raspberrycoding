def numb():
    i=0
    while True:
        i+=1
        yield i
#that is a generator function
#and it is all int number
n=numb()
#this is a generator
for a in range(100):
    b=next(n)
    print(b)



"""
this is similar to
for a in range(100):
  print(a)
"""
a=iter(list(range(100)))
while True :
    try:
        b=next(a)
        print(b)
    except StopIteration:
        break


#to get returning value
def a():
    yield(1)
    yield(2)
    yield(3)
    return ("fuck you")
b=a()
while True:
    try: next(b)
    
    except StopIteration as e:
        print("we left a message for you , that is %s.have a good time!"%(e.value))
        break


    

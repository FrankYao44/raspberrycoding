#coding: utf-8
#map
def Square(a):
    return a**2
#this is a Iterator
def Number():
    i=0
    while True:
        i=i+1
        yield i
numb=Number()
#map :IterableA=function=>IteratorB
m=map(Square,numb)
i=0
while i<100:
    n=next(m)
    print(n)
    i+=1
#pratice map
LITTERS=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
litters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
def  Litter_Aa(a):
    try:m=LITTERS.index(a)
    except:raise ValueError
    print(m)
    return litters[m]
def  Litter_aA(a):
    try:m=litters.index(a)
    except:raise ValueError
    print(m)
    return LITTERS[m]
def normalize(name):
    m=0
    result=[]
    for n in name:
        
        if m==0 and n in litters:
            o=Litter_aA(n)
        elif m!=0 and n in LITTERS:
            o=Litter_Aa(n)
        else:
            o=n
        result+=o
        m+=1
    result=''.join(result)
    return result
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)

#this is reduce

#1       
from functools import reduce

def prod(i):
    return reduce(lambda x, y: x * y,i)

print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))            

#2
#map and reduce

def str2float(s):
    def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
    m=-(len(s)-s.index(".")-1)
    s=list(s)
    s.remove(".")
    n=reduce(lambda x, y: x * 10 + y, map(char2num, s))
    return n*(10**m)
print('str2float(\'123.456\') =', str2float('123.456'))   
    

        
    
    
    

    


















    
    
        

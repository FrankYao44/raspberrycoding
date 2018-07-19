# -*- coding : utf-8 -*-
#for filler
def is_palindrome(n):
    assert isinstance(n,int),"n must be an int"
    assert n>=10,"n must bigger than ten"
    m=list(str(n))
    m.reverse()
    k=int("".join(m))
    return k==n
output = filter(is_palindrome, range(10, 1000))
print(list(output))


# -*- coding: utf-8 -*-

L = [('Bob', 75,), ('Adam', 92,), ('Bart', 66,), ('Lisa', 88,)]
print(len(L))
def by_name(t):
    return t[0]
def by_score(t):
    return t[1]
  
L1= sorted(L,key=by_name)
print(L1)
L2 = sorted(L,key=by_score)
print(L2)



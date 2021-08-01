class Prime(object):
 def __init__(self,a):
 self.__a=a
 def odd():
 lova1=1
 while True:
 lova1+=2
 yield lova1
 def not_divisible(n):
 return lambda lova2: lova2 % n != 0
 def primes():
 yield 2
 numb = odd()
 while True:
 n= next(numb)
 yield n
 numb = filter(not_divisible(n), numb)
 result=[]
 for n in primes():
 if n<a :
 result.append(n)
 else:break
 self.value=result
  # coding:UTF-8
"""
made by Yao44
This is radical.py
@2544762897 in qq if any bug
"""
'''
we suggest you to use the fraction as the number of radical or there will be much mistakes
'''
from fractions import Fraction
import decimal,prime,math
class __Radicaler__(object):
 pass
class RadicalGroup(__Radicaler__):
 def __init__(self,a,b):
 #self.a=a
 self.b=b
 if not(isinstance(b,list)):
 try:
 n=a+b+233+2
 except:
 raise ValueError("%s cannot be coefficient or %s cannot be radicand"%(a,b))
 lova1=0
 value=" "
 for n in a:
 value+=str(Radical(n,b[lova1]).value)
 lova1+=1
 self.value=value
 a=self.a
 b=self.b
 lova1=0
 value=0
 for num in a:
 c=num
 d=b[lova1]
 lova1+=1
 value+=(math.sqrt(d)*c)
 self.realvalue=value
 def __repr__(self):
 return self.value
class Radical(__Radicaler__):
 def __init__(self,a,b):
 self.a=a
 self.b=b
 if not(isinstance(b,list)):
 try:
 n=a+b+233+2
 except:
 raise ValueError("%s cannot be coefficient or %s cannot be radicand"%(a,b))
 if self.b<0:
 raise ValueError("the number %s in genhao should >=0"%(self.b))
 if isinstance(b,float):
 while True:
 lova3=int(b)
 if lova3==b:
 break
 b*=100
 a=a/10
 if isinstance(a,float):
 a=decimal.Decimal(a).quantize(decimal.Decimal("0.0001"))
 b=int(b)
 if isinstance(self.b,Fraction):
 lova4=int(b.numerator)
 lova5=int(b.denominator)
 a/=lova4
 b=lova4*lova5
 if isinstance(b,int):
 vola6=1
 for num in prime.Prime(b).value:
 a2=num**2
 while b%a2==0:
 vola6*=num
 b/=a2
 b=int(b)
 a*=num
 if b!=1:
 if a>0:
 dd="+%s"%(a)
 elif a==1:
 dd="+"
 elif a==-1:
 dd="-"
 else:dd=a
 value="%s√%s"%(dd,b)
 else: value=a
 self.value=value
 self.a=[a]
 self.b=
 a=self.a
 b=self.b
 lova1=0
 value=0
 for num in a:
 c=num
 d=b[lova1]
 lova1+=1
 h=decimal.Decimal(math.sqrt(d)).quantize(decimal.Decimal("0.0001"))
 value+=(h*c)
 value=float(value)
 self.realvalue=value
 def __str__(self): return "%s"%(self.value)
 __repr__ = __str__
 #a(c)√b
class RadicalCalculation(object):
 def plus(a,b):
 if not(isinstance(a,__Radicaler__)) or not(isinstance(b,__Radicaler__)):
 try:a+b
 except:raise ValueError("%s and %s cannot be calculated for Radical calculation"%(a,b))
 if isinstance(a,int)|isinstance(a,float):
 a=Genshi(a,1)
 if isinstance(b,int)|isinstance(b,float):
 b=Genshi(b,1)
 am=a.a
 bm=a.b
 an=b.a
 bn=b.b
 #am add an ==>a_all
 lova1=0
 for i in bm:
 lova2=0
 for j in bn:
 if i==j:
 am[lova1]+=an[lova2]
 bn.pop(lova2)
 an.pop(lova2)
 lova2+=1
 lova1+=1
 a_all=am+an
 b_all=bm+bn
 value=RadicalGroup(a_all,b_all)
 return value
 def minus(a,b):
 if not(isinstance(b,__Radicaler__)) or not(isinstance(a,__Radicaler__)):
 try:a+b
 except:raise ValueError("%s and %s cannot be calculated for Radical calculation"%(a,b))
 if isinstance(a,int)|isinstance(a,float):
 a=Radical(a,1)
 if isinstance(b,int)|isinstance(b,float):
 b=Radical(b,1)
 am=a.a
 bm=a.b
 an=b.a
 bn=b.b
 #am and an ==>azong
 pi=0
 for mmm in bm:
 qi=0
 for nnn in bn:
 if nnn==mmm:
 am[pi]-=an[qi]
 bn.pop(qi)
 an.pop(qi)
 qi+=1
 pi+=1
 azong=am+an
 bzong=bm+bn
 a=RadicalGroup(azong,bzong)
 return a
 def multiply(a,b):
 if not(isinstance(b,__Radicaler__)) or not(isinstance(a,__Radicaler__)):
 try:a+b
 except:raise ValueError("%s and %s cannot be calculated for Radical calculation"%(a,b))
 if isinstance(a,int)|isinstance(a,float):
 a=Radical(a,1)
 if isinstance(b,int)|isinstance(b,float):
 b=Radical(b,1)
 am=a.a
 bm=a.b
 an=b.a
 w=[]
 v=[]
 bn=b.b
 pi=0
 for mmm in am:
 qi=0
 for nnn in an:
 l=mmm*nnn
 m=bm[pi]*bn[qi]
 n=
 w+=n[0]
 v+=n[1]
 qi+=1
 pi+=1
 a=RadicalGroup(w,v)
 return a
 def divide(a,b):
 if (not(isinstance(b,__Radicaler__)))|(not(isinstance(a,__Radicaler__))) :
 try:a+b
 except:raise ValueError("%s and %s cannot be calculated for Radical calculation"%(a,b))
 def hhh(a,b):
 while True:
 c=int(a)
 d=int(b)
 if (a==c)&(b==d):
 break
 a*=10
 b*=10
 return int(a),int(b)
 if isinstance(a,int)|isinstance(a,float):
 a=Radical(a,1)
 if isinstance(b,int)|isinstance(b,float):
 b=Radical(b,1)
 if len(b.b)!=1:
 raise Exception("sorry,we are unable to do it like(√a+√b)/(√c+√d)")
 am=a.a
 bm=a.b
 an=b.a[0]
 w=[]
 v=[]
 bn=b.b[0]
 for amm in am :
 l=hhh(amm,an)
 c=[Fraction(l[0],l[1])]
 w+=c
 for bmm in bm:
 l=hhh(bmm,bn)
 c=[Fraction(l[0],l[1])]
 v+=c
 a=RadicalGroup(w,v)
 return a
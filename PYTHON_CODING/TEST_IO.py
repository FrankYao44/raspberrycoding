# -*- coding:utf-8-*-
import os
#1
try:
    f=open("/home/pi/Desktop/PYTHON_CODING/test.txt",'r')
    print(f.read(10))
finally:
    if f:
        f.close()
#2
with open("/home/pi/Desktop/PYTHON_CODING/test.txt",'r') as f:
    for line in f.readlines():
        print(line.strip())
#w for txt wb for two 
with open("/home/pi/Desktop/PYTHON_CODING/test.txt",'w') as f:
    f.write("raspberry")
#this is for coding gbk, ignore while reading ununderstand str
with open('/home/pi/Desktop/PYTHON_CODING/test.txt', 'r', encoding='gbk', errors='ignore') as f:
    print(f.read())
#ram reading
#for str
from io import StringIO
f=StringIO()
f.write("hello")
print(f.write("   "))
f.write("goodbye")
print(f.getvalue())
n=StringIO("hello   goodbye")
while True:
    s=n.readline()
    if s == '':
        break
    print(s.strip())
#for two bytes
from io import BytesIO
f=BytesIO()
f.write("中文".encode("utf-8"))
print(f.getvalue())

#uname
print(os.name)
print(os.uname())
print(os.environ)
print(os.environ.get("PATH"))
print(os.path.abspath('.'))
p=os.path.join("/home/pi/Desktop/PYTHON_CODING","testdir")
#it's good habit
print(p)
os.mkdir(p)
os.rmdir(p)
print(os.path.split(p))
print(os.path.splitext("/home/pi/Desktop/PYTHON_CODING/test.txt"))
os.rename("test.txt","test.py")
os.rename("test.py","test.txt")
print([x for x in os.listdir('/home/pi/') if os.path.isdir(os.path.join("/home/pi",x))])
print(os.path.isdir("/home/pi/Desktop"))
print([x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]==".py"])


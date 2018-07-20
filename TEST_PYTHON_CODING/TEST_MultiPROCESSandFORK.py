#multiprocess
from multiprocessing import Process
import os
def child_p(a):
    for i in range(5):
        print('child')
        
p=Process(target=child_p,args=(None,))
p.start()
p.join()
for i in range(5):
    print('parent')
print()

#fork
import os
p=os.fork()
if p==0:
    print("child",os.getpid())
    print("parent is %s"%(os.getppid()))
    for i in range(5):
        print("child!!")
else:
    print("parent",os.getppid())
    print("child is %s"%(p))
    for i in range(5):
        print("parent!!")
print()

from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
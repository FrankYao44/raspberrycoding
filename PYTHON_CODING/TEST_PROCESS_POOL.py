from multiprocessing import Pool
import os,time
def waittime(a):
    print(a)
    time.sleep(1)
print("incoming tranmission")
p=Pool(2)
for i in range(5):
    p.apply_async(waittime,args=(i,))
p.close()
p.join()
print("mission failed")
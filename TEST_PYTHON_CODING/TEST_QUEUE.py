from multiprocessing import Process, Queue
import os, time
def writer(a):
    print(a)
    for i in range(10):
        a.put(i)
        time.sleep(1)
    print("writeover")
def reader(a):
    print(a)
    while True:
        i=a.get(True)
        print(i)
q=Queue()
p1=Process(target=writer,args=(q,))
p2=Process(target=reader,args=(q,))
p2.start()
p1.start()
p1.join()
p2.terminate()
        
        
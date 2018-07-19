import threading, time
locker=threading.Lock()
balance=0
def balancer(n):
    global balance
    locker.acquire()
    try:
        balance=balance+n
    finally:
           locker.release()
def loop():
    print('incoming tranmission, ',threading.current_thread().name)
    for i in range(5):
        print(i)
        balancer(i)
        time.sleep(1)
    print('game over, ',threading.current_thread().name)
    
print('incoming tranmission, ',threading.current_thread().name)
t1 = threading.Thread(target = loop, args = ( ), name='LoopA')
t2 = threading.Thread(target = loop, args = ( ), name = 'LoopB')
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
print('incoming tranmission, ',threading.current_thread().name)

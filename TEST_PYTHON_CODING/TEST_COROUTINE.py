import time
def calculate():
    n=2
    for _ in range(30):
        r=yield  n
        n=n*2
        print(r)
        if not n:
            return
def produce(c):
    c.send(None)
    while True:
        try:
            n=c.send(1)
            print(n)
        except StopIteration:
            c.close()
            print("it is done")
            break
c=calculate()
produce(c)

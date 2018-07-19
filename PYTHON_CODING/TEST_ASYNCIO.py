import asyncio, time
@asyncio.coroutine
def calculate():
    n=2
    r=2
    while n<50000000:
        n=n**2
        r=yield from asyncio.sleep(0.1)
        print(n)
    return

loop=asyncio.get_event_loop()
loop.run_until_complete(calculate())

async def reader():
    i=0
    while i<60:
            with open('/home/pi/Desktop/PYTHON_CODING/TEST_AIO/test1','r') as f:
                n=f.read()
            print(n)
            i=i+1
            await asyncio.sleep(0)
async def calculater():
    n=2
    for i in range(1,40):
        n=n*i
        print(n)
        await asyncio.sleep(0)
looper=asyncio.get_event_loop()
tasks=[reader(),calculater()]
looper.run_until_complete(asyncio.wait(tasks))
looper.close()
        
        

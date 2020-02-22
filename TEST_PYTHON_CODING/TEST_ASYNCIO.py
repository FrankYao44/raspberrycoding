import asyncio, time
@asyncio.coroutine
def calculate():
    n=2
    r=2
    while n<50000000:
        n=n**2
        r=await(asyncio.sleep(1))
        print(n)
    return

loop=asyncio.get_event_loop()
loop.run_until_complete(calculate())

        
        

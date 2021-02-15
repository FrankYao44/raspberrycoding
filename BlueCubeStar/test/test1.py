import asyncio
import time

def new_async(loop,fn,arg):
    time.sleep(2)
    loop.run_until_complete(fn(arg))
    print('fk')

async def a(arg):
    print(arg)
    await asyncio.sleep(5)
    print('a',arg,'done')
    await asyncio.sleep(1)

async def b(loop,arg):
    loop.call_soon(new_async,loop,a,arg)
    await asyncio.sleep(1)
    print('b done')

loop = asyncio.get_event_loop()
task = asyncio.ensure_future(b(loop,1))
loop.run_until_complete(task)
loop.run_forever()

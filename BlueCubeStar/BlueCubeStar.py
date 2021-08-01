import asyncio
from Cloudpiercer.cloudpiercer_main import CloudPiecer
from Cyberkernal.Cyberkernal import Cyberkernal


loop = asyncio.get_event_loop()
cyber = Cyberkernal(loop)
print('cyber')
cloud = CloudPiecer()
cloud.init()
print('cloud')
loop.run_until_complete(cyber.scanning())
loop.run_forever()

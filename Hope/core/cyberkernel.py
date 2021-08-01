import os
import threading
import asyncio
from core.config import configs as c
configs = c['cyberkernel']


class EventLoopPolicy(asyncio.DefaultEventLoopPolicy):

    def _search_expand_runnable(self):
        route_servers = [x.split('.')[0] for x in os.listdir(configs['expand_path'])
                         if os.path.splitext(x)[1] == '.py']
        for module_name in route_servers:
            mod = __import__(configs['expand_path'] + module_name, globals(), locals(), [module_name])
            for attr in dir(mod):
                if 'main' in attr:
                    fn = getattr(mod, attr)
                    self.runnable_expand[mod.__name__] = fn

    async def _init_expand(self, expand_name):
        t1 = threading.Thread(target=self.runnable_expand[expand_name], args=(self,))
        self.running_expand[expand_name] = t1
        t1.start()

    async def _new_expand(self, expand_name):
        # used to connect an expand known
        expand_list = await self._get('127.0.0.1:8000/cyberkernal/expand_list')
        if (expand_name not in expand_list) | expand_name not in self.runnable_expand:
            raise ValueError('no expand named %s' % expand_name)
        t1 = threading.Thread(target=self.runnable_expand[expand_name].main)
        self.running_expand[expand_name] = t1
        t1.start()

    def _show_expand(self):
        return [key for key in self.running_expand]

    def _kill_expand(self, name):
        # stop an expand, with data saved and quit safely
        self.loop.call_soon(self.running_expand[name].stop())

    async def _run_order(self, order):
        while True:
            try:
                task = self.loop.create_task(order.next_line())
                result = await task
                order.set_result_to_present_line(result)
            except StopIteration:
                return

    async def scanning(self):
        while True:
            if self.order_list:
                self.loop.create_task(self._run_order(self.order_list[0]))
                self.order_list.pop(0)
            await asyncio.sleep(0)

    def new_cyber_process(self):
        # create a new process running cyberkernal
        pass

    def cancel_cyber_process(self):
        # just as what is says
        pass

    def get_event_loop(self):

        loop = super().get_event_loop()
        loop.running_expand = dict()
        loop.runnable_expand = dict()
        loop.order_list = []
        loop.dictionary = dict()
        loop.connected_args = dict()
        self._search_expand_runnable()
        [loop.run_until_complete(self._init_expand(i)) for i in loop.runnable_expand.keys()]
        loop.init_expand = self._init_expand
        loop.create_expand = self._new_expand
        loop.delete_expand = self._kill_expand
        loop.show_expand = self._show_expand
        loop.copy = self.new_cyber_process
        loop.destroy = self.cancel_cyber_process
        loop.scanning = self.scanning
        loop.create_new_order = self._run_order
        self._search_expand_runnable()
        return loop


asyncio.set_event_loop_policy(EventLoopPolicy())


#!/usr/bin python3
# -*- coding: utf-8 -*-
import asyncio
import Cloudpiercer.orm as orm
import os
from functools import reduce
from some_useful_func import str_in_iterable_turns_into_tuple_factory
from aiohttp import web
from config import configs


async def logger_factory(app, handler):
    async def logger(request):
        pass
        return await handler(request)
    return logger


async def response_factory(app, handler):
    async def response(request):
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, int) and 100 <= r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and 100 <= t < 600:
                return web.Response(t, str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response


def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    url = getattr(fn, '__url__', None)
    if method is None or url is None:
        raise ValueError('@method or url not defined in %s.' % str(fn))
        #  this might be a bug
    app.router.add_route(method, url, RequestHandler(app, fn))


def add_routes(app):
    route_servers = [x.split('.')[0] for x in os.listdir(
        os.path.join(os.path.abspath('Cloudpiercer'), 'PandoraHub_API'))
                     if os.path.splitext(x)[1] == '.py']
    for module_name in route_servers:
        mod = __import__('Cloudpiercer.PandoraHub_API.%s' % module_name, globals(), locals(), [module_name])
        for attr in dir(mod):
            if attr.startswith('_'):
                continue
            fn = getattr(mod, attr)
            if callable(fn):
                method = getattr(fn, '__method__', None)
                if method:
                    add_route(app, fn)


class Network(web.Application):
    def __init__(self, middlewares=(logger_factory, response_factory)):
        super().__init__(middlewares=middlewares)

    async def network_online(self):
        runner = web.AppRunner(self)
        await runner.setup()
        site = web.TCPSite(runner, configs['cloudpiercer']['IP'], configs['cloudpiercer']['port'])
        srv = await site.start()
        return srv

    def addition(self):
        pass


class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn

    async def __call__(self, request):
        if self._func.__method__ == 'post':
            params = await request.post()
            kw = dict(**params)
        else:
            kw = dict(**request.match_info)
        try:
            r = await self._func(**kw)
            return r
        except Exception:
            raise


class CloudPiecer(object):

    def __init__(self, ):
        self.loop = asyncio.get_event_loop()

#   def new_server(self, server_name, address, level, db_id=next_id(), table_name='MCV_table'):
#       self.cursor.execute('insert into %s (id,server_name,level,address) values (%s, %s)' % table_name,
#                           (db_id, server_name, level, address))
#       rs = self.cursor.fetchall
#       self.conn.commit()

    async def __create__(self):
        for server in configs['cloudpiercer']['pandora_server']:
            await orm.create_pool(loop=self.loop, **configs['cloudpiercer']['db'], db=server)
        network = Network()
        add_routes(network)
        await network.network_online()

    def init(self):
        self.loop.run_until_complete(self.__create__())

    def f(self):
        self.loop.run_forever()


if __name__ == 'main':
    s = CloudPiecer()
    s.init()
    print('Battle control online')
    s.f()


#!/usr/bin python3
# -*- coding: utf-8 -*-
from aiohttp import web


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


class Cyberkernel(web.Application):
    def __init__(self, loop, middlewares=[logger_factory, response_factory]):
        return super().__init__(loop=loop, middlewares=middlewares)

    async def cyber_kernel_online(self):
        srv = await self.loop.create_server(self.make_handler(), '127.0.0.1', 9000)
        return srv

    def addition(self):
        pass

#!/usr/bin python3
# -*- coding: utf-8 -*-
import os
import asyncio
import inspect


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


def add_route(cyber_kernel_app, fn):
    method = getattr(fn, '__method__', None)
    url = getattr(fn, '__url__', None)
    if method is None or url is None:
        raise ValueError('@method or url not defined in %s.' % str(fn))
        #  this might be a bug
    cyber_kernel_app.router.add_route(method, url, RequestHandler(cyber_kernel_app, fn))


def add_routes(cyber_kernel_app, modules_name, MCV_server_dict):
    MCV_server_name = list(MCV_server_dict.keys())
    route_servers = [x.split('.')[0] for x in os.listdir(os.path.abspath('%s' % modules_name))
                     if os.path.splitext(x)[1] == '.py' and x.split('.')[0] in MCV_server_name]
    for module_name in route_servers:
        mod = __import__(modules_name+'.'+module_name, globals(), locals(), [module_name])
        MCV_build_in_args = MCV_server_dict[module_name]
        mod._interface(MCV_build_in_args)
        for attr in dir(mod):
            if attr.startswith('_') or attr not in MCV_build_in_args['server_args']:
                continue

            fn = getattr(mod, attr)
            if callable(fn):
                method = getattr(fn, '__method__', None)
                if method:
                    add_route(cyber_kernel_app, fn)


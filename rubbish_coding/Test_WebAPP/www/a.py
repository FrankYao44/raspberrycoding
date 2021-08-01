import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

# -*- coding: utf-8 -*-
import logging
logging.basicConfig(level=logging.INFO)
import os,json,time,asyncio
from datetime import datetime
from aiohttp import web

# def index(request): # 原始简单的url处理函数
#     return web.Response(body=b'<h1>Awesome</h1>',content_type='text/html')

def init_jinja2(app, **kw): #初始化 jinja2的 env
   pass

async def logger_factory(app, handler):
    async def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        return (await handler(request))
    return logger

#  生产  post 提交的数据
async def data_factory(app, handler):
   pass

#将url处理函数的返回值 转换成 response 对象
async def response_factory(app, handler):
    pass
    return response

#  将blog  评论的发布时间 转换成 多少时间以前
def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

async def init(loop):
    #db = configs.configs.db
    await orm.create_pool(loop=loop,)
    #DeprecationWarning: loop argument is deprecated
    app = web.Application(loop = loop,middlewares=[ #拦截器 一个URL在被某个函数处理前，可以经过一系列的middleware的处理。
        logger_factory, response_factory #工厂模式
    ])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')
    add_static(app)

    # DeprecationWarning: Application.make_handler(...) is deprecated, use AppRunner API instead
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '192.168.2.101', 9000)
    logging.info('server started at http://192.168.2.101:9000...')
    await site.start()
     
    #以前的写法
    # srv = await loop.create_server(app.make_handler(), '192.168.2.101', 9000)
    # logging.info('server started at http://192.168.2.101:9000...')
    # return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

def index(request):
    return web.Response(body=b'<h1>Awesome</h1>')

@asyncio.coroutine
async def init(loop):
    logging.info('server started at http://127.0.0.1:9000...')
    app = web.Application(loop = loop)
    app.router.add_route("get","/",index)
    runner=web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    return site
loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
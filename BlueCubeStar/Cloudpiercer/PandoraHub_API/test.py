#!/usr/bin python3
# -*- coding: utf-8 -*-
import inspect
import asyncio
from Cloudpiercer.orm_field import *
from some_useful_func import decorator_builder, next_id
from Cloudpiercer.orm import Model
Test = decorator_builder('url')


class TestTable(Model):
    table_name = 'test'
    db = 'test'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(400)')
    name = StringField(ddl='varchar(400)')


def interface(MCV_build_in_args):
    pass


@Test(method='get', url='/test')
async def test_init():
    print('this is a test module')
    return 'test'


@Test(method='post', url='/test/in')
async def write_in(name):
    rs = TestTable(name=name)
    await rs.save()
    return rs


@Test(method='get', url='/test/out/{name}')
async def write_out(name):
    rs = TestTable(name=name)
    rs = await rs.findAll(where='name = ?', args=name)
    return rs


@Test(method='get', url='/atomheart/init/{password}')
async def init(password):
    if password:
        pass
    result = {}
    for fn in globals().values():
        if getattr(fn, '__method__', None):
            url = fn.url
            args_signature = inspect.signature(fn)
            pk_input = {}
            pk_default = {}
            args = False
            kw = False
            for name, param in args_signature.parameters.items():
                if param.kind == param.POSITIONAL_OR_KEYWORD:
                    if param.default is param.empty:
                        pk_input[name] = inspect.Parameter.empty
                    else:
                        pk_default[name] = param.default
                elif param.kind == param.VAR_POSITIONAL:
                    args = True
                elif param.kind == param.VAR_KEYWORD:
                    kw = True
            result[fn.__name__] = {'fn': fn, 'url': url, 'pk_input': pk_input, 'pk_default': pk_default, 'args': args, 'kw': kw}
        await asyncio.sleep(0)
    return result










#!/usr/bin python3
# -*- coding: utf-8 -*-
from orm_field import *
from some_useful_func import decorator_builder, next_id
from orm import Model
Test = decorator_builder('url')


class TestTable(Model):
    table_name = 'test'
    db = 'test'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(400)')
    name = StringField(ddl='varchar(400)')


def _interface(MCV_build_in_args):
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







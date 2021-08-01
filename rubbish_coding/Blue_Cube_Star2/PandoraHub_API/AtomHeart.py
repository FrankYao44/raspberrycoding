#!/usr/bin python3
# -*- coding: utf-8 -*-
import functools
import json
from some_useful_func import decorator_builder, next_id
from orm import Model
from orm_field import *
atom_heart_decorator = decorator_builder('url')


def subject_detective(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        global _MCV_build_in_args
        if kw['subject'] not in _MCV_build_in_args['table_names']:
            return 'wrong input'
        return func(*args, **kw)
    return wrapper


def _atom_heart_model_creator(subject):
    return type('AtomHeart', (Model, ),
                dict(table_name=subject,
                     id=StringField(primary_key=True, default=next_id, ddl='varchar(400)'),
                     text=StringField(ddl='text(65535)'),
                     level=IntegerField(),
                     image_address=StringField(ddl='varchar(2000)'),
                     belong_to=StringField(ddl='varchar(20000))'),
                     addition=StringField(ddl='text(65535)')))


def _interface(MCV_build_in_args):
    global _MCV_build_in_args
    _MCV_build_in_args = MCV_build_in_args
    global _atom_heart_model_db_dict
    _atom_heart_model_db_dict = dict(zip(MCV_build_in_args['table_names'],
                                     map(_atom_heart_model_creator, MCV_build_in_args['table_names'])))


@subject_detective
@atom_heart_decorator(method='get', url='/atomheart/visitor/{subject}')
async def atom_heart_init(subject):
    print('this is a test module')
    return 'test'


@subject_detective
@atom_heart_decorator(method='post', url='/atomheart/in/{subject}')
async def write_in(subject, text, level, belong_to, image_address=None, addition=None):
    global _atom_heart_model_db_dict
    rs = _atom_heart_model_db_dict[subject](subject=subject, text=text, level=level,
                                       belong_to=belong_to, image_address=image_address, addition=addition)
    await rs.save()
    return rs


@subject_detective
@atom_heart_decorator(method='get', url='/atomheart/out/{subject}/{key}/{args}')
async def print_out(subject, key, args):
    rs = _atom_heart_model_db_dict[subject]()
    if key == 'all' and args == 'all':
        rs = await rs.findAll(orderBy='belong_to,level')
    else:
        rs = await rs.findAll(where='%s=?' % key, args=[args], orderBy='belong_to,level')
    return json.dumps(rs)


@subject_detective
@atom_heart_decorator(method='get', url='/atomheart/del/{subject}/{id}')
async def wipe_out(subject, id):
    rs = _atom_heart_model_db_dict[subject](id=id)
    await rs.remove()
    return rs


@subject_detective
@atom_heart_decorator(method='post', url='/atomheart/update/{subject}')
async def up_to_date(subject, id, **kw):
    rs = _atom_heart_model_db_dict[subject](id=id, **kw)
    rs = await rs.update()
    return rs



#!/usr/bin python3
# -*- coding: utf-8 -*-
import functools
import json
from Cloudpiercer.some_useful_func import decorator_builder, next_id, password
from Cloudpiercer.orm import Model
from Cloudpiercer.orm_field import *
import time
atom_heart_decorator = decorator_builder('url')
_MCV_build_in_args = {}
_atom_heart_model_db_dict = {}


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


class ExpandSelfModel(Model):
    table_name = 'Atomheart'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(400)')
    time = IntegerField()
    log_info = StringField(ddl='varchar(2000)')


def _interface(mcv_build_in_args):
    global _MCV_build_in_args
    _MCV_build_in_args = mcv_build_in_args
    global _atom_heart_model_db_dict
    _atom_heart_model_db_dict = dict(zip(mcv_build_in_args['table_names'],
                                         map(_atom_heart_model_creator, mcv_build_in_args['table_names'])))
    _atom_heart_model_db_dict['main'] = ExpandSelfModel


@subject_detective
@atom_heart_decorator(method='get', url='/atomheart/visitor/{subject}')
async def atom_heart_init(subject):
    print('this is a test module of %s' % subject)
    return 'test'


@subject_detective
@atom_heart_decorator(method='post', url='/atomheart/in/{subject}')
async def save(subject, text, level, belong_to, image_address=None, addition=None):
    global _atom_heart_model_db_dict
    rs = _atom_heart_model_db_dict[subject](subject=subject, text=text, level=level,
                                            belong_to=belong_to, image_address=image_address, addition=addition)
    await rs.save()
    return rs


@subject_detective
@atom_heart_decorator(method='get', url='/atomheart/out/{subject}/{key}/{args}')
async def find(subject, key, args):
    rs = _atom_heart_model_db_dict[subject]()
    if key == 'all' and args == 'all':
        rs = await rs.findAll(orderBy='belong_to,level')
    else:
        rs = await rs.findAll(where='%s=?' % key, args=[args], orderBy='belong_to,level')
    return json.dumps(rs)


@subject_detective
@atom_heart_decorator(method='get', url='/atomheart/del/{subject}/{id}')
async def delete(subject, data_id):
    rs = _atom_heart_model_db_dict[subject](id=data_id)
    await rs.remove()
    return rs


@subject_detective
@atom_heart_decorator(method='post', url='/atomheart/update/{subject}')
async def update(subject, data_id, **kw):
    rs = _atom_heart_model_db_dict[subject](id=data_id, **kw)
    rs = await rs.update()
    return rs


@subject_detective
@atom_heart_decorator(method='get', url='/atomheart/init/{password}', )
async def init(pw):
    # here, you have to check the url of applicant
    # check the pw
    pw_n = password(time.time)
    if len(set(pw + pw_n)) == 4:
        return Exception
    elif len(set(pw + pw_n)) == 3:
        print('great')
    result = {}
    for fn in globals().values():
        result[fn.__name__] = {'fn': fn,
                               'url': fn.url,
                               'pk_input': fn.position_or_keyword_input,
                               'pk_default': fn.position_or_keyword_default,
                               'args': fn.args,
                               'kw': fn.kwargs}
        # get every writen functions' fn, name, url, params
    await _atom_heart_model_db_dict['main'](time=time.time(), log_info='inited by sth')
    return result

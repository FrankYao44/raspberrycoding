#!/usr/bin python3
# -*- coding: utf-8 -*-
import functools
import json
from some_useful_func import decorator_builder, next_id, password
from Cloudpiercer.orm import Model
from Cloudpiercer.orm_field import *
import time
atom_heart_decorator = decorator_builder('url')
_atom_heart_model_db_dict = {}


def _atom_heart_model_creator(subject):
    return type('atomheart', (Model, ),
                dict(table_name=subject,
                     id=StringField(primary_key=True, default=next_id, ddl='varchar(400)'),
                     text=StringField(ddl='text(65535)'),
                     level=IntegerField(),
                     image_address=StringField(ddl='varchar(2000)'),
                     belong_to=StringField(ddl='varchar(20000))'),
                     addition=StringField(ddl='text(65535)')))


@atom_heart_decorator(method='get', url='/atomheart/visitor/{subject}')
async def atom_heart_init(subject):
    print('this is a test module of %s' % subject)
    return 'test'


@atom_heart_decorator(method='post', url='/atomheart/in/{subject}')
async def save(subject, text, level, belong_to, image_address=None, addition=None):
    global _atom_heart_model_db_dict
    rs = _atom_heart_model_db_dict[subject](subject=subject, text=text, level=level,
                                            belong_to=belong_to, image_address=image_address, addition=addition)
    await rs.save()
    return rs


@atom_heart_decorator(method='get', url='/atomheart/out/{subject}/{key}/{args}')
async def find(subject, key, args):
    rs = _atom_heart_model_db_dict[subject]()
    if key == 'all' and args == 'all':
        rs = await rs.findAll(orderBy='belong_to,level')
    else:
        rs = await rs.findAll(where='%s=?' % key, args=[args], orderBy='belong_to,level')
    return json.dumps(rs)


@atom_heart_decorator(method='get', url='/atomheart/del/{subject}/{id}')
async def delete(subject, data_id):
    rs = _atom_heart_model_db_dict[subject](id=data_id)
    await rs.remove()
    return rs


@atom_heart_decorator(method='post', url='/atomheart/update/{subject}')
async def update(subject, data_id, **kw):
    rs = _atom_heart_model_db_dict[subject](id=data_id, **kw)
    rs = await rs.update()
    return rs


@atom_heart_decorator(method='get', url='/atomheart/init/{pw}', )
async def init(pw):
    class atomheart(Model):
        table_name = 'Atomheart'
        id = StringField(primary_key=True, default=next_id, ddl='varchar(400)')
        time = IntegerField()
        log_info = StringField(ddl='varchar(2000)')
    # here, you have to check the url of applicant
    # check the pw
    pw = pw.split(',')
    pw_n = password(time.time())
    if len(set(pw + pw_n)) == 4:
        return Exception
    elif len(set(pw + pw_n)) == 3:
        print('great')
    result = {}
    global _atom_heart_model_db_dict
    _atom_heart_model_db_dict = dict()
    _atom_heart_model_db_dict['main'] = atomheart
    main = atomheart()
    result_list = await main.findAll()
    subject_list = result_list[-1]['log_info'].split(',')
    _atom_heart_model_db_dict.update(dict(zip(subject_list,
                                              map(_atom_heart_model_creator, subject_list))))
    for fn in globals().values():
        if not callable(fn):
            continue
        if not getattr(fn, 'url', None):
            continue
        result[fn.__name__] = {'fn': fn,
                               'url': fn.url,
                               'pk_input': fn.position_or_keyword_input,
                               'pk_default': fn.position_or_keyword_default,
                               'args': fn.args,
                               'kw': fn.kwargs}
        # get every writen functions' fn, name, url, params
    result = _atom_heart_model_db_dict['main'](time=time.time(), log_info='inited by sth')
    result = await result.save()
    return result

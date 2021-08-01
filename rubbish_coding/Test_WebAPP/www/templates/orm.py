#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio, logging

import aiomysql

@asyncio.coroutine
def create_pool(loop,**kw):
    logging.info("creating database connection pool")
    global __pool 
    __pool=yield from aiomysql.create_pool(
        host=kw.get('host','localhost'),
        port=kw.get('port'),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf-8'),
        autocommit=kw.get('autocommit',True),
        minsize=kw.get('minsize',1),
        maxsize=kw.get('maxsize',10),
        loop=loop
        )
@asyncio.coroutine
def select(sql,args,size=None):
    log(sql,args)
    global __pool
    with (yield from __pool) as conn:
        cur=yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?',"%s"),args or ())
        if size:
            res=yield from cur.fetchmany(size)
        else:
            res=yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows return %s'%(len(res)))
        return res
@asyncio.coroutine
def execute(sql,args):
    with (yield from __pool) as conn:
        try:
            cur=conn.cursor()
            yield from cur.execute(sql.replace('?',"%s"),args)
            affected=cur.rowcount
            yield from cur.close()
        except BaseException as e:
            raise
        return affected



class Model(dict,metaclass=ModelMetaclass):
    def __init__(self,**kw):
        super(Model,self).__init__(**kw)
    def __getattr__(self,key):
        try:return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
    def __setattr__(self,key,value):
        self[key]=value
    def getValue__(self,key):
        return getattr(self,key,None)
    def getValueOrDefault(self,key):
        value=getattr(self,key,None)
        if value is None:
            field=self.__mappings__[key]
            if field.default is not None:
                value=field.default() if callable(field,default) else field.default
                longging.debug("using defalut value for %s"%(key,str(value)))
                setattr(self,key,value)
            return value
        
        






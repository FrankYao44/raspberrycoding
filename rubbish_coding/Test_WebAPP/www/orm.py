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
    global __pool
    with (yield from __pool) as conn:
        try:
            cur=conn.cursor()
            yield from cur.execute(sql.replace('?',"%s"),args)
            affected=cur.rowcount
            yield from cur.close()
        except BaseException as e:
            raise
        return affected
def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)
class Field(object):
    def __init__(self,name,column_type,primary_key,default):
        self.name=name
        self.column_typt=column_type
        self.primary_key=primary_key
        self.default=default
    def __str__(self):
        return '<%s,%s:%s>'%(self.__class__.__name__,self.column_typt,self.name)
class StringField(Field):
    def __init__(self,name=None,primary_key=False,default=None,ddl='varchar(100)'):
        super().__init__(name,ddl,primary_key,default)

class ModelMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        tableName=attrs.get('table',None) or name
        logging.info('find Model %s ,name %s'%(name,tableName))
        mappings=dict()
        field=[]
        primarykey=None
        for k,v in attrs.items():
            if isinstance(v,Field):
                logging.info('fould mapping %s ==> %s'%(k,v))
                mappings[k]=v
                if v.primary_key:
                    if primarykey:
                         RuntimeError('Duplicate primary key for field: %s' % k)
                    primarykey=k
                else:
                    field.append(k)
        if not primarykey:
            raise RuntimeError('Primary key not found.')

        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields=list(map(lambda f:'%s'%(f),field))
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primarykey # 主键属性名
        attrs['__fields__'] = field # 除主键外的属性名
        # 构造默认的SELECT, INSERT, UPDATE和DELETE语句:
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primarykey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primarykey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), field)), primarykey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primarykey)
        return type.__new__(cls, name, bases, attrs)


class Model(dict,metaclass=ModelMetaclass):
    def __init__(self,**kw):
        super(Model,self).__init__(**kw)
        print(self)
    def __getattr__(self,key):
        try:return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
    def __setattr__(self,key,value):
        self[key]=value
    def getValue(self,key):
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
    @classmethod
    @asyncio.coroutine
    def find(cls,pk):
        rs=yield from select('%s where `s`=?'%(cls.__select__,cls.__primary_key__),[pk],1)
        if len(rs)==0:
            return None
        return cls(**rs[0])

    @asyncio.coroutine
    def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = yield from execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)

def __main():
    print(6)
    class User(Model):
        __table__ = 'users'

        id = StringField(primary_key=True)
        name = StringField()


    print(5)
    user = User(id='123', name='Michael')
    print(4)
    a=yield from user.save()
    b=yield from user.find(123)
    print(2)
    print(a)
    print(b)
    print(1)
if __name__=='__main__':
    print(3)
    a=__main()
    list(a)
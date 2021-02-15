#!/usr/bin python3
# -*- coding: utf-8 -*-
__level__ = 2
import aiomysql
import aiofiles
import logging
from orm_field import Field


async def create_pool(loop, **kw):
    logging.info('new connection pool')
    global __pool
    try:
        __pool
    except Exception:
        __pool = dict()

    __pool.setdefault(kw['db'], await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    ))


async def select(sql, args, db, size=None):
    #
    global __pool
    with (await __pool[db]) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs


async def execute(sql, args, db, autocommit=True):
    with (await __pool[db]) as conn:
        if not autocommit:
            await conn.begin()
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            await cur.close()
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


class ModelMetaclass(type):

    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return type.__new__(mcs, name, bases, attrs)
        db = attrs.get('db', None) or name
        table_name = attrs.get('table_name', None) or 'main'
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primaryKey:
                        raise Exception('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise Exception('Primary key not found.')
        for k in mappings.keys():

                fields.pop(k)

            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings
        attrs['db'] = db
        attrs['table_name'] = table_name
        attrs['__primary_key__'] = primaryKey
        attrs['__fields__'] = fields

        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), table_name)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % \
                              (table_name, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields)
                                                                                                     + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % \
                              (table_name, ', '.join(map(lambda f: '`%s`=?' %
                                                                   (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (table_name, primaryKey)
        return type.__new__(mcs, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        sql = [cls.__select__]
        db = cls.db
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql), args, db)
        return [cls(**r) for r in rs]

    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        db = cls.db
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__tablename__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, db, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    async def find(cls, pk):
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], cls.db, 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args, self.db)
        if rows != 1:
            return 'failed to insert record: affected rows: %s' % rows

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args, self.db)
        if rows != 1:
            return 'failed to update by primary key: affected rows: %s' % rows

    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args, self.db)
        if rows != 1:
            return 'failed to remove by primary key: affected rows: %s' % rows

    async def save_file(self, info):
        async with aiofiles.open(info.name, mode='a') as f:
            try :
                await f.write(info.content)
            except Exception as e:
                return e
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args, self.db)
        if rows != 1:
            return 'failed to insert record: affected rows: %s' % rows

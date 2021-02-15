#!/usr/bin python3
# -*- coding: utf-8 -*-
try:
    import mysql.connector as mysql_database
except ImportError:
    import MySQLdb as mysql_database
import asyncio
import orm
from haddler import add_routes
from functools import reduce
from cyberkernel import Cyberkernel
from some_useful_func import str_in_iterable_turns_into_tuple_factory, thread_creator
from config import configs


class MCV(object):

    def dir_server(self, table_name='MCV_table'):
        self.cursor.execute('select server_name, level, server_args, table_names, addition from %s' % table_name)
        return self.cursor.fetchall()

    def __init__(self, loop, ):
        conn = mysql_database.connect(user=configs['db']['user'], password=configs['db']['password'], database='MCV_database')
        cursor = conn.cursor()
        self.cursor = cursor
        self.conn = conn
        self.loop = loop
        self.server_dict = reduce(str_in_iterable_turns_into_tuple_factory, [reduce(lambda element1, element2: [element1.update(element2), element1][1], [{x[0]: dict(zip(['server_name', 'level', 'server_args', 'table_names', 'addition'], x))}for x in self.dir_server()]), 'server_args', 'table_names', 'addition'])

#   def new_server(self, server_name, address, level, db_id=next_id(), table_name='MCV_table'):
#       self.cursor.execute('insert into %s (id,server_name,level,address) values (%s, %s)' % table_name,
#                           (db_id, server_name, level, address))
#       rs = self.cursor.fetchall
#       self.conn.commit()

    def listener(self):
        # OK,there should be a __create__ function ,but it seems that ...
        self.loop.run_forever()

    async def __create__(self):
        for server in self.server_dict.keys():
            await orm.create_pool(loop=self.loop, **configs['db'], db=server)
        cyber_kernel = Cyberkernel(self.loop)
        add_routes(cyber_kernel, 'PandoraHub_API', self.server_dict)
        await cyber_kernel.cyber_kernel_online()

    def creator(self):

        self.loop.run_until_complete(self.__create__())


s = MCV(asyncio.get_event_loop())
s.creator()
print('Battle control online')
s.listener()


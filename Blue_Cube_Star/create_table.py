#!/usr/bin python3
# -*- coding: utf-8 -*-
from some_useful_func import next_id
import mysql.connector
conn = mysql.connector.connect(user='MCV', password='raspberrypi', database='AtomHeart')
cursor = conn.cursor()
cursor.execute('create table  Chemistry_competition (id varchar(500) primary key, text text(65535), level Int, '
               'image_address varchar(2000), belong_to varchar(20000), addition text(65535))')
# cursor.execute('create table  Chemistry_competition (id varchar(500) primary key, text text(65535), level Int, '
#               'image_address varchar(2000), belong_to varchar(20000), addition text(65535))')
# cursor.execute('insert into MCV_table (id, server_name, level, server_args, table_names) values '
#               '(%s, %s, %s, %s, %s)', [next_id(), 'AtomHeart', 10, 'atom_heart_init,write_in,',
#                                        'Chemistry(normal),Chemistry(competition)'])
conn.commit()
cursor.close()
cursor = conn.cursor()
cursor.execute('select * from user where id = %s', ('1',))
values = cursor.fetchall()
cursor.close()
conn.close()

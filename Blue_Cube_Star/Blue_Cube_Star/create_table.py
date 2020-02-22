import mysql.connector
conn = mysql.connector.connect(user='MCV', password='raspberrypi', database='MCV_database')
cursor = conn.cursor()
# cursor.execute('create table MCV_table (id varchar(500) primary key, server_name varchar(200), level Int, '
#               'server_args varchar(2000), table_names varchar(20000), addition varchar(10000))')
cursor.execute('insert into MCV_table (id, server_name, level, server_args, table_names) values '
               '(%s, %s, %s, %s, %s)', ['0', 'test', 10, 'test_init,write_in,write_out', 'test'])
conn.commit()
cursor.close()
cursor = conn.cursor()
cursor.execute('select * from user where id = %s', ('1',))
values = cursor.fetchall()
cursor.close()
conn.close()
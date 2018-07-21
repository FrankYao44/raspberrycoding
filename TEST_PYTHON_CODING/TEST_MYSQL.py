import mysql.connector
try:
    conn=mysql.connector.connect(user='root', password='raspberrypi', database='test')
    cursor=conn.cursor()
    #cursor.execute('create table user(id varchar(2)primary key,name varchar(2))')
    #cursor.execute('insert into user (id,name) values(%s, %s)',('9','K'))
    cursor.execute('select * from user where name=%s',("K",))
    values=cursor.fetchall()
    print(values)
finally:
    conn.commit()
    cursor.close()
    

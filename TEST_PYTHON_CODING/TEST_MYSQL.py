import mysql.connector
conn=mysql.connector.connect(user='root', password='root', database='test')
cursor=conn.cursor()
try:

    #cursor.execute('create table user(id varchar(2)primary key,name varchar(2))')
    #cursor.execute('insert into user (id,name) values(%s, %s)',('9','K'))
    cursor.execute('select * from user where name=%s',("K",))
    values=cursor.fetchall()
    print(values)
finally:
    conn.commit()
    cursor.close()
    

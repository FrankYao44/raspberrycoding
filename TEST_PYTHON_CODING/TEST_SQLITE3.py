import sqlite3
try:
    conn=sqlite3.connect('/home/pi/Desktop/raspberrycoding/TEST_PYTHON_CODING/TEST_AIO/test.db')
    cursor=conn.cursor()
    try:
        cursor.execute('create table Booqd (id varchar(1000) primary key, game varchar(1000))')
    except: pass
    #cursor.execute('insert into Booqd (id,name) values(\'199\',\'ga\')')
    print(cursor.rowcount)
    cursor.execute('select * from Book where name=?',("ga",))
    print(cursor.fetchall())
finally:
    cursor.close()
    conn.commit()
    conn.close()

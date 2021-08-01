import sqlite3
from datetime import datetime
class dream(object):
    def __init__(self,cursor):
        self.cursor=cursor
        
    def Past(self,primary_key):

        self.cursor.execute('create table ME (time varchar(64) primary key,words varchar(1024))')

    def Persent(self,time,words):
        self.cursor.execute('insert into ME values(?,?)',(time,words))
        cursor.execute('select * from ME')
        r=cursor.fetchall()
        print(len(r))

        
    def Future(self,result,time):
        print("have you made it?")
        cursor.execute('select * from ME')
        r=cursor.fetchall()
        n=0
        for i in r :
            n=n+1
            print(n)
            print("\n")
            print("time:")       
            print(i[1])
            print("words:")       
            print(i[0])
            input()
        print("time is a place")
        print("right?")
        input()
        print("and")
        print("you got it :%s"%(result))
        self.cursor.execute('insert into ME values(?,?)',(time,result))

            
if __name__=="__main__":
    try:
        conn=sqlite3.connect('/home/pi/Desktop/raspberrycoding/TEST_PYTHON_CODING/test.db')
        cursor=conn.cursor()
        Blue=dream(cursor)
        a=input("How is it going?\n")
        if a=='finally':
            r=input("what is the result?\n")
            Blue.Future(r,datetime.now())
        else:
            w=input("huh\n")
            Blue.Persent(w,datetime.now())
    finally:

        cursor.close()
        conn.commit()
        conn.close()
        
